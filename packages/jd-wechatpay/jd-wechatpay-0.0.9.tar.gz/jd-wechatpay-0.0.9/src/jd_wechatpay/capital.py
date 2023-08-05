# -*- coding: utf-8 -*-
from urllib.parse import urlencode


class Capital:
    """
    其他——银行组件
    https://pay.weixin.qq.com/wiki/doc/apiv3_partner/Offline/apis/chapter11_2_1.shtml
    """

    def __init__(self, parent):
        from .mch import WeChatPay

        if not isinstance(parent, WeChatPay):
            raise Exception('BasePay need WeChatPay!')
        self._p = parent    # 父对象

    def search_bank_number(self, account_number):
        """获取对私银行卡号开户银行
        :param account_number: 银行卡号，示例值：'1234567890123'
        """
        params = {}
        params.update({'account_number': self._p.core.encrypt(account_number)})
        path = 'https://api.mch.weixin.qq.com/v3/capital/capitallhh/banks/search-banks-by-bank-account?%s' % \
               urlencode(params)
        return self._p.core.request(path, cipher_data=True)

    def personal_banks(self, offset=0, limit=200):
        """查询支持个人业务的银行列表
        :param offset: 本次查询偏移量，示例值：0
        :param limit: 本次请求最大查询条数，示例值：200
        """
        path = 'https://api.mch.weixin.qq.com/v3/capital/capitallhh/banks/personal-banking' \
               '?offset=%s&limit=%s' % (offset, limit)
        return self._p.core.request(path)

    def corporate_banks(self, offset=0, limit=200):
        """查询支持对公业务的银行列表
        :param offset: 本次查询偏移量，示例值：0
        :param limit: 本次请求最大查询条数，示例值：200
        """
        path = 'https://api.mch.weixin.qq.com/v3/capital/capitallhh/banks/corporate-banking' \
               '?offset=%s&limit=%s' % (offset, limit)
        return self._p.core.request(path)

    def provinces(self):
        """查询省份列表
        """
        path = 'https://api.mch.weixin.qq.com/v3/capital/capitallhh/areas/provinces'
        return self._p.core.request(path)

    def cities(self, province_code):
        """查询城市列表
        :param province_code: 省份编码，唯一标识一个省份。示例值：10
        """
        path = 'https://api.mch.weixin.qq.com/v3/capital/capitallhh/areas/provinces/%s/cities' % province_code
        return self._p.core.request(path)

    def branches(self, bank_alias_code, city_code, offset=0, limit=100):
        """查询支行列表
        :param bank_alias_code: 银行别名的编码，查询支行接口仅支持需要填写支行的银行别名编码。示例值：1000006247
        :param city_code: 城市编码，唯一标识一座城市，用于结合银行别名编码查询支行列表。示例值：536
        :param offset: 本次查询偏移量，示例值：0
        :param limit: 本次请求最大查询条数，示例值：100
        """
        if bank_alias_code and city_code:
            path = 'https://api.mch.weixin.qq.com/v3/capital/capitallhh/banks/%s/branches' \
                   '?city_code=%s&offset=%s&limit=%s' % (bank_alias_code, city_code, offset, limit)
        else:
            raise Exception('bank_alias_code or city_code is not assigned.')
        return self._p.core.request(path)
