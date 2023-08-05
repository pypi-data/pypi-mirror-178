# -*- coding: utf-8 -*-
import os.path

from .type import RequestType
from .utils import sha256


class Media:
    """
    其他能力-> 图片上传 和 视频上传
    参考 https://pay.weixin.qq.com/wiki/doc/apiv3_partner/apis/chapter2_1_1.shtml
    """

    def __init__(self, parent):
        from .mch import WeChatPay

        if not isinstance(parent, WeChatPay):
            raise Exception('BasePay need WeChatPay!')
        self._p = parent    # 父对象， 服务商

    def media_upload(self, filepath, filename, path):
        if not (filepath and os.path.exists(filepath) and os.path.isfile(filepath) and path):
            raise Exception('filepath is not assigned or not exists')
        with open(filepath, mode='rb') as f:
            content = f.read()
        if not filename:
            filename = os.path.basename(filepath)
        params = {}
        params.update({'meta': '{"filename":"%s","sha256":"%s"}' % (filename, sha256(content))})
        mimes = {
            '.bmp': 'image/bmp',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.avi': 'video/x-msVideo',
            '.wmv': 'video/x-ms-wmv',
            '.mpeg': 'video/mpeg',
            '.mp4': 'video/mp4',
            '.mov': 'video/quicktime',
            '.mkv': 'video/x-matroska',
            '.flv': 'video/x-flv',
            '.f4v': 'video/x-f4v',
            '.m4v': 'video/x-m4v',
            '.rmvb': 'application/vnd.rn-realMedia-vbr'
        }
        media_type = os.path.splitext(filename)[-1]
        if media_type not in mimes:
            raise Exception('sdk does not support this media type.')
        files = [('file', (filename, content, mimes[media_type].lower()))]
        return self._p.core.request(path, method=RequestType.POST, data=params,
                                    sign_data=params.get('meta'), files=files)

    def image_upload(self, filepath, filename=None):
        """图片上传
        :param filepath: 图片文件路径
        :param filename: 文件名称，未指定则从filepath参数中截取
        """
        return self.media_upload(filepath, filename, path='/v3/merchant/media/upload')

    def video_upload(self, filepath, filename=None):
        """视频上传
        :param filepath: 视频文件路径
        :param filename: 文件名称，未指定则从filepath参数中截取
        """
        return self.media_upload(filepath, filename, path='/v3/merchant/media/video_upload')
