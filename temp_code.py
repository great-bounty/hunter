import pandas as pd
import pandas_ta as ta
import plotly.graph_objs as go
import plotly.io as pio
import requests
from pathlib import Path
from example.SMASignal import SignalMonitor as SMASignal
from binance.um_futures import UMFutures
import os
import certifi
os.environ['SSL_CERT_FILE'] = certifi.where()

# 获取微软最新股价
def get_data_frame(kline_list: list):
    data_frame = pd.DataFrame(
            kline_list, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
    data_frame['Date'] = data_frame['Date'].values.astype(
            dtype='datetime64[ms]')
    data_frame.index = data_frame['Date']
        
    return data_frame

# 获取微软最新股价
symbol = 'BTCUSDT'
interval = '1h'
ba_client = UMFutures()
kline_infos = ba_client.klines(symbol=symbol, interval=interval, limit=365)
klines = []
for val_list in kline_infos:
    if len(val_list) > 6:
        val_list = val_list[:6]
        klines.append(val_list)
    else:
        pass# 用pandas_ta计算klines的sma指标


df = get_data_frame(kline_list=klines)
# 定义函数识别出波段高低点中的动量转换
def momentum_conversion(hl_point_list):
    momentum_list = []
    for i in range(1, len(hl_point_list)):
        if not pd.isna(hl_point_list[i]) and not pd.isna(hl_point_list[i-1]):
            momentum_list.append(hl_point_list[i] - hl_point_list[i-1])
        else:
            momentum_list.append(pd.NaT)
    return momentum_list

hl_point_list = [nan, nan, nan, nan, nan, 0.2714, nan, 0.2656, nan, nan, nan, nan, nan, 0.2712, nan, nan, nan, nan, nan, nan, nan, nan, nan, 0.2604, nan, nan, nan, nan, 0.2651, nan, 0.2484, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, 0.2947, nan, nan, nan, nan, nan, nan, 0.279, nan, nan, nan, nan, nan, 0.2925, nan, nan, 0.2833, nan, 0.3175, nan, 0.306, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, 0.595, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, 0.4546, nan, 0.494, nan, nan, nan, nan, nan, nan, nan, nan, nan, 0.4515, nan, nan, nan, nan, nan, nan, nan, nan, nan, 0.6538, nan, nan, nan, 0.596, nan, nan, nan, nan, 0.69, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, 0.5913, nan, 0.6182, nan, nan, nan, nan, nan, 0.5898, nan, nan, nan, nan, nan, nan, 0.746, nan, nan, 0.653, nan, nan, nan, nan, 0.71, nan, nan, nan, nan, nan, nan, nan, 0.6601, nan, nan, nan, nan, 0.7347, nan, nan, nan, nan, 0.6471, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, 0.8548, nan, nan, 0.8006, nan, nan, nan, nan, 0.9392, nan, nan, nan, nan, nan, nan, 0.7752, nan, nan, nan, nan, 0.843, nan, nan, nan, nan, nan, nan, nan, 0.787, nan, nan, nan, 0.828, 0.7853, nan, nan, nan, 0.8394, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, 0.703, nan, nan, 0.7689, nan, nan, nan, nan, nan, 0.7141, nan, nan, nan, nan, 0.7752, nan, nan, nan, nan, nan, nan, nan, nan, nan, 0.7043, nan, nan, 0.732, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, 0.6713, nan, nan, nan, 0.6866, nan, 0.6657, nan, nan, nan, nan, nan, 0.7269, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, 0.626, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, 0.6319, nan, nan, 0.61, nan, nan, nan, nan, nan, nan, nan, nan, 0.6472, nan, nan, nan, nan, 0.6003, nan, nan, nan, nan, nan, 0.637, nan, nan]