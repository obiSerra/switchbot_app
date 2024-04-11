#!/usr/bin/env bash
source env_variables

export AWS_PROFILE=obiserra-pers

echo ""
aws configure list
echo ""
echo "ACCOUNT"
echo $(aws sts get-caller-identity)
echo ""


sam deploy --capabilities CAPABILITY_NAMED_IAM --parameter-overrides "SWITCHBOTTOKEN=$SWITCHBOT_TOKEN SWITCHBOTSECRET=$SWITCHBOT_SECRET" $@