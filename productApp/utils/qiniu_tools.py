import os
import time
from datetime import datetime
from qiniu import Auth, put_data, BucketManager

from django.conf import settings


class QiNiuStorage(object):
    """七牛云存储"""
    def __init__(self, child_name, is_public=True):

        self.__is_public = is_public

        if is_public:
            # 访问图片的根地址
            self.__base_url = settings.QINIU_BASE_URL
            # 存储图片的空间名
            self.__backet_name = settings.QINIU_BASE_BACKET_NAME
        else:
            self.__base_url = settings.QINIU_PRIVATE_URL
            self.__backet_name = settings.QINIU_PRIVATE_BACKET_NAME

        # 七牛 access_key
        self.__access_key = settings.QINIU_ACCESS_KEY
        # 七牛 secret_key
        self.__secret_key = settings.QINIU_SECRET_KEY
        # 七牛云-构建鉴权对象
        self.qiniu_server = Auth(self.__access_key, self.__secret_key)
        # 存储图片的子空间名
        self.child_name = child_name

    def get_token(self):
        return self.qiniu_server.upload_token(self.__backet_name)

    def upload(self, name, content, is_date_splice=True, is_rename=True):
        """
        存储函数
        :param is_date_splice: 按时间分文件夹
        :param is_rename: 名字重新构建
        :param name: 文件名
        :param content: 文件
        :return:
        """
        # 七牛云-生成上传 Token，可以指定过期时间等
        token = self.get_token()

        # 利用七牛的put_data方法上传文件内容
        upload_url = self.__new_name(name, self.child_name, is_date_splice, is_rename)
        ret, info = put_data(
            token,
            upload_url,
            content if isinstance(content, bytes) else content.read(),
        )
        # 根据七牛的返回结果中的响应状态码，判断是否上传成功
        if info.status_code == 200:
            return upload_url
        else:
            raise Exception("上传七牛失败")

    def delete(self, name):
        bucket = BucketManager(self.qiniu_server)
        ret, info = bucket.delete(self.__backet_name, name)
        if ret == {} and info.status_code == 200:
            return True
        else:
            raise Exception('对象存储异常！')

    @staticmethod
    def __new_name(name, child_name, is_date_splice=True, is_rename=True):
        """
        将上传的文件重新命名
        :param name: 文件名
        :param child_name: 子空间域名
        :param is_date_splice: 按时间分文件夹
        :param is_rename: 名字重新构建
        :return: 新的文件名
        """
        if is_date_splice:
            # 获取当前的时间：年_月_日，作为二级文件夹的名字
            now_time = datetime.now().strftime("%Y_%m_%d")
            # 整理路径，并返回
            new_name = f"{child_name}/{now_time}/"
        else:
            new_name = f"{child_name}/"

        if is_rename:
            # 获取文件后缀
            file_extension = name.split('.').pop()
            # 因为业务量级不大，所以以时间戳为文件名字
            name = int(time.time())
            new_name += f"{name}.{file_extension}"
        else:
            new_name += name
        return new_name

    def get_private_download_url(self, key, expires=3600):
        """
        获取私有空间文件的临时下载地址
        :param key: 文件在七牛云上的完整路径
        :param expires: 链接的有效期（秒），默认1小时
        :return: 临时下载地址
        """
        if self.__is_public:
            raise ValueError("This method is only for private buckets")

        base_url = f'{self.__base_url}{key}'
        private_url = self.qiniu_server.private_download_url(base_url, expires=expires)
        return private_url


if __name__ == '__main__':
    # print(gaode_get_city(113.271899, 23.132837))
    # send_sms("123456", "18675474738")
    qiniu = QiNiuStorage("avatars", is_public=False)
    # with open("qiniu_tools.py", 'rb') as f:
    #     url = qiniu.upload("test2.py", f, is_date_splice=False, is_rename=False)
    #     print(url)
    print(qiniu.get_private_download_url("avatars/test2.py"))

