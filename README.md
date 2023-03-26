## 介绍

Hunter是一款基于Tradingview研发的,可以用Python自定义技术指标和交易信号的合约交易软件.

市场数据源自币安永续合约交易对.

### 下载

[Windows(x86)下载](https://hunter.focuschance.com/download.html)

[Mac(Intel)下载](https://hunter.focuschance.com/download.html)

[Linux(x86)下载](https://hunter.focuschance.com/download.html)

### 安装

#### Windows版

1. 下载zip文件后解压
2. 进入解压目录
3. 找到Hunter.exe
4. 双击运行

#### Mac版

1. 下载zip文件后解压
2. 将解压得到的Hunter.app移动到应用程序目录中
3. 双击Hunter.app运行

#### Linux版

1. 下载zip文件后解压
2. 进入解压目录
3. 找到Hunter或Hunter.bin
4. 双击运行

## 行情

数据源自币安,仅支持币安的永续合约交易对.

### 如何使用自定义指标?

<iframe src="https://hunter.focuschance.com/config/files/videos/use_custom_id.mp4" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true" height="480px" sandbox></iframe>

### 如何修改自定义指标参数?

<iframe src="https://hunter.focuschance.com/config/files/videos/change_id_params.mp4" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true" height="480px" sandbox></iframe>

### 如何创建自定义指标?

自定义指标代码必须符合以下格式规范:

1. 自定义指标的类名必须为 `TVIndicator`
2. `TVIndicator`必须实现 `def tv_shape_infos(self, symbol: str, interval: str, klines: list):`函数
3. `tv_shape_infos`必须返回Tradingview形状数据的数组
4. 除了上面必须实现的函数外,您还可以为`TVIndicator`添加任意属性和方法

关于调试:

> 可用logger.info('xxx')输出调试日志,并在日志文件中查看
>
> 日志文件路径:
>
> windows日志文件路径:`安装目录/data/Hunter/Temp/tourist@signout.com/log`
>
> Mac/Linux日志文件路径:`/home/%USER%/Downloads/Hunter/Temp/tourist@signout.com/log`

详见以下示例代码:

[自定义指标-示例代码下载](https://github.com/great-bounty/hunter.git)

```python
import pandas as pd
import numpy as np
import pandas_ta as ta
import math
import copy
import logging
import time
from datetime import *
from py_app.utils.logger_tools import logger
# 仅支持导入以上系统/第三方库,导入其他库,可能造成异常

class TVIndicator:
    name: str = '' # 指标的名字(必选)
    version: str = '' # 指标的版本(Default: 1.0.0)
    deploy_version: str = '' # 指标支持的Hunter的最低版本(Default: 100.100.100)
    detail_url: str = '' # 指标的详情页面,可为博文或视频地址(可选)
    open_source: str = 'YES' # 是否开源, YES其他用户可以复制源码, NO其他用户不可以复制源码(Default: YES)
    indicator_params: dict = { # 指标里用的到参数
        "number": {
            "type": "number",
            "value": 5
        },
        "string": {
            "type": "string",
            "value": '10'
        },
        "bool": {
            "type": "bool",
            "value": True
        },
        "color": {
            "type": "color",
            "value": 'rgba(255, 0, 0, 0.4)'
        },
        "enum": {
            "type": "enum",
            "value": 'SMA',
            "options": ['SMA', "EMA", "DEMA"]
        },
    }

    def tv_shape_infos(self, symbol: str, interval: str, klines: list):
    		'''
    		symbol 当前交易对名字
    		interval 当前时间周期: 1s/1m/3m/5m/15m/30m/1h/2h/4h/6h/8h/12h/1d/3d/1w/1M
    		klines K线数据列表: [[time, open, high, low, close, volume]...]
    		-------------------------------------------------------
    		访问indicator_params的示例:
    		number_value = self.indicator_params['number']['value']
    		string_value = self.indicator_params['string']['value']
    		...
    		-------------------------------------------------------
    		return Tradingview的Shape信息的列表
    		-------------------------------------------------------
            **重要**:
            "time": 需要精确到秒级,
            "price": 需要经过强制类型转换float(price),否则会导致数据类型错误
    		'''
    		
        return []
```

Tradingview形状属性列表详见文档:

[TradingView添加自定义形状(createmultipointshape)](https://zlq4863947.gitbook.io/tradingview/4-tu-biao-ding-zhi/chart-methods#createMultipointShapepoints-options)

[Tradingview形状与覆盖](https://zlq4863947.gitbook.io/tradingview/fu-lu/shapes-and-overrides)

备用地址:[TradingView添加自定义形状(createmultipointshape)](https://hunter.focuschance.com/help/tradingview/4-tu-biao-ding-zhi/chart-methods.html#createmultipointshapepoints-options)

备用地址:[TradingView形状与覆盖](https://hunter.focuschance.com/help/tradingview/fu-lu/shapes-and-overrides.html)

示例代码:

```python
def tv_shape_infos(self, symbol: str, interval: str, klines: list):
	return [{ # 矩形
        "shape_name":"smc_rectangle",
        "shape_type":"multi_point_shape",
        "points":[
            {
                "time":1679531400,
                "price":1.1846
            },
            {
                "time":1679539500,
                "price":1.1813
            }
        ],
        "options":{
            "shape":"rectangle",
            "lock":true,
            "disableSelection":true,
            "disableSave":true,
            "disableUndo":true,
            "overrides":{
                "backgroundColor":"#FFB90F",
                "color":"#FFB90F",
                "borderColor":"#FFB90F",
                "borderWidth":0,
                "linewidth":0,
                "drawBorder":false,
                "transparency":85,
                "backgroundTransparency":85,
                "borderTransparency":85
            }
        }
    },{ # 折线
        "shape_name":"zigzag_line",
        "shape_type":"multi_point_shape",
        "points":[
            {
                "time":1679381100,
                "price":1.2892
            },
            {
                "time":1679386500,
                "price":1.2257
            },
            {
                "time":1679403600,
                "price":1.3418
            },
            {
                "time":1679408100,
                "price":1.2874
            }
        ],
        "options":{
            "shape":"path",
            "lock":true,
            "disableSelection":true,
            "disableSave":true,
            "disableUndo":true,
            "overrides":{
                "linecolor":"#0000FF",
                "linewidth":2,
                "transparency":80
            }
        }
    }]
```

### 如何测试/发布自定义指标?

<iframe src="https://hunter.focuschance.com/config/files/videos/save_public_id.mp4" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true" height="480px" sandbox></iframe>

## 信号监测

### 如何使用自定义信号?

<iframe src="https://hunter.focuschance.com/config/files/videos/use_custom_signal.mp4" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true" height="480px" sandbox></iframe>

### 如何创建自定义信号?

自定义信号代码必须符合以下格式规范:

1. 自定义指标的类名必须为 `SignalMonitor`

2. `SignalMonitor`必须实现以下函数:

 >  `def check_signal(self, symbol: str, interval: str, klines: list):`函数
 >
 >  `def save_image(self, symbol: str, interval: str, klines: list, to_path: str):`函数

   3.除了上面必须实现的函数外,您还可以为`SignalMonitor`添加任意属性和方法

关于调试:

> 可用logger.info('xxx')输出调试日志,并在日志文件中查看
>
> 日志文件路径:
>
> windows日志文件路径:`安装目录/data/Hunter/Temp/tourist@signout.com/log`
>
> Mac/Linux日志文件路径:`/home/%USER%/Downloads/Hunter/Temp/tourist@signout.com/log`

详见以下示例代码:

[自定义信号-示例代码下载](https://github.com/great-bounty/hunter.git)

```python
import pandas as pd
import numpy as np
import pandas_ta as ta
import math
import copy
import logging
import time
from datetime import *
from py_app.utils.logger_tools import logger
import plotly.graph_objects as pygo
from plotly import subplots
# 仅支持导入以上系统/第三方库,导入其他库,可能造成异常

class SignalMonitor:
    name: str = '' # 信号的名字(必选)
    version: str = '' # 信号的版本(Default: 1.0.0)
    deploy_version: str = '' # 信号支持的Hunter的最低版本(Default: 100.100.100)
    detail_url: str = '' # 信号的详情页面,可为博文或视频地址(可选)
    open_source: str = 'YES' # 是否开源, YES其他用户可以复制源码, NO其他用户不可以复制源码(Default: YES)
    signal_params = { # 信号里用的到参数
        "number": { # number类型示例
            "type": "number",
            "value": 5
        },
        "string": { # string类型示例
            "type": "string",
            "value": '10'
        },
        "bool": { # bool类型示例
            "type": "bool",
            "value": True
        },
        "color": { # color类型示例
            "type": "color",
            "value": 'rgba(255, 0, 0, 0.4)'
        },
        "enum": { # enum类型示例
            "type": "enum",
            "value": 'SMA',
            "options": ['SMA', "EMA", "DEMA"]
        },
    }
    
    def check_signal(self, symbol: str, interval: str, klines: list):
    	'''
    	symbol 当前交易对名字
    	interval 当前时间周期: 1s/1m/3m/5m/15m/30m/1h/2h/4h/6h/8h/12h/1d/3d/1w/1M
    	klines K线数据列表: [[time, open, high, low, close, volume],...]
    	-------------------------------------------------------
    	访问signal_params的示例:
    	number_value = self.signal_params['number']['value']
    	string_value = self.signal_params['string']['value']
    	...
    	-------------------------------------------------------
    	return 信号检测结果
    	'''
        return {
            'appear': True, # bool True:出现信号, False:没有出现信号
            'detail_msg': '' # str 信号描述
        }

    def save_image(self, symbol: str, interval: str, klines: list, to_path: str):
        '''
    	symbol 当前交易对名字
    	interval 当前时间周期: 1s/1m/3m/5m/15m/30m/1h/2h/4h/6h/8h/12h/1d/3d/1w/1M
    	klines K线数据列表: [[time, open, high, low, close, volume]...]
    	to_path 图片保存的目标地址
    	-------------------------------------------------------
    	访问signal_params的示例:
    	number_value = self.signal_params['number']['value']
    	string_value = self.signal_params['string']['value']
    	...
    	'''
```

在`save_image`函数中用`plotly`库绘制图形,并保存到`to_path`.



### 如何测试/发布自定义信号?

<iframe src="https://hunter.focuschance.com/config/files/videos/save_public_signal.mp4" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true" height="480px" sandbox></iframe>

## K线回放

### 如何自定义K线回放时间?

<iframe src="https://hunter.focuschance.com/config/files/videos/select_replay_time.mp4" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true" height="480px" sandbox></iframe>

### 如何多周期同时回放?

<iframe src="https://hunter.focuschance.com/config/files/videos/replay_windows.mp4" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true" height="480px" sandbox></iframe>

K线多周期同时回放,可以完美的重现历史行情波动的快慢,直观感受多空力量的强弱!可以更好的培养自己的盘感,有效的提升自己技术分析能力!

注意要点:

> 多窗口排列好,并分别设定好时间周期之后,在大周期窗口中不要进行任何操作,并在最小的时间周期窗口中启用播放,即可实现多周期同时回放.
>
> 如果在多个窗口中同时启用了播放功能,则可能造成混乱!

## 设置

### 如何设置API Key?

仅支持币安API交易.

首先需要创建API Key.

参考文档:[如何创建API | 币安 (binance.com)](https://www.binance.com/zh-CN/support/faq/如何创建api-360002502072)

将创建的API Key和Secret复制,粘贴到对应的文本框中.

![](https://hunter.focuschance.com/config/files/images/api_key_setting.png)

### 业自建应用设置

[详情视频](https://v.douyin.com/AJthoyY/)

### 如何设置自定义通知?

#### 如何自定义企业微信通知?

##### 企业自建应用设置

> 企业ID(必填)
>
> Agent ID(必填)
>
> Secret(必填)

详细步骤可参考文档:

[企业自建应用-消息通知文档](https://open.work.weixin.qq.com/wwopen/helpguide/detail?t=selfBuildApp)

##### 群机器人设置

> 企业ID(留空)
>
> Agent ID(留空)
>
> Web hook Key(必填)

详细步骤可参考文档:

[如何设置群机器人 -发送消息文档](https://open.work.weixin.qq.com/help2/pc/14931?person_id=1&from=homesearch)

[企业微信群机器人设置视频教程](https://www.bilibili.com/video/BV1Ke41137Ky/?share_source=copy_web&vd_source=2bdbf1083d52bf447f49a6e78c8cb443)

#### 如何自定义WebHook通知?

![web_hook_img](https://hunter.focuschance.com/config/files/images/web_hook_img.png)

在url栏输入自定义地址.示例:`http://127.0.0.1:61188/send/ict/trade/signal`

在`SecretKey`栏输入自定义密钥.示例:`ABRRRQAUUUUAFFFFABRRRQAUUUUA`

当价格提醒,交易信号,成交通知触发时,会向URL地址发送POST请求,参数格式如下:

```json
{
    "msg_type":"", // 消息类型
    "data":{}, // 消息对应数据
    "time_stamp":"", // 消息触发时的毫秒级时间戳
    "secret":"" // 加密字段,用于校验请求合法性
}
```

参数说明:

> msg_type: 价格提醒/信号通知/成交通知
>
> data: 消息数据
>
> time_stamp: 毫秒级时间戳
>
> secret: 计算方法为SecretKey加上time_stamp之后取md5.示例:md5(SecretKey+time_stamp).

价格提醒示例:

```json
{
    "msg_type":"价格提醒",
    "data":{
        "a_id":"1679664338757",
        "condition":"<=",
        "createTime":1679664338757,
        "enable":true,
        "from_price":1.173,
        "interval":"1",
        "remainTimes":1,
        "status":"invalid",
        "symbol":"IMXUSDT",
        "to_price":1.172874,
        "detail_msg":"",
        "md_msg":""
    },
    "secret":"e1d3834ee2a9cbe67ece8f87c458c6d6",
    "time_stamp":"1679664413318"
}
```

信号通知示例:

```json
{
    "msg_type":"信号通知",
    "data":{
        "s_id":"1679663701000",
        "symbol":"APTUSDT",
        "interval":"15m",
        "time":1679663701,
        "name":"ICT&SMC-SignalMonitor",
        "image_path":"",
        "image_url":"",
        "signal_info":{
            "appear":true,
            "type":"sell",
            "enter_price":0,
            "profit_price":0,
            "stop_price":0,
            "win_percentage":0,
            "detail_msg":"ict_smc_signal 价格进入15m供应区FVG"
        },
        "image_base64":"/9j/4AAQSkZJRgABAQAAAQABAAD2wBDAAgGBg...."
    },
    "secret":"a308cdfe8c44712a43a2c2c9834ba7f9",
    "time_stamp":"1679663701542"
}
```

成交通知示例:

```json
{
    "msg_type":"成交通知",
    "data":{
        "avgPrice":"1.1697",
        "clientOrderId":"gKxGfiMgYQOo7TPbGnRUVtXY1yy0pZWW",
        "cumQuote":"100.5942",
        "executedQty":"86",
        "orderId":90696011,
        "origQty":"86",
        "origType":"TAKE_PROFIT",
        "price":"1.1697",
        "reduceOnly":false,
        "side":"SELL",
        "positionSide":"SHORT",
        "status":"FILLED",
        "stopPrice":"1.1697",
        "closePosition":false,
        "symbol":"IMXUSDT",
        "time":1679664861497,
        "timeInForce":"GTC",
        "type":"LIMIT",
        "activatePrice":"0.0",
        "priceRate":"0.0",
        "updateTime":1679664861497,
        "workingType":"CONTRACT_PRICE",
        "priceProtect":true
    },
    "secret":"8c9a1c6dc877d1728698e5698e08e895",
    "time_stamp":"1679664862927"
}
```

### 如何充值

扫码(或复制重置地址)充值成功后,复制交易的哈希ID,并粘贴到输入框中,点击`确认充值`按钮即可到账!

<iframe src="https://hunter.focuschance.com/config/files/videos/recharge.mp4" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true" height="480px" sandbox></iframe>

## 交流群

QQ交流群:`772598403`

## 商务合作

软件定制/指标定制/信号定制

联系微信:`XYKJ21191`

联系邮箱:`2024292041@qq.com`

## 常见问题

### Mac提示未信任的开发者怎么办?

[Mac不能安装非信任应用的解决方法 打不开身份不明的开发者?文件已损坏? ](https://zhuanlan.zhihu.com/p/161341622)

### Mac提示应用损坏无法打开?

1. 将解压后的Hunter.app移动到`应用程序`目录

2. 打开终端，输入以下命令：

3. ```fallback
   sudo xattr -rd com.apple.quarantine /Applications/Hunter.app
   ```

   然后按键盘的回车键（Enter），输入密码后按回车键即可完成！

   好了，再看一下是不是可以打开APP了！

   如果还是无法打开APP,可参考:[当Mac软件提示损坏时可以绕过公证或者在Mac本地为软件签名](https://lapulace.com/macOS_Notarization.html)

### 如何快速切换交易对?

<iframe src="https://hunter.focuschance.com/config/files/videos/quick_change_symbol.mp4" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true" height="480px" sandbox></iframe>

