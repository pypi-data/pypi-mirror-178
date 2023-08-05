# -*- coding: utf-8 -*-

from .type import RequestType


class Apply:
    """
    特约商户进件
    参考 https://pay.weixin.qq.com/wiki/doc/apiv3_partner/apis/chapter11_1_1.shtml
    """

    def __init__(self, parent):
        from .mch import WeChatPay

        if not isinstance(parent, WeChatPay):
            raise Exception('BasePay need WeChatPay!')
        self._p = parent    # 父对象， 服务商

    def applyment(self,
                  business_code,
                  contact_info,
                  subject_info,
                  business_info,
                  settlement_info,
                  bank_account_info,
                  addition_info=None):
        """特约商户进件 提交申请单
        :param business_code: 服务商自定义的唯一编号，示例值：APPLY_00000000001
        :param contact_info: 特约商户的超级管理员，请确定其为商户法定代表人或负责人
        :param subject_info: 请填写商家的营业执照/登记证书、经营者/法人的证件等信息
        :param business_info: 请填写商家的经营业务信息、售卖商品/提供服务场景信息
        :param settlement_info: 请填写商家的结算费率规则、特殊资质等信息
        :param bank_account_info: 请填写商家提现收款的银行账户信息
        :param addition_info: 根据实际审核情况，额外要求商家提供指定的补充资料
        """
        params = {}
        if business_code:
            params.update({'business_code': business_code})
        else:
            raise Exception('business_code is not assigned.')
        if contact_info:
            params.update({'contact_info': contact_info})
        else:
            raise Exception('contact_info is not assigned.')
        if subject_info:
            params.update({'subject_info': subject_info})
        else:
            raise Exception('subject_info is not assigned.')
        if business_info:
            params.update({'business_info': business_info})
        else:
            raise Exception('business_info is not assigned')
        if settlement_info:
            params.update({'settlement_info': settlement_info})
        else:
            raise Exception('settlement_info is not assigned.')
        if bank_account_info:
            params.update({'bank_account_info': bank_account_info})
        else:
            raise Exception('bank_account_info is not assigned.')
        if addition_info:
            params.update({'addition_info': addition_info})
        if params.get('contact_info').get('contact_name'):
            params['contact_info']['contact_name'] = self._p.core.encrypt(params['contact_info']['contact_name'])
        if params.get('contact_info').get('contact_id_number'):
            params['contact_info']['contact_id_number'] = self._p.core.encrypt(
                params['contact_info']['contact_id_number'])
        if params.get('contact_info').get('openid'):
            params['contact_info']['openid'] = self._p.core.encrypt(params['contact_info']['openid'])
        if params.get('contact_info').get('mobile_phone'):
            params['contact_info']['mobile_phone'] = self._p.core.encrypt(params['contact_info']['mobile_phone'])
        if params.get('contact_info').get('contact_email'):
            params['contact_info']['contact_email'] = self._p.core.encrypt(params['contact_info']['contact_email'])
        id_card_name = params.get('subject_info').get('identity_info').get('id_card_info', {}).get('id_card_name')
        if id_card_name:
            params['subject_info']['identity_info']['id_card_info']['id_card_name'] = self._p.core.encrypt(id_card_name)
        id_card_number = params.get('subject_info').get('identity_info').get('id_card_info', {}).get('id_card_number')
        if id_card_number:
            params['subject_info']['identity_info']['id_card_info']['id_card_number'] = self._p.core.encrypt(
                id_card_number)
        id_card_address = params.get('subject_info').get('identity_info').get('id_card_info', {}).get('id_card_address')
        if id_card_address:
            params['subject_info']['identity_info']['id_card_info']['id_card_address'] = self._p.core.encrypt(
                id_card_address)
        id_doc_name = params.get('subject_info').get('identity_info').get('id_doc_info', {}).get('id_doc_name')
        if id_doc_name:
            params['subject_info']['identity_info']['id_doc_info']['id_doc_name'] = \
                self._p.core.encrypt(id_doc_name)
        id_doc_number = params.get('subject_info').get('identity_info').get('id_doc_info', {}).get('id_doc_number')
        if id_doc_number:
            params['subject_info']['identity_info']['id_doc_info']['id_doc_number'] = \
                self._p.core.encrypt(id_doc_number)
        id_doc_address = params.get('subject_info').get('identity_info').get('id_doc_info', {}).get('id_doc_address')
        if id_doc_address:
            params['subject_info']['identity_info']['id_doc_info']['id_doc_address'] = self._p.core.encrypt(
                id_doc_address)
        if params.get('subject_info').get('ubo_info_list'):
            for ubo_info in params['subject_info']['ubo_info_list']:
                ubo_info['ubo_id_doc_name'] = self._p.core.encrypt(ubo_info['ubo_id_doc_name'])
                ubo_info['ubo_id_doc_number'] = self._p.core.encrypt(ubo_info['ubo_id_doc_number'])
                ubo_info['ubo_id_doc_address'] = self._p.core.encrypt(ubo_info['ubo_id_doc_address'])
        params['bank_account_info']['account_name'] = self._p.core.encrypt(params['bank_account_info']['account_name'])
        params['bank_account_info']['account_number'] = self._p.core.encrypt(
            params['bank_account_info']['account_number'])
        path = '/v3/applyment4sub/applyment/'
        return self._p.core.request(path, method=RequestType.POST, data=params, cipher_data=True)

    def applyment_query(self, business_code=None, applyment_id=None):
        """通过 业务申请编号 或 申请单号 查询申请状态
        :param business_code: 1、只能由数字、字母或下划线组成，建议前缀为服务商商户号。
                              2、服务商自定义的唯一编号。
                              3、每个编号对应一个申请单，每个申请单审核通过后生成一个微信支付商户号。
                              4、若申请单被驳回，可填写相同的“业务申请编号”，即可覆盖修改原申请单信息。
                              示例值：1900013511_10000
        :param applyment_id: 微信支付分配的申请单号，示例值：2000001234567890
        """
        if not (business_code or applyment_id):
            raise Exception('params is not assigned')
        if business_code:
            path = '/v3/applyment4sub/applyment/business_code/%s' % business_code
        else:
            path = '/v3/applyment4sub/applyment/applyment_id/%s' % applyment_id
        return self._p.core.request(path)

    def settlement_modify(self, sub_mch_id, account_type, account_bank, bank_address_code,
                          account_number, bank_name=None, bank_branch_id=None
                          ):
        """修改结算账号
        :param sub_mch_id: 本服务商负责进件的特约商户号, 示例值：1511101111
        :param account_type: 特约商户号的主体类型，示例值：ACCOUNT_TYPE_BUSINESS
        :param account_bank: 开户银行名称，详细参见开户银行对照表。
                            注：17家直连银行，请根据开户银行对照表直接填写银行名
                            非17家直连银行，该参数请填写为“其他银行” 示例值：工商银行
        :param bank_address_code: 需至少精确到市，示例值：110000
        :param account_number: 数字，长度遵循系统支持的开户银行对照表中对公/对私卡号长度要求
                                示例值：d+xT+MQCvrLH2V...
        :param bank_name: 若开户银行为“其他银行”，则需二选一填写“开户银行全称（含支行）”或“开户银行联行号”
                            填写银行全称，如"深圳农村商业银行XXX支行" ，详细参见开户银行全称（含支行）对照表
                            示例值：施秉县农村信用合作联社城关信用社
        :param bank_branch_id: 若开户银行为“其他银行”，则需二选一填写“开户银行全称（含支行）”或“开户银行联行号”
                                填写银行联行号，详细参见开户银行全称（含支行）对照表。
                                示例值：402713354941
        """
        params = {}
        if sub_mch_id:
            path = '/v3/apply4sub/sub_merchants/%s/modify-settlement' % sub_mch_id
        else:
            raise Exception('sub_mch_id is not assigned.')
        if account_type:
            params.update({'account_type': account_type})
        else:
            raise Exception('account_type is not assigned')
        if account_bank:
            params.update({'account_bank': account_bank})
        else:
            raise Exception('account_bank is not assigned')
        if bank_address_code:
            params.update({'bank_address_code': bank_address_code})
        else:
            raise Exception('bank_address_code is not assigned')
        if account_number:
            params.update({'account_number': self._p.core.encrypt(account_number)})
        else:
            raise Exception('account_number is not assigned')
        if bank_name:
            params.update({'bank_name': bank_name})
        if bank_branch_id:
            params.update({'bank_branch_id': bank_branch_id})
        return self._p.core.request(path, method=RequestType.POST, data=params, cipher_data=True)

    def settlement_query(self, sub_mch_id):
        """查询结算账户
        :param sub_mch_id: 本服务商进件、已签约的特约商户号，示例值：1900006491
        """
        if sub_mch_id:
            path = '/v3/apply4sub/sub_merchants/%s/settlement' % sub_mch_id
        else:
            raise Exception('sub_mch_id is not assigned.')
        return self._p.core.request(path)
