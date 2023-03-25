import pandas as pd
import numpy as np
import pandas_ta as ta
import math
import copy
import logging
import time
from datetime import *
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