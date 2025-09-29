#!/bin/bash

# environment variables for LocalStack
export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
export AWS_DEFAULT_REGION=us-east-1

# Point AWS and SAM to LocalStack
export SERVICES="cloudformation,s3,lambda,iam"
export LOCALSTACK_HOST=localhost
export EDGE_PORT=4566
export SAM_CLI_TELEMETRY=0

# create S3 buckets
aws --endpoint-url=http://localhost:4566 s3 mb s3://original-bucket || true 
aws --endpoint-url=http://localhost:4566 s3 mb s3://processed-bucket || true

# list S3 buckets
aws --endpoint-url=http://localhost:4566 s3 ls

samlocal.bat build

# deploy using samlocal
samlocal.bat deploy --guided
