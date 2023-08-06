#  Python CodePay 码支付
> 支付宝 QQ全免 微信免手续费只需交易额度
> 无需担心第三方跑路资金直接到账 这里不会瞧不起个人站长 免费帮助个人实现支付后立即通知
> 
> Alipay QQ free Wechat free of fees only transaction limit ;There is no need to worry about the third party running funds directly to the account here will not look down on personal webmaster free help personal payment immediately after notice

# 使用教程 module Using the Tutorial

### 1. CodePayObj 初始化 
```angular2html
 codepay_obj = CodePay(
            codepay_id='22XXXXX00638', # 商家ID
            key='eead8fbdXXXX12080e64', # 秘钥
            codepay_url= '创建订单的URL'
        )
```

### 2. 调用功能
#### 2.1 获取codePay 支付订单url
```angular2html
   codepay_order_create_url = codepay_obj.get_codepay_pay_url(
            type=1, # 支付类型
            price=1, # 价格
            pay_id='2000xxx9000', # 唯一支付ID 
            page=1,
            notify_url='支付完毕回调地址',
            return_url='支付完毕回调地址'
        )
```

#### 2.2 校验codePay返回的订单结果,
```angular2html
    verify_result = codepay_obj.verify_order_return_result(订单相关参数)
    if verify_result:
        print('校验通过')
    else:
        print('校验不通过, 有人冒充CodePay平台')
```



