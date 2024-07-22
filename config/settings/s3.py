from .env import env

AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
AWS_S3_CUSTOM_DOMAIN = env("AWS_S3_CUSTOM_DOMAIN")
AWS_S3_ENDPOINT_URL = env("AWS_S3_ENDPOINT_URL")
AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")

S3_CONFIG = {
    "endpoint_url": f"https://{AWS_S3_ENDPOINT_URL}",
    "aws_access_key_id": AWS_ACCESS_KEY_ID,
    "aws_secret_access_key": AWS_SECRET_ACCESS_KEY,
}

AWS_S3_CUSTOM_DOMAIN = f"{AWS_S3_CUSTOM_DOMAIN}/{AWS_STORAGE_BUCKET_NAME}"
AWS_S3_ENDPOINT_URL = f"https://{AWS_S3_ENDPOINT_URL}"

AWS_QUERYSTRING_AUTH = False
# DO NOT change these unless you know what you're doing.
_AWS_EXPIRY = 60 * 60 * 24 * 7
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": f"max-age={_AWS_EXPIRY}, s-maxage={_AWS_EXPIRY}, must-revalidate"
}

AWS_IS_GZIPPED = True
AWS_AUTO_CREATE_BUCKET = True
AWS_DEFAULT_ACL = 'public-read'
AWS_BUCKET_ACL = 'public-read'

# STATIC
# ------------------------
STATICFILES_STORAGE = "contrib.utils.storages.StaticRootS3Boto3Storage"
COLLECTFAST_STRATEGY = "collectfast.strategies.boto3.Boto3Strategy"
STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/static/"
# MEDIA
# ------------------------------------------------------------------------------
DEFAULT_FILE_STORAGE = "contrib.utils.storages.MediaRootS3Boto3Storage"
MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/media/"
