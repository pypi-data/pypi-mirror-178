import unittest

import requests

from CodePay_Python.codePay import CodePay


class Test(unittest.TestCase):
    def setUp(self) -> None:
        # 实例化 codepay 对象
        self.codePay = CodePay(
            codepay_id='2208800638',
            key='eead8fbdb09964dc560b232c12080e64'
        )
        self.wait_verify_test_data = {
            "pay_id": "200003388889",
            "money": 1.01,
            "price": 1,
            "type": 1,
            "pay_no": "20221128082600366266",
            "param": "",
            "pay_time": 0,
            "pay_tag": 0,
            "id": "2208800638",
            "sign": "656dd2e7c7687f23eb65a454bb56a628"

        }

    def tearDown(self) -> None:
        del self.codePay

    def test_codepay_order_crate_url(self):
        code_pay_create_order_url = self.codePay.get_codepay_pay_url(
            type=1,
            price=1,
            pay_id='2000033889000',
            page=1,
            notify_url='http://192.168.88.100:8000/fees_recharge_order/check_order_water/',
            return_url='http://192.168.88.100:8000/fees_recharge_order/check_order_water/'
        )

        # print(code_pay_create_order_url)
        response = requests.get(code_pay_create_order_url)
        self.assertIn('在线支付', response.content.decode(), '支付页面显示成功')

    def test_codepay_return_order_result(self):
        verify_result = self.codePay.verify_order_return_result(self.wait_verify_test_data)
        self.assertTrue(verify_result, '校验通过')
