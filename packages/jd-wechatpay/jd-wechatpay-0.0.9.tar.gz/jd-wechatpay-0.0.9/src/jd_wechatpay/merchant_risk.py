# -*- coding: utf-8 -*-

from .type import RequestType


class MerchantRisk:
    """
    风险合规——商户违规通知回调
    https://pay.weixin.qq.com/wiki/doc/apiv3_partner/apis/chapter10_3_1.shtml
    仅支持服务商
    """

    def __init__(self, parent):
        from .mch import WeChatPay

        if not isinstance(parent, WeChatPay):
            raise Exception('BasePay need WeChatPay!')
        self._p = parent    # 父对象， 服务商

    def callback_create(self, notify_url=None):
        """创建商户违规通知回调地址
        :param notify_url: 通知地址，示例值:'https://www.weixin.qq.com/wxpay/pay.php'
        """
        params = {}
        if notify_url:
            params.update({'notify_url': notify_url})
        path = '/v3/merchant-risk-manage/violation-notifications'
        return self._p.core.request(path, method=RequestType.POST, data=params)

    def callback_query(self):
        """查询商户违规通知回调地址
        """
        path = '/v3/merchant-risk-manage/violation-notifications'
        return self._p.core.request(path)

    def callback_update(self, notify_url=None):
        """修改商户违规通知回调地址
        :param notify_url: 通知地址，示例值:'https://www.weixin.qq.com/wxpay/pay.php'
        """
        params = {}
        if notify_url:
            params.update({'notify_url': notify_url})
        path = '/v3/merchant-risk-manage/violation-notifications'
        return self._p.core.request(path, method=RequestType.PUT, data=params)

    def callback_delete(self):
        """查询商户违规通知回调地址
        """
        path = '/v3/merchant-risk-manage/violation-notifications'
        return self._p.core.request(path, method=RequestType.DELETE)
