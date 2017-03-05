# -*- coding: utf-8 -*-

import utils
import datetime
import pandas as pd
import xlwt
import os


def caculate_revenue():
    series_dict = utils.get_dict('series_dict')
    revenue_days = 60
    revenue_dict = {}
    for key in series_dict:
        value_list = series_dict[key]
        code_df = utils.read(key)
        for date_string in value_list:
            print key
            print date_string
            series_date = (datetime.datetime.strptime(date_string, '%Y-%m-%d')).date()
            series_df = code_df[code_df['date'].isin([date_string])]
            series_close = float(series_df['close'])
            revenue_date = series_date

            for days in range(revenue_days):
                revenue_list = revenue_dict.get(str(days), [])
                revenue_date = revenue_date + datetime.timedelta(days=1)
                revenue_date_string = revenue_date.strftime('%Y-%m-%d')
                revenue_df = code_df[code_df['date'].isin([revenue_date_string])]

                if revenue_df.empty:
                    for nextday in range(10):
                        revenue_date = revenue_date + datetime.timedelta(days=1)
                        revenue_date_string = revenue_date.strftime('%Y-%m-%d')
                        revenue_df = code_df[code_df['date'].isin([revenue_date_string])]
                        if not revenue_df.empty:
                            break

                if revenue_df.empty:
                    continue

                revenue_close = float(revenue_df['close'])
                revenue = revenue_close / series_close
                revenue_list.append(revenue)
                revenue_dict[str(days)] = revenue_list
                # print days
                # print revenue_date
                # print revenue
    utils.save_dict(revenue_dict, 'revenue_dict')


def statistic():
    revenue_dict = utils.get_dict('revenue_dict')
    value_list = []
    key_list = []
    for key in revenue_dict:
        key_list.append(key)
        revenue_list = revenue_dict.get(key, [])
        avg_value = sum(revenue_list) / float(len(revenue_list))
        value_list.append(avg_value)

    df = pd.DataFrame({'days': key_list, 'revenue': value_list})
    utils.save(df, 'red_candle_revenue')


def save_series():
    workbook = xlwt.Workbook(encoding='utf-8')
    sheet = workbook.add_sheet("datelist", cell_overwrite_ok=True)
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = 'SimSun'  # 指定“宋体”
    style.font = font
    series_dict = utils.get_dict('series_dict')
    sheet.write(0, 0, '代码')
    sheet.write(0, 1, '日期')
    row = 0
    for keys in series_dict:
        row = row + 1
        date_list = series_dict.get(keys, [])
        sheet.write(row, 0, keys)
        for i in range(len(date_list)):
            sheet.write(row, i + 1, date_list[i])
    workbook.save(os.path.dirname(os.getcwd()) + '\\data\\xiaoyangxian.xls')


if __name__ == '__main__':
    # caculate_revenue()
    # statistic()
    save_series()