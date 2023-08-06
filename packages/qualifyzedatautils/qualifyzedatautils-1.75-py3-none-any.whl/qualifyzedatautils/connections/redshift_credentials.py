
import redshift_connector
from ._decode_secret import decode_secret
from ._retrieve_awssecret import retrieve_awssecret

def initialize_redshift_credentials():
    redshift_secret = retrieve_awssecret("redshiftcluster_credentials", "eu-central-1")
    redshift_decoded_secret = decode_secret(redshift_secret)
    redshift_credentials = redshift_decoded_secret

    return redshift_credentials

def establish_redshift_connection():
    return print("aaaa")


print('loaded')


