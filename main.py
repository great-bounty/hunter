from pathlib import Path
from example.SMASignal import SignalMonitor as SMASignal
from example.ICTIndicator import TVIndicator as ICTIndicator
from example.ICTSignal import SignalMonitor as ICTSignal
from binance.um_futures import UMFutures
from py_app.utils.logger_tools import logger
import os
import certifi
os.environ['SSL_CERT_FILE'] = certifi.where()

def check_signal(symbol: str, interval: str, klines: list):
    signal = ICTSignal()
    # 监测信号
    signal_info = signal.check_signal(
        symbol=symbol, interval=interval, klines=klines)
    logger.info(signal_info)

    # 保存图片
    project_dir = Path().resolve()
    to_path = project_dir.joinpath(f'{symbol}_{interval}.jpg')
    signal.save_image(symbol=symbol, interval=interval,
                          klines=klines, to_path=to_path)

def check_indicator(symbol: str, interval: str, klines: list):
    indicator = ICTIndicator()
    shape_infos = indicator.tv_shape_infos(symbol=symbol, interval=interval, klines=klines)
    logger.debug(shape_infos)

if __name__ == '__main__':
    symbol = 'ZRXUSDT'
    interval = '15m'
    ba_client = UMFutures()
    kline_infos = ba_client.klines(symbol=symbol, interval=interval, limit=365)
    klines = []
    for val_list in kline_infos:
        if len(val_list) > 6:
            val_list = val_list[:6]
            klines.append(val_list)
        else:
            pass

    check_signal(symbol=symbol, interval=interval, klines=klines)
    

