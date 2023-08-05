from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from hbshare.quant.CChen.cta_factor.factor_func import factor_compute
from hbshare.quant.CChen.stk import trade_calendar
from hbshare.quant.CChen.cta_factor.const import stock_data_indicator
from hbshare.quant.CChen.cta_factor.factor_algo import (
    tscarry, carry, tsmom, tsrev, xsmom, xsrev, tswr, xswr, mr, mrchg, tsmr,
    tsbasismom, xsbasismom, tspoichg, xspoichg, xssigma,
    xsmr, xstsmr, xsmrchg, tspvolchg, xspvolchg, tsskew, xsskew,
    tsstock, xsstock
)


def run(sql_path, sql_info):
    start_date = datetime(2010, 1, 1).date()
    # end_date = datetime(2021, 4, 9).date()
    end_date = datetime.now().date()

    window_days_list = [1, 2, 3, 5, 10, 20, 30, 40, 50, 60, 90, 100, 150, 200, 250]
    liq_d = 20

    table = 'hsjy_fut_com_index'
    table_wr = 'hsjy_fut_wr'
    table_mr = 'hsjy_fut_memberrank'
    table_contracts_info = 'hsjy_fut_info_c'
    table_p_info = 'hsjy_fut_info_p'
    table_raw = 'hsjy_fut_com'

    data = pd.read_sql_query(
        'select * from ' + table + ' where TDATE<='
        + end_date.strftime('%Y%m%d')
        + ' and TDATE>=' + (start_date - timedelta(days=500)).strftime('%Y%m%d')
        + ' order by TDATE',
        sql_path
    )
    data_wr0 = pd.read_sql_query(
        'select TDATE, EXCHANGE, PCODE, PNAME, WRQCURRENT from ' + table_wr + ' where TDATE<='
        + end_date.strftime('%Y%m%d')
        + ' and TDATE>=' + (start_date - timedelta(days=500)).strftime('%Y%m%d')
        + ' and FREQ=5 order by TDATE, EXCHANGE, PCODE',
        sql_path
    ).drop_duplicates(subset=['TDATE', 'EXCHANGE', 'PCODE']).reset_index(drop=True)
    calendar = data[['TDATE']].sort_values(by='TDATE').drop_duplicates().reset_index(drop=True)
    data_wr = pd.DataFrame()
    for e in data['EXCHANGE'].drop_duplicates().tolist():
        PCODEs = data[data['EXCHANGE'] == e]['PCODE'].drop_duplicates().tolist()
        for p in PCODEs:
            data_wr_p = data_wr0[np.array(data_wr0['EXCHANGE'] == e) & np.array(data_wr0['PCODE'] == p)]
            data_wr_p = pd.merge(calendar, data_wr_p, on='TDATE', how='left').fillna(method='ffill')
            data_wr_p = data_wr_p[data_wr_p['WRQCURRENT'] >= 0].reset_index(drop=True)
            data_wr = pd.concat([data_wr, data_wr_p])
    data_wr = data_wr.reset_index(drop=True)

    data_mr = pd.read_sql_query(
        'select TDATE, CCODE, INDICATORCODE as SIDE, sum(INDICATORVOL) as MR, sum(INDICATORCHG) as MRCHG from ' + table_mr
        + ' where TDATE<=' + end_date.strftime('%Y%m%d')
        + ' and TDATE>=' + (start_date - timedelta(days=500)).strftime('%Y%m%d')
        + ' and INDICATORCODE in (3, 4) GROUP BY INDICATORCODE, TDATE, CCODE order by TDATE, CCODE, INDICATORCODE',
        sql_path
    )
    data_info = pd.read_sql_query(
        'select * from ' + table_contracts_info, sql_path
    )
    data_mr = pd.merge(data_mr, data_info[['CCODE', 'EXCHANGE', 'PCODE']], on='CCODE', how='left')
    data_mr = data_mr.groupby(by=['TDATE', 'SIDE', 'EXCHANGE', 'PCODE']).sum().reset_index()
    data_mr['SIDE'] = data_mr['SIDE'].apply(lambda x: 1 if x == 3 else (-1 if x == 4 else 0))
    data_mr['MR'] = data_mr['MR'] * data_mr['SIDE']
    data_mr['MRCHG'] = data_mr['MRCHG'] * data_mr['SIDE']

    data_contracts = pd.read_sql_query(
        'select * from ' + table_raw + ' where CCODE in ' + str(tuple(np.unique(data[['CCODE', 'CCODE2']].dropna())))
        + ' order by CCODE, TDATE',
        sql_path
    )

    # 库存数据
    stock_table = 'wind_edb'
    stock_data_code = []
    for i in stock_data_indicator:
        stock_data_code += stock_data_indicator[i]


    stock_data_raw = pd.read_sql_query(
        'select * from ' + stock_table + ' where code in ' + str(tuple(stock_data_code)).replace(',)', ')'),
        sql_path
    ).pivot(index='t_date', columns='code', values='close').ffill()
    stock_data_info = pd.read_csv('E:\\codes\\hbshare\\hbshare\\quant\\CChen\\data\\wind_edb.csv')
    for i in stock_data_raw.columns:
        stock_data_raw.loc[:, i] = (
                stock_data_raw.loc[:, i] * stock_data_info[stock_data_info['指标ID'] == i]['乘数'].tolist()[0]
        )
    tdate_list = trade_calendar(
        start_date=stock_data_raw.index[0],
        end_date=stock_data_raw.index[len(stock_data_raw) - 1]
    )

    stock_data = pd.DataFrame(
        {
            't_date': tdate_list
        }, index=range(len(tdate_list))
    ).merge(stock_data_raw, on='t_date', how='left')

    hsjy_p_info = pd.read_sql_query(
        'select * from ' + table_p_info, sql_path
    )

    data_stock = pd.DataFrame()
    for i in stock_data_indicator:
        data_p = stock_data[stock_data_indicator[i][0]].fillna(0)
        if len(stock_data_indicator[i]) > 1:
            for c in range(1, len(stock_data_indicator[i])):
                data_p += stock_data[stock_data_indicator[i][c]].fillna(0)
        p_info = hsjy_p_info[hsjy_p_info['CODE'] == i]
        data_p = pd.DataFrame(
            {
                'TDATE': tdate_list,
                'WRQCURRENT': data_p
            }
        )
        data_p['EXCHANGE'] = p_info['EXCHANGE'].tolist()[0]
        data_p['PCODE'] = p_info['PCODE'].tolist()[0]
        data_p['PNAME'] = p_info['PNAME'].tolist()[0]
        data_stock = data_stock.append(data_p)

    factor_compute(
        window_days_list=[10, 20, 30, 50, 90, 150, 250],
        hedge_ratio_list=[50, 75],
        data=data,
        factor_func=xssigma,
        liq_days=liq_d,
        data_raw=data_contracts,
        sql_info=sql_info,
        to_sql_path=sql_path
    )

    factor_compute(
        window_days_list=window_days_list[:10],
        hedge_ratio_list=[50, 75],
        data=data,
        factor_func=xsbasismom,
        liq_days=liq_d,
        data_raw=data_contracts,
        sql_info=sql_info,
        to_sql_path=sql_path
    )

    factor_compute(
        window_days_list=window_days_list[:10],
        data=data,
        factor_func=tsbasismom,
        liq_days=liq_d,
        data_raw=data_contracts,
        sql_info=sql_info,
        to_sql_path=sql_path
    )

    factor_compute(
        window_days_list=[20, 50],
        hedge_ratio_list=[50, 60, 70, 80, 90],
        data=data, factor_func=carry,
        liq_days=liq_d,
        sql_info=sql_info,
        to_sql_path=sql_path
    )

    factor_compute(
        window_days_list=window_days_list,
        data=data,
        factor_func=tsmom,
        liq_days=liq_d,
        sql_info=sql_info,
        to_sql_path=sql_path
    )

    factor_compute(
        window_days_list=window_days_list,
        data=data,
        factor_func=tscarry,
        liq_days=liq_d,
        sql_info=sql_info,
        to_sql_path=sql_path
    )

    factor_compute(
        window_days_list=window_days_list[1:],
        data=data, factor_func=tsskew,
        liq_days=liq_d,
        sql_info=sql_info,
        to_sql_path=sql_path
    )

    factor_compute(
        window_days_list=window_days_list,
        data=data,
        factor_func=tsrev,
        liq_days=liq_d,
        sql_info=sql_info,
        to_sql_path=sql_path
    )

    factor_compute(
        window_days_list=window_days_list,
        hedge_ratio_list=[50, 75],
        data=data,
        factor_func=xsmom,
        liq_days=liq_d,
        sql_info=sql_info,
        to_sql_path=sql_path
    )

    factor_compute(
        window_days_list=window_days_list[1:],
        hedge_ratio_list=[50, 75],
        data=data,
        factor_func=xsskew,
        liq_days=liq_d,
        sql_info=sql_info,
        to_sql_path=sql_path
    )

    factor_compute(
        window_days_list=window_days_list,
        hedge_ratio_list=[50, 75],
        data=data,
        factor_func=xsrev,
        liq_days=liq_d,
        sql_info=sql_info,
        to_sql_path=sql_path
    )

    factor_compute(
        window_days_list=window_days_list,
        data=data,
        factor_func=tspoichg,
        liq_days=liq_d,
        sql_info=sql_info,
        to_sql_path=sql_path
    )

    factor_compute(
        window_days_list=window_days_list,
        data=data,
        factor_func=tspvolchg,
        liq_days=liq_d,
        sql_info=sql_info,
        to_sql_path=sql_path
    )

    factor_compute(
        window_days_list=window_days_list,
        hedge_ratio_list=[50, 75],
        data=data,
        factor_func=xspoichg,
        liq_days=liq_d,
        sql_info=sql_info,
        to_sql_path=sql_path
    )

    factor_compute(
        window_days_list=window_days_list,
        hedge_ratio_list=[50, 75],
        data=data,
        factor_func=xspvolchg,
        liq_days=liq_d,
        sql_info=sql_info,
        to_sql_path=sql_path
    )

    factor_compute(
        window_days_list=window_days_list,
        hedge_ratio_list=[50, 75],
        data=data,
        data_wr=data_wr,
        factor_func=xswr,
        liq_days=liq_d,
        price_field='OPEN',
        sql_info=sql_info,
        to_sql_path=sql_path
    )

    factor_compute(
        window_days_list=window_days_list,
        data=data,
        data_wr=data_wr,
        factor_func=tswr,
        liq_days=liq_d,
        price_field='OPEN',
        sql_info=sql_info,
        to_sql_path=sql_path
    )

    factor_compute(
        window_days_list=window_days_list,
        hedge_ratio_list=[50, 75],
        data=data,
        data_wr=data_stock,
        factor_func=xsstock,
        liq_days=liq_d,
        price_field='OPEN',
        sql_info=sql_info,
        to_sql_path=sql_path,
    )

    factor_compute(
        window_days_list=window_days_list,
        data=data,
        data_wr=data_stock,
        factor_func=tsstock,
        liq_days=liq_d,
        price_field='OPEN',
        sql_info=sql_info,
        to_sql_path=sql_path,
    )

    factor_compute(
        window_days_list=window_days_list,
        data=data,
        data_mr=data_mr,
        factor_func=mr,
        liq_days=liq_d,
        price_field='OPEN',
        sql_info=sql_info, to_sql_path=sql_path
    )

    factor_compute(
        window_days_list=window_days_list,
        hedge_ratio_list=[50, 75],
        data=data,
        data_mr=data_mr,
        factor_func=xsmr,
        liq_days=liq_d,
        price_field='OPEN',
        sql_info=sql_info, to_sql_path=sql_path
    )

    factor_compute(
        window_days_list=window_days_list,
        data=data,
        data_mr=data_mr,
        factor_func=mrchg,
        liq_days=liq_d,
        price_field='OPEN',
        sql_info=sql_info, to_sql_path=sql_path
    )

    factor_compute(
        window_days_list=window_days_list,
        hedge_ratio_list=[50, 75],
        data=data,
        data_mr=data_mr,
        factor_func=xsmrchg,
        liq_days=liq_d,
        price_field='OPEN',
        sql_info=sql_info, to_sql_path=sql_path
    )

    factor_compute(
        window_days_list=window_days_list,
        data=data,
        data_mr=data_mr,
        factor_func=tsmr,
        liq_days=liq_d,
        price_field='OPEN',
        sql_info=sql_info, to_sql_path=sql_path
    )

    factor_compute(
        window_days_list=window_days_list,
        hedge_ratio_list=[50, 75],
        data=data,
        data_mr=data_mr,
        factor_func=xstsmr,
        liq_days=liq_d,
        price_field='OPEN',
        sql_info=sql_info, to_sql_path=sql_path
    )


