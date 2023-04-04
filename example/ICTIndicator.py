
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
from py_app.utils.logger_tools import logger

class TVIndicator:
    name = 'ICT&SMC-Indicator'
    version = '1.0.0'
    deploy_version = '100.100.100'
    detail_url = 'https://www.bilibili.com/video/BV19k4y1t77h/?share_source=copy_web&vd_source=2bdbf1083d52bf447f49a6e78c8cb443'
    open_source = 'YES'
    indicator_params = {
        "long deep": {
            "type": "number",
            "value": 20
        },
        "short deep": {
            "type": "number",
            "value": 5
        },
        "show FVG": {
            "type": "bool",
            "value": True
        },
        "show OB": {
            "type": "bool",
            "value": True
        },
        "show Long HL Line": {
            "type": "bool",
            "value": True
        },
        "show Short HL Line": {
            "type": "bool",
            "value": True
        },
        "long HL Line Color": {
            "type": "color",
            "value": 'rgba(244, 164, 96, 0.4)'
        },
        "short HL Line Color": {
            "type": "color",
            "value": 'rgba(192, 192, 192, 0.4)'
        },
        # ,
        # "string": {
        #     "type": "string",
        #     "value": '10'
        # },
        # "bool": {
        #     "type": "bool",
        #     "value": True
        # },
        # "enum": {
        #     "type": "enum",
        #     "value": 'SMA',
        #     "options": ['SMA', "EMA", "DEMA"]
        # },
    }

    def getDateString(self, date_str):

        return date_str

    def find_high_low_point_list(self, data_frame: pd.DataFrame, deep: int):
        high_nums = data_frame['High'].tolist()
        low_nums = data_frame['Low'].tolist()
        latest_high_list = [high_nums[-1]] * deep
        latest_low_list = [low_nums[-1]] * deep

        high_nums.extend(latest_low_list)
        low_nums.extend(latest_high_list)

        # 定义每组元素个数
        group_size = deep
        # 使用列表推导式和切片将数组分割为二维数组
        high_point_list = [np.nan] * len(high_nums)
        for i in range(deep, len(high_nums)-deep):
            sub_value = high_nums[i]
            sub_list = high_nums[i-deep:i+deep]
            max_value = max(sub_list)
            if sub_value == max_value:
                high_point_list[i] = max_value
            else:
                pass

        # 使用列表推导式和切片将数组分割为二维数组
        low_point_list = [np.nan] * len(low_nums)
        for i in range(deep, len(low_nums)-deep):
            sub_value = low_nums[i]
            sub_list = low_nums[i-deep:i+deep]
            min_value = min(sub_list)
            if sub_value == min_value:
                low_point_list[i] = min_value
            else:
                pass

        same_point_list = []
        hl_point_list = []
        for index in range(0, len(high_point_list)):
            h_value = high_point_list[index]
            l_value = low_point_list[index]
            if math.isnan(h_value) == False and  math.isnan(l_value): # 只是最高点
                hl_point_list.append(h_value)
                same_point_list.append(0)
            elif math.isnan(h_value) and  math.isnan(l_value) == False: # 只是最低点
                hl_point_list.append(l_value)
                same_point_list.append(0)
            else: # 最高点与最低点在同一根线上
                hl_point_list.append(np.nan)
                same_point_list.append(1)
        # 解决冲突的点
        for index in range(0, len(high_point_list)):
            same_value = same_point_list[index]
            if same_value == 1:
                # 找到前一个非零点
                pre_index = index
                pre_value = np.nan
                while pre_index > 0:
                    pre_value = hl_point_list[pre_index]
                    pre_index = pre_index - 1
                    if math.isnan(pre_value):
                        continue
                    else:
                        break
                if math.isnan(pre_value):
                    hl_point_list[index] = high_point_list[index]
                else:
                    pass
                # 找到后一个非零点
                next_index = index
                next_value = np.nan
                while next_index < len(hl_point_list):
                    next_value = hl_point_list[next_index]
                    next_index = next_index + 1
                    if math.isnan(next_value):
                        continue
                    else:
                        break
                if math.isnan(next_value):
                    hl_point_list[index] = high_point_list[index]
                else:
                    pass
                if same_value < pre_value and same_value < next_value:
                    hl_point_list[index] = low_point_list[index]
                elif same_value > pre_value and same_value > next_value:
                    hl_point_list[index] = high_point_list[index]
                elif same_value > pre_value and same_value < next_value:
                    hl_point_list[index] = high_point_list[index]
                elif same_value < pre_value and same_value > next_value:
                    hl_point_list[index] = low_point_list[index]
                else:
                    pass
            else:
                pass
        
        count = 2
        while count > 0:
            count = count - 1
            # # 将间隔不够的高低点过滤掉
            # value_1 = np.nan
            # index_1 = 0
            # value_2 = np.nan
            # index_2 = 0
            # value_3 = np.nan
            # index_3 = 0
            # find_target = False
            # for index in range(0, len(hl_point_list)):
            #     cur_value = hl_point_list[index]
            #     if math.isnan(cur_value):
            #         pass
            #     else:
            #         if math.isnan(value_1):
            #             value_1 = cur_value
            #             index_1 = index
            #         elif math.isnan(value_2):
            #             value_2 = cur_value
            #             index_2 = index
            #         elif math.isnan(value_3):
            #             value_3 = cur_value
            #             index_3 = index
            #         else:
            #             index_1 = index_2
            #             index_2 = index_3
            #             index_3 = index
            #             value_1 = value_2
            #             value_2 = value_3
            #             value_3 = cur_value
            #             if (index_3 - index_2) <= deep:# 间隔不足deep
            #                 if value_1 >= value_2 and value_1 >= value_3:
            #                     if value_2 <= value_3:
            #                         hl_point_list[index_3] = np.nan
            #                     else:
            #                         hl_point_list[index_2] = np.nan
            #                 elif value_1 <= value_2 and value_1 <= value_3:
            #                     if value_2 < value_3:
            #                         hl_point_list[index_2] = np.nan
            #                     else:
            #                         hl_point_list[index_3] = np.nan
            #                 else:
            #                     pass
            #             else:
            #                 pass
            
            # 将连续的高点或者连续的低点过滤掉
            value_1 = np.nan
            index_1 = 0
            value_2 = np.nan
            index_2 = 0
            value_1_type = None
            value_2_type = None
            for index in range(0, len(hl_point_list)):
                cur_value = hl_point_list[index]
                if math.isnan(cur_value):
                    pass
                else:
                    if math.isnan(value_1):
                        value_1 = cur_value
                        index_1 = index
                    elif math.isnan(value_2):
                        value_2 = cur_value
                        index_2 = index
                    else:
                        index_1 = index_2
                        index_2 = index
  
                        value_1 = value_2
                        value_2 = cur_value
                        if value_1 == high_nums[index_1]:
                            value_1_type = 'high'
                        elif value_1 == low_nums[index_1]:
                            value_1_type = 'low'
                        else:
                            pass
                        if value_2 == high_nums[index_2]:
                            value_2_type = 'high'
                        elif value_2 == low_nums[index_2]:
                            value_2_type = 'low'
                        else:
                            pass
                        if count == 1:
                            # 在连续的高点之间插入低点或者在连续的低点之间插入高点
                            if value_1_type == value_2_type and value_1_type == 'high':
                                start_index = index_1 + 1
                                end_index = index_2 - 1
                                sub_lows = low_nums[start_index:end_index]
                                if len(sub_lows) > 0:
                                    low_value = min(sub_lows)
                                    sub_index = sub_lows.index(low_value)
                                    low_index = start_index + sub_index
                                    hl_point_list[low_index] = low_value
                                else:
                                    pass
                            elif value_1_type == value_2_type and value_1_type == 'low':
                                start_index = index_1 + 1
                                end_index = index_2 - 1
                                sub_highs = high_nums[start_index:end_index]
                                if len(sub_highs) > 0:
                                    high_value = max(sub_highs)
                                    sub_index = sub_highs.index(high_value)
                                    high_index = start_index + sub_index
                                    hl_point_list[high_index] = high_value
                                else:
                                    pass
                            else:
                                pass
                        else: 
                            # 将连续的高点合并
                            if value_1_type == value_2_type and value_1_type == 'high':
                                if value_1 > value_2:
                                    hl_point_list[index_2] = np.nan
                                else:
                                    hl_point_list[index_1] = np.nan
                            elif value_1_type == value_2_type and value_1_type == 'low':
                                if value_1 > value_2:
                                    hl_point_list[index_1] = np.nan
                                else:
                                    hl_point_list[index_2] = np.nan
                            else:
                                pass
        
        hl_point_list = hl_point_list[:-deep]
        return hl_point_list

    def zigzag_line_point_list(self, hl_point_list: list, data_frame: pd.DataFrame):
        zigzag_point_list = []
        for p_index in range(0, len(hl_point_list)):
            p_value = hl_point_list[p_index]
            date_value = data_frame['Date'].iloc[p_index]
            if math.isnan(p_value) == False:
                zigzag_point_list.append((date_value, p_value))
            else:
                pass

        return zigzag_point_list
    
    def is_overlap(self, a1, a2, b1, b2):
            overlap = (min(a1, a2) <= max(b1, b2)) and (max(a1, a2) >= min(b1, b2))
            return overlap

    def find_fair_value_gap_infos(self, data_frame: pd.DataFrame):
        date_nums = data_frame['Date'].tolist()
        open_nums = data_frame['Open'].tolist()
        high_nums = data_frame['High'].tolist()
        low_nums = data_frame['Low'].tolist()
        close_nums = data_frame['Close'].tolist()
        ohlc_infos = []
        min_price = 9999999999
        max_price = -9999999999

        fvg_infos = []
        for index_2 in range(2, len(date_nums)):
            index_0 = index_2 - 2
            index_1 = index_2 - 1
            high_0 = high_nums[index_0]
            high_1 = high_nums[index_1]
            high_2 = high_nums[index_2]
            low_0 = low_nums[index_0]
            low_1 = low_nums[index_1]
            low_2 = low_nums[index_2]
            open_1 = open_nums[index_1]
            close_1 = close_nums[index_1]
            if high_2 < low_0: # 出现FVG
                # 过滤掉比较小的FVG
                fvg_dis = abs(high_2 - low_0)
                body_dis = abs(open_1 - close_1)
                if body_dis == 0.0:
                    body_dis = fvg_dis*0.1
                else:
                    pass
                if fvg_dis/body_dis < 0.3: # 造成FVG的这根K线的涨跌幅
                    continue
                else:
                    pass
                
                fvg_info = {
                    'index': index_0,
                    'start_ts': date_nums[index_0],
                    'end_ts': date_nums[-1],
                    'high': low_0,
                    'low': high_2,
                    'type': 'supply',
                    'vaild': True,
                    'refill': 0
                }
                for next_index in range(index_2, len(date_nums)):
                    next_high = high_nums[next_index]
                    next_date = date_nums[next_index]
                    if next_high > high_2:
                        if next_high < (low_0+high_2)/2.0:
                            # fvg_info['low'] = next_high
                            pass
                        else:
                            fvg_info['end_ts'] = next_date
                            fvg_info['vaild'] = False
                            break
                    else:
                        pass
                fvg_infos.append(fvg_info)
            elif low_2 > high_0: # 出现FVG
                # 过滤掉比较小的FVG
                fvg_dis = abs(low_2 - high_0)
                body_dis = abs(open_1 - close_1)
                if body_dis == 0.0:
                    body_dis = fvg_dis*0.1
                else:
                    pass
                if fvg_dis/body_dis < 0.3:
                    continue
                else:
                    pass

                fvg_info = {
                    'index': index_0,
                    'start_ts': date_nums[index_0],
                    'end_ts': date_nums[-1],
                    'high': low_2,
                    'low': high_0,
                    'type': 'demand',
                    'vaild': True,
                    'refill': 0
                }
                for next_index in range(index_2, len(date_nums)):
                    next_low = low_nums[next_index]
                    next_date = date_nums[next_index]
                    if next_low < low_2:
                        if next_low > (high_0+low_2)/2.0:
                            # fvg_info['high'] = next_low
                            pass
                        else:
                            fvg_info['end_ts'] = next_date
                            fvg_info['vaild'] = False
                            break
                    else:
                        pass 
                fvg_infos.append(fvg_info)
            else:
                pass

        return fvg_infos
    
    def find_order_block_infos(self, data_frame: pd.DataFrame, zigzag_point_list: list):
        date_nums = data_frame['Date'].tolist()
        high_nums = data_frame['High'].tolist()
        low_nums = data_frame['Low'].tolist()
        min_price = 9999999999
        max_price = -9999999999

        order_block_infos = []
        for p_index in range(2, len(zigzag_point_list)):
            (date_value_0, p_value_0) = zigzag_point_list[p_index-2]
            (date_value_1, p_value_1) = zigzag_point_list[p_index-1]
            (date_value_2, p_value_2) = zigzag_point_list[p_index]

            condition_0 = (data_frame['Date'] >= date_value_0) & (data_frame['Date'] <= date_value_1 )
            sub_open_nums_0 = data_frame[condition_0]['Open'].tolist()
            sub_close_nums_0 = data_frame[condition_0]['Close'].tolist()
            sub_high_nums_0 = data_frame[condition_0]['High'].tolist()
            sub_low_nums_0 = data_frame[condition_0]['Low'].tolist()
            sub_date_nums_0 = data_frame[condition_0]['Date'].tolist()

            condition_1 = (data_frame['Date'] >= date_value_1) & (data_frame['Date'] <= date_value_2)
            sub_open_nums = data_frame[condition_1]['Open'].tolist()
            sub_close_nums = data_frame[condition_1]['Close'].tolist()
            sub_high_nums = data_frame[condition_1]['High'].tolist()
            sub_low_nums = data_frame[condition_1]['Low'].tolist()
            sub_date_nums = data_frame[condition_1]['Date'].tolist()
            # 过滤掉假突破,或者小幅度突破
            dis_1 = p_value_1 - p_value_0
            dis_2 = p_value_2 - p_value_1
            if dis_1 == 0.0:
                dis_1 = dis_2
            else:
                pass
            if abs(dis_2)/abs(dis_1) < 1.5:
                # 不算大幅度突破,不算订单块
                continue
            else:
                # 算大幅度突破,算订单块
                pass

            if p_value_1 > p_value_0 and p_value_1 > p_value_2 and p_value_2 < p_value_0: # 向下突破
                # 找到突破的那根K线
                ob_info = None
                for s_index in range(0, len(sub_high_nums)):
                    s_high = sub_high_nums[s_index]
                    s_low = sub_low_nums[s_index]
                    s_open = sub_open_nums[s_index]
                    s_close = sub_close_nums[s_index]
                    s_date = sub_date_nums[s_index]
                    if s_low < p_value_0 and s_high > p_value_0: # 在这里出现了突破
                        ob_info = {
                            'index': None,
                            'high': None,
                            'low': None,
                            'start_ts': None,
                            'end_ts': date_nums[-1],
                            'vaild': True,
                            'type': 'supply'
                        }
                        if s_index == 0:
                            # 第一根线就出现了突破,订单块在前一个区间
                            p_s_index = len(sub_high_nums_0) - 1
                            while p_s_index > 0:
                                p_s_high = sub_high_nums_0[p_s_index]
                                p_s_low = sub_low_nums_0[p_s_index]
                                p_s_open = sub_open_nums_0[p_s_index]
                                p_s_close = sub_close_nums_0[p_s_index]
                                p_s_date = sub_date_nums_0[p_s_index]
                                p_s_index = p_s_index- 1
                                if p_s_close > p_s_open: # 是阳线
                                    ob_info['start_ts'] = p_s_date
                                    ob_info['end_ts'] = date_nums[-1]
                                    if ob_info['high'] is None:
                                        ob_info['high'] = p_s_high
                                    else:
                                        ob_info['high'] = max(ob_info['high'], p_s_high)
                                    if ob_info['low'] is None:
                                        ob_info['low'] = p_s_low
                                    else:
                                        ob_info['low'] = min(ob_info['low'], p_s_low)
                                else: # 不是阳线
                                    if ob_info['start_ts'] is None:# 并且还没找到阳线,继续往前找
                                        continue
                                    else:# 并且找到了阳线,停止寻找
                                        break
                        else:
                            p_s_index = s_index
                            while p_s_index >= 0:
                                p_s_high = sub_high_nums[p_s_index]
                                p_s_low = sub_low_nums[p_s_index]
                                p_s_open = sub_open_nums[p_s_index]
                                p_s_close = sub_close_nums[p_s_index]
                                p_s_date = sub_date_nums[p_s_index]
                                p_s_index = p_s_index- 1
                                if p_s_close > p_s_open: # 是阳线
                                    ob_info['start_ts'] = p_s_date
                                    ob_info['end_ts'] = date_nums[-1]
                                    if ob_info['high'] is None:
                                        ob_info['high'] = p_s_high
                                    else:
                                        ob_info['high'] = max(ob_info['high'], p_s_high)
                                    if ob_info['low'] is None:
                                        ob_info['low'] = p_s_low
                                    else:
                                        ob_info['low'] = min(ob_info['low'], p_s_low)
                                else: # 是阴线
                                    if ob_info['start_ts'] is None:# 并且还没找到阳线,继续往前找
                                        continue
                                    else:# 并且找到了阳线,停止寻找
                                        break
                        break
                    else:
                        pass
                if ob_info is not None:
                    if ob_info['start_ts'] is not None:
                        # 计算OB的有效性
                        ob_vaild_ts = date_value_2
                        next_open_nums = data_frame[data_frame['Date'] >= ob_vaild_ts]['Open'].tolist()
                        next_close_nums = data_frame[data_frame['Date'] >= ob_vaild_ts]['Close'].tolist()
                        next_high_nums = data_frame[data_frame['Date'] >= ob_vaild_ts]['High'].tolist()
                        next_low_nums = data_frame[data_frame['Date'] >= ob_vaild_ts]['Low'].tolist()
                        next_date_nums = data_frame[data_frame['Date'] >= ob_vaild_ts]['Date'].tolist()
                        for next_index in range(0, len(next_date_nums)):
                            next_high = next_high_nums[next_index]
                            next_low = next_low_nums[next_index]
                            next_date = next_date_nums[next_index]

                            ob_high = ob_info['high']
                            ob_low = ob_info['low']
                            if next_high > ob_low:
                                if next_high < (ob_high+ob_low)/2.0:
                                    # ob_info['low'] = next_high
                                    pass
                                else:
                                    ob_info['end_ts'] = next_date
                                    ob_info['vaild'] = False
                                    break
                            else:
                                pass
                        order_block_infos.append(ob_info)
                    else:
                        pass
                else:
                    pass
            elif p_value_1 < p_value_0 and p_value_1 < p_value_2 and p_value_2 > p_value_0: # 向上突破
                # 找到突破的那根K线
                ob_info = None
                for s_index in range(0, len(sub_high_nums)):
                    s_high = sub_high_nums[s_index]
                    s_low = sub_low_nums[s_index]
                    s_open = sub_open_nums[s_index]
                    s_close = sub_close_nums[s_index]
                    s_date = sub_date_nums[s_index]
                    if s_low < p_value_0 and s_high > p_value_0: # 在这里出现了突破
                        ob_info = {
                            'index': None,
                            'high': None,
                            'low': None,
                            'start_ts': None,
                            'end_ts': date_nums[-1],
                            'vaild': True,
                            'type': 'demand'
                        }
                        if s_index == 0:
                            # 第一根线就出现了突破,订单块在前一个区间
                            p_s_index = len(sub_high_nums_0) - 1
                            while p_s_index > 0:
                                p_s_high = sub_high_nums_0[p_s_index]
                                p_s_low = sub_low_nums_0[p_s_index]
                                p_s_open = sub_open_nums_0[p_s_index]
                                p_s_close = sub_close_nums_0[p_s_index]
                                p_s_date = sub_date_nums_0[p_s_index]
                                p_s_index = p_s_index- 1
                                if p_s_close < p_s_open: # 是阴线
                                    ob_info['start_ts'] = p_s_date
                                    if ob_info['high'] is None:
                                        ob_info['high'] = p_s_high
                                    else:
                                        ob_info['high'] = max(ob_info['high'], p_s_high)
                                    if ob_info['low'] is None:
                                        ob_info['low'] = p_s_low
                                    else:
                                        ob_info['low'] = min(ob_info['low'], p_s_low)
                                else: # 不是阴线
                                    if ob_info['start_ts'] is None:# 并且还没找到阴线,继续往前找
                                        continue
                                    else:# 并且找到了阴线,停止寻找
                                        break
                        else:
                            p_s_index = s_index
                            while p_s_index >= 0:
                                p_s_high = sub_high_nums[p_s_index]
                                p_s_low = sub_low_nums[p_s_index]
                                p_s_open = sub_open_nums[p_s_index]
                                p_s_close = sub_close_nums[p_s_index]
                                p_s_date = sub_date_nums[p_s_index]
                                p_s_index = p_s_index- 1
                                if p_s_close < p_s_open: # 是阴线
                                    ob_info['start_ts'] = p_s_date
                                    if ob_info['high'] is None:
                                        ob_info['high'] = p_s_high
                                    else:
                                        ob_info['high'] = max(ob_info['high'], p_s_high)
                                    if ob_info['low'] is None:
                                        ob_info['low'] = p_s_low
                                    else:
                                        ob_info['low'] = min(ob_info['low'], p_s_low)
                                else: # 是阳线
                                    if ob_info['start_ts'] is None:# 并且还没找到阴线,继续往前找
                                        continue
                                    else:# 并且找到了阴线,停止寻找
                                        break
                        break
                    else:
                        pass

                if ob_info is not None:
                    if ob_info['start_ts'] is not None:
                        # 计算OB的有效性
                        ob_vaild_ts = date_value_2
                        next_open_nums = data_frame[data_frame['Date'] >= ob_vaild_ts]['Open'].tolist()
                        next_close_nums = data_frame[data_frame['Date'] >= ob_vaild_ts]['Close'].tolist()
                        next_high_nums = data_frame[data_frame['Date'] >= ob_vaild_ts]['High'].tolist()
                        next_low_nums = data_frame[data_frame['Date'] >= ob_vaild_ts]['Low'].tolist()
                        next_date_nums = data_frame[data_frame['Date'] >= ob_vaild_ts]['Date'].tolist()
                        for next_index in range(0, len(next_date_nums)):
                            next_high = next_high_nums[next_index]
                            next_low = next_low_nums[next_index]
                            next_date = next_date_nums[next_index]

                            ob_high = ob_info['high']
                            ob_low = ob_info['low']
                            if next_low < ob_high:
                                if next_low > (ob_low+ob_high)/2.0:
                                    # ob_info['high'] = next_low
                                    pass
                                else:
                                    ob_info['end_ts'] = next_date
                                    ob_info['vaild'] = False
                                    break
                            else:
                                pass
                        order_block_infos.append(ob_info)
                    else:
                        pass
                else:
                    pass
            else:
                pass

        return order_block_infos
        
    
    def find_fair_value_gap_and_order_block_infos(self, data_frame: pd.DataFrame, zigzag_point_list: list):
        fvg_infos = self.find_fair_value_gap_infos(data_frame=data_frame)
        ob_infos = self.find_order_block_infos(data_frame=data_frame, zigzag_point_list=zigzag_point_list)

        return (fvg_infos, ob_infos)

    def getUTCDateStrFromTimestamp(self, timestamp: int):
        utc_time = datetime.utcfromtimestamp(timestamp)
        utc_time = utc_time.replace(tzinfo=timezone.utc)
        # date_str = "{0}-{1}-{2} {3}:{4}:{5}".format(str.zfill(str(utc_time.year), 4),
        #                                             str.zfill(str(utc_time.month), 2),
        #                                             str.zfill(str(utc_time.day), 2),
        #                                             str.zfill(str(utc_time.hour), 2),
        #                                             str.zfill(str(utc_time.minute), 2),
        #                                             str.zfill(str(utc_time.second), 2))
        date_str = "{0}-{1}-{2}".format(str.zfill(str(utc_time.year), 4),
                                                    str.zfill(str(utc_time.month), 2),
                                                    str.zfill(str(utc_time.day), 2))
        return date_str

    def getQuotesFromHTTPKlineData(self, kline_list: list):
        date_nums = []
        open_nums = []
        high_nums = []
        low_nums = []
        close_nums = []
        vol_nums = []

        for index in range(0, len(kline_list)):
            k_info = kline_list[index]
            open_nums.append(float(k_info[1]))
            high_nums.append(float(k_info[2]))
            low_nums.append(float(k_info[3]))
            close_nums.append(float(k_info[4]))
            vol_nums.append(float(k_info[5]))
            start_time = k_info[0]
            start_ts = int(start_time) / 1000
            start_time_str = self.getUTCDateStrFromTimestamp(start_ts)
            date_nums.append(start_time_str)

        quotes = {
            "Date": date_nums,
            "Open": open_nums,
            "Close": close_nums,
            "High": high_nums,
            "Low": low_nums,
            "Volume": vol_nums
        }

        return quotes

    def get_pandas_dataFrame_from_quotes(self, quotes: dict):
        date_nums = quotes['Date']
        date_nums = np.array(date_nums)
        data_frame = pd.DataFrame(quotes, index=date_nums)

        return data_frame

    def get_data_frame(self, kline_list: list):
        # quotes = self.getQuotesFromHTTPKlineData(kline_list=kline_list)
        # data_frame = self.get_pandas_dataFrame_from_quotes(quotes=quotes)
        for index in range(0, len(kline_list)):
            k_list = kline_list[index]
            k_number_list = []
            for v_index in range(0, 6):
                k_v = k_list[v_index]
                if isinstance(k_v, str):
                    k_v = float(k_v)
                else:
                    pass

                k_number_list.append(k_v)
            kline_list[index] = k_number_list

        data_frame = pd.DataFrame(kline_list, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
        data_frame['Date'] = data_frame['Date'].values.astype(dtype='datetime64[ms]')
        data_frame.index = data_frame['Date']
        return data_frame

    def save_image(self, symbol: str, interval: str, klines: list, to_path: str):
        data_frame = self.get_data_frame(kline_list=klines)
        print('save_image-->', to_path)
        tv_shape_infos = self.shapes_on_chart(symbol=symbol, interval=interval, klines=klines)
        dateNums = data_frame['Date']
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
        for index in range(0, len(dateNums)):
            o = data_frame['Open'][index]
            c = data_frame['Close'][index]
            if o >= c:
                vol_colors.append('red')
            else:
                vol_colors.append('green')
        fig.add_trace(pygo.Bar(x=data_frame['Date'], y=data_frame['Volume'], marker_color=vol_colors, showlegend=False), row=2, col=1)

        datetime_p = datetime.now()
        datetime_s = datetime.strftime(datetime_p, '%Y-%m-%d %H:%M:%S')
        title = f'{symbol}/{interval} {datetime_s} {self.name}'
        fig.update_layout(
            xaxis_rangeslider_visible=False,
            title=title,
            yaxis_title=symbol
        )
        for sp_info in tv_shape_infos:
            shape_name = sp_info['shape_name']
            if shape_name == 'smc_rectangle':
                points = sp_info['points']
                point1 = points[0]
                point2 = points[1]
                x0 = point1['time']
                y0 = point1['price']
                x1 = point2['time']
                y1 = point2['price']
                options = sp_info['options']
                overrides = options['overrides']
                backgroundColor = overrides['backgroundColor']
                fig.add_shape(type="rect",
                              opacity=0.25,
                              x0=x0, y0=y0, x1=x1, y1=y1,
                              line=dict(
                                  color=backgroundColor,
                                  width=0.0,
                              ),
                              fillcolor=backgroundColor,
                              )
            elif shape_name == 'zigzag_line':
                points = sp_info['points']
                options = sp_info['options']
                overrides = options['overrides']
                lineColor = overrides['lineColor']
                x_list = []
                y_list = []
                for p_info in points:
                    time = p_info['time']
                    price = p_info['price']
                    x_list.append(time)
                    y_list.append(price)
                fig.add_trace(pygo.Scatter(
                    x=x_list,
                    y=y_list,
                    line=dict(
                        color='gray',
                        width=1
                    ),
                    mode="lines",
                    name="zigzag",
                    showlegend=False
                ))
            else:
                pass
        fig.update_shapes(dict(xref='x', yref='y'))
        fig.write_image(to_path, width=1920, height=1080, scale=2)

    def check_signal(self, symbol: str, interval: str, klines: list):
        data_frame = self.get_data_frame(kline_list=klines)
        if len(data_frame['Date']) < 100:
            return {
                'appear': False,
                'type': 'buy',
                'enter_price': 0.0,
                'profit_price': 0.0,
                'stop_price': 0.0,
                'win_percentage': -1,
                'detail_msg': f'ict_smc_signal {interval}没有出现信号'
            }
        else:
            pass
        deep = self.indicator_params['long deep']['value']
        deep = int(deep)
        # 计算波段高低点
        hl_point_list = self.find_high_low_point_list(data_frame=data_frame, deep=deep)
        zigzag_point_list = self.zigzag_line_point_list(hl_point_list=hl_point_list, data_frame=data_frame)
        (fvg_infos, ob_infos) = self.find_fair_value_gap_and_order_block_infos(data_frame=data_frame, zigzag_point_list=zigzag_point_list)
        open_nums = data_frame['Open'].tolist()
        close_nums = data_frame['Close'].tolist()
        high_nums = data_frame['High'].tolist()
        low_nums = data_frame['Low'].tolist()

        latest_open = open_nums[-2]
        latest_close = close_nums[-2]
        latest_high = high_nums[-2]
        latest_low = low_nums[-2]

        
        
        for fvg_info in fvg_infos:
            vaild = fvg_info['vaild']
            high = fvg_info['high']
            low = fvg_info['low']
            type = fvg_info['type']
            if vaild and self.is_overlap(latest_high, latest_low, high, low):
                if type == 'supply':
                    return {
                        'appear': True,
                        'type': 'sell',
                        'enter_price': 0.0,
                        'profit_price': 0.0,
                        'stop_price': 0.0,
                        'win_percentage': 0.0,
                        'detail_msg': f'ict_smc_signal 价格进入{interval}供应区FVG'
                    }
                elif type == 'demand':
                    return {
                        'appear': True,
                        'type': 'buy',
                        'enter_price': 0.0,
                        'profit_price': 0.0,
                        'stop_price': 0.0,
                        'win_percentage': 0.0,
                        'detail_msg': f'ict_smc_signal 价格进入{interval}需求区FVG'
                    }
                else:
                    pass
            else:
                pass

        for ob_info in ob_infos:
            vaild = ob_info['vaild']
            high = ob_info['high']
            low = ob_info['low']
            type = ob_info['type']
            if vaild and self.is_overlap(latest_high, latest_low, high, low):
                if type == 'supply':
                    return {
                        'appear': True,
                        'type': 'sell',
                        'enter_price': 0.0,
                        'profit_price': 0.0,
                        'stop_price': 0.0,
                        'win_percentage': 0.0,
                        'detail_msg': f'ict_smc_signal 价格进入{interval}供应区order_block'
                    }
                elif type == 'demand':
                    return {
                        'appear': True,
                        'type': 'buy',
                        'enter_price': 0.0,
                        'profit_price': 0.0,
                        'stop_price': 0.0,
                        'win_percentage': 0.0,
                        'detail_msg': f'ict_smc_signal 价格进入{interval}需求区order_block'
                    }
                else:
                    pass
            else:
                pass

        return {
            'appear': False,
            'type': 'buy',
            'enter_price': 0.0,
            'profit_price': 0.0,
            'stop_price': 0.0,
            'win_percentage': -1,
            'detail_msg': f'ict_smc_signal {interval}没有出现信号'
        }

    def shapes_on_chart(self, symbol: str, interval: str, klines: list, for_tv: bool = False):
        data_frame = self.get_data_frame(kline_list=klines)
        deep = self.indicator_params['long deep']['value']
        deep = int(deep)
        # 计算波段高低点
        hl_point_list = self.find_high_low_point_list(data_frame=data_frame, deep=deep)
        zigzag_point_list = self.zigzag_line_point_list(hl_point_list=hl_point_list, data_frame=data_frame)
        (fvg_infos, ob_infos) = self.find_fair_value_gap_and_order_block_infos(data_frame=data_frame, zigzag_point_list=zigzag_point_list)

        yellow_color = '#FFB90F'
        red_color = '#FF3030'
        green_color = '#00FA9A'
        rectangle_info_list = []
        for f_index in range(0, len(fvg_infos)):
            fvg_info = fvg_infos[f_index]
            start_ts: pd.Timestamp = fvg_info['start_ts']
            end_ts: pd.Timestamp = fvg_info['end_ts']
            high = fvg_info['high']
            high = float(high)
            low = fvg_info['low']
            low = float(low)
            if for_tv:
                start_ts = int(pd.to_datetime(start_ts).value / 10 ** 9)
                end_ts = int(pd.to_datetime(end_ts).value / 10 ** 9)
            else:
                pass

            type = fvg_info['type']
            if type == 'supply':
                rectangle_info = {
                    'shape_name': 'smc_rectangle',
                    'shape_type': 'multi_point_shape',
                    'points': [{'time': start_ts, 'price': high},
                               {'time': end_ts, 'price': low}],
                    'options': {
                        'shape': 'rectangle',
                        'lock': True,
                        'disableSelection': True,
                        'disableSave': True,
                        'disableUndo': True,
                        'overrides': {
                            'backgroundColor': yellow_color,
                            'color': yellow_color,
                            'borderColor': yellow_color,
                            'borderWidth': 0,
                            'linewidth': 0,
                            'drawBorder': False,
                            'transparency': 85,
                            'backgroundTransparency': 85,
                            'borderTransparency': 85
                        }
                    }
                }
                rectangle_info_list.append(rectangle_info)
            else:
                rectangle_info = {
                    'shape_name': 'smc_rectangle',
                    'shape_type': 'multi_point_shape',
                    'points': [{'time': start_ts, 'price': high},
                               {'time': end_ts, 'price': low}],
                    'options': {
                        'shape': 'rectangle',
                        'lock': True,
                        'disableSelection': True,
                        'disableSave': True,
                        'disableUndo': True,
                        'overrides': {
                            'backgroundColor': yellow_color,
                            'color': yellow_color,
                            'borderColor': yellow_color,
                            'borderWidth': 0,
                            'linewidth': 0,
                            'drawBorder': False,
                            'transparency': 90,
                            'backgroundTransparency': 90,
                            'borderTransparency': 90
                        }
                    }
                }
                rectangle_info_list.append(rectangle_info)

        for f_index in range(0, len(ob_infos)):
            ob_info = ob_infos[f_index]
            start_ts: pd.Timestamp = ob_info['start_ts']
            end_ts: pd.Timestamp = ob_info['end_ts']
            if start_ts is None or end_ts is None:
                logger.debug(f'{start_ts}--{end_ts}')
                continue
            else:
                pass
            high = ob_info['high']
            high = float(high)
            low = ob_info['low']
            low = float(low)
            if for_tv:
                start_ts = int(pd.to_datetime(start_ts).value / 10 ** 9)
                end_ts = int(pd.to_datetime(end_ts).value / 10 ** 9)
            else:
                pass

            type = ob_info['type']
            if type == 'supply':
                rectangle_info = {
                    'shape_name': 'smc_rectangle',
                    'shape_type': 'multi_point_shape',
                    'points': [{'time': start_ts, 'price': high},
                               {'time': end_ts, 'price': low}],
                    'options': {
                        'shape': 'rectangle',
                        'lock': True,
                        'disableSelection': True,
                        'disableSave': True,
                        'disableUndo': True,
                        'overrides': {
                            'backgroundColor': red_color,
                            'color': red_color,
                            'borderColor': red_color,
                            'borderWidth': 0,
                            'linewidth': 0,
                            'drawBorder': False,
                            'transparency': 85,
                            'backgroundTransparency': 85,
                            'borderTransparency': 85
                        }
                    }
                }
                rectangle_info_list.append(rectangle_info)
            else:
                rectangle_info = {
                    'shape_name': 'smc_rectangle',
                    'shape_type': 'multi_point_shape',
                    'points': [{'time': start_ts, 'price': high},
                               {'time': end_ts, 'price': low}],
                    'options': {
                        'shape': 'rectangle',
                        'lock': True,
                        'disableSelection': True,
                        'disableSave': True,
                        'disableUndo': True,
                        'overrides': {
                            'backgroundColor': green_color,
                            'color': green_color,
                            'borderColor': green_color,
                            'borderWidth': 0,
                            'linewidth': 0,
                            'drawBorder': False,
                            'transparency': 90,
                            'backgroundTransparency': 90,
                            'borderTransparency': 90
                        }
                    }
                }
                rectangle_info_list.append(rectangle_info)

        zigzag_point_list_2 = []
        for p_index in range(0, len(zigzag_point_list)):
            (p_ts, p_price) = zigzag_point_list[p_index]
            p_price = float(p_price)
            if for_tv:
                p_ts = int(pd.to_datetime(p_ts).value / 10 ** 9)
            else:
                pass
            zigzag_point_list_2.append({'time': p_ts, 'price': p_price})
        zigzag_point_list_2.append(zigzag_point_list_2[-1])
        zigzag_line_info = {
            'shape_name': 'zigzag_line',
            'shape_type': 'multi_point_shape',
            'points': zigzag_point_list_2,
            'options': {
                'shape': 'path',
                'lock': True,
                'disableSelection': True,
                'disableSave': True,
                'disableUndo': True,
                'overrides': {
                    'lineColor': '#F4A460',
                    'lineWidth': 2,
                    'lineStyle': 0,
                    'transparency': 80,
                    'rightEnd': 0
                }
            }
        }
        shape_infos = [zigzag_line_info]
        shape_infos.extend(rectangle_info_list)

        deep = self.indicator_params['short deep']['value']
        # 计算波段高低点
        hl_point_list = self.find_high_low_point_list(data_frame=data_frame, deep=deep)
        zigzag_point_list = self.zigzag_line_point_list(hl_point_list=hl_point_list, data_frame=data_frame)
        zigzag_point_list_2 = []
        for p_index in range(0, len(zigzag_point_list)):
            (p_ts, p_price) = zigzag_point_list[p_index]
            p_price = float(p_price)
            if for_tv:
                p_ts = int(pd.to_datetime(p_ts).value / 10 ** 9)
            else:
                pass
            zigzag_point_list_2.append({'time': p_ts, 'price': p_price})
        zigzag_point_list_2.append(zigzag_point_list_2[-1])
        zigzag_line_info = {
            'shape_name': 'zigzag_line',
            'shape_type': 'multi_point_shape',
            'points': zigzag_point_list_2,
            'options': {
                'shape': 'path',
                'lock': True,
                'disableSelection': True,
                'disableSave': True,
                'disableUndo': True,
                'overrides': {
                    'lineColor': '#C0C0C0',
                    'lineWidth': 1,
                    'lineStyle': 0,
                    'transparency': 50,
                    'rightEnd': 0
                }
            }
        }
        shape_infos.append(zigzag_line_info)

        return shape_infos

    def tv_shape_infos(self, symbol: str, interval: str, klines: list):
        return self.shapes_on_chart(symbol=symbol, interval=interval, klines=klines, for_tv=True)

