import os
import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException


def _get_google_service_account_path_from_ssm(key_name):
    # デフォルトポートは2773
    end_point = "http://localhost:2773"
    path = "/systemsmanager/parameters/get/?name={}".format(key_name)
    url = end_point + path
    headers = {
        "X-Aws-Parameters-Secrets-Token": os.environ.get("AWS_SESSION_TOKEN", "")
    }

    try:
        res = requests.get(url, headers=headers, timeout=5)  # タイムアウト設定
        res.raise_for_status()  # HTTPエラーが発生した場合例外を発生させる
        return res.json()
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # HTTPエラーの場合
    except ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")  # 接続エラーの場合
    except Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")  # タイムアウトの場合
    except ValueError as json_err:
        print(f"JSON decoding error: {json_err}")  # JSONパースエラーの場合
    except RequestException as req_err:
        print(f"An error occurred: {req_err}")  # その他のリクエストエラー
    except Exception as err:
        print(f"An unexpected error occurred: {err}")  # その他の予期しないエラー

    return None  # エラー発生時にはNoneを返す


def lambda_handler(event, context):
    key_name = os.environ.get("AWS_SSM_KEY_NAME")
    if not key_name:
        print("Environment variable 'AWS_SSM_KEY_NAME' is not set")
        return

    gcp_sa_res = _get_google_service_account_path_from_ssm(key_name)
    print("gcp_sa_res", gcp_sa_res)
    if gcp_sa_res:
        print(gcp_sa_res.get("Parameter", {}).get("Value", "Key not found"))
    else:
        print("Failed to retrieve parameter value")
