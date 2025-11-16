import os

SELLER_SERVICE_HOST = \
    f"http://{os.environ.get('SERVICE_HOST', '193.108.113.4:84')}"
