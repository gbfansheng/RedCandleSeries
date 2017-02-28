# -*- coding: utf-8 -*-

import utils
import datetime


def begin_date():
    return datetime.date(2016, 1, 1);

def is_little_red_candle(df):
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

def filterCandle():
    today_df = utils.get_today()
    code_list = list(today_df['code'])
    end_date = datetime.datetime.now().date()
    for code in code_list:
        print (code)
        code_df = utils.read_code(code)
        for i in range((end_date - begin_date()).days + 1):
            mark_date = begin_date() + datetime.timedelta(days=i)
            df_data = code_df[code_df['date'].isin([mark_date])]
            if is_little_red_candle(df_data) :
                mark_date_1 = begin_date() + datetime.timedelta(days=i + 1)
                