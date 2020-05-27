#!/bin/sh
ssh -o StrictHostKeyChecking=no ec2-user@$EC2_PUBLIC_IP_ADDRESS << 'ENDSSH'
  cd /home/ec2-user/app
  export $(cat .env.staging | xargs)
  docker login -u $DOCKERHUB_USER -p $DOCKERHUB_PASSWORD $DOCKERHUB_REGISTRY
  docker pull $DOCKERHUB_REGISTRY/$WEB_IMAGE
  docker pull $DOCKERHUB_REGISTRY/$NGINX_IMAGE
  docker-compose up -d
ENDSSH