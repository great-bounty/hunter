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


class SignalMonitor:
    name = 'SMA-SignalMonitor'
    version = '1.0.0'
    deploy_version = '100.100.100'
    detail_url = ''
    open_source = 'YES'
    signal_params = {
        "period": {
            "type": "number",
            "value": 20
        }
    }

    def get_data_frame(self, kline_list: list):
        data_frame = pd.DataFrame(
            kline_list, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
        data_frame['Date'] = data_frame['Date'].values.astype(
            dtype='datetime64[ms]')
        data_frame.index = data_frame['Date']
        
        return data_frame

    def save_image(self, symbol: str, interval: str, klines: list, to_path: str):
        data_frame = self.get_data_frame(kline_list=klines)
        length = self.signal_params['period']['value']
        length = int(length)
        # 计算SMA技术指标
        sma_list = data_frame.ta.sma(length=length, append=True)

        # Create subplots and mention plot grid size
        # rows: 行数
        # cols: 列数
        # shared_xaxes: k线和成交量共享x轴
        # vertical_spacing: k线和成交量上下间隔
        # subplot_titles: 子图标题
        # row_width: 这是一个向前兼容的参数, 方向是从下往上, 0.2对应的成交量的高度, 0.7对应的k线
        # row_heights: row_width的替代参数, 默认方向是从上到下, 如果这里使用的话, 应该设为[0.7, 0.2]
        fig = subplots.make_subplots(rows=2, cols=1, shared_xaxes=True,
                            vertical_spacing=0.0,
                            row_heights=[0.75, 0.2]
                            )
        # Plot OHLC on 1st row
        fig.add_trace(pygo.Candlestick(x=data_frame['Date'],
                                             open=data_frame['Open'], high=data_frame['High'],
                                             low=data_frame['Low'], close=data_frame['Close'],
                                                 increasing_fillcolor='green',
                                                 increasing_line_color='green',
                                                 increasing_line_width=0.5,
                                                 decreasing_fillcolor='red',
                                                 decreasing_line_color='red',
                                                 decreasing_line_width=0.5,
                                                 name='ohlc',
                                                 showlegend=False
                                                 )
                              ,row=1, col=1)

        # Bar trace for volumes on 2nd row without legend
        # showlegend: 是否显示右侧图标, 成交量不需要显示了, 有k线就够了
        vol_colors = []
        for index in range(0, len(data_frame['Date'])):
            o = data_frame['Open'][index]
            c = data_frame['Close'][index]
            if o >= c:
                vol_colors.append('red')
            else:
                vol_colors.append('green')
                
        volume_list = data_frame['Volume'].tolist()
        volume = []
        for vlo in volume_list:
            volume.append(float(vlo))
        fig.add_trace(pygo.Bar(x=data_frame['Date'], y=volume, marker_color=vol_colors, showlegend=False), row=2, col=1)

        datetime_p = datetime.now()
        datetime_s = datetime.strftime(datetime_p, '%Y-%m-%d %H:%M:%S')
        title = f'{symbol}/{interval} {datetime_s} {self.name}'
        fig.update_layout(
            xaxis_rangeslider_visible=False,
            title=title,
            yaxis_title=symbol
        )
        fig.update_shapes(dict(xref='x', yref='y'))
        fig.write_image(to_path, width=1920, height=1080, scale=2)

    def check_signal(self, symbol: str, interval: str, klines: list):
        data_frame = self.get_data_frame(kline_list=klines)
        length = self.signal_params['period']['value']
        length = int(length)
        # 计算SMA技术指标
        sma_list = data_frame.ta.sma(length=length, append=True)
        latest_high = data_frame['High'].tolist()[-1]
        latest_high = float(latest_high)
        latest_low = data_frame['Low'].tolist()[-1]
        latest_low = float(latest_low)
        latest_sma = sma_list.tolist()[-1]
        latest_sma = float(latest_sma)

        if latest_sma > latest_low and latest_sma < latest_high:
            print(f'{latest_low} < {latest_sma} < latest_high')
            return {
                'appear': True,
                'detail_msg': f'sma_signal {interval} 出现信号'
            }
        else:
            return {
                'appear': False,
                'detail_msg': f'sma_signal {interval} 没有出现信号'
            }
