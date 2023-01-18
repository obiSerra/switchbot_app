#!/usr/bin/env bash

export AWS_PROFILE=obiserra-pers

echo ""
aws configure list
echo ""
echo "ACCOUNT"
echo $(aws sts get-caller-identity)
echo ""


sam build -m ./requirements.txt -t ./template.yaml