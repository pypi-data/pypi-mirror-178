
from ._decode_secret import decode_secret
from ._retrieve_awssecret import retrieve_awssecret

def initialize_bigquery_credentials():
    bigquery_secret = retrieve_awssecret("bigquery_credentials", "eu-central-1")
    bigquery_decoded_secret = decode_secret(bigquery_secret)
    bigquery_credentials = bigquery_decoded_secret

    return bigquery_credentials