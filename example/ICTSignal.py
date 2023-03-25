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
    name = 'ICT&SMC-SignalMonitor'
    version = '1.0.0'
    deploy_version = '1.0.0'
    detail_url = 'https://www.bilibili.com/video/BV19k4y1t77h/?share_source=copy_web&vd_source=2bdbf1083d52bf447f49a6e78c8cb443'
    open_source = 'YES'
    signal_params = {
        "deep": {
            "type": "number",
            "value": 5
        }
        # ,
        # "string": {
        #     "type": "string",
        #     "value": '10'
        # },
        # "bool": {
        #     "type": "bool",
        #     "value": True
        # },
        # "color": {
        #     "type": "color",
        #     "value": 'rgba(255, 0, 0, 0.4)'
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
        open_nums = data_frame['Open'].tolist()
        high_nums = data_frame['High'].tolist()
        low_nums = data_frame['Low'].tolist()
        close_nums = data_frame['Close'].tolist()
        date_nums = data_frame['Date'].tolist()

        for count in range(0, deep):
            open_nums.append(open_nums[-1])
            close_nums.append(open_nums[-1])
            high_nums.append(open_nums[-1])
            low_nums.append(open_nums[-1])
            date_nums.append(date_nums[-1])

        high_point_list = []
        low_point_list = []
        for k_index in range(0, len(high_nums)):
            if k_index < deep:
                high_point_list.append(np.nan)
                low_point_list.append(np.nan)
            elif k_index > (len(high_nums) - deep):
                high_point_list.append(np.nan)
                low_point_list.append(np.nan)
            else:
                date_ha = date_nums[k_index]
                date_ha_str = self.getDateString(date_ha)
                high_ha = high_nums[k_index]
                low_ha = low_nums[k_index]
                left_high = True
                right_high = True
                if date_ha_str == '2022-12-23 21:30:00':
                    print(date_ha)
                else:
                    pass
                for left_index in range(k_index - deep, k_index):
                    left_high_ha = high_nums[left_index]
                    if left_high_ha > high_ha:
                        left_high = False
                        break
                    else:
                        pass
                for right_index in range(k_index, k_index + deep):
                    right_high_ha = high_nums[right_index]
                    if right_high_ha > high_ha:
                        right_high = False
                        break
                    else:
                        pass
                if right_high and left_high:
                    high_point_list.append(high_ha)
                else:
                    high_point_list.append(np.nan)

                left_low = True
                right_low = True
                for left_index in range(k_index - deep, k_index):
                    left_low_ha = low_nums[left_index]
                    if left_low_ha < low_ha:
                        left_low = False
                        break
                    else:
                        pass
                for right_index in range(k_index, k_index + deep):
                    right_low_ha = low_nums[right_index]
                    if right_low_ha < low_ha:
                        right_low = False
                        break
                    else:
                        pass
                if right_low and left_low:
                    low_point_list.append(low_ha)
                else:
                    low_point_list.append(np.nan)
        # 过滤
        # print('high_point_list-->', high_point_list)
        # print('low_point_list-->', low_point_list)
        for count in range(0, 3):
            pre_high_value = np.nan
            pre_low_value = np.nan
            pre_is_high = False
            pre_high_index = np.nan
            pre_is_low = False
            pre_low_index = np.nan
            for p_index in range(0, len(high_point_list)):
                high_value = high_point_list[p_index]
                low_value = low_point_list[p_index]
                if low_value == 2.356:
                    print('low_value-->', low_value)
                else:
                    pass
                if math.isnan(high_value) == False and math.isnan(low_value) == False:
                    if pre_is_high:
                        if high_value > pre_high_value and low_value > pre_low_value:
                            high_point_list[pre_high_index] = np.nan
                        elif high_value < pre_high_value and low_value > pre_low_value:
                            high_point_list[p_index] = np.nan
                        elif high_value > pre_high_value and low_value < pre_low_value:
                            high_point_list[p_index] = np.nan
                        elif high_value < pre_high_value and low_value < pre_low_value:
                            high_point_list[p_index] = np.nan
                    if pre_is_low:
                        if high_value > pre_high_value and low_value > pre_low_value:
                            low_point_list[p_index] = np.nan
                        elif high_value < pre_high_value and low_value > pre_low_value:
                            low_point_list[p_index] = np.nan
                        elif high_value > pre_high_value and low_value < pre_low_value:
                            low_point_list[p_index] = np.nan
                        elif high_value < pre_high_value and low_value < pre_low_value:
                            low_point_list[pre_low_index] = np.nan
                elif math.isnan(high_value) == False:
                    if pre_is_high:
                        if pre_high_value > high_value:
                            high_point_list[p_index] = np.nan
                        else:
                            high_point_list[pre_high_index] = np.nan
                            pre_high_value = high_value
                            pre_high_index = p_index
                    else:
                        pre_is_high = True
                        pre_is_low = False
                        pre_high_value = high_value
                        pre_high_index = p_index
                elif math.isnan(low_value) == False:
                    if pre_is_low:
                        if pre_low_value < low_value:
                            low_point_list[p_index] = np.nan
                        else:
                            low_point_list[pre_low_index] = np.nan
                            pre_low_value = low_value
                            pre_low_index = p_index
                    else:
                        pre_is_high = False
                        pre_is_low = True
                        pre_low_value = low_value
                        pre_low_index = p_index
                else:
                    pass
        high_point_list = high_point_list[:-deep]
        low_point_list = low_point_list[:-deep]
        return (high_point_list, low_point_list)

    def zigzag_line_point_list(self, high_point_list: list, low_point_list: list, date_nums: list):

        date_nums = date_nums.tolist()
        zigzag_point_list = []
        for p_index in range(0, len(high_point_list)):
            high_value = high_point_list[p_index]
            low_value = low_point_list[p_index]
            date_value = date_nums[p_index]
            if math.isnan(high_value) == False:
                zigzag_point_list.append((date_value, high_value))
            elif math.isnan(low_value) == False:
                zigzag_point_list.append((date_value, low_value))
            else:
                pass

        return zigzag_point_list

    def caculation_fvg_infos(self, data_frame: pd.DataFrame, break_down: bool = False):
        date_nums = data_frame['Date']
        open_nums = data_frame['Open']
        high_nums = data_frame['High']
        low_nums = data_frame['Low']
        close_nums = data_frame['Close']
        ohlc_infos = []
        min_price = 9999999999
        max_price = -9999999999

        sub_date_0 = date_nums[0]
        sub_date_0_str = self.getDateString(sub_date_0)
        if sub_date_0_str == '2022-12-29 04:55:00':
            print(sub_date_0_str)
        else:
            pass
        for c_index in range(0, len(date_nums)):
            ohlc_info = {
                'o': open_nums[c_index],
                'h': high_nums[c_index],
                'l': low_nums[c_index],
                'c': close_nums[c_index]
            }
            ohlc_infos.append(ohlc_info)
            l_price = ohlc_info['l']
            h_price = ohlc_info['h']
            if l_price < min_price:
                min_price = l_price
            else:
                pass
            if h_price > max_price:
                max_price = h_price
            else:
                pass

        fvg_list = []
        for c_index in range(1, len(ohlc_infos)-2):
            ohlc_info_0 = ohlc_infos[c_index - 1]
            o_price_0 = ohlc_info_0['o']
            h_price_0 = ohlc_info_0['h']
            l_price_0 = ohlc_info_0['l']
            c_price_0 = ohlc_info_0['c']
            sub_date_0 = date_nums[c_index - 1]
            body_0 = math.fabs(o_price_0 - c_price_0)

            ohlc_info_1 = ohlc_infos[c_index]
            o_price_1 = ohlc_info_1['o']
            c_price_1 = ohlc_info_1['c']
            sub_date_1 = date_nums[c_index]
            sub_date_1_str = self.getDateString(sub_date_1)
            # print('sub_date_1_str---->', sub_date_1_str)
            if sub_date_1_str == '2023-01-07 21:00:00':
                print(sub_date_1_str)
            else:
                pass

            body_1 = math.fabs(o_price_1 - c_price_1)
            if body_0 > 0.0:
                body_rate_10 = body_1 / body_0
            else:
                body_rate_10 = 100.0

            ohlc_info_2 = ohlc_infos[c_index + 1]
            o_price_2 = ohlc_info_2['o']
            h_price_2 = ohlc_info_2['h']
            l_price_2 = ohlc_info_2['l']
            c_price_2 = ohlc_info_2['c']
            body_2 = math.fabs(o_price_2 - c_price_2)

            if body_2 > 0.0:
                body_rate_12 = body_1 / body_2
            else:
                body_rate_12 = 100.0

            if o_price_0 > c_price_0 and o_price_1 > c_price_1 and o_price_2 > c_price_2 and l_price_0 > h_price_2 and break_down == True:
                # 向下突破的阴线
                fvg_list.append({
                    'index': c_index,
                    'start_ts': sub_date_0,
                    'high': l_price_0,
                    'low': h_price_2,
                    'type': 'supply'
                })
            elif o_price_0 < c_price_0 and o_price_1 < c_price_1 and o_price_2 < c_price_2 and h_price_0 < l_price_2 and break_down == False:
                # 向上突破的阳线
                fvg_list.append({
                    'index': c_index,
                    'start_ts': sub_date_0,
                    'high': l_price_2,
                    'low': h_price_0,
                    'type': 'demand'
                })
            elif body_rate_10 > 1.5 and body_rate_12 > 1.5 and o_price_1 > c_price_1 and l_price_0 > h_price_2 and break_down == True:
                # 大阴线形成的缺口
                fvg_list.append({
                    'index': c_index,
                    'start_ts': sub_date_0,
                    'high': l_price_0,
                    'low': h_price_2,
                    'type': 'supply'
                })
            elif body_rate_10 > 1.5 and body_rate_12 > 1.5 and o_price_1 < c_price_1 and h_price_0 < l_price_2 and break_down == False:
                # 大阳线形成的缺口
                fvg_list.append({
                    'index': c_index,
                    'start_ts': sub_date_0,
                    'high': l_price_2,
                    'low': h_price_0,
                    'type': 'demand'
                })
            else:
                pass
        return fvg_list

    def caculation_order_block_infos(self, data_frame: pd.DataFrame, pre_price_2_time: pd.Timestamp, pre_price_3_time: pd.Timestamp, break_price: float, break_down: bool):
        sub_data_frame = data_frame.loc[pre_price_2_time:pre_price_3_time]
        sub_date_nums = sub_data_frame['Date']
        sub_open_nums = sub_data_frame['Open']
        sub_high_nums = sub_data_frame['High']
        sub_low_nums = sub_data_frame['Low']
        sub_close_nums = sub_data_frame['Close']

        ohlc_infos = []
        min_price = 9999999999
        max_price = -9999999999
        sub_date_0 = sub_date_nums[0]
        sub_date_0_str = self.getDateString(sub_date_0)
        if sub_date_0_str == '2022-12-29 04:55:00':
            print(sub_date_0_str)
        else:
            pass
        for c_index in range(0, len(sub_date_nums)):
            ohlc_info = {
                'o': sub_open_nums[c_index],
                'h': sub_high_nums[c_index],
                'l': sub_low_nums[c_index],
                'c': sub_close_nums[c_index]
            }
            ohlc_infos.append(ohlc_info)
            l_price = ohlc_info['l']
            h_price = ohlc_info['h']
            if l_price < min_price:
                min_price = l_price
            else:
                pass
            if h_price > max_price:
                max_price = h_price
            else:
                pass

        # 找到第一根突破的K线
        latest_break_index = -1
        for c_index in range(0, len(ohlc_infos)):
            ohlc_info_0 = ohlc_infos[c_index]
            h_price_0 = ohlc_info_0['h']
            l_price_0 = ohlc_info_0['l']
            o_price_0 = ohlc_info_0['o']
            c_price_0 = ohlc_info_0['c']
            if break_down:
                if h_price_0 > break_price and l_price_0 < break_price and c_price_0 < o_price_0: # 第一根向下突破的阴线
                    latest_break_index = c_index
                    break
                else:
                    pass
            else:
                if h_price_0 > break_price and l_price_0 < break_price and c_price_0 > o_price_0:  # 第一根向上突破的阳线
                    latest_break_index = c_index
                    break
                else:
                    pass
        if latest_break_index == -1:
            latest_break_index = len(ohlc_infos) - 2
        else:
            pass
        # 找到最后一跟反向K线
        latest_reverse_index = 0
        for c_index in range(0, len(ohlc_infos)):
            ohlc_info_0 = ohlc_infos[c_index]
            o_price_0 = ohlc_info_0['o']
            c_price_0 = ohlc_info_0['c']

            if break_down:
                # 向下突破
                if c_price_0 > o_price_0: # 阳线
                    latest_reverse_index = c_index
                else:
                    pass
            else:
                # 向上突破
                if c_price_0 < o_price_0:  # 阴线
                    latest_reverse_index = c_index
                else:
                    pass
            if c_index >= latest_break_index:
                break
            else:
                pass

        # 合并连续的反向K线
        first_reverse_index = latest_reverse_index
        while first_reverse_index > 0:
            first_reverse_index = first_reverse_index - 1
            ohlc_info_0 = ohlc_infos[first_reverse_index]
            o_price_0 = ohlc_info_0['o']
            c_price_0 = ohlc_info_0['c']

            if break_down:
                # 向下突破
                if c_price_0 > o_price_0:  # 阳线
                    pass
                else:
                    first_reverse_index = first_reverse_index + 1
                    break
            else:
                # 向上突破
                if c_price_0 < o_price_0:  # 阴线
                    pass
                else:
                    first_reverse_index = first_reverse_index + 1
                    break

        ohlc_info_0 = ohlc_infos[first_reverse_index]
        h_price_0 = ohlc_info_0['h']
        l_price_0 = ohlc_info_0['l']

        sub_date_0 = sub_date_nums[first_reverse_index]
        ohlc_info_1 = ohlc_infos[latest_reverse_index]
        h_price_1 = ohlc_info_1['h']
        l_price_1 = ohlc_info_1['l']

        if break_down:
            ob_info = {
                'index': first_reverse_index,
                'high': max(h_price_0, h_price_1),
                'low': min(l_price_0, l_price_1),
                'start_ts': sub_date_0,
                'min_end_ts': sub_date_nums[-1],
                'end_ts': None,
                'vaild': True,
                'type': 'supply'
            }
        else:
            ob_info = {
                'index': first_reverse_index,
                'high': max(h_price_0, h_price_1),
                'low': min(l_price_0, l_price_1),
                'start_ts': sub_date_0,
                'min_end_ts': sub_date_nums[-1],
                'end_ts': None,
                'vaild': True,
                'type': 'demand'
            }

        return ob_info

    def find_fair_value_gap_and_order_block_infos(self, zigzag_point_list: list, data_frame: pd.DataFrame, data_count: int):
        pre_price_1 = 0.0
        pre_price_2 = 0.0
        pre_price_3 = 0.0
        pre_price_1_time = 0
        pre_price_2_time = 0
        pre_price_3_time = 0
        pre_price_1_index = 0
        pre_price_2_index = 0
        pre_price_3_index = 0
        final_fvg_list = []
        order_block_infos = []
        for p_index in range(0, len(zigzag_point_list)):
            (date_ts, price_value) = zigzag_point_list[p_index]
            if math.isnan(price_value) == False:
                if pre_price_1 == 0.0:
                    pre_price_1 = price_value
                    pre_price_1_index = p_index
                    pre_price_1_time = date_ts
                elif pre_price_2 == 0.0:
                    pre_price_2 = price_value
                    pre_price_2_index = p_index
                    pre_price_2_time = date_ts
                elif pre_price_3 == 0.0:
                    pre_price_3 = price_value
                    pre_price_3_index = p_index
                    pre_price_3_time = date_ts
                else:
                    pass
                if p_index == len(zigzag_point_list)-3:
                    print(pre_price_2_time, pre_price_3_time)
                else:
                    pass

                if pre_price_1 != 0.0 and pre_price_2 != 0.0 and pre_price_3 != 0.0:
                    ob_info = None
                    fvg_list = []
                    if (pre_price_1 < pre_price_2 and pre_price_1 > pre_price_3):
                        # 向下突破
                        fvg_list = self.caculation_fvg_infos(data_frame.loc[pre_price_2_time:pre_price_3_time], break_down=True)
                        ob_info = self.caculation_order_block_infos(data_frame, pre_price_2_time, pre_price_3_time,
                                                               pre_price_1, True)
                    elif (pre_price_1 > pre_price_2 and pre_price_1 < pre_price_3):
                        # 向上突破
                        fvg_list = self.caculation_fvg_infos(data_frame.loc[pre_price_2_time:pre_price_3_time], break_down=False)
                        ob_info = self.caculation_order_block_infos(data_frame, pre_price_2_time, pre_price_3_time,
                                                               pre_price_1, False)
                    else:
                        pass
                    pre_price_1 = pre_price_2
                    pre_price_2 = pre_price_3
                    pre_price_3 = price_value
                    pre_price_1_time = pre_price_2_time
                    pre_price_2_time = pre_price_3_time
                    pre_price_3_time = date_ts
                    pre_price_1_index = pre_price_2_index
                    pre_price_2_index = pre_price_3_index
                    pre_price_3_index = p_index
                    if p_index == len(zigzag_point_list) - 1:
                        if (pre_price_1 < pre_price_2 and pre_price_1 > pre_price_3):
                            # 向下突破
                            fvg_list = self.caculation_fvg_infos(data_frame.loc[pre_price_2_time:pre_price_3_time], break_down=True)
                            ob_info = self.caculation_order_block_infos(data_frame, pre_price_2_time, pre_price_3_time,
                                                                   pre_price_1, True)
                        elif (pre_price_1 > pre_price_2 and pre_price_1 < pre_price_3):
                            # 向上突破
                            fvg_list = self.caculation_fvg_infos(data_frame.loc[pre_price_2_time:pre_price_3_time], break_down=False)
                            ob_info = self.caculation_order_block_infos(data_frame, pre_price_2_time, pre_price_3_time,
                                                                   pre_price_1, False)
                        else:
                            pass
                    else:
                        pass
                    if len(fvg_list) > 0:
                        final_fvg_list.extend(fvg_list)
                    else:
                        pass
                    if ob_info is not None:
                        order_block_infos.append(ob_info)
                    else:
                        pass
                else:
                    pass
            else:
                pass

        date_nums = data_frame['Date']
        open_nums = data_frame['Open']
        high_nums = data_frame['High']
        low_nums = data_frame['Low']
        close_nums = data_frame['Close']

        fill_between_list = []
        # 计算fvg的有效性
        for f_index in range(0, len(final_fvg_list)):
            fvg_info = final_fvg_list[f_index]
            start_ts = fvg_info['start_ts']
            high = fvg_info['high']
            low = fvg_info['low']
            type = fvg_info['type']

            start_index = -1
            end_index = -1
            end_ts = None
            where_values_1 = (data_frame['Date'] >= start_ts).values
            for w_index in range(0, len(date_nums) - 3):
                here = where_values_1[w_index]
                if here and start_index == -1:
                    start_index = w_index
                else:
                    pass
                if start_index != -1:
                    c_high = high_nums[w_index]
                    c_low = low_nums[w_index]
                    if type == 'supply':
                        if c_high > low and c_low < low and w_index > (start_index + 2):
                            # 进入供应区
                            end_index = w_index
                            end_ts = date_nums[end_index]
                            break
                        else:
                            pass
                    else:
                        if c_high > high and c_low < high and w_index > (start_index + 2):
                            # 进入需求区
                            end_index = w_index
                            end_ts = date_nums[end_index]
                            break
                        else:
                            pass

                else:
                    pass
            if type == 'supply':
                color = 'y'
            else:
                color = 'y'
            if end_ts is None:
                end_ts = date_nums[-1]
                where_values_2 = where_values_1
            else:
                where_values_2 = (data_frame['Date'] <= end_ts).values
            fvg_info['end_ts'] = end_ts
            where_values = []
            for w_index in range(0, len(where_values_2)):
                where_1 = where_values_1[w_index]
                where_2 = where_values_2[w_index]
                if where_1 and where_2:
                    where_values.append(True)
                else:
                    where_values.append(False)
            where_values = where_values[data_count:]
            fvg_info['valid'] = where_values[-1]
            fill_between = dict(y1=low, y2=high,
                                where=where_values, alpha=0.15,
                                color=color)
            fill_between_list.append(fill_between)

        # 计算order_block的有效性
        for o_index in range(0, len(order_block_infos)):
            ob_info = order_block_infos[o_index]
            start_ts = ob_info['start_ts']
            high = ob_info['high']
            low = ob_info['low']
            type = ob_info['type']
            min_end_ts = ob_info['min_end_ts']

            start_index = -1
            end_index = -1
            end_ts = None
            where_values_1 = (data_frame['Date'] >= start_ts).values
            for w_index in range(0, len(date_nums) - 3):
                cur_ts = date_nums[w_index]
                here = where_values_1[w_index]
                if here and start_index == -1:
                    start_index = w_index
                else:
                    pass
                if start_index != -1 and cur_ts > min_end_ts:
                    c_high = high_nums[w_index]
                    c_low = low_nums[w_index]
                    if type == 'supply':
                        if c_high > low and c_low < low and w_index > (start_index + 2):
                            # 进入供应区
                            end_index = w_index
                            end_ts = date_nums[end_index]
                            break
                        else:
                            pass
                    else:
                        if c_high > high and c_low < high and w_index > (start_index + 2):
                            # 进入需求区
                            end_index = w_index
                            end_ts = date_nums[end_index]
                            break
                        else:
                            pass

                else:
                    pass

            if type == 'supply':
                color = 'r'
            else:
                color = 'g'
            if end_ts is None:
                end_ts = date_nums[-1]
                where_values_2 = where_values_1
            else:
                where_values_2 = (data_frame['Date'] <= end_ts).values
            ob_info['end_ts'] = end_ts
            where_values = []
            for w_index in range(0, len(where_values_2)):
                where_1 = where_values_1[w_index]
                where_2 = where_values_2[w_index]
                if where_1 and where_2:
                    where_values.append(True)
                else:
                    where_values.append(False)
            where_values = where_values[data_count:]
            ob_info['valid'] = where_values[-1]
            fill_between = dict(y1=low, y2=high,
                                where=where_values, alpha=0.15,
                                color=color)
            fill_between_list.append(fill_between)

        return (fill_between_list, final_fvg_list, order_block_infos)

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
                linecolor = overrides['linecolor']
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
        date_nums = data_frame['Date']
        if len(date_nums) < 170:
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

        data_count = -(len(date_nums) - 5)
        deep = self.signal_params['deep']['value']
        deep = int(deep)
        # 计算波段高低点
        (high_point_list, low_point_list) = self.find_high_low_point_list(data_frame=data_frame, deep=deep)
        high_point_list = high_point_list[data_count:]
        low_point_list = low_point_list[data_count:]
        real_date_nums = date_nums[data_count:]
        zigzag_point_list1 = self.zigzag_line_point_list(high_point_list=high_point_list, low_point_list=low_point_list,
                                                        date_nums=real_date_nums)

        (fill_between_list, final_fvg_list, order_block_infos) = self.find_fair_value_gap_and_order_block_infos(zigzag_point_list=zigzag_point_list1,
                                                                   data_frame=data_frame, data_count=data_count)

        open_nums = data_frame['Open']
        close_nums = data_frame['Close']
        high_nums = data_frame['High']
        low_nums = data_frame['Low']

        latest_open = open_nums[-2]
        latest_close = close_nums[-2]
        latest_high = high_nums[-2]
        latest_low = low_nums[-2]
        final_fvg_list.pop()# 删除最后一个fvg防止频繁无效提醒
        for fvg_info in final_fvg_list:
            valid = fvg_info['valid']
            high = fvg_info['high']
            low = fvg_info['low']
            type = fvg_info['type']
            if valid:
                # if type == 'supply':
                #     print(
                #         f'check_signal_for_fvg_info-->{symbol} {interval} {latest_high}-{low}-{latest_low} {high} {type}')
                # else:
                #     print(
                #         f'check_signal_for_fvg_info-->{symbol} {interval} {latest_high}-{high}-{latest_low} {low} {type}')
                pass
            else:
                pass
            if type == 'supply' and latest_high > low and latest_low < low and valid:
                return {
                    'appear': True,
                    'type': 'sell',
                    'enter_price': 0.0,
                    'profit_price': 0.0,
                    'stop_price': 0.0,
                    'win_percentage': 0.0,
                    'detail_msg': f'ict_smc_signal 价格进入{interval}供应区FVG'
                }
            elif type == 'demand' and latest_high > high and latest_low < high and valid:
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

        order_block_infos.pop() # 删除最后一个订单块,防止频繁提示
        for ob_info in order_block_infos:
            valid = ob_info['valid']
            high = ob_info['high']
            low = ob_info['low']
            type = ob_info['type']
            if valid:
                # if type == 'supply':
                #     print(
                #         f'check_signal_for_fvg_info-->{symbol} {interval} {latest_high}-{low}-{latest_low} {high} {type}')
                # else:
                #     print(
                #         f'check_signal_for_fvg_info-->{symbol} {interval} {latest_high}-{high}-{latest_low} {low} {type}')
                pass
            else:
                pass
            if type == 'supply' and latest_high > low and latest_low < low and valid:
                return {
                    'appear': True,
                    'type': 'sell',
                    'enter_price': 0.0,
                    'profit_price': 0.0,
                    'stop_price': 0.0,
                    'win_percentage': 0.0,
                    'detail_msg': f'ict_smc_signal 价格进入{interval}供应区order_block'
                }
            elif type == 'demand' and latest_high > high and latest_low < high and valid:
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
        date_nums = data_frame['Date']
        data_count = 5 - len(date_nums)
        deep = self.signal_params['deep']['value']
        deep = int(deep)
        # 计算波段高低点
        (high_point_list, low_point_list) = self.find_high_low_point_list(data_frame=data_frame, deep=deep)
        high_point_list = high_point_list[data_count:]
        low_point_list = low_point_list[data_count:]
        real_date_nums = date_nums[data_count:]
        zigzag_point_list1 = self.zigzag_line_point_list(high_point_list=high_point_list,
                                                         low_point_list=low_point_list,
                                                         date_nums=real_date_nums)
        # print('zigzag_point_list-->', zigzag_point_list1)
        # 计算公允价值缺口
        (fill_betweens, fvg_info_list, order_block_infos) = self.find_fair_value_gap_and_order_block_infos(
            zigzag_point_list=zigzag_point_list1, data_frame=data_frame,
            data_count=data_count)

        yellow_color = '#FFB90F'
        red_color = '#FF3030'
        green_color = '#00FA9A'
        rectangle_info_list = []
        for f_index in range(0, len(fvg_info_list)):
            fvg_info = fvg_info_list[f_index]
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

        for f_index in range(0, len(order_block_infos)):
            ob_info = order_block_infos[f_index]
            start_ts: pd.Timestamp = ob_info['start_ts']
            end_ts: pd.Timestamp = ob_info['end_ts']
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

        zigzag_point_list = []
        for p_index in range(0, len(zigzag_point_list1)):
            (p_ts, p_price) = zigzag_point_list1[p_index]
            p_price = float(p_price)
            if for_tv:
                p_ts = int(pd.to_datetime(p_ts).value / 10 ** 9)
            else:
                pass
            zigzag_point_list.append({'time': p_ts, 'price': p_price})
        zigzag_point_list.append(zigzag_point_list[-1])
        zigzag_line_info = {
            'shape_name': 'zigzag_line',
            'shape_type': 'multi_point_shape',
            'points': zigzag_point_list,
            'options': {
                'shape': 'path',
                'lock': True,
                'disableSelection': True,
                'disableSave': True,
                'disableUndo': True,
                'overrides': {
                    'linecolor': '#0000FF',
                    'linewidth': 2,
                    'transparency': 80
                }
            }
        }
        shape_infos = [zigzag_line_info]
        shape_infos.extend(rectangle_info_list)

        return shape_infos

    def shapes_on_tv_chart(self, symbol: str, interval: str, klines: list):
        return self.shapes_on_chart(symbol=symbol, interval=interval, klines=klines, for_tv=True)

