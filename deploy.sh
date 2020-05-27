#!/bin/bash
ssh -o StrictHostKeyChecking=no ec2-user@$EC2_PUBLIC_IP_ADDRESS << 'ENDSSH'
  cd /home/ec2-user/app
  export $(cat .env | xargs)
  docker-compose up -d
ENDSSH