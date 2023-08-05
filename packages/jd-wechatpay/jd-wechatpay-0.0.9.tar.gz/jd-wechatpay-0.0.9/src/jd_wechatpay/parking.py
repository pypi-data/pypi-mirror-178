# -*- coding: utf-8 -*-

from .type import RequestType


class ParkingService:
    """
    行业方案——微信支付分停车服务
    https://pay.weixin.qq.com/wiki/doc/apiv3/apis/chapter8_8_1.shtml
    https://pay.weixin.qq.com/wiki/doc/apiv3_partner/apis/chapter8_8_1.shtml
    """

    def __init__(self, parent):
        from .mch import WeChatPay

        if not isinstance(parent, WeChatPay):
            raise Exception('BasePay need WeChatPay!')
        self._p = parent    # 父对象

    def find(self, plate_number, plate_color, openid, sub_mchid=None):
        """查询车牌服务开通信息
        :param plate_number: 车牌号，示例值：'粤B888888'
        :param plate_color: 车牌颜色，车牌颜色，枚举值：BLUE：蓝色，GREEN：绿色，YELLOW：黄色，BLACK：
                            黑色，WHITE：白色，LIMEGREEN：黄绿色
        :param openid: 用户标识，示例值：'oUpF8uMu...'
        :param sub_mchid: (服务商模式)子商户的商户号，由微信支付生成并下发。示例值:'1900000109'
        """
        path = '/v3/vehicle/parking/services/find?appid=%s' % self._p.app_id
        if plate_number:
            path = path + '&plate_number=%s' % plate_number
        else:
            raise Exception('plate_number is not assigned.')
        if plate_color:
            path = path + '&plate_color=%s' % plate_color
        else:
            raise Exception('plate_color is not assigned.')
        if openid:
            path = path + '&openid=%s' % openid
        else:
            raise Exception('openid is not assigned.')
        if self._p.partner_mode:
            if sub_mchid:
                path = '%s&sub_mchid=%s' % (path, sub_mchid)
            else:
                raise Exception('sub_mchid is not assigned.')
        return self._p.core.request(path)

    def parking_enter(self, out_parking_no, plate_number, plate_color, start_time, parking_name,
                      free_duration, notify_url=None, sub_mchid=None):
        """创建停车入场
        车辆入场以后，商户调用该接口，创建停车入场信息。
        :param out_parking_no: 商户入场id，商户侧入场标识id，在同一个商户号下唯一，示例值：'1231243'
        :param plate_number: 车牌号，示例值：'粤B888888'
        :param plate_color: 车牌颜色，车牌颜色，枚举值：BLUE：蓝色，GREEN：绿色，YELLOW：黄色，
                            BLACK：黑色，WHITE：白色，LIMEGREEN：黄绿色
        :param notify_url: 回调通知url，接受入场状态变更回调通知的url，只接受https，
                            示例值：https://yoursite.com/wxpay.html
        :param start_time: 入场时间，示例值：'2017-08-26T10:43:39+08:00'
        :param parking_name: 停车场名称，示例值：'欢乐海岸停车场'
        :param free_duration: 免费时长，单位为秒，示例值：3600
        :param sub_mchid: (服务商模式)子商户的商户号，由微信支付生成并下发。示例值:'1900000109'
        """
        params = {}
        params.update({'out_parking_no': out_parking_no})
        params.update({'plate_number': plate_number})
        params.update({'plate_color': plate_color})
        if not (notify_url or self._p.notify_url):
            raise Exception('notify_url is not assigned.')
        params.update({'notify_url': notify_url or self._p.notify_url})
        params.update({'start_time': start_time})
        params.update({'parking_name': parking_name})
        params.update({'free_duration': free_duration})
        if self._p.partner_mode:
            if sub_mchid:
                params.update({'sub_mchid': sub_mchid})
            else:
                raise Exception('sub_mchid is not assigned.')
        path = 'https://api.mch.weixin.qq.com/v3/vehicle/parking/parkings'
        return self._p.core.request(path, method=RequestType.POST, data=params)

    def order(self, description, out_trade_no, total, parking_id, plate_number, plate_color, start_time,
              end_time, parking_name, charging_duration, device_id, trade_scene='PARKING', profit_sharing='N',
              currency='CNY', attach=None, goods_tag=None, notify_url=None, appid=None, sub_appid=None, sub_mchid=None):
        """停车扣费受理
        商户请求扣费受理接口，会完成订单受理。微信支付进行异步扣款，支付完成后，会将订单支付结果发送给商户。
        :param description: 服务描述，商户自定义字段，用于交易账单中对扣费服务的描述。示例值：'停车场扣费'
        :param out_trade_no: 商户订单号，商户系统内部订单号，只能是数字、大小写字母，且在同一个商户号下唯一，示例值：'20150806125346'
        :param notify_url: 回调通知url，只接受https，示例值：'https://yoursite.com/wxpay.html'
        :param total: 订单总金额，单位为分，只能为整数，示例值：888
        :param parking_id: 停车入场id，通过入场通知接口获取的入场id，示例值：'5K8264...'
        :param plate_number: 车牌号，仅包括省份+车牌，不包括特殊字符。示例值：'粤B888888'
        :param plate_color: 车牌颜色，枚举值：BLUE：蓝色，GREEN：绿色，YELLOW：黄色，BLACK：黑色，WHITE：白色，LIMEGREEN：黄绿色，示例值：BLUE
        :param start_time: 入场时间，示例值：'2017-08-26T10:43:39+08:00'
        :param end_time: 出场时间，示例值：'2017-08-26T10:43:39+08:00'
        :param parking_name: 停车场名称，示例值：'欢乐海岸停车场'
        :param charging_duration: 计费时长，单位为秒，示例值：3600
        :param device_id: 停车场设备id，示例值：'12313'
        :param trade_scene: 交易场景值，目前支持 'PARKING'：车场停车场景
        :param profit_sharing: 分账标识，枚举值：'Y'：是，需要分账，'N'：否，不分账，字母要求大写，不传默认不分账。
        :param currency: 货币类型，目前只支持人民币：'CNY'
        :param attach: 附加数据，在查询API和支付通知中原样返回，可作为自定义参数使用，示例值：'深圳分店'
        :param goods_tag: 订单优惠标记，代金券或立减优惠功能的参数，示例值：WXG
        :param appid: 应用ID，可不填，默认传入初始化时的appid，示例值:'wx1234567890ab3def'
        :param sub_appid: (服务商模式)子商户应用ID，示例值:'wxd678efh567hg6999'
        :param sub_mchid: (服务商模式)子商户的商户号，由微信支付生成并下发。示例值:'1900000109'
        """
        params = {}
        amount = {}
        parking_info = {}
        params.update(dict(appid=appid or self._p.app_id))
        params.update({'description': description})
        params.update({'out_trade_no': out_trade_no})
        if not (notify_url or self._p.notify_url):
            raise Exception('notify_url is not assigned.')
        params.update({'notify_url': notify_url or self._p.notify_url})
        if total:
            amount.update({'total': total})
        else:
            raise Exception('total is not assigned')
        if parking_id:
            parking_info.update({'parking_id': parking_id})
        else:
            raise Exception('parking_id is not assigned')
        if plate_number:
            parking_info.update({'plate_number': plate_number})
        else:
            raise Exception('plate_number is not assigned')
        if plate_color:
            parking_info.update({'plate_color': plate_color})
        else:
            raise Exception('plate_color is not assigned')
        parking_info.update({'start_time': start_time})
        parking_info.update({'end_time': end_time})
        parking_info.update({'parking_name': parking_name})
        parking_info.update({'charging_duration': charging_duration})
        parking_info.update({'device_id': device_id})
        if trade_scene:
            params.update({'trade_scene': trade_scene})
        else:
            raise Exception('trade_scene is not assigned')
        if profit_sharing:
            params.update({'profit_sharing': profit_sharing})
        else:
            raise Exception('profit_sharing is not assigned')
        if currency:
            amount.update({'currency': currency})
        else:
            raise Exception('currency is not assigned')
        if attach:
            params.update({'attach': attach})
        if goods_tag:
            params.update({'goods_tag': goods_tag})
        params.update({'amount': amount})
        params.update({'parking_info': parking_info})
        if self._p.partner_mode:
            if sub_appid:
                params.update(dict(sub_appid=sub_appid))
            else:
                raise Exception('sub_appid is not assigned.')
            if sub_mchid:
                params.update(dict(sub_mchid=sub_mchid))
            else:
                raise Exception('sub_mchid is not assigned.')
        path = '/v3/vehicle/transactions/parking'
        return self._p.core.request(path, method=RequestType.POST, data=params)

    def order_query(self, out_trade_no, sub_mchid=None):
        """查询订单
        停车扣费订单查询
        :param out_trade_no: 商户订单号，商户系统内部订单号，只能是数字、大小写字母，且在同一个商户号下唯一，示例值：'20150806125346'
        :param sub_mchid:   子商户号  string[1, 32]
        """
        if not out_trade_no:
            raise Exception('out_trade_no is not assigned')
        path = '/v3/vehicle/transactions/out-trade-no/%s' % out_trade_no
        if self._p.partner_mode:
            if sub_mchid:
                path = '%s?sub_mchid=%s' % (path, sub_mchid)
            else:
                raise Exception('sub_mchid is not assigned.')
        return self._p.core.request(path)
