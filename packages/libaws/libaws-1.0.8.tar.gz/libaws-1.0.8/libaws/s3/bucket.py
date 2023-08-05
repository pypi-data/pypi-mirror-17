#coding:utf-8
import os
import argparse
from libaws.common.boto import * 
from libaws.common import config
from libaws.common.logger import logger

def put_bucket_policy(bucket,json_file):

    with open(json_file) as f:
        content = f.read()
        print content
        response = client_s3.put_bucket_policy(
            Bucket=bucket,Policy= content
        )


def list_as_dir(bucket,key):
    dir_keys = []
    paginator = client_s3.get_paginator('list_objects')
    if key == "/":
        key = ""
    results = paginator.paginate(Bucket=bucket,Delimiter='/',Prefix=key)
    for prefix in results.search('CommonPrefixes'):
        if prefix is None:
            continue
        prefix = prefix.get('Prefix')
        keys = list_as_dir(bucket,prefix)
        dir_keys.extend(keys)

    for res in results:
        if not res.has_key('Contents'):
            logger.error("key %s is not exist in bucket %s",key,bucket)
            continue
        contents = res['Contents']
        for content in contents:
            content_key = content['Key']
            if content_key == key:
                continue
            dir_keys.append(content_key)
    return dir_keys

def main():
    parser = argparse.ArgumentParser()
    #指定下载的bucket,必须参数
    parser.add_argument("-name", "--name", type=str, dest="bucket",help='dest bucket to operate',default=config.DEFAULT_BUCKET_NAME)
    #指定下载bucket中的文件,必须参数
    parser.add_argument("-put-bucket-policy", "--put-bucket-policy", action="store_true", dest="is_put_bucket_policy", help = 'set bucket policy',required=False)
    parser.add_argument("-json", "--json", type=str, dest="bucket_policy_json",help='bucket policy json file')

    args = parser.parse_args()
    bucket = args.bucket

    if args.is_put_bucket_policy:
        put_bucket_policy(bucket,args.bucket_policy_json)
   
