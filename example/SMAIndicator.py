
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

class TVIndicator:
    name = 'SMA-Indicator'
    version = '1.0.0'
    deploy_version = '100.100.100'
    detail_url = ''
    open_source = 'YES'
    indicator_params = {
        "period": {
            "type": "number",
            "value": 5
        }
    }

    def get_data_frame(self, kline_list: list):
        data_frame = pd.DataFrame(
            kline_list, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
        data_frame['Date'] = data_frame['Date'].values.astype(
            dtype='datetime64[ms]')
        data_frame.index = data_frame['Date']
        
        return data_frame

    def shapes_on_chart(self, symbol: str, interval: str, klines: list, for_tv: bool = False):
        data_frame = self.get_data_frame(kline_list=klines)
        length = self.indicator_params['period']['value']
        length = int(length)
        # 计算SMA技术指标
        sma_list = data_frame.ta.sma(length=length, append=True)
        date_list = data_frame['Date'].tolist()
        sma_list = sma_list.tolist()
        date_list = date_list[-len(sma_list):]
        path = []

        for index in range(0, len(sma_list)):
            t_s = date_list[index]
            price = sma_list[index]
            path.append({
                'time':  int(pd.to_datetime(t_s).value / 10 ** 9),
                'value': float(price),
            })
        path.append(path[-1]) # 最后两个值相等则表示绘制结束
        sma_line_info = {
            'shape_name': f'sma_{length}_line',
            'shape_type': 'multi_point_shape',
            'points': path,
            'options': {
                'shape': 'path',
                'lock': True,
                'disableSelection': True,
                'disableSave': True,
                'disableUndo': True,
                'overrides': {
                    'lineColor': '#0000FF',
                    'lineWidth': 1,
                    'lineStyle': 0,
                    'transparency': 80,
                    'rightEnd': 0
                }
            }
        }
        shape_infos = [sma_line_info]

        return shape_infos

    def tv_shape_infos(self, symbol: str, interval: str, klines: list):
        return self.shapes_on_chart(symbol=symbol, interval=interval, klines=klines, for_tv=True)
