import boto3
import botocore
import re
import os
import json
import sys

from functools32 import lru_cache
from tempfile import NamedTemporaryFile

udf = {}

def get_bash_cmd(dataset, success_only = False, recent_versions = None, version = None):
    m = re.search("s3://([^/]*)/(.*)", dataset)
    bucket_name = m.group(1)
    prefix = m.group(2)

    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    versions = get_versions(bucket, prefix)

    if version is not None:
        versions = [v for v in versions if v[2] == version]
        if not versions:
            sys.stderr.write("No schemas available with that version")

    bash_cmd, versions_loaded = "", 0
    for (version_prefix, dataset_name, version) in versions:
        sample, success_exists = "", False
        keys = sorted(bucket.objects.filter(Prefix=version_prefix), key = lambda obj : obj.last_modified, reverse = True)
        for key in keys:
            partition = "/".join(key.key.split("/")[:-1])
            if success_only:
                if check_success_exists(s3, bucket.name, partition):
                    success_exists = True
                else:
                    continue

            sample = key
            if not sample.key.endswith("/"): # ignore "folders"
                filename = sample.key.split("/")[-1]
                if not filename.startswith("_"): # ignore files that are prefixed with underscores
                    break

        if not sample:
            if success_only and not success_exists:
                sys.stderr.write("Ignoring dataset missing _SUCCESS file\n")
            else:
                sys.stderr.write("Ignoring empty dataset\n")
            continue

        sys.stderr.write("Analyzing dataset {}, {}\n".format(dataset_name, version))
        s3_client = boto3.client('s3')
        tmp_file = NamedTemporaryFile()
        s3_client.download_file(sample.bucket_name, sample.key, tmp_file.name)

        meta = os.popen("java -jar {} meta {}".format(find_jar_path(), tmp_file.name)).read()
        schema = json.loads("{" + re.search("(org.apache.spark.sql.parquet.row.metadata|parquet.avro.schema) = {(.+)}", meta).group(2) + "}")
        partitions = get_partitioning_fields(sample.key[len(prefix):])

        bash_cmd += "hive -hiveconf hive.support.sql11.reserved.keywords=false -e '{}'".format(avro2sql(schema, dataset_name, version, dataset, partitions)) + '\n'
        if versions_loaded == 0:  # Most recent version
            bash_cmd += "hive -e '{}'".format(avro2sql(schema, dataset_name, version, dataset, partitions, with_version=False)) + '\n'

        versions_loaded += 1
        if recent_versions is not None and versions_loaded >= recent_versions:
            break

    return bash_cmd


def get_versions(bucket, prefix):
    if not prefix.endswith('/'):
        prefix = prefix + '/'

    xs = bucket.meta.client.list_objects(Bucket=bucket.name, Delimiter='/', Prefix=prefix)
    tentative = [ o.get('Prefix') for o in xs.get('CommonPrefixes', []) ]

    result = []
    for version_prefix in tentative:
        tmp = filter(bool, version_prefix.split("/"))
        if len(tmp) < 2:
            sys.stderr.write("Ignoring incompatible versioning scheme\n")
            continue

        dataset_name = tmp[-2]
        version = tmp[-1]
        if not re.match("^v[0-9]+$", version):
            sys.stderr.write("Ignoring incompatible versioning scheme: version must be an integer prefixed with a 'v'\n")
            continue

        result.append((version_prefix, dataset_name, int(version[1:])))

    return [(prefix, name, "v{}".format(version))
        for (prefix, name, version)
        in sorted(result, key = lambda x : x[2], reverse = True)]

@lru_cache(maxsize = 64)
def check_success_exists(s3, bucket, prefix):
    if not prefix.endswith('/'):
        prefix = prefix + '/'

    success_obj_loc = prefix + '_SUCCESS'
    exists = False

    try:
        res = s3.Object(bucket, success_obj_loc).load()
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            exists = False
        else:
            raise e
    else:
        exists = True

    return exists


def find_jar_path():
    paths = []
    jar_file = "parquet-tools.jar"
    lib_dir = 'parquet2hivemodules/'

    paths.append(jar_file)
    paths.append(lib_dir + jar_file)
    paths.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../../" + lib_dir + jar_file))
    paths.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../share/" + lib_dir + jar_file))
    paths.append("../../../current-release/" + jar_file)
    paths.append(os.path.join(sys.prefix, "share/" + lib_dir + jar_file))

    for path in paths:
        if os.path.exists(path):
            return path

    raise Exception("Failure to locate parquet-tools.jar")

def get_partitioning_fields(prefix):
    return re.findall("([^=/]+)=[^=/]+", prefix)


def avro2sql(avro, name, version, location, partitions, with_version=True):
    fields = [avro2sql_column(field) for field in avro["fields"]]
    fields_decl = ", ".join(fields)

    if partitions:
        columns = ", ".join(["{} string".format(p) for p in partitions])
        partition_decl = " partitioned by ({})".format(columns)
    else:
        partition_decl = ""

    # check for duplicated fields
    field_names = [field["name"] for field in avro["fields"]]
    duplicate_columns = set(field_names) & set(partitions)
    assert not duplicate_columns, "Columns {} are in both the table columns and the partitioning columns; they should only be in one or another".format(", ".join(duplicate_columns))
    table_name = name + "_" + version if with_version else name
    return "drop table if exists {0}; create external table {0}({1}){2} stored as parquet location '\"'{3}/{4}'\"'; msck repair table {0};".format(table_name, fields_decl, partition_decl, location, version)


def avro2sql_column(avro):
    return "`{}` {}".format(avro["name"], transform_type(avro["type"]))


def transform_type(avro):
    is_dict, is_list, is_str = isinstance(avro, dict), isinstance(avro, list), isinstance(avro, str) or isinstance(avro, unicode)

    unchanged_types = ['string', 'int', 'float', 'double', 'boolean', 'date', 'timestamp', 'binary']
    mapped_types = {'integer' : 'int', 'long' : 'bigint'}

    if is_str and avro in unchanged_types:
        sql_type = avro
    elif is_str and avro in mapped_types:
        sql_type = mapped_types[avro]
    elif is_dict and avro["type"] == "map":
        value_type = avro.get("values", avro.get("valueType")) # this can differ depending on the Avro schema version
        sql_type = "map<string,{}>".format(transform_type(value_type))
    elif is_dict and avro["type"] == "array":
        item_type = avro.get("items", avro.get("elementType")) # this can differ depending on the Avro schema version
        sql_type = "array<{}>".format(transform_type(item_type))
    elif is_dict and avro["type"] in ("record", "struct"):
        fields_decl = ", ".join(["`{}`: {}".format(field["name"], transform_type(field["type"])) for field in avro["fields"]])
        sql_type = "struct<{}>".format(fields_decl)
        if avro["type"] == "record":
            udf[avro["name"]] = sql_type 
    elif is_list:
        sql_type = transform_type(avro[0] if avro[1] == "null" else avro[1])
    elif avro in udf:
        sql_type = udf[avro]
    else:
        raise Exception("Unknown type {}".format(avro))

    return sql_type


