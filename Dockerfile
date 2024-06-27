# lambda拡張機能の追加
FROM alpine:latest as layer-copy


ARG AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION:-"ap-northeast-1"}
ARG AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID:-""}
ARG AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY:-""}
ENV AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION}
ENV AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
ENV AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}

RUN apk add aws-cli curl unzip

RUN mkdir -p /opt

RUN curl $(aws lambda get-layer-version-by-arn --arn 'arn:aws:lambda:ap-northeast-1:133490724326:layer:AWS-Parameters-and-Secrets-Lambda-Extension:11' --query 'Content.Location' --output text) --output layer.zip && \
    unzip layer.zip -d /opt && \
    rm layer.zip


FROM public.ecr.aws/lambda/python:3.12
COPY --from=layer-copy /opt /opt

COPY requirements.lock ${LAMBDA_TASK_ROOT}
COPY pyproject.toml ${LAMBDA_TASK_ROOT}

RUN sed -n 's/^\(.*\)==\(.*\)$/\1==\2/p' requirements.lock > requirements.txt && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

COPY Credentials /opt/python/Credentials

# 実行する lambda ファイル
COPY lambda.py ${LAMBDA_TASK_ROOT}

CMD [ "lambda.lambda_handler" ]
