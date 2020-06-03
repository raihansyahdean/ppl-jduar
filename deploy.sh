#!/bin/sh

ssh -o StrictHostKeyChecking=no ec2-user@$EC2_PUBLIC_IP_ADDRESS << "ENDSSH"
  cd /home/ec2-user/smartcrm_backend
  export $(cat .env.staging | xargs)
  docker login -u $DOCKERHUB_USER -p $DOCKERHUB_PASSWORD $DOCKERHUB_REGISTRY
  docker pull $DOCKERHUB_USER/$WEB_IMAGE
  docker pull $DOCKERHUB_USER/$NGINX_IMAGE
  docker-compose -f docker-compose.aws.yml up -d
ENDSSH
