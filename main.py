from pathlib import Path
from example.SMASignal import SignalMonitor as SMASignal
from example.ICTSignal import SignalMonitor as ICTSignal
from binance.um_futures import UMFutures
from py_app.utils.logger_tools import logger
import os
import certifi
os.environ['SSL_CERT_FILE'] = certifi.where()

if __name__ == '__main__':
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

    sma_signal = SMASignal()
    # 监测信号
    signal_info = sma_signal.check_signal(
        symbol=symbol, interval=interval, klines=klines)
    logger.info(signal_info)

    # 保存图片
    project_dir = Path().resolve()
    to_path = project_dir.joinpath(f'{symbol}_{interval}.jpg')
    sma_signal.save_image(symbol=symbol, interval=interval,
                          klines=klines, to_path=to_path)
