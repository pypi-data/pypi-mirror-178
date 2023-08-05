# -*- coding: utf-8 -*-

from .type import RequestType


class Apply4Subject:
    """
    风险合格——商户开户意愿确认
    https://pay.weixin.qq.com/wiki/doc/apiv3_partner/open/pay/chapter6_1_1.shtml
    """

    def __init__(self, parent):
        from .mch import WeChatPay

        if not isinstance(parent, WeChatPay):
            raise Exception('BasePay need WeChatPay!')
        self._p = parent    # 父对象， 服务商

    def applyment(self, business_code, contact_info, subject_info, identification_info, channel_id=None,
                  addition_info=None, ubo_info_list=None):
        """（商户开户意愿）提交申请单
        :param business_code: 业务申请编号，示例值:'APPLYMENT_00000000001'
        :param contact_info: 联系人信息，示例值:{'name':'张三','id_card_number':'320311770706001','mobile':'13900000000'}
        :param subject_info: 主体信息，示例值:{'subject_type':'SUBJECT_TYPE_ENTERPRISE','business_license_info':
                {'license_copy':'demo-media-id','license_number':'123456789012345678',
                'merchant_name':'腾讯科技有限公司','legal_person':'张三',
                'company_address':'广东省深圳市南山区xx路xx号','licence_valid_date':'["1970-01-01","forever"]'}}
        :param identification_info: 法人身份信息，示例值:{'identification_type':'IDENTIFICATION_TYPE_IDCARD',
                'identification_name':'张三','identification_number':'110220330044005500','identification_valid_date':
                '["1970-01-01","forever"]','identification_front_copy':'0P3ng6K1IW4-Q_l2FjKLZ...',
                'identification_back_copy':'0P3ng6KT1W4-Q_l2FjKLZ...'}
        :param channel_id: 渠道商户号，示例值:'20001111'
        :param addition_info: 补充材料，示例值:{'confirm_mchid_list':['20001113']}
        :param ubo_info_list: 最终受益人信息列表，示例值:[{'ubo_id_doc_type':'IDENTIFICATION_TYPE_IDCARD',
                'ubo_id_doc_name':'张三','ubo_id_doc_number':'110220330044005500'}]
        """
        params = {}
        params.update({'business_code': business_code, 'contact_info': contact_info,
                       'subject_info': subject_info, 'identification_info': identification_info})
        if channel_id:
            params.update({'channel_id': channel_id})
        if addition_info:
            params.update({'addition_info': addition_info})
        if ubo_info_list:
            params.update({'ubo_info_list': ubo_info_list})
        contact_name = params['contact_info'].get('name')
        if contact_name:
            params['contact_info']['name'] = self._p.core.encrypt(contact_name)
        contact_mobile = params['contact_info'].get('mobile')
        if contact_mobile:
            params['contact_info']['mobile'] = self._p.core.encrypt(contact_mobile)
        contact_number = params['contact_info'].get('id_card_number')
        if contact_number:
            params['contact_info']['id_card_number'] = self._p.core.encrypt(contact_number)
        identification_name = params['identification_info'].get('identification_name')
        if identification_name:
            params['identification_info']['identification_name'] = self._p.core.encrypt(identification_name)
        identification_number = params['identification_info'].get('identification_number')
        if identification_number:
            params['identification_info']['identification_number'] = self._p.core.encrypt(identification_number)
        identification_address = params['identification_info'].get('identification_address')
        if identification_address:
            params['identification_info']['identification_address'] = self._p.core.encrypt(identification_address)
        if params.get('ubo_info_list'):
            for ubo_info in params['ubo_info_list']:
                ubo_info['ubo_id_doc_name'] = self._p.core.encrypt(ubo_info['ubo_id_doc_name'])
                ubo_info['ubo_id_doc_number'] = self._p.core.encrypt(ubo_info['ubo_id_doc_number'])
                ubo_info['ubo_id_doc_address'] = self._p.core.encrypt(ubo_info['ubo_id_doc_address'])
        path = '/v3/apply4subject/applyment'
        return self._p.core.request(path, method=RequestType.POST, data=params, cipher_data=True)

    def cancel(self, business_code=None, applyment_id=None):
        """（商户开户意愿）撤销申请单
        :param business_code: 业务申请编号，示例值:'2000001234567890'
        :param applyment_id: 申请单编号，示例值:2000001234567890
        """
        if business_code:
            path = '/v3/apply4subject/applyment/%s/cancel' % business_code
        elif applyment_id:
            path = '/v3/apply4subject/applyment/%s/cancel' % applyment_id
        else:
            raise Exception('business_code or applyment_id is not assigned.')
        return self._p.core.request(path)

    def query(self, business_code=None, applyment_id=None):
        """（商户开户意愿）查询申请单审核结果
        :param business_code: 业务申请编号，示例值:'2000001234567890'
        :param applyment_id: 申请单编号，示例值:2000001234567890
        """
        if business_code:
            path = '/v3/apply4subject/applyment?business_code=%s' % business_code
        elif applyment_id:
            path = '/v3/apply4subject/applyment?applyment_id=%s' % applyment_id
        else:
            raise Exception('business_code or applyment_id is not assigned.')
        return self._p.core.request(path)

    def state(self, sub_mchid):
        """（商户开户意愿）获取商户开户意愿确认状态
        :param sub_mchid: 特约商户号，示例值:'1511101111'
        """
        if sub_mchid:
            path = '/v3/apply4subject/applyment/merchants/%s/state' % sub_mchid
        else:
            raise Exception('sub_mchid is not assigned.')
        return self._p.core.request(path)
