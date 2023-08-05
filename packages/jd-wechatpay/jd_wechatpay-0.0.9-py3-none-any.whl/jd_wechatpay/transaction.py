# -*- coding: utf-8 -*-

from .type import RequestType, WeChatPayType


class BasePay:
    """
    直联商户 基础支付
    参考 https://pay.weixin.qq.com/wiki/doc/apiv3/open/pay/chapter2_7_0.shtml

    # 服务商 基础支付
    # 参考 https://pay.weixin.qq.com/wiki/doc/apiv3_partner/apis/chapter4_5_1.shtml
    """

    def __init__(self, parent):
        from .mch import WeChatPay

        if not isinstance(parent, WeChatPay):
            raise Exception('BasePay need WeChatPay!')
        self._p = parent    # 父对象

    def pay(self,
            description,
            out_trade_no,
            amount,
            payer=None,
            time_expire=None,
            attach=None,
            goods_tag=None,
            detail=None,
            scene_info=None,
            settle_info=None,
            notify_url=None,
            app_id=None,
            mch_id=None,
            sub_app_id=None,
            sub_mch_id=None,
            support_invoice=False,
            pay_type=None
            ):
        """统一下单
        :return code, message:

        :param description: 商品描述，示例值：'Image形象店-深圳腾大-QQ公仔'
        :param out_trade_no: 商户订单号，示例值：'1217752501201407033233368018'
        :param amount: 订单金额，示例值：{'total':100, 'currency':'CNY'}
        :param payer: 支付者，示例值：{'openid':'oHkCY...'}
        :param time_expire: 交易结束时间，示例值：'2018-06-08T10:34:56+08:00'
        :param attach: 附加数据，示例值：'自定义数据'
        :param goods_tag: 订单优惠标记，示例值：'WXG'
        :param detail: 优惠功能，示例值：{'cost_price':608800, 'invoice_id':'微信123',
          'goods_detail':[{'merchant_goods_id':'商品编码', 'wechatpay_goods_id':'1001',
          'goods_name':'iPhoneX 256G', 'quantity':1, 'unit_price':828800}]}
        :param scene_info: 场景信息，示例值：{'payer_client_ip':'14.23.150.211',
           'device_id':'013467007045764', 'store_info':{'id':'0001', 'name':'腾讯大厦分店',
           'area_code':'440305', 'address':'广东省深圳市南山区科技中一道10000号'}}
        :param settle_info: 结算信息，示例值：{'profit_sharing':False}
        :param notify_url: 通知地址，示例值：'https://www.weixin.qq.com/wxpay/pay.php'
        :param app_id: 应用ID，可不填，默认初始化时传入的app id，示例值：'wx1234567890...'
        :param mch_id: 微信支付商户号，可不填，默认传入初始化的 mch id，示例值：'987654321'
        :param sub_app_id: (服务商模式)子商户应用ID，示例值：'wxd678efh567hg6999'
        :param sub_mch_id: (服务商模式)子商户的商户号，由微信支付生成并下发。示例值：'1900000109'
        :param support_invoice: 电子发票入口开放标识，传入true时，支付成功消息和支付详情页将出现开票入口。
        :param pay_type: 微信支付类型，示例值:WeChatPayType.JSAPI
        """
        params = {}
        if not (notify_url or self._p.notify_url):
            raise Exception('notify_url is not assigned.')
        params.update({'notify_url': notify_url or self._p.notify_url,
                       'description': description, 'out_trade_no': out_trade_no,
                       'amount': amount})
        if payer:
            params.update({'payer': payer})
        if scene_info:
            params.update({'scene_info': scene_info})
        if time_expire:
            params.update({'time_expire': time_expire})
        if attach:
            params.update({'attach': attach})
        if goods_tag:
            params.update({'goods_tag': goods_tag})
        if detail:
            params.update({'detail': detail})
        if settle_info:
            params.update({'settle_info': settle_info})

        pay_type = pay_type or self._p.type
        path = ''
        if self._p.partner_mode:    # 服务商
            params.update(dict(
                sp_appid=app_id or self._p.app_id,
                sp_mchid=mch_id or self._p.mch_id
            ))
            if sub_mch_id:
                params.update(dict(sub_mchid=sub_mch_id))
            else:
                raise Exception('sub_mchid is not assigned.')
            if sub_app_id:
                params.update(dict(sub_appid=sub_app_id))
            if pay_type in [WeChatPayType.JSAPI, WeChatPayType.MINI_APP]:
                if not payer:
                    raise Exception('payer is not assigned')
                path = '/v3/pay/partner/transactions/jsapi'
            elif pay_type == WeChatPayType.APP:
                path = '/v3/pay/partner/transactions/app'
            elif pay_type == WeChatPayType.H5:
                if not scene_info:
                    raise Exception('scene_info is not assigned.')
                path = '/v3/pay/partner/transactions/h5'
            elif pay_type == WeChatPayType.NATIVE:
                path = '/v3/pay/partner/transactions/native'
        else:   # 直连商户
            params.update(dict(
                appid=app_id or self._p.app_id,
                mchid=mch_id or self._p.mch_id,
            ))
            if pay_type in [WeChatPayType.JSAPI, WeChatPayType.MINI_APP]:
                if not payer:
                    raise Exception('payer is not assigned')
                path = '/v3/pay/transactions/jsapi'
            elif pay_type == WeChatPayType.APP:
                path = '/v3/pay/transactions/app'
            elif pay_type == WeChatPayType.H5:
                if not scene_info:
                    raise Exception('scene_info is not assigned.')
                path = '/v3/pay/transactions/h5'
            elif pay_type == WeChatPayType.NATIVE:
                path = '/v3/pay/transactions/native'

        if support_invoice:
            params.update(dict(support_fapiao=support_invoice))
        return self._p.core.request(path, method=RequestType.POST, data=params)

    def close(self, out_trade_no, mch_id=None, sub_mch_id=None):
        """关闭订单
        :param out_trade_no: 商户订单号，示例值：'1217752501201407033233368018'
        :param mch_id: 微信支付商户号，可不传，默认传入初始化的 mch id。示例值：'987654321'
        :param sub_mch_id: (服务商模式)子商户的商户号，由微信支付生成并下发。示例值：'1900000109'
        """
        if not out_trade_no:
            raise Exception('out_trade_no is not assigned.')

        if self._p.partner_mode:    # 服务商
            path = '/v3/pay/partner/transactions/out-trade-no/%s/close' % out_trade_no
            if sub_mch_id:
                params = dict(sp_mchid=mch_id or self._p.mch_id, sub_mchid=sub_mch_id)
            else:
                raise Exception('sub_mchid is not assigned.')
        else:   # 直连商户
            path = '/v3/pay/transactions/out-trade-no/%s/close' % out_trade_no
            params = dict(mchid=self._p.mch_id)
        return self._p.core.request(path, method=RequestType.POST, data=params)

    def query(self, transaction_id=None, out_trade_no=None, mch_id=None, sub_mch_id=None):
        """查询订单
        :param transaction_id: 微信支付订单号，示例值：1217752501201407033233368018
        :param out_trade_no: 商户订单号，示例值：1217752501201407033233368018
        :param mch_id: 微信支付商户号，可不传，默认传入初始化的 mch id。示例值：'987654321'
        :param sub_mch_id: (服务商模式)子商户的商户号，由微信支付生成并下发。示例值：'1900000109'
        """
        if not (transaction_id or out_trade_no):
            raise Exception('transaction_id or out_trade_no is not assigned')

        if self._p.partner_mode:    # 服务商模式
            if transaction_id:
                path = '/v3/pay/partner/transactions/id/%s' % transaction_id
            else:
                path = '/v3/pay/partner/transactions/out-trade-no/%s' % out_trade_no
            path = '%s?sp_mchid=%s&sub_mchid=%s' % (path, mch_id or self._p.mch_id, sub_mch_id)
        else:   # 直连商户
            if transaction_id:
                path = '/v3/pay/transactions/id/%s' % transaction_id
            else:
                path = '/v3/pay/transactions/out-trade-no/%s' % out_trade_no
            path = '%s?mchid=%s' % (path, self._p.mch_id)
        return self._p.core.request(path)

    def refund(self,
               out_refund_no,
               amount,
               transaction_id=None,
               out_trade_no=None,
               reason=None,
               funds_account=None,
               goods_detail=None,
               notify_url=None,
               sub_mch_id=None):
        """申请退款
        :param out_refund_no: 商户退款单号，示例值：'1217752501201407033233368018'
        :param amount: 金额信息，示例值：{'refund':888, 'total':888, 'currency':'CNY'}
        :param transaction_id: 微信支付订单号，示例值：'1217752501201407033233368018'
        :param out_trade_no: 商户订单号，示例值：'1217752501201407033233368018'
        :param reason: 退款原因，示例值：'商品已售完'
        :param funds_account: 退款资金来源，示例值：'AVAILABLE'
        :param goods_detail: 退款商品，示例值：{'merchant_goods_id':'1217752501201407033233368018',
          'wechatpay_goods_id':'1001', 'goods_name':'iPhone6s 16G', 'unit_price':528800,
           'refund_amount':528800, 'refund_quantity':1}
        :param notify_url: 通知地址，示例值：'https://www.weixin.qq.com/wxpay/pay.php'
        :param sub_mch_id: (服务商模式)子商户的商户号，由微信支付生成并下发。示例值：'1900000109'
        """
        params = {}
        params.update({'notify_url': notify_url or self._p.notify_url})
        if out_refund_no:
            params.update({'out_refund_no': out_refund_no})
        else:
            raise Exception('out_refund_no is not assigned.')
        if amount:
            params.update({'amount': amount})
        else:
            raise Exception('amount is not assigned.')
        if transaction_id:
            params.update({'transaction_id': transaction_id})
        elif out_trade_no:
            params.update({'out_trade_no': out_trade_no})
        else:
            raise Exception('transaction_id is not assigned.')
        if reason:
            params.update({'reason': reason})
        if funds_account:
            params.update({'funds_account': funds_account})
        if goods_detail:
            params.update({'goods_detail': goods_detail})
        if self._p.partner_mode:   # 服务商
            if sub_mch_id:
                params.update(dict(sub_mchid=sub_mch_id))
            else:
                raise Exception('sub_mch_id is not assigned.')
        path = '/v3/refund/domestic/refunds'
        return self._p.core.request(path, method=RequestType.POST, data=params)

    def query_refund(self, out_refund_no, sub_mch_id=None):
        """查询单笔退款
        :param out_refund_no: 商户退款单号，示例值：'1217752501201407033233368018'
        :param sub_mch_id: (服务商模式)子商户的商户号，由微信支付生成并下发。示例值：'1900000109'
        """
        path = '/v3/refund/domestic/refunds/%s' % out_refund_no
        if self._p.partner_mode:    # 服务商模式
            if sub_mch_id:
                path = '%s?sub_mchid=%s' % (path, sub_mch_id)
            else:
                raise Exception('sub_mch_id is not assigned.')
        return self._p.core.request(path)

    def trade_bill(self, bill_date, bill_type='ALL', tar_type='GZIP', sub_mchid=None):
        """申请交易账单
        :param bill_date: 账单日期，示例值：'2019-06-11'
        :param bill_type: 账单类型, 默认值：'ALL'
        :param tar_type: 压缩类型，默认值：'GZIP'
        :param sub_mchid: (服务商模式)子商户的商户号，由微信支付生成并下发。示例值：'1900000109'
        """
        path = '/v3/bill/tradeBill?bill_date=%s&bill_type=%s&tar_type=%s' % (bill_date, bill_type, tar_type)
        if self._p.partner_mode and sub_mchid:
            path = '%s&sub_mchid=%s' % (path, sub_mchid)
        return self._p.core.request(path)

    def fund_flow_bill(self, bill_date, account_type='BASIC', tar_type='GZIP'):
        """申请资金账单
        :param bill_date: 账单日期，示例值：'2019-06-11'
        :param account_type: 资金账户类型, 默认值：'BASIC'，基本账户, 可选：'OPERATION'，运营账户；'FEES'，手续费账户
        :param tar_type: 压缩类型，默认值：'GZIP'
        """
        if not bill_date:
            raise Exception('bill_date is not assigned.')
        path = '/v3/bill/fundFlowBill?bill_date=%s&account_type=%s&tar_type=%s' % (bill_date, account_type, tar_type)
        return self._p.core.request(path)

    def sub_merchant_fund_flow_bill(self, sub_mchid, bill_date, account_type='BASIC', algorithm='AEAD_AES_256_GCM',
                                    tar_type='GZIP'):
        """申请单个子商户资金账单
        https://pay.weixin.qq.com/wiki/doc/apiv3_partner/apis/chapter4_5_12.shtml
        :param sub_mchid: 子商户号，示例值：'19000000001'
        :param bill_date: 账单日期，示例值：'2019-06-11'
        :param account_type: 资金账户类型, 默认值：'BASIC'，基本账户, 可选：'OPERATION'，运营账户；'FEES'，手续费账户
        :param algorithm: 加密算法，示例值：AEAD_AES_256_GCM
        :param tar_type: 压缩类型，默认值：'GZIP'
        """
        if not sub_mchid:
            raise Exception('sub_mchid is not assigned.')
        if not bill_date:
            raise Exception('bill_date is not assigned.')
        path = 'https://api.mch.weixin.qq.com/v3/bill/sub-merchant-fundflowbill' \
               '?sub_mchid=%s&bill_date=%s&account_type=%s&algorithm=%s&tar_type=%s'\
               % (sub_mchid, bill_date, account_type, algorithm, tar_type)
        return self._p.core.request(path)

    def download_bill(self, url):
        """下载账单
        :param url: 账单下载地址，示例值：'https://api.mch.weixin.qq.com/v3/billdownload/file?token=xxx'
        """
        path = url[len(self._p.core.gate_way):] if url.startswith(self._p.core.gate_way) else url
        return self._p.core.request(path, skip_verify=True)

    def combine_pay(self,
                    combine_out_trade_no,
                    sub_orders,
                    scene_info=None,
                    combine_payer_info=None,
                    time_start=None,
                    time_expire=None,
                    combine_appid=None,
                    combine_mchid=None,
                    notify_url=None):
        """合单支付下单
        :param combine_out_trade_no: 合单商户订单号, 示例值：'P20150806125346'
        :param sub_orders: 子单信息，示例值：[{'mchid':'1900000109', 'attach':'深圳分店',
          'amount':{'total_amount':100,'currency':'CNY'}, 'out_trade_no':'20150806125346',
          'description':'腾讯充值中心-QQ会员充值', 'settle_info':{'profit_sharing':False, 'subsidy_amount':10}}]
        :param scene_info: 场景信息, 示例值：{'device_id':'POS1:123', 'payer_client_ip':'14.17.22.32'}
        :param combine_payer_info: 支付者, 示例值：{'openid':'oUpF8uMuAJO_M2pxb1Q9zNjWeS6o'}
        :param time_start: 交易起始时间，示例值：'2019-12-31T15:59:59+08:00'
        :param time_expire: 交易结束时间, 示例值：'2019-12-31T15:59:59+08:00'
        :param combine_appid: 合单商户appid, 示例值：'wxd678efh567hg6787'
        :param combine_mchid: 合单发起方商户号，示例值：'1900000109'
        :param notify_url: 通知地址, 示例值：'https://yourapp.com/notify'
        """
        params = dict(combine_appid=combine_appid or self._p.app_id,
                      combine_mchid=combine_mchid or self._p.mch_id)
        if not (notify_url or self._p.notify_url):
            raise Exception('notify_url is not assigned.')
        params.update({'notify_url': notify_url or self._p.notify_url})
        if combine_out_trade_no:
            params.update({'combine_out_trade_no': combine_out_trade_no})
        else:
            raise Exception('combine_out_trade_no is not assigned.')
        if sub_orders:
            params.update({'sub_orders': sub_orders})
        else:
            raise Exception('sub_orders is not assigned.')
        if scene_info:
            params.update({'scene_info': scene_info})
        if combine_payer_info:
            params.update({'combine_payer_info': combine_payer_info})
        if time_start:
            params.update({'time_start': time_start})
        if time_expire:
            params.update({'time_expire': time_expire})

        path = ''
        if self._p.type in [WeChatPayType.JSAPI, WeChatPayType.MINI_APP]:
            if not combine_payer_info:
                raise Exception('combine_payer_info is not assigned')
            path = '/v3/combine-transactions/jsapi'
        elif self._p.type == WeChatPayType.APP:
            path = '/v3/combine-transactions/app'
        elif self._p.type == WeChatPayType.H5:
            if not scene_info:
                raise Exception('scene_info is not assigned.')
            path = '/v3/combine-transactions/h5'
        elif self._p.type == WeChatPayType.NATIVE:
            path = '/v3/combine-transactions/native'
        return self._p.core.request(path, method=RequestType.POST, data=params)

    def combine_query(self, combine_out_trade_no):
        """合单查询订单
        :param combine_out_trade_no: 合单商户订单号，示例值：P20150806125346
        """
        params = {}
        if not combine_out_trade_no:
            raise Exception('combine_out_trade_no is not assigned')
        else:
            params.update({'combine_out_trade_no': combine_out_trade_no})
        path = '/v3/combine-transactions/out-trade-no/%s' % combine_out_trade_no
        return self._p.core.request(path)

    def combine_close(self, combine_out_trade_no, sub_orders, combine_appid=None):
        """合单关闭订单
        :param combine_out_trade_no: 合单商户订单号，示例值：'P20150806125346'
        :param sub_orders: 子单信息, 示例值：[{'mchid': '1900000109', 'out_trade_no': '20150806125346'}]
        :param combine_appid: 合单商户appid, 示例值：'wxd678efh567hg6787'
        """
        params = dict(combine_appid=combine_appid or self._p.app_id)
        if not combine_out_trade_no:
            raise Exception('combine_out_trade_no is not assigned.')
        if not sub_orders:
            raise Exception('sub_orders is not assigned.')
        else:
            params.update({'sub_orders': sub_orders})
        path = '/v3/combine-transactions/out-trade-no/%s/close' % combine_out_trade_no
        return self._p.core.request(path, method=RequestType.POST, data=params)
