#!/bin/bash

samlocal.bat local invoke ImageProcessorFunction -e events/event2.json --env-vars env.json --docker-network localstack-net

# we dont need docker network anymore 
aws lambda invoke  --function-name sam-app-ImageProcessorFunction-3b42b2fe   --payload fileb://events/event2.json   --endpoint-url http://localhost:4566   response.json
cat response.json