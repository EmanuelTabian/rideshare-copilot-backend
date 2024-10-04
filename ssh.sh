#!/usr/bin/env bash

# Description: Script used to create a new ECS task with the exact version and configuration as running in AWS
# Description: This new task will not receive traffic from the load balancer, but allows running management and django/db shell commands
# Description: If the new task does not exit cleanly, it will run for at most 24 hours

# Usage: `./ssh`

# Prerequisite: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html
# Prerequisite: https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-working-with-install-plugin.html
# Prerequisite: AWS CLI configured with the AWS account on the default profile


SERVICE="rideshare-backend"
TASK_DEFINITION="rideshare-copilot"
CONTAINER_NAME="server"

ENVIRONMENT="production"
CLUSTER="rideshare-copilot"
SECURITY_GROUP="sg-05a46fc5bc7eff248"
SUBNETS='"subnet-07ad83f23c22b4003","subnet-057f34558a925e1da","subnet-0ef873cb62c08dc0d"'

echo "Starting a new Fargate task for the $SERVICE service on the $ENVIRONMENT to SSH into..."

AWS_ECS_TASK_ID=$(aws ecs run-task --region eu-central-1 --cluster $CLUSTER \
    --task-definition $TASK_DEFINITION \
    --enable-execute-command \
    --launch-type "FARGATE" \
    --network-configuration '{"awsvpcConfiguration":{"subnets":['"$SUBNETS"'],"securityGroups":["'"$SECURITY_GROUP"'"],"assignPublicIp":"ENABLED"}}' \
    --query "tasks[0].taskArn" \
    --output text \
    | cut -d'/' -f3)

echo "Your new task is ready with ID:" $AWS_ECS_TASK_ID

echo "Waiting for the task to start..."
aws ecs wait tasks-running --region eu-central-1 --cluster $CLUSTER --tasks $AWS_ECS_TASK_ID
sleep 15

if [[ "$ENVIRONMENT" == "prod" ]]; then
    echo -e "\n=========================================\n"
    echo -e "WARNING: You are operating on the Production environment.\n\nPlease exercise caution."
    echo -e "\n=========================================\n"
fi

echo "Your new task is running and ready for SSH! Logging you in and opening a shell..."
aws ecs execute-command --region eu-central-1 --cluster $CLUSTER --container $CONTAINER_NAME --interactive --command "/bin/bash" --task $AWS_ECS_TASK_ID

echo "Stopping the task using the following command:"
echo "aws ecs stop-task --region eu-central-1 --cluster $CLUSTER --task $AWS_ECS_TASK_ID"
aws ecs stop-task --region eu-central-1 --cluster $CLUSTER --task $AWS_ECS_TASK_ID >/dev/null 2>&1
echo "Task is being stopped. Please wait..."
aws ecs wait tasks-stopped --region eu-central-1 --cluster $CLUSTER --tasks $AWS_ECS_TASK_ID
echo "The task is now stopped. Have a nice day!"
