# -*- coding: utf-8 -*-

from .type import RequestType, WeChatPayType


class BusinessCircle:
    """
    行业方案——智慧商圈      直连商户 和 服务商模式
    https://pay.weixin.qq.com/wiki/doc/apiv3/open/pay/chapter3_6_1.shtml
    https://pay.weixin.qq.com/wiki/doc/apiv3_partner/apis/chapter8_6_7.shtml
    """

    def __init__(self, parent):
        from .mch import WeChatPay

        if not isinstance(parent, WeChatPay):
            raise Exception('BasePay need WeChatPay!')
        self._p = parent    # 父对象

    def points_notify(self, transaction_id, openid, earn_points, increased_points, points_update_time,
                      no_points_remarks=None, total_points=None, appid=None, sub_mchid=None):
        """商圈积分同步
        :param self:         WeChatPay 对象
        :param transaction_id: 微信订单号，示例值：'1217752501201407033233368018'
        :param openid: 用户标识，示例值：'oWmnN4NHIGf...'
        :param earn_points: 是否获得积分，示例值：True
        :param increased_points: 订单新增积分值，示例值：100
        :param points_update_time: 积分更新时间，示例值：'2020-05-20T13:29:35.120+08:00'
        :param no_points_remarks: 未获得积分的备注信息，示例值：'商品不参与积分活动'
        :param total_points: 顾客积分总额，示例值：888888
        :param appid: 应用ID，可不填，默认传入初始化时的appid，示例值:'wx1234567890ab3def'
        :param sub_mchid: (服务商模式)子商户的商户号，由微信支付生成并下发。示例值:'1900000109'
        """
        if self._p.type != WeChatPayType.MINI_APP:
            raise Exception('points notify only supports wechat mini program')
        params = dict(appid=appid or self._p.app_id)
        params.update({'transaction_id': transaction_id})
        params.update({'openid': openid})
        params.update({'earn_points': earn_points})
        params.update({'increased_points': increased_points})
        params.update({'points_update_time': points_update_time})
        if no_points_remarks:
            params.update({'no_points_remarks': no_points_remarks})
        if total_points:
            params.update({'total_points': total_points})
        if self._p.partner_mode and sub_mchid:
            params.update({'sub_mchid': sub_mchid})
        path = 'https://api.mch.weixin.qq.com/v3/businesscircle/points/notify'
        return self._p.core.request(path, method=RequestType.POST, data=params)

    def user_authorization(self, openid, appid=None, sub_mchid=None):
        """智慧商圈积分授权查询
        :param self:         WeChatPay 对象
        :param openid: 用户标识，示例值：'oWmnN42NHIGf1xd8...'
        :param appid: 小程序appid，顾客授权积分时使用的小程序的appid，默认传入初始化时的appid，示例值:'wx1234567890ab3def'
        :param sub_mchid: (服务商模式)子商户的商户号，由微信支付生成并下发。示例值:'1900000109'
        """
        if self._p.type != WeChatPayType.MINI_APP:
            raise Exception('points notify only supports wechat mini program')
        if not openid:
            raise Exception('openid is not assigned.')
        if self._p.partner_mode:
            path = 'https://api.mch.weixin.qq.com/v3/businesscircle/user-authorizations/%s?appid=%s' %\
                   (openid, appid or self._p.app_id)
            if sub_mchid:
                path = '%s&sub_mchid=%s' % (path, sub_mchid)
        else:
            path = 'https://api.mch.weixin.qq.com/v3/businesscircle/user-authorizations/%s?appid=%s' % \
                   (openid, self._p.app_id)
        return self._p.core.request(path)

    def business_parking_sync(self, openid, brand_id, plate_number, state, time, appid=None, sub_mchid=None):
        """商圈会员停车状态同步
        :param openid: 用户标识，示例值:'oWmnN4xx2xxe92NHIGf1xd8'
        :param brand_id: 品牌ID，示例值:1000
        :param plate_number: 车牌号，示例值: '粤B888888'
        :param state: 停车状态，IN=入场，用户开车进入商圈，OUT=离场，用户开车离开商圈。示例值:IN
        :param time: 时间，示例值：2022-06-01T10:43:39+08:00
        :param appid: 小程序appid，顾客授权积分时使用的小程序的appid，默认传入初始化时的appid，示例值:'wx1234567890ab3def'
        :param sub_mchid: (服务商模式)子商户的商户号，由微信支付生成并下发。示例值:'1900000109'
        """
        params = {}
        params.update({'appid': appid or self._p.app_id, 'openid': openid, 'plate_number': plate_number})
        params.update(dict(brandid=brand_id))
        params.update({'state': state, 'time': time})
        if self._p.partner_mode:
            if not sub_mchid:
                raise Exception('sub_mchid is not assigned.')
            else:
                params.update({'sub_mchid': sub_mchid})
        path = 'https://api.mch.weixin.qq.com/v3/businesscircle/parkings'
        return self._p.core.request(path, method=RequestType.POST, date=params)

    def business_point_status(self, openid, brand_id, appid=None, sub_mchid=None):
        """商圈会员待积分状态查询
        :param openid: 用户标识，示例值:'oWmnN4x1x2x3e92NHIGf1xd8'
        :param brand_id: 品牌ID，示例值:1000
        :param appid: 小程序appid，顾客授权积分时使用的小程序的appid，默认传入初始化时的appid，示例值:'wx1234567890ab3def'
        :param sub_mchid: (服务商模式)子商户的商户号，由微信支付生成并下发。示例值:'1900000109'
        """
        if not (openid and brand_id):
            raise Exception('openid and/or brand_id is not assigned.')
        else:
            path = 'https://api.mch.weixin.qq.com/v3/businesscircle/users/%s/points/commit_status' % openid

        params = dict(brandid=brand_id, appid=appid or self._p.app_id)
        if sub_mchid:
            params.update(dict(sub_mchid=sub_mchid))
        return self._p.core.request(path, data=params)
