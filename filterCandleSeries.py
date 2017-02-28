# -*- coding: utf-8 -*-

import utils
import datetime


def begin_date():
    return datetime.date(2016, 1, 1);

def is_little_red_candle(df):
    if df.empty :
        return False
    p_change = float(df['p_change'])
    high = float(df['high'])
    low = float(df['low'])
    close = float(df['close'])
    base_price = close / (1 + p_change / 100)
    vibration = (high - low) / base_price
    if p_change >= 0.5 and p_change <= 3 and vibration <= 0.04:
        return True
    else:
        return False

def is_series(code_df, date):
    series_length = 3
    for i in range(series_length):
        series_date = date + datetime.timedelta(days=i)
        df_data = code_df[code_df['date'].isin([series_date])]
        if i < 2:
            if is_little_red_candle(df_data):
                continue
            else:
                return False, series_date
        else:
            if is_little_red_candle(df_data):
                return True, series_date
            else:
                return False, series_date


def filterCandle():
    today_df = utils.get_today()
    code_list = list(today_df['code'])
    end_date = datetime.datetime.now().date()
    series_dict = {}
    for code in code_list:
        print (code)
        code_df = utils.read_code(code)
        for i in range((end_date - begin_date()).days + 1):
            mark_date = begin_date() + datetime.timedelta(days=i)
            (is_series, series_date) = is_series(code_df, mark_date)
            if is_series:
                series_list = series_dict.get(code, [])
                series_list.append(series_date)
                series_dict[code] = series_list
    utils.save_dict(series_dict,'series_dict')
