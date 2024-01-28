import random
import time

import requests
from loguru import logger

from constants import FORM_URL
from config import (
    SLEEP_TIME,
    ADDRESSES_FILE_PATH,
    EMAILS_FILE_PATH,
    ERROR_SLEEP_TIME
)


def read_from_txt(file_path):
    try:
        with open(file_path, "r") as file:
            return [line.strip() for line in file]
    except Exception as e:
        raise Exception(f"Encountered an error while reading a txt file '{file_path}': {str(e)}")


def fill_form(address: str, email: str):
    logger.info(f'Filling form for {address} - {email}')
    value = {
        "emailAddress": email,
        "entry.908064693": address,
        "dlut": 1706437372756
    }

    try:
        res = requests.post(FORM_URL, data=value)
        if res.status_code != 200:
            raise Exception('Not success')
        else:
            logger.success('Successfully filled')
    except:
        logger.error('Response not success. Sleeping...')
        time.sleep(ERROR_SLEEP_TIME)
        fill_form(address, email)


def worker():
    addresses = read_from_txt(ADDRESSES_FILE_PATH)
    emails = read_from_txt(EMAILS_FILE_PATH)

    if len(addresses) != len(emails):
        logger.error('Addresses should be 1 to one with Emails')
        exit()

    logger.info('Starting wallets processing')
    for address in addresses:
        address_index = addresses.index(address)
        email = emails[address_index]

        fill_form(address, email)
        time.sleep(random.randrange(*SLEEP_TIME))

    logger.success('All wallets processed')


if __name__ == '__main__':
    worker()