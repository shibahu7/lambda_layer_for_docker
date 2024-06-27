from Credentials.credential import credential


def lambda_handler(event, context):
    print(credential["gcp"])
