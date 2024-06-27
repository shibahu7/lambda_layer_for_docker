# lambda-layer-for-docker

## 【解決】Dockerfileにlambdaの拡張機能を加えてデプロイしたところ、権限は足りてると思われるのにエラーになる

```
lambdaのエントリーポイントである関数（主に `lambda_handler`）外で実行されるパラメータストアへのリクエストはすべて400 bad requestになる. ただし、なぜそうなのかは全く不明.

解決策として下記があげられる
- `lambda_handler` 関数内でパラメータストアへのリクエストを行う
- `lambda_handler` 関数外にパラメータストアへのリクエストを行う関数を定義して、`lambda_handler` 関数内で呼び出す
- 別モジュールにする場合は特に注意が必要
    - *importされた時点でファイル内のトップレベルのコードはすべて実行される*
	- つまり、別モジュールをimportする時は大体`lambda_handler` 関数外で行うが、パラメータストアへのリクエストがトップレベルで書かれている場合、import時点で処理が走るためうまく動作しなくなる → 従って、`lambda_handler` 内でimportすればよいという、ちょっと不思議な解決方法をとってしまいがち
```

- 関連しそうな記事

https://qiita.com/hayate_h/items/00c6cf92b0dd7886c1f6

https://stackoverflow.com/questions/76878491/lambda-function-invoked-before-secrets-extension-initialized

### 試したこと

- handler内での呼び出し → ok
- handler外での呼び出し、但し同一ファイル内 → ok
- 別ファイルからの呼び出し → *No*
    - 但し、自作モジュールの呼び出しをhandler内で行うと問題ない

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

## 検証用lambda関数

コンテナとzipの環境差異だと思っていたけど、全然関係なかった。zipのほうがコンソールでソースを変更できてすぐに結果が見れてうれしいので、パラメータストアのリクエストを呼び出すパターンをコメントアウトしておいた。これらをコメントアウトを解除していい感じに、検証してみてほしい。

その他、lambdaを使うのに必要な権限やSSMの設定はUsageを参照のこと

- python.zip
    - layerに追加する（requestsとパラメータストアのリクエストをモジュール化したものが入っている）
- src/lambda_container.py
    - エントリーポイントとなるソース
	- コピペして使えばok
