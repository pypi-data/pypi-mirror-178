
# -*- coding: UTF-8 -*-
import argparse
from connectiq import get_html_text_from_url, analyse_local_reviews_data, get_single_page_review_json_using_bs4, analyse_remote_reviews_data, analyse_local_reviews_data, get_multi_page_review_json_using_bs4
import os


# clear my proxy temporarily
os.environ["http_proxy"] = ''
os.environ["https_proxy"] = ''
print(os.environ["http_proxy"])
print(os.environ["http_proxy"])

# # 下载json评论数据
# get_multi_page_review_json_using_bs4(
#     'https://apps.garmin.cn/en-US/apps/6c5b540e-32f3-40b3-9913-9ba196739fab')

# analyse_local_reviews_data(os.path.join(os.getcwd(),
#                                         '2022_11_27_GRun中文版_62278_208.json'))
# # 离线分析数据
# analyse_local_reviews_data(os.path.join(os.getcwd(),
#                                         '2022_11_27_Quatro 中文版_23194_1580.json'))
# analyse_local_reviews_data(os.path.join(os.getcwd(),
#                                         '2022_11_27_JumpJump跳绳_42885_232.json'))

analyse_remote_reviews_data(
    'https://apps.garmin.cn/zh-CN/apps/dc6ceca8-6ec6-49f2-b711-4ebc0d347177')
