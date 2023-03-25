import pandas as pd
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
        pass

df = get_data_frame(kline_list=klines)
