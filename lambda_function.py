from __future__ import print_function

import boto3
import time

def lambda_handler(event, context):
    path = []
    for items in event["Records"]:
        # If "index.html" has changed CloudFront should invalidate "/"
        if items["s3"]["object"]["key"] == "index.html":
            path.append("/")
        else:
            path.append("/" + items["s3"]["object"]["key"])
        # Get bucket name
        bucket_name = items["s3"]["bucket"]["name"]

    client = boto3.client('s3')
    # Get CloudFront distribution ID from S3 tag
    tags = client.get_bucket_tagging(Bucket=bucket_name)
    for tag in tags['TagSet']:
        if tag["Key"] == "distributionId":
            distribution_id = tag["Value"]
            break

    # Perform the invalidation
    client = boto3.client('cloudfront')
    invalidation = client.create_invalidation(DistributionId=distribution_id,
        InvalidationBatch={
            'Paths': {
                'Quantity': 1,
                'Items': path
        },
        'CallerReference': str(time.time())
    })
