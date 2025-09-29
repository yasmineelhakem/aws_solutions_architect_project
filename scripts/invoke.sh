#!/bin/bash

samlocal.bat local invoke ImageProcessorFunction -e events/event2.json --env-vars env.json --docker-network localstack-net