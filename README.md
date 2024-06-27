# lambda-layer-for-docker

## Dockerfileにlambdaの拡張機能を加えてデプロイしたところ、権限は足りてると思われるのにエラーになる

- handler内での呼び出し → ok
- handler外での呼び出し、但し同一ファイル内 → ok
- 別ファイルからの呼び出し → *No*

```error.sh
[AWS Parameters and Secrets Lambda Extension] 2024/06/26 02:34:50 PARAMETERS_SECRETS_EXTENSION_LOG_LEVEL is not present. Log level set to info.
[AWS Parameters and Secrets Lambda Extension] 2024/06/26 02:34:50 INFO Systems Manager Parameter Store and Secrets Manager Lambda Extension 1.0.94
[AWS Parameters and Secrets Lambda Extension] 2024/06/26 02:34:50 INFO Serving on port 2773
EXTENSION	Name: AWSParametersAndSecretsLambdaExtension	State: Ready	Events: [SHUTDOWN, INVOKE]
START RequestId: e2a94706-2b18-48eb-9999-41200c64afc8 Version: $LATEST
[AWS Parameters and Secrets Lambda Extension] 2024/06/26 02:34:50 INFO ready to serve traffic
[AWS Parameters and Secrets Lambda Extension] 2024/06/26 02:34:51 ERROR GetParameter request encountered an error: operation error SSM: GetParameter, https response error StatusCode: 400, RequestID: 9a2e7fa8-e26a-4808-815b-0be2f5f3a857, api error AccessDeniedException: User: arn:aws:sts::000000000000:assumed-role/test-role/test is not authorized to perform: ssm:GetParameter on resource: arn:aws:ssm:ap-northeast-1:000000000000:parameter/test_param because no identity-based policy allows the ssm:GetParameter action
HTTP error occurred: 400 Client Error: Bad Request for url: http://localhost:2773/systemsmanager/parameters/get/?name=test_param
test_param None
Failed to retrieve parameter value
END RequestId: e2a94706-2b18-48eb-9999-41200c64afc8
REPORT RequestId: e2a94706-2b18-48eb-9999-41200c64afc8	Duration: 877.10 ms	Billed Duration: 1249 ms	Memory Size: 128 MB	Max Memory Used: 73 MB	Init Duration: 371.00 ms
```

## Usage

1. .envの作成
2. `deploy.sh`
3. awsのコンソールでlambdaの関数を作成
    1. `tutorial_lambda_for_docker` という名前のリポジトリが作られているはず
    1. 実行ロールが自動で作られたら下記のポリシーを追加する
4. SSMにパラメータを追加（なんでもいい）
5. 環境変数に `AWS_SSM_KEY_NAME` を追加して、先ほど追加したSSMのパラメータのキー名を入れる
6. コンソールでテスト実行


```policy
{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Effect": "Allow",
			"Action": "ssm:GetParameter",
			"Resource": "arn:aws:ssm:ap-northeast-1:YOUR_AWS_ACCOUNT_ID:parameter/*"
		}
	]
}
```