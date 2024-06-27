

def lambda_handler(event, context):
    from Credentials.credential import credential
    print(credential["gcp"])
