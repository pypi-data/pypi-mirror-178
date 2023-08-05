# -*- coding: utf-8 -*-
import os.path
from .type import RequestType
from .utils import sm3


class Invoice:
    """
    其他——电子发票
    https://pay.weixin.qq.com/wiki/doc/apiv3/Offline/apis/chapter4_8_5.shtml
    """

    def __init__(self, parent):
        from .mch import WeChatPay

        if not isinstance(parent, WeChatPay):
            raise Exception('BasePay need WeChatPay!')
        self._p = parent    # 父对象， 服务商

    def card_template(self, card_template_information, card_appid=None):
        """创建电子发票卡券模板
        :param card_template_information: 卡券模板信息。示例值:{'logo_url':'https://mmbiz.qpic.cn/mmbiz/iaL1LJM1mF9aRKPZJkmG8xX'}
        :param card_appid: 插卡公众号AppID，若是服务商模式，则可以是服务商申请的appid，也可以是子商户申请的appid；
                           若是直连模式，则是直连商户申请的appid。示例值：wxb1170446a4c0a5a2
        """
        params = {}
        params.update({'card_appid': card_appid or self._p.app_id})
        if card_template_information:
            params.update({'card_template_information': card_template_information})
        else:
            raise Exception('card_template_information is not assigned.')
        path = 'https://api.mch.weixin.qq.com/v3/new-tax-control-fapiao/card-template'
        return self._p.core.request(path, method=RequestType.POST, data=params)

    def merchant_config(self, callback_url=None):
        """配置开发选项
        :param callback_url: 商户回调地址。收取微信的授权通知、开票通知、插卡通知等相关通知。示例值：'https://pay.weixin.qq.com/callback'
        """
        params = {}
        params.update({'callback_url': callback_url or self._p.notify_url})
        path = 'https://api.mch.weixin.qq.com/v3/new-tax-control-fapiao/merchant/development-config'
        return self._p.core.request(path, method=RequestType.PATCH, data=params)

    def get_merchant_config(self):
        """查询商户配置的开发选项
        """
        path = 'https://api.mch.weixin.qq.com/v3/new-tax-control-fapiao/merchant/development-config'
        return self._p.core.request(path)

    def title_url(self, apply_id, source, total_amount, openid, appid=None,
                  seller_name=None, show_phone_cell=False, must_input_phone=False,
                  show_email_cell=False, must_input_email=False):
        """获取抬头填写链接
        :param apply_id: 发票申请单号，示例值：'4200000444201910177461284488'
        :param source: 开票来源，WEB：微信H5开票，MINIPROGRAM：微信小程序开票，示例值：'WEB'
        :param total_amount: 总金额，单位：分，示例值：100
        :param openid: 需要填写发票抬头的用户在商户AppID下的OpenID，示例值：'plN5twRbHym_j-QcqCz1tl0HmwEs'
        :param appid: 若开票来源是WEB，则为商户的公众号AppID；若开票来源是MINIPROGRAM，则为商户的小程序AppID，示例值：'wxb1170446a4c0a5a2'
        :param seller_name: 销售方名称，若不传则默认取商户名称，示例值：'深圳市南山区测试商户'
        :param show_phone_cell: 是否需要展示手机号填写栏
        :param must_input_phone: 是否必须填写手机号，仅当需要展示手机号填写栏时生效
        :param show_email_cell: 是否需要展示邮箱地址填写栏
        :param must_input_email: 是否必须填写邮箱地址，仅当需要展示邮箱地址填写栏时生效
        """
        path = 'https://api.mch.weixin.qq.com/v3/new-tax-control-fapiao/user-title/title-url'
        params = {}
        params.update(dict(
            fapiao_apply_id=apply_id, source=source, total_amount=total_amount,
            appid=appid or self._p.app_id, openid=openid,
        ))
        if seller_name:
            params.update(dict(seller_name=seller_name))
        if show_phone_cell:
            params.update(dict(show_phone_cell=True))
        if must_input_phone:
            params.update(dict(must_input_phone=True))
        if show_email_cell:
            params.update(dict(show_email_cell=True))
        if must_input_email:
            params.update(dict(must_input_email=True))
        return self._p.core.request(path, data=params)

    def title(self, apply_id, scene='WITH_WECHATPAY'):
        """获取用户填写的抬头
        :param apply_id: 发票申请单号，示例值：'4200000444201910177461284488'
        :param scene: 场景值，目前只支持WITH_WECHATPAY。示例值：'WITH_WECHATPAY'
        """
        path = 'https://api.mch.weixin.qq.com/v3/new-tax-control-fapiao/user-title'
        params = dict(
            fapiao_apply_id=apply_id, scene=scene
        )
        return self._p.core.request(path, data=params)

    def tax_codes(self, offset=0, limit=20):
        """获取商品和服务税收分类对照表
        :param offset: 查询的起始位置，示例值：0
        :param limit: 查询的最大数量，最大值20
        """
        path = 'https://api.mch.weixin.qq.com/v3/new-tax-control-fapiao/merchant/tax-codes?offset=%s&limit=%s' % \
               (offset, limit)
        return self._p.core.request(path)

    def merchant_base_info(self):
        """获取商户开票基础信息
        """
        path = 'https://api.mch.weixin.qq.com/v3/new-tax-control-fapiao/merchant/base-information'
        return self._p.core.request(path)

    def applications(self, apply_id, buyer_information, information, scene='WITH_WECHATPAY'):
        """开具电子发票
        :param apply_id: 发票申请单号，示例值：'4200000444201910177461284488'
        :param buyer_information: 购买方信息，示例值：{'type':'ORGANIZATION','name':'深圳市南山区测试企业'}
        :param information: 需要开具的发票信息
        :param scene: 场景值，目前只支持WITH_WECHATPAY。示例值：'WITH_WECHATPAY'
        """
        params = dict(fapiao_apply_id=apply_id, fapiao_information=information, scene=scene)
        cipher_data = False
        if buyer_information:
            if buyer_information.get('phone'):
                buyer_information.update({'phone': self._p.core.encrypt(buyer_information.get('phone'))})
                cipher_data = True
            if buyer_information.get('email'):
                buyer_information.update({'email': self._p.core.encrypt(buyer_information.get('email'))})
                cipher_data = True
            params.update({'buyer_information': buyer_information})
        else:
            raise Exception('buyer_information is not assigned.')
        path = 'https://api.mch.weixin.qq.com/v3/new-tax-control-fapiao/fapiao-applications'
        return self._p.core.request(path, method=RequestType.POST, data=params, cipher_data=cipher_data)

    def invoice_query(self, apply_id, invoice_id=None):
        """查询电子发票
        :param apply_id: 发票申请单号，示例值：'4200000444201910177461284488'
        :param invoice_id: 商户发票单号，示例值：'20200701123456'
        """
        path = 'https://api.mch.weixin.qq.com/v3/new-tax-control-fapiao/fapiao-applications/%s' % apply_id
        params = {}
        if invoice_id:
            params.update(dict(fapiao_id=invoice_id))
        return self._p.core.request(path, data=params)

    def invoice_reverse(self, apply_id, reverse_reason, information):
        """冲红电子发票
        :param apply_id: 发票申请单号，示例值：'4200000444201910177461284488'
        :param reverse_reason: 冲红原因，示例值：'退款'
        :param information: 需要冲红的发票信息，示例值：{'id':'20200701123456','code':'044001911211','number':'12897794'}
        """
        path = 'https://api.mch.weixin.qq.com/v3/new-tax-control-fapiao/fapiao-applications/%s/reverse' % apply_id
        params = {}
        if reverse_reason:
            params.update({'reverse_reason': reverse_reason})
        if information:
            params.update(dict(fapiao_information=information))
        else:
            raise Exception('[invoice] information is not assigned.')
        return self._p.core.request(path, method=RequestType.POST, data=params)

    def invoice_upload_file(self, filepath):
        """上传电子发票文件
        :filepath: 电子发票文件路径，只支持pdf和odf两种格式，示例值：'./invoice/0001.pdf'
        """
        if not (filepath and os.path.exists(filepath) and os.path.isfile(filepath)):
            raise Exception('filepath is not assigned or not exists')
        with open(filepath, mode='rb') as f:
            content = f.read()
        filename = os.path.basename(filepath)
        filetype = os.path.splitext(filename)[-1][1:].upper()
        mimes = {
            'PDF': 'application/pdf',
            'ODF': 'application/odf'
        }
        if filetype not in mimes:
            raise Exception('jd-wechatpay does not support this file type.')
        params = {}
        params.update({'meta': dict(file_type=filetype, digest_alogrithm="SM3", digest=sm3(content))})
        files = [('file', (filename, content, mimes[filetype]))]
        path = 'https://api.mch.weixin.qq.com/v3/new-tax-control-fapiao/fapiao-applications/upload-fapiao-file'
        return self._p.core.request(path, method=RequestType.POST, data=params, sign_data=params.get('meta'),
                                    files=files)

    def invoice_insert_cards(self, apply_id, buyer_information, card_information, scene='WITH_WECHATPAY'):
        """将电子发票插入微信用户卡包
        :param apply_id: 发票申请单号，示例值：'4200000444201910177461284488'
        :param buyer_information: 购买方信息，即发票抬头。示例值：{'type':'ORGANIZATION','name':'深圳市南山区测试企业'}
        :param card_information: 电子发票卡券信息列表，最多五条。示例值：
            [{'media_id':'AS1FZ4mr2e/+3LqYdlQyEA==','number':'123456','code':'044001911211',
            'time':'2020-07-01T12:00:00+08:00','check_code':'69001808340631374774'......}]
        :param scene: 场景值，目前只支持WITH_WECHATPAY。示例值：'WITH_WECHATPAY'
        """
        path = 'https://api.mch.weixin.qq.com/v3/new-tax-control-fapiao/fapiao-applications/%s/insert-cards' % apply_id
        params = {}
        if buyer_information:
            params.update({'buyer_information': buyer_information})
        else:
            raise Exception('buyer_information is not assigned.')
        if card_information:
            params.update(dict(fapiao_card_information=card_information))
        else:
            raise Exception('[invoice]card_information is not assigned.')
        params.update({'scene': scene})
        return self._p.core.request(path, method=RequestType.POST, data=params)
