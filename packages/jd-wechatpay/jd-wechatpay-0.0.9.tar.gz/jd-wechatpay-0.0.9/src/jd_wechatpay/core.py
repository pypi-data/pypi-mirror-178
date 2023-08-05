# -*- coding: utf-8 -*-
import json
import os
from datetime import datetime

from urllib.parse import urlencode
import requests
from urllib3.exceptions import MaxRetryError, NewConnectionError

from .type import RequestType, SignType
from .utils import (aes_decrypt, build_authorization, load_certificate,
                    load_private_key, rsa_decrypt, rsa_encrypt, rsa_sign,
                    rsa_verify, hmac_sign, jd_concat)

_timeout = (3.05, 27)   # 超时时间, 连接超时 和 读取超时
# _timeout = None


__version__ = '1.0.3'


class Core:
    def __init__(self,
                 mch_id,            # 直连商户商户号，或 服务商商户号
                 cert_serial_no,    # 证书序列号
                 private_key,       # 证书私钥
                 api_v3_key,        # API v3 KEY
                 cert_dir=None,     # 证书目录
                 logger=None,       # 日志
                 proxy=None         # 代理
                 ):
        self._proxy = proxy
        self._mch_id = mch_id
        self._cert_serial_no = cert_serial_no
        self._private_key = load_private_key(private_key)
        self._api_v3_key = api_v3_key
        self.gate_way = 'https://api.mch.weixin.qq.com'
        self._certificates = []
        self._cert_dir = cert_dir + '/' if cert_dir else None
        self._logger = logger
        self._init_certificates()

    def _update_certificates(self):
        path = '/v3/certificates'
        self._certificates.clear()
        code, message = self.request(path, skip_verify=True, show_request=False, show_rsp=False)
        if code != 200:
            return
        data = message.get('data')
        for value in data:
            serial_no = value.get('serial_no')
            effective_time = value.get('effective_time')
            expire_time = value.get('expire_time')
            encrypt_certificate = value.get('encrypt_certificate')
            algorithm = nonce = associated_data = ciphertext = None
            if encrypt_certificate:
                algorithm = encrypt_certificate.get('algorithm')
                nonce = encrypt_certificate.get('nonce')
                associated_data = encrypt_certificate.get('associated_data')
                ciphertext = encrypt_certificate.get('ciphertext')
            if not (serial_no and effective_time and expire_time and algorithm and nonce
                    and associated_data and ciphertext):
                continue
            cert_str = aes_decrypt(
                nonce=nonce,
                ciphertext=ciphertext,
                associated_data=associated_data,
                api_v3_key=self._api_v3_key)
            certificate = load_certificate(cert_str)
            if not certificate:
                continue
            now = datetime.utcnow()
            if now < certificate.not_valid_before or now > certificate.not_valid_after:
                continue
            self._certificates.append(certificate)
            if not self._cert_dir:
                continue
            if not os.path.exists(self._cert_dir):
                os.makedirs(self._cert_dir)
            if not os.path.exists(self._cert_dir + serial_no + '.pem'):
                f = open(self._cert_dir + serial_no + '.pem', 'w')
                f.write(cert_str)
                f.close()

    def _verify_signature(self, headers, body):     # 校验签名
        signature = headers.get('Wechatpay-Signature')
        timestamp = headers.get('Wechatpay-Timestamp')
        nonce = headers.get('Wechatpay-Nonce')
        serial_no = headers.get('Wechatpay-Serial')
        cert_found = False
        certificate = ''
        for cert in self._certificates:
            if int('0x' + serial_no, 16) == cert.serial_number:
                cert_found = True
                certificate = cert
                break
        if not cert_found:
            self._update_certificates()
            for cert in self._certificates:
                if int('0x' + serial_no, 16) == cert.serial_number:
                    cert_found = True
                    certificate = cert
                    break
            if not cert_found:
                return False
        if not rsa_verify(timestamp, nonce, body, signature, certificate):
            return False
        return True

    def request(self, path, method=RequestType.GET, data=None, skip_verify=False, sign_data=None,
                files=None, cipher_data=False, headers=None,
                show_url=True, show_response=True, force_data=False,
                show_request=True, show_rsp=True):
        """
        请求 POST 、GET
        :param path:            接口 路径， 网关 + path 构成请求接口地址
        :param method:          POST、GET(default method)
        :param data:            请求数据
        :param skip_verify:     跳过验证签名  False-不跳过， True-跳过
        :param sign_data:       签名数据
        :param files:           请求文件
        :param cipher_data:     加密数据
        :param headers:         请求头
        :param show_request:    是否显示请求信息，包括 url， POST/GET类型，头部，请求参数。 True-显示， False-不显示
        :param show_url:        是否在日志显示 url。 优先级小于 show_request
        :param show_rsp:        是否在日志显示接口返回所有内容（状态码，header，text）。 True-显示， False-不显示
        :param show_response:   是否在日志显示接口返回内容。优先级小于 show_rsp
        :param force_data:      按 字节方式传递 data
        :return:    (status_code, message)
        """
        if headers is None:
            headers = {}
        if files:
            headers.update({'Content-Type': 'multipart/form-data'})
        else:
            headers.update({'Content-Type': 'application/json'})
        headers.update({'Accept': 'application/json'})
        headers.update({'User-Agent': 'jd-wechatpay v3 python sdk'})
        if cipher_data:
            headers.update({'Wechatpay-Serial': hex(self._last_certificate().serial_number)[2:].upper()})

        netloc = path.find("://", 4, 8)   # http:// or https://.  '://' start begin 4 or 5
        if netloc > 0:   # path 为完成 url，含有域名
            first_path = path.find('/', netloc + 3)     # 3 为 '://' 的长度， 查找 url中的路径，第一个 /
            if first_path >= 0:
                sign_path = path[first_path:]
                if method == RequestType.GET and data:
                    sign_path += f"?{urlencode(data)}"      # 通过 GET， data 传递参数时
            else:   # wrong branch， domain maybe error.
                sign_path = path
            url = path
        else:   # path 为路径
            sign_path = path
            url = jd_concat(self.gate_way, path)
        authorization = build_authorization(
            sign_path,      # 去掉域名后的路径，以 / 开头
            method.value,
            self._mch_id,
            self._cert_serial_no,
            self._private_key,
            data=sign_data or data)
        headers.update({'Authorization': authorization})
        if self._logger and show_request:   # 显示请求信息
            if show_url:
                self._logger.debug('Request url: %s' % url)
            self._logger.debug('Request type: %s' % method.value)
            self._logger.debug('Request headers: %s' % headers)
            self._logger.debug('Request params: %s' % data)
        try:
            if method == RequestType.GET:   # 为了 签名正确，GET方式，不要通过 data 传递 参数， 需要写到 path 中
                response = requests.get(url=url, params=data, headers=headers, proxies=self._proxy, timeout=_timeout)
            elif method == RequestType.POST:
                para_json = None if force_data or files else data
                para_byte = data if force_data or files else None
                if force_data and isinstance(para_byte, (str, dict)):  # 字符串、字典 转 byte
                    para_byte = json.dumps(para_byte, ensure_ascii=False).encode("utf-8")
                response = requests.post(url=url, json=para_json, data=para_byte, headers=headers, files=files,
                                         proxies=self._proxy, timeout=_timeout)
            elif method == RequestType.PATCH:
                response = requests.patch(url=url, json=data, headers=headers, proxies=self._proxy, timeout=_timeout)
            elif method == RequestType.PUT:
                response = requests.put(url=url,  json=data, headers=headers, proxies=self._proxy, timeout=_timeout)
            elif method == RequestType.DELETE:
                response = requests.delete(url=url, headers=headers, proxies=self._proxy, timeout=_timeout)
            else:
                raise Exception('sdk does no support this request type.')
        except (TimeoutError, requests.exceptions.ConnectionError, MaxRetryError, NewConnectionError):
            return 500, {'code': 500, 'msg': 'Timeout Error'}
        if self._logger and show_request and show_url:  # 真实 url
            self._logger.debug('Request [real] url: %s' % response.url)
        if self._logger and show_rsp:
            self._logger.debug('Response status code: %s' % response.status_code)
            self._logger.debug('Response headers: %s' % response.headers)
            if show_response:
                self._logger.debug('Response content: %s' % response.text)
        if response.status_code in range(200, 300) and not skip_verify:
            if not self._verify_signature(response.headers, response.text):
                raise Exception('failed to verify the signature')
        if response.status_code == 404:
            return response.status_code, {'code': response.status_code, 'msg': response.text}
        elif response.status_code in [405]:
            return response.status_code, {'code': response.status_code, 'msg': 'Method Not Allowed'}
        message = response.text if 'application/json' in response.headers.get('Content-Type') else response.content
        try:
            if isinstance(message, str):
                message = json.loads(message)
            elif isinstance(message, bytes):
                message = json.loads(message.decode("utf-8"))
        except json.decoder.JSONDecodeError:
            message = {}
        return response.status_code, message

    def sign(self, data, sign_type=SignType.RSA_SHA256):
        if sign_type == SignType.RSA_SHA256:
            sign_str = '\n'.join(data) + '\n'
            return rsa_sign(self._private_key, sign_str)
        elif sign_type == SignType.HMAC_SHA256:
            key_list = sorted(data.keys())
            sign_str = ''
            for k in key_list:
                v = data[k]
                sign_str += str(k) + '=' + str(v) + '&'
            sign_str += 'key=' + self._private_key
            return hmac_sign(self._private_key, sign_str)
        else:
            raise ValueError('unexpected value of sign_type.')

    def decrypt_callback(self, headers, body):
        if isinstance(body, bytes):
            body = body.decode('UTF-8')
        if self._logger:
            self._logger.debug('Callback Header: %s' % headers)
            self._logger.debug('Callback Body: %s' % body)
        if not self._verify_signature(headers, body):
            return None
        data = json.loads(body)
        resource_type = data.get('resource_type')
        if resource_type != 'encrypt-resource':
            return None
        resource = data.get('resource')
        if not resource:
            return None
        algorithm = resource.get('algorithm')
        if algorithm != 'AEAD_AES_256_GCM':
            raise Exception('sdk does not support this algorithm')
        nonce = resource.get('nonce')
        ciphertext = resource.get('ciphertext')
        associated_data = resource.get('associated_data')
        if not (nonce and ciphertext):
            return None
        if not associated_data:
            associated_data = ''
        result = aes_decrypt(
            nonce=nonce,
            ciphertext=ciphertext,
            associated_data=associated_data,
            api_v3_key=self._api_v3_key)
        if self._logger:
            self._logger.debug('Callback resource: %s' % result)
        return result

    def callback(self, headers, body):
        if isinstance(body, bytes):
            body = body.decode('UTF-8')
        result = self.decrypt_callback(headers=headers, body=body)
        if result:
            data = json.loads(body)
            data.update({'resource': json.loads(result)})
            return data
        else:
            return result

    def _init_certificates(self):
        if self._cert_dir and os.path.exists(self._cert_dir):
            for file_name in os.listdir(self._cert_dir):
                if not file_name.lower().endswith('.pem'):
                    continue
                with open(self._cert_dir + file_name, encoding="utf-8") as f:
                    certificate = load_certificate(f.read())
                now = datetime.utcnow()
                if certificate and certificate.not_valid_before <= now <= certificate.not_valid_after:
                    self._certificates.append(certificate)
        if not self._certificates:
            self._update_certificates()
        if not self._certificates:
            self._logger.error('No wechatpay platform certificate, please double check your init params.')
            # raise Exception('No wechatpay platform certificate, please double check your init params.')

    def decrypt(self, ciphertext):
        return rsa_decrypt(ciphertext=ciphertext, private_key=self._private_key)

    def encrypt(self, text):
        return rsa_encrypt(text=text, certificate=self._last_certificate())

    def _last_certificate(self):
        if not self._certificates:
            self._update_certificates()
        certificate = self._certificates[0]
        for cert in self._certificates:
            if certificate.not_valid_after < cert.not_valid_after:
                certificate = cert
        return certificate
