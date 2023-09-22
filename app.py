import hashlib
import json
import logging
import os
import sys

import requests


def run_exec():
    print(sys.argv)
    if len(sys.argv) > 1:
        # should detect this
        exec(sys.argv[1])
    if os.getenv('SOME_UNSANITIZED_VAR'):
        # should detect this
        exec(os.getenv('SOME_UNSANITIZED_VAR'))
    # this is "fine"...ish
    exec("print('hello')")


def insecure_hash():
    # should detect this
    print(hashlib.new('md5', 'test'.encode('utf-8')).hexdigest())
    # should detect this, but doesn't work
    print(hashlib.md5('test'.encode('utf-8')).hexdigest())
    # this is fine
    print(hashlib.sha256('test'.encode('utf-8')).hexdigest())


def disabled_tls_verification():
    # should detect disabling tls verification
    requests.get('https://example.com', verify=False)


# This is undetected, looking for an alternative
def logger_credential_leak():
    logging.basicConfig()
    logger = logging.getLogger()
    logger.setLevel('INFO')

    secret = 'somesecret'
    body = {'somekey': 'somevalue'}
    response = requests.post(url='https://example.com', headers={'Authorization': f'Bearer {secret}'}, json=body)
    logger.info(f"sent request with body: {response.request.body}, headers: {response.request.headers}")


def main():
    run_exec()
    insecure_hash()
    disabled_tls_verification()
    logger_credential_leak()


if __name__ == '__main__':
    main()
