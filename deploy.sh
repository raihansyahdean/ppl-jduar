#!/bin/sh

ssh -o StrictHostKeyChecking=no ec2-user@$EC2_PUBLIC_IP_ADDRESS << 'ENDSSH'
  cd /home/ec2-user/jduar-nvidia-smart-crm
  export $(cat .env.staging | xargs)
  docker login -u $DOCKERHUB_USER -p $DOCKERHUB_PASSWORD $DOCKERHUB_REGISTRY
  docker-compose up -d
ENDSSH