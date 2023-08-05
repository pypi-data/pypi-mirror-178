# -*- coding: utf8 -*-
from .type import SignType

__version__ = '2.0.2'


class WeChatPay(object):    # 微信支付 v3 直连商户 或 服务商模式
    def __init__(self,
                 pay_type,
                 mch_id,
                 private_key,
                 cert_serial_no,
                 app_id,            # 服务商应用ID， 或者 直联商户应用ID
                 api_v3_key,
                 notify_url=None,
                 cert_dir=None,
                 logger=None,
                 partner_mode=False,    # 接入模式，默认False为直连商户模式，True为服务商模式
                 proxy=None
                 ):
        """
        :param pay_type:        微信支付类型，示例值：WeChatPayType.MINI_APP
        :param mch_id:          直连商户号 或者 服务商商户号，示例值：'1230000109'
        :param private_key:     商户证书私钥，示例值：'MIIEvwIBADANBg3hkiG9w0...'
        :param cert_serial_no:  商户证书序列号，示例值：'444F4864EA9B34415...'
        :param app_id:          应用ID，示例值：'wxd678efh567hg6787'
        :param api_v3_key:      商户APIv3密钥，示例值：'a12d3924fd499ed5...'
        :param notify_url:      通知地址，示例值：'https://www.weixin.qq.com/wxpay/pay.php'
        :param cert_dir:        平台证书存放目录，示例值：'/server/cert'
        :param logger:          日志记录器，示例值logging.getLogger('demo')
        :param partner_mode:    接入模式，默认False为直连商户模式，True为服务商模式
        :param proxy:           代理设置，示例值：{"https": "http://10.10.1.10:1080"}
        """
        from .core import Core
        from .media import Media
        from .transaction import BasePay
        from .profitsharing import ProfitSharing
        from .parking import ParkingService
        from .marketing import Marketing
        from .businesscircle import BusinessCircle
        from .complaint import Complaint
        from .payscore import PayScore
        from .smartguide import Guide
        from .applyment import Apply
        from .transfer import Transfer
        from .gold_plan import GoldPlan
        from .merchant_risk import MerchantRisk
        from .invoice import Invoice
        from .apply4subject import Apply4Subject
        from .capital import Capital

        self.type = pay_type
        self.mch_id = mch_id
        self.app_id = app_id
        self.notify_url = notify_url
        self.core = Core(mch_id=self.mch_id,
                         cert_serial_no=cert_serial_no,
                         private_key=private_key,
                         api_v3_key=api_v3_key,
                         cert_dir=cert_dir,
                         logger=logger,
                         proxy=proxy)
        self.partner_mode = partner_mode

        # API 接口
        self.media = Media(self)                        # 图片上传、视频上传
        self.pay = BasePay(self)                        # 基础支付
        self.profit_sharing = ProfitSharing(self)       # 分账
        self.parking = ParkingService(self)             # 停车服务
        self.marketing = Marketing(self)                # 营销工具
        self.business_circle = BusinessCircle(self)     # 智慧商圈
        self.complaint = Complaint(self)                # 消费者投诉
        self.pay_score = PayScore(self)                 # 支付分
        self.guide = Guide(self)                        # 支付即服务
        self.apply = Apply(self)                        # 特约商户进件 服务商
        self.transfer = Transfer(self)                  # 资金应用——商家转账到零钱
        self.gold = GoldPlan(self)                      # 经营能力——点金计划
        self.risk = MerchantRisk(self)                  # 风险合规——商户违规通知回调
        self.invoice = Invoice(self)                    # 其他——电子发票
        self.apply4subject = Apply4Subject(self)        # 风险合格——商户开户意愿确认
        self.capital = Capital(self)                    # 其他——银行组件

    def sign(self, data, sign_type=SignType.RSA_SHA256):
        """使用RSA with SHA256或HMAC_256算法计算签名值供调起支付时使用
        :param data: 需要签名的参数清单
        :param sign_type:
        微信支付订单采用RSA with SHA256算法时，示例值:['wx888','1414561699','5K8264CQ2502S....','prepay_id=wx201495522657....']
        微信支付分订单采用HMAC_SHA256算法时，示例值:{'mch_id':'1230000109','service_id':'88888888000011','out_order_no':'123432343252'}
        """
        return self.core.sign(data, sign_type)

    def callback(self, headers, body):
        """解密回调接口收到的信息，返回所有传入的参数
        :param headers: 回调接口收到的headers
        :param body: 回调接口收到的body
        """
        return self.core.callback(headers, body)

    def decrypt_callback(self, headers, body):
        """解密回调接口收到的信息
        :param headers: 回调接口收到的headers
        :param body: 回调接口收到的body
        """
        return self.core.decrypt_callback(headers, body)

    def decrypt(self, ciphertext):
        """解密微信支付平台返回的信息中的敏感字段
        :param ciphertext: 加密后的敏感字段，示例值：'Qe41VhP/sGdNe...'
        """
        return self.core.decrypt(ciphertext)
