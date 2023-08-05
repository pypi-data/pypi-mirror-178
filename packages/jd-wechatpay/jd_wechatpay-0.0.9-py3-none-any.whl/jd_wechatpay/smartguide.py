# -*- coding: utf-8 -*-

from .type import RequestType


class Guide:
    """
    直联商户 支付即服务——服务人员注册 等
    参考 https://pay.weixin.qq.com/wiki/doc/apiv3/apis/chapter8_4_1.shtml
    """

    def __init__(self, parent):
        from .mch import WeChatPay

        if not isinstance(parent, WeChatPay):
            raise Exception('BasePay need WeChatPay!')
        self._p = parent    # 父对象

    def register(self, corp_id, store_id, userid, name, mobile, qr_code, avatar, group_qrcode=None, sub_mchid=None):
        """服务人员注册
        :param corp_id: 企业ID, 示例值：'1234567890'
        :param store_id: 门店ID, 示例值：12345678
        :param userid: 企业微信的员工ID, 示例值：'robert'
        :param name: 企业微信的员工姓名, 示例值：'robert'
        :param mobile: 手机号码, 示例值：'13900000000'
        :param qr_code: 员工个人二维码, 示例值：'https://open.work.weixin.qq.com/wwopen/userQRCode?vcode=xxx'
        :param avatar: 头像URL, 示例值：'https://wx.qlogo.cn/mmopen/ajNVdqHZLLA3WJ.../0'
        :param group_qrcode: 群二维码URL, 示例值：'https://p.qpic.cn/wwhead/nMl9ssowtibVGyrmvBiaibzDtp/0'
        :param sub_mchid: (服务商模式)子商户的商户号，由微信支付生成并下发。示例值:'1900000109'
        """
        params = {}
        if corp_id:
            params.update(dict(corpid=corp_id))
        else:
            raise Exception('corp_id is not assigned.')
        if store_id:
            params.update({'store_id': store_id})
        else:
            raise Exception('store_id is not assigned.')
        if userid:
            params.update({'userid': userid})
        else:
            raise Exception('userid is not assigned.')
        if name:
            params.update({'name': self._p.core.encrypt(name)})
        else:
            raise Exception('name is not assigned')
        if mobile:
            params.update({'mobile': self._p.core.encrypt(mobile)})
        else:
            raise Exception('mobile is not assigned.')
        if qr_code:
            params.update({'qr_code': qr_code})
        else:
            raise Exception('qr_code is not assigned.')
        if avatar:
            params.update({'avatar': avatar})
        else:
            raise Exception('avatar is not assigned.')
        if group_qrcode:
            params.update({'group_qrcode': group_qrcode})
        if self._p.partner_mode and sub_mchid:
            params.update({'sub_mchid': sub_mchid})
        path = '/v3/smartguide/guides'
        return self._p.core.request(path, method=RequestType.POST, data=params, cipher_data=True)

    def assign(self, guide_id, out_trade_no):
        """服务人员分配
        :param guide_id: 服务人员ID，示例值：'LLA3WJ6DSZ...'
        :param out_trade_no: 商户订单号, 示例值：'20150806125346'
        """
        params = {}
        if out_trade_no:
            params.update({'out_trade_no': out_trade_no})
        else:
            raise Exception('out_trade_no is not assigned.')
        if not guide_id:
            raise Exception('guide_id is not assigned.')
        path = '/v3/smartguide/guides/%s/assign' % guide_id
        return self._p.core.request(path, method=RequestType.POST, data=params)

    def guides_query(self, store_id, userid=None, mobile=None, work_id=None, limit=None, offset=0, sub_mchid=None):
        """
        服务人员查询
        :param store_id:    门店ID, 示例值：1234
        :param userid:      企业微信的员工ID, 示例值：'robert'
        :param mobile:      手机号码, 需进行加密处理, 示例值：'7mKQe3p...'
        :param work_id:     工号, 示例值：'robert'
        :param limit:       最大资源条数, 示例值：5
        :param offset:      请求资源起始位置, 示例值：0
        :param sub_mchid:   (服务商模式)子商户的商户号，由微信支付生成并下发。示例值:'1900000109'
        :return:
        """
        if not store_id:
            raise Exception('store_id is not assigned.')
        path = '/v3/smartguide/guides?store_id=%s' % store_id
        if userid:
            path = path + '&userid=%s' % userid
        cipher_data = False
        if mobile:
            path = path + '&mobile=%s' % self._p.core.encrypt(mobile)
            cipher_data = True
        if work_id:
            path = path + '&work_id=%s' % work_id
        if limit:
            path = path + '&limit=%s' % limit
        if offset:
            path = path + '&offset=%s' % offset
        if self._p.partner_mode and sub_mchid:
            path = '%s&sub_mchid=%s' % (path, sub_mchid)
        return self._p.core.request(path, cipher_data=cipher_data)

    def update(self, guide_id, name=None, mobile=None, qr_code=None, avatar=None, group_qrcode=None, sub_mchid=None):
        """服务人员信息更新
        :params guide_id: 服务人员ID, 示例值：'LLA3WJ6DSZ...'
        :params name: 服务人员姓名, 示例值：'robert'
        :params mobile: 服务人员手机号码, 示例值：'13900000000'
        :params qr_code: 服务人员二维码URL, 示例值：'https://open.work.weixin.qq.com/wwopen/userQRCode?vcode=xxx'
        :params avatar: 服务人员头像URL, 示例值：'https://wx.qlogo.cn/mmopen/ajNVdqHZLLA3WJ6DSZ.../0'
        :params group_qrcode: 群二维码URL, 示例值：'https://p.qpic.cn/wwhead/nMl9ssowtibVGyrmvBiaibzDtp/0'
        :params sub_mchid: (服务商模式)子商户的商户号，由微信支付生成并下发。示例值:'1900000109'
        """
        params = {}
        if not guide_id:
            raise Exception('guide_id is not assigned.')
        path = '/v3/smartguide/guides/%s' % guide_id
        cipher_data = False
        if name:
            params.update({'name': self._p.core.encrypt(name)})
            cipher_data = True
        if mobile:
            params.update({'mobile': self._p.core.encrypt(mobile)})
            cipher_data = True
        if qr_code:
            params.update({'qr_code': qr_code})
        if avatar:
            params.update({'avatar': avatar})
        if group_qrcode:
            params.update({'group_qrcode': group_qrcode})
        if self._p.partner_mode and sub_mchid:
            params.update({'sub_mchid': sub_mchid})
        return self._p.core.request(path, method=RequestType.PATCH, data=params, cipher_data=cipher_data)
