# -*- coding: utf-8 -*-

import utils
import datetime


def begin_date():
    return datetime.date(2016, 1, 4)


def is_little_red_candle(df):
    if df.empty:
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
    series_date = date
    for i in range(series_length):
        series_date = series_date + datetime.timedelta(days=1)
        series_date_string = series_date.strftime('%Y-%m-%d')
        df_data = code_df[code_df['date'].isin([series_date_string])]
        if df_data.empty:
            for nextday in range(15):
                series_date = series_date + datetime.timedelta(days=1)
                series_date_string = series_date.strftime('%Y-%m-%d')
                df_data = code_df[code_df['date'].isin([series_date_string])]
                if not df_data.empty:
                    break

        if df_data.empty:
            return False, series_date_string

        if i < (series_length - 1):
            if not is_little_red_candle(df_data):
                return False, series_date_string
        else:
            if is_little_red_candle(df_data):
                return True, series_date_string
            else:
                return False, series_date_string


def is_include_series(series_list, date_string):
    datet = datetime.datetime.strptime(date_string, '%Y-%m-%d')
    date = datet.date()
    for yester in range(21):
        yester_date = date - datetime.timedelta(days=yester)
        yester_date_string = yester_date.strftime('%Y-%m-%d')
        if yester_date_string in series_list:
            return True
    return False


def filter_candle():
    today_df = utils.get_today()
    code_list = list(today_df['code'])
    end_date = datetime.datetime.now().date()
    series_dict = {}
    for code in code_list:
        print (code)
        series_list = series_dict.get(code, [])
        code_df = utils.read(code)
        for i in range((end_date - begin_date()).days + 1):
            mark_date = begin_date() + datetime.timedelta(days=i)
            fit_series, series_date = is_series(code_df, mark_date)
            if fit_series and not is_include_series(series_list, series_date):
                series_list.append(series_date)
                series_dict[code] = series_list
    utils.save_dict(series_dict, 'series_dict')
    print series_dict



if __name__ == '__main__':
    filter_candle()