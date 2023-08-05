# -*- coding: utf-8 -*-
import json
import time
import uuid
from base64 import b64decode, b64encode

from cryptography.exceptions import InvalidSignature, InvalidTag
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15, OAEP, MGF1
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.hashes import SHA256, SHA1, SM3, Hash
from cryptography.hazmat.primitives.hmac import HMAC
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.x509 import load_pem_x509_certificate


def build_authorization(path,       # 获取请求的绝对URL，并去除域名部分得到参与签名的URL。
                        method,     # HTTP请求的方法（GET,POST,PUT）等
                        mch_id,     # 发起请求的商户（包括直连商户、服务商或渠道商）的商户号
                        serial_no,  # 商户API证书序列号
                        private_key,
                        data=None,
                        nonce_str=None  # 请求随机串
                        ):
    """
    生成签名，参考 https://pay.weixin.qq.com/wiki/doc/apiv3/wechatpay/wechatpay4_0.shtml

    """
    time_stamp = str(int(time.time()))
    nonce_str = nonce_str or ''.join(str(uuid.uuid4()).split('-')).upper()
    body = data if isinstance(data, str) else json.dumps(data) if data else ''
    sign_str = '%s\n%s\n%s\n%s\n%s\n' % (method, path, time_stamp, nonce_str, body)
    signature = rsa_sign(private_key=private_key, sign_str=sign_str)
    authorization = 'WECHATPAY2-SHA256-RSA2048 mchid="%s",nonce_str="%s",signature="%s",timestamp="%s",serial_no="%s"'\
                    % (mch_id, nonce_str, signature, time_stamp, serial_no)
    return authorization


def rsa_sign(private_key, sign_str):  # RSA 签名
    message = sign_str.encode('UTF-8')
    signature = private_key.sign(data=message, padding=PKCS1v15(), algorithm=SHA256())
    sign = b64encode(signature).decode('UTF-8').replace('\n', '')
    return sign


def aes_decrypt(nonce, ciphertext, associated_data, api_v3_key):
    key_bytes = api_v3_key.encode('UTF-8')
    nonce_bytes = nonce.encode('UTF-8')
    associated_data_bytes = associated_data.encode('UTF-8')
    data = b64decode(ciphertext)
    aes_gcm = AESGCM(key=key_bytes)
    try:
        result = aes_gcm.decrypt(nonce=nonce_bytes, data=data, associated_data=associated_data_bytes).decode('UTF-8')
    except InvalidTag:
        result = None
    return result


def format_private_key(private_key_str):
    pem_start = '-----BEGIN PRIVATE KEY-----\n'
    pem_end = '\n-----END PRIVATE KEY-----'
    if not private_key_str.startswith(pem_start):
        private_key_str = pem_start + private_key_str
    if not private_key_str.endswith(pem_end):
        private_key_str = private_key_str + pem_end
    return private_key_str


def load_certificate(certificate_str):
    try:
        return load_pem_x509_certificate(data=certificate_str.encode('UTF-8'), backend=default_backend())
    except (ValueError, AttributeError, TypeError):
        return None


def load_private_key(private_key_str):

    try:
        return load_pem_private_key(data=format_private_key(private_key_str).encode('UTF-8'), password=None,
                                    backend=default_backend())
    except (ValueError, AttributeError, TypeError):
        raise Exception('failed to load private key.')


def rsa_verify(timestamp, nonce, body, signature, certificate):  # 签名校验
    sign_str = '%s\n%s\n%s\n' % (timestamp, nonce, body)
    public_key = certificate.public_key()
    message = sign_str.encode('UTF-8')
    signature = b64decode(signature)
    try:
        public_key.verify(signature, message, PKCS1v15(), SHA256())
    except InvalidSignature:
        return False
    return True


def rsa_encrypt(text, certificate):  # RSA 加密
    data = text.encode('UTF-8')
    public_key = certificate.public_key()
    cipher_byte = public_key.encrypt(
        plaintext=data,
        padding=OAEP(mgf=MGF1(algorithm=SHA1()), algorithm=SHA1(), label=None)
    )
    return b64encode(cipher_byte).decode('UTF-8')


def rsa_decrypt(ciphertext, private_key):   # RSA 解密
    data = private_key.decrypt(
        ciphertext=b64decode(ciphertext),
        padding=OAEP(mgf=MGF1(algorithm=SHA1()), algorithm=SHA1(), label=None)
    )
    result = data.decode('UTF-8')
    return result


def hmac_sign(key, sign_str):
    hmac = HMAC(key.encode('UTF-8'), SHA256())
    hmac.update(sign_str.encode('UTF-8'))
    sign = hmac.finalize().hex().upper()
    return sign


def sha256(data):
    _hash = Hash(SHA256())
    _hash.update(data)
    return _hash.finalize().hex()


def sm3(data):
    _hash = Hash(SM3())
    _hash.update(data)
    return _hash.finalize().hex()


def build_query_url(params: dict):
    """
    构造 GET 方法的 url。 未对特色字符编码
    """
    query = []
    if isinstance(params, dict):
        for k, v in params.items():
            if isinstance(v, bool):
                v = 'true' if v else 'false'
            query.append(f"{k}={v}")
    return '&'.join(query)


def jd_concat(url: str, path: str):
    """
    url 合并， 去掉重复的 / 字符
    :param url:     url 网关，例如： 'https://domain.com
    :param path:    请求路径，例如： '/some_path/books_get'
    :return:    合并后的路径  url + path，去掉 多余 字符('/')
    """
    if url and path:
        n = 1 if url[-1] == '/' else 0
        if path[0] == '/':
            n += 1

        if 2 == n:
            return url + path[1:]
        elif 0 == n:
            return f"{url}/{path}"

    return (url or '') + (path or '')
