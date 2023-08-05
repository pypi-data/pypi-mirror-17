微信SDK
======

提供微信登陆，公众号管理，微信支付，微信消息等处理

## 安装

    pip install weixin-python

## 用法


### 微信消息

首先初始化

    from flask import Flask
    from weixin.msg import WeixinMsg

    app = Flask(__name__)
    msg = WeixinMsg("e10adc3949ba59abbe56e057f20f883e", None, 0)

如果使用flask建议使用默认视图函数

    app.add_url_rule("/", view_func=msg.view_func)

    @msg.all
    def all(**kwargs):
        return msg.reply(
            kwargs['sender'], sender=kwargs['receiver'], content='all'
        )

上面例子可以接收所有的用户发送的所有类型的消息, 如果仅仅是需要接受文本类型的消息

    @msg.text("*") # @msg.text()
    def all_text(**kwargs):
        return msg.reply(
            kwargs['sender'], sender=kwargs['receiver'], content='hello world'
        )

如果需要接收文本消息的指定内容，可以使用

    @msg.text("help")
    def text_help(**kwargs):
        return msg.reply(
            kwargs['sender'], sender=kwargs['receiver'], content='帮组文档'
        )

如果要接收用户的图像消息

    @msg.image
    def image(**kwargs):
        print kwargs
        return ""

有以下消息类型包装器

* 所有类型 `@msg.all`
* 文本类型 `@msg.text()` `@msg.text("help")`
* 图片类型 `@msg.image`
* 视频类型 `@msg.video` `@msg.shortvideo`
* 音频类型 `@msg.voice`
* 坐标类型 `@msg.location`
* 链接类型 `@msg.link`
* 事件类型 `@msg.event`

还可以监听具体的事件

* 订阅事件 `@msg.subscribe`
* 取消订阅事件 `@msg.unsubscribe`
* 点击事件 `@msg.click`
* 其它事件 `@msg.{event}`

具体使用方式可以参考 `example/msg.py`

### 微信登陆

初始化

    from weixin.login import WeixinLogin

    login = WeixinLogin(app_id, app_secret)

微信有两种scope

1. snsapi_base 只能获取用户的openid，不需要用户确认
2. snsapi_userinfo 可以获取用户信息，需要用户主动确认


snsapi_base方式

    url = login.authorize("http://example.com/authorized", "snsapi_base")

snsapi_usrinfo方式

    url = login.authorize("http://example.com/authorized", "snsapi_userinfo")

获取用户信息

    # 首根据code获取access_token跟openid
    data = login.access_token(code)
    # 如果scope为`snsapi_userinfo`可以执行以下操作
    user_info = login.user_info(data.access_token, data.openid)
    print user_info.nickname
    print usre_info.name

更多用法可以参考 `example/login.py`

### 公众号管理

初始化

    from weixin.mp import WeixinMP

    mp = WeixinMP(app_id, app_secret)

获取公众号唯一凭证

    print mp.access_token

创建临时qrcode

    data = mp.qrcode_create(123, 30)
    print mp.qrcode_show(data.ticket)

创建永久性qrcode

    # scene_id类型
    mp.qrcode_create_limit(123)
    # scene_str类型
    mp.qrcode_create_limit("456")

长链接变短链接

    mp.shorturl("http://example.com/test")

菜单管理

    # 获取菜单
    try:
        print mp.menu_get()
    except WeixinError:
        pass

    # 创建菜单
    data = [
        {
            "type": "view",
            "name": "测试",
            "url": "http://code.show/",
        },
    ]
    print mp.menu_create(data)

    # 删除菜单
    print mp.menu_delete()

更多用法参考 `example/mp.py`

### 微信支付

初始化

    from weixin.pay import WeixinPay

    pay = WeixinPay(app_id, mch_id, mch_key, notify_url)

创建统一订单

    out_trade_no = pay.nonce_str
    try:
        raw = pay.unified_order(openid="openid", trade_type="JSAPI", body=u"测试", out_trade_no=out_trade_no, total_fee=1)
        print raw["prepay_id"]
    except WeixinPayError, e:
        print e.message

也可以用JSAPI快速创建统一订单,并且快速返回js调起支付所需要的参数
参数包括 `package`, `appId`, `timeStamp`, `nonceStr`, `sign`

    # total_fee 单位为分
    pay.jsapi(openid='openid', body='测试', out_trade_no=out_trade_no, total_fee=1)

查询订单

    pay.close_order(out_trade_no)

关闭订单

    pay.order_query(out_trade_no=out_trade_no)

检查签名是否通过

    if pay.check(pay.to_dict(request.data)):
        print "OK"
