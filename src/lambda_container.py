from tmp_pkg.hello import hello


def lambda_handler(event, context):
    from Credentials.credential import credential

    hello()
    print(credential["gcp"])
