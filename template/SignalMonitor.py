import pandas as pd
import numpy as np
import pandas_ta as ta
import math
import copy
import logging
import time
from datetime import *
import plotly.graph_objects as pygo
from plotly import subplots
# 仅支持导入以上系统/第三方库,导入其他库,可能造成异常

class SignalMonitor:
    name: str = '' # 信号的名字(必选)
    version: str = '' # 信号的版本(Default: 1.0.0)
    deploy_version: str = '' # 信号支持的Hunter的最低版本(Default: 100.100.100)
    detail_url: str = '' # 信号的详情页面,最好是信号的介绍和用法,可为博文或视频地址(可选)
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
        klines K线数据列表: [[time, open, high, low, close, volume]...]
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
        pass

