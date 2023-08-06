# @Author: LCF
# @Software: PyCharm
# @Time: 2022/11/28

from hashlib import md5
from urllib.parse import quote_plus


class CodePay(object):
    """
    码支付主功能类
    """

    def __init__(self, codepay_id=None, key=None, codepay_url=None):
        """
        :param codepay_id: 商户ID business_id
        :param key: 商户支付秘钥 pay_key
        :param codepay_url: 支付接口网关url  codepay_gateway_url
        """
        self.codepay_id = codepay_id
        self.pay_key = key
        self.codepay_url = codepay_url or 'https://cs-vlwmwhfu51z343.zhifuhucc.juhe.apihuya.com/creat_order/'

    def get_codepay_pay_url(self, type, price, pay_id, page, notify_url, return_url, **kwargs):

        """
            :param id: codepay_id bitint, register codepay id
            :param type: int , pay_method default 1, contains 1,2,3; 1:alipay, 3:wechat_pay
            :param price: float min-max(0.01-99999.99), good_price
            :param pay_id: unique string not null, like: user_id or order_id or username
            :param param: (optional) string , custom param
            :param notify_url: string 100 bytes, async notice url, Notice by POST after payment.
                               The highest priority is left blank as the notification address in the system Settings to improve confidentiality
            :param return_url: (optional) string , Users jump to the page after payment
            :param sign: data md5 sign
            :param call: (optional) call back function.
            :param page: int pay_page_method, 1,2,3,4; Different ways to display payment pages
                         4: Return JSON 3: Return JS function if call is passed as callback
            Usage::
                  import CodePay
                  codepay_auth = CodePay(codepay_id='2220003',pay_key="3eduoi3ii43ii43", codepay_url="http://xxx.com/create_order" )
                  codepay_url = codepay_auth.get_codepay_pay_url()

        """

        """
           id  码支付ID 无符号整数bigint类型 码支付注册所生成
           key 通信密钥 字符串string 6-100位字符 不要传递sign加密用的
           type 支付方式 整数int 1位 1,2,3 1：支付宝 3：微信支付。默认值：1
           price 商品价格 浮点float 保留2位小数 最大值99999.99最小值0.01
           pay_id 唯一标识 字符串string 不可留空 用户ID,订单ID,用户名确保是唯一
           param 自定义参数 字符串string 可留空 原封返回 避免特殊字符
           notify_url	异步通知地址	字符串string 100位字符	付款后POST通知。优先级最高 留空为系统设置中的通知地址可提高保密性
           return_url  同步通知地址  字符串string 可留空  付款后用户跳转页面
           sign 数据MD5签名 字符串string 可留空 数据加密md5(a=1&b=2&c=3替换密钥)将需要构造的参数按首字母排序并拼接成url参数 如首字母相同则依次比对下一个字母 此参数跟token参数2选1如果看不懂可传递token参数
           call 回调函数 字符串string 可留空 js回调的函数名 参考值：callback
           page 付款页面方式 整数int  1,2,3,4 展示付款页面不同的方式, 4：返回JSON 3：需传入call值为callback时返回JS函数
        """
        # 1. 接收 订单需要的必传参数 ; recive order must params
        data_dict = {
            'id': self.codepay_id,
            'type': type,
            'price': price,
            'pay_id': pay_id,
            'page': page,
            'notify_url': notify_url,
            'return_url': return_url
        }
        # 2. 非必传参数 如果有传递, 就合并在 data_dict; if kwargs not null, should concat from data_dict
        if len(kwargs) > 0:
            data_dict.update(kwargs)

        # 3. md5加密参数
        query_params = self.md5_sign(data=data_dict)

        # 6.返回拼接完整的url
        return self.codepay_url + '?' + query_params

    def verify_order_return_result(self, return_result):
        """
        verify codepay return order result 校验 codepay 平台返回的订单信息是不是真的
        :param return_result: codepay 返回的订单数据
        :return: Bool, True 校验通过, False 有人冒充codePay平台
        """
        self_sign = self.md5_sign(return_result, type='verify')
        sign = return_result.get('sign', '')
        if self_sign != sign:
            return False
        return True

    def md5_sign(self, data, type='create'):
        """
        md5 secrect pramas md5加密参数
        :param data: 需要加密的字典数据 dict
        :param type: 默认 create,  校验返回结果的时候不需要返回urls,可以设置type='verify'
        :return: string
        """
        # 根据 字典的键key, 对所有参数进行排序, 之后在强转回dict
        sort_data = dict(sorted(data.items(), key=lambda x: x[0]))

        sign = ''
        if type == 'create':
            urls = ''
        # 遍历 字典, 排除值是空字符串和 key是 sign的数据,  以 k=v&k1=v1进行拼接
        for k, v in sort_data.items():
            if v == '' or k == 'sign':
                continue
            if sign != '':
                sign += '&'
                if type == 'create':
                    urls += '&'
            sign = sign + k + '=' + str(v)
            if type == 'create':
                urls = urls + k + '=' + quote_plus(str(v))  # url转译

        # 使用sign值+商户支付秘钥 pay_key, 在经过md5加密
        md5_sign = md5((sign + self.pay_key).encode()).hexdigest()

        if type == 'create':
            # ?id=2208800638&%2F&type=1&sign=a5a6cba492e72cf3a7e9ddbcd927cd38
            return urls + '&sign=' + md5_sign

        # a5a6cba492e72cf3a7e9ddbcd927cd38
        return md5_sign
