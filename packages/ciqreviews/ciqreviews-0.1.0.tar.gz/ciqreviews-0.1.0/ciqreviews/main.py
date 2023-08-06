# -*- coding: UTF-8 -*-
import argparse
from connectiq import get_html_text_from_url, analyse_local_reviews_data, get_single_page_review_json_using_bs4, analyse_remote_reviews_data, analyse_local_reviews_data, get_multi_page_review_json_using_bs4

import os


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # https://apps.garmin.cn/zh-CN/apps/dc6ceca8-6ec6-49f2-b711-4ebc0d347177
    parser.add_argument(
        "app_url", help="e.g. https://apps.garmin.cn/en-US/apps/02d16e10-84dc-46aa-8edb-c42834c9b907")
    options = parser.parse_args()
    analyse_remote_reviews_data(options.app_url)
