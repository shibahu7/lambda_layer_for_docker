import os
import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException

# TODO: handle 関数外で外部モジュールのssm取得関数読み込み（import時に実行される）
# from credentials.credential import credential
# gcp_sa_res = credential["gcp"]
# TODO: handle 関数外で外部モジュールのssm取得関数読み込み（import時に実行されない）
# from credentials.credential_factory import create_credential
# gcp_sa_res = create_credential()["gcp"]


def _get_google_service_account_path_from_ssm(key_name):
    end_point = "http://localhost:2773"
    path = "/systemsmanager/parameters/get/?name={}".format(key_name)
    url = end_point + path
    headers = {
        "X-Aws-Parameters-Secrets-Token": os.environ.get("AWS_SESSION_TOKEN", "")
    }

    try:
        res = requests.get(url, headers=headers, timeout=5)
        res.raise_for_status()
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

    return None


# TODO: handle 関数外でssm取得実行
# end_point = "http://localhost:2773"
# path = "/systemsmanager/parameters/get/?name={}".format(key_name)
# url = end_point + path
# headers = {
#     "X-Aws-Parameters-Secrets-Token": os.environ.get("AWS_SESSION_TOKEN", "")
# }
# res = requests.get(url, headers=headers, timeout=5)
# res.raise_for_status()
# gcp_sa_res = res.json()


def lambda_handler(event, context):
    # TODO: handle 関数内で外部モジュールのssm取得関数読み込み（import時に実行される）
    # from credentials.credential import credential
    # gcp_sa_res = credential["gcp"]
    # TODO: handle 関数外で外部モジュールのssm取得関数読み込み（import時に実行されない）
    # from credentials.credential_factory import create_credential
    # gcp_sa_res = create_credential()["gcp"]

    key_name = os.environ.get("AWS_SSM_KEY_NAME")
    if not key_name:
        print("Environment variable 'AWS_SSM_KEY_NAME' is not set")
        return

    # TODO: handle 関数内でssm取得関数実行
    gcp_sa_res = _get_google_service_account_path_from_ssm(key_name)

    # TODO: handle 関数内でssm取得実行
    # end_point = "http://localhost:2773"
    # path = "/systemsmanager/parameters/get/?name={}".format(key_name)
    # url = end_point + path
    # headers = {
    #     "X-Aws-Parameters-Secrets-Token": os.environ.get("AWS_SESSION_TOKEN", "")
    # }
    # res = requests.get(url, headers=headers, timeout=5)
    # res.raise_for_status()
    # gcp_sa_res = res.json()

    if gcp_sa_res:
        print(gcp_sa_res["Parameter"]["Value"])
        print(gcp_sa_res.get("Parameter", {}).get("Value", "Key not found"))
    else:
        print("Failed to retrieve parameter value")
