#!/bin/bash

# .envファイルから環境変数を読み込む
export $(grep -v '^#' .env | xargs)

# リポジトリが存在しない場合は作成
aws ecr describe-repositories --repository-names tutorial_lambda_for_docker --region ap-northeast-1 > /dev/null 2>&1
if [ $? -ne 0 ]; then
    aws ecr create-repository --repository-name tutorial_lambda_for_docker --region ap-northeast-1
fi

# Dockerイメージのビルド
docker build . --platform linux/amd64 \
               -t tutorial_lambda_for_docker \
               --build-arg AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
               --build-arg AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY

# ECRにログイン
aws ecr get-login-password --region ap-northeast-1 | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.ap-northeast-1.amazonaws.com

# イメージにタグを付ける
docker tag tutorial_lambda_for_docker:latest ${AWS_ACCOUNT_ID}.dkr.ecr.ap-northeast-1.amazonaws.com/tutorial_lambda_for_docker

# ECRにプッシュ
docker push ${AWS_ACCOUNT_ID}.dkr.ecr.ap-northeast-1.amazonaws.com/tutorial_lambda_for_docker

