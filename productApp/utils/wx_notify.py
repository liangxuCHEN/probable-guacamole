"""
File: 企业微信机器人相关脚本工具
Author: Liangxu.CHEN
Data: 2024/5/29
"""
import os
import requests

WX_HOST = "https://qyapi.weixin.qq.com/cgi-bin/webhook"
WX_KEY = os.getenv("WX_KEY") or "1ac0118a-d73d-4cb1-876e-6ef6e26bd18b"
WX_URL = os.getenv("WX_URL") or f"{WX_HOST}/send?key={WX_KEY}"


def push_info_to_wx(content, url=WX_URL):
    """
    推送信息到企业微信
    :param content: 内容
    :param url: 群地址
    :return:
    """
    data = {
          "msgtype": "markdown",
          "markdown": {
            "content": content
          }
        }

    requests.post(url=url, json=data)


def push_file_to_wx(file_path, file_name, key=WX_KEY):
    # 定义请求的URL和boundary
    url = f"{WX_HOST}/upload_media?key={key}&type=file"
    # 准备请求头
    headers = {
        "Content-Type": "multipart/form-data"
    }
    # 准备请求体
    files = {
        'media': (file_name, open(file_path, 'rb'))
    }
    wx_url = f"{WX_HOST}/send?key={key}"
    # 发送文件上传请求
    response = requests.post(url, headers=headers, files=files)
    # 检查响应是否成功
    if response.status_code == 200:
        # 解析响应内容，获取media_id
        upload_result = response.json()
        media_id = upload_result.get('media_id')
        data = {
            "msgtype": "file",
            "file": {
                 "media_id": media_id
            }
        }
        res = requests.post(url=wx_url, json=data)
        if res.status_code == 200:
            print("发送文件成功")
    else:
        print("发送文件失败")
