import pandas as pd
from datetime import datetime, timedelta

# 读取 iChoice 数据
hs300 = pd.read_csv('/Users/fanshengxia/clawd/hs300_ichoice.csv')
bond10y = pd.read_csv('/Users/fanshengxia/clawd/bond10y_ichoice.csv')

# 处理日期格式
hs300['DATES'] = pd.to_datetime(hs300['DATES'])
hs300.set_index('DATES', inplace=True)
bond10y['DATES'] = pd.to_datetime(bond10y['DATES'])
bond10y.set_index('DATES', inplace=True)

print(f"沪深300数据: {len(hs300)} 条, 时间范围: {hs300.index.min()} 至 {hs300.index.max()}")
print(f"国债收益率数据: {len(bond10y)} 条, 时间范围: {bond10y.index.min()} 至 {bond10y.index.max()}")

# 两会时间数据 (2008-2025)
lianghui_dates = {
    2008: {"cppcc": "03-03", "npc": "03-05", "end": "03-18"},
    2009: {"cppcc": "03-03", "npc": "03-05", "end": "03-13"},
    2010: {"cppcc": "03-03", "npc": "03-05", "end": "03-14"},
    2011: {"cppcc": "03-03", "npc": "03-05", "end": "03-14"},
    2012: {"cppcc": "03-03", "npc": "03-05", "end": "03-14"},
    2013: {"cppcc": "03-03", "npc": "03-05", "end": "03-17"},
    2014: {"cppcc": "03-03", "npc": "03-05", "end": "03-13"},
    2015: {"cppcc": "03-03", "npc": "03-05", "end": "03-15"},
    2016: {"cppcc": "03-03", "npc": "03-05", "end": "03-16"},
    2017: {"cppcc": "03-03", "npc": "03-05", "end": "03-15"},
    2018: {"cppcc": "03-03", "npc": "03-05", "end": "03-20"},
    2019: {"cppcc": "03-03", "npc": "03-05", "end": "03-15"},
    2020: {"cppcc": "05-21", "npc": "05-22", "end": "05-28"},
    2021: {"cppcc": "03-04", "npc": "03-05", "end": "03-11"},
    2022: {"cppcc": "03-04", "npc": "03-05", "end": "03-11"},
    2023: {"cppcc": "03-04", "npc": "03-05", "end": "03-13"},
    2024: {"cppcc": "03-04", "npc": "03-05", "end": "03-11"},
    2025: {"cppcc": "03-04", "npc": "03-05", "end": "03-11"},
}

def get_closest_price(df, target_date, direction='backward'):
    """获取最接近目标日期的价格"""
    if target_date in df.index:
        return df.loc[target_date].iloc[0]
    
    if direction == 'backward':
        # 向前查找
        mask = df.index < target_date
        if mask.any():
            return df[mask].iloc[-1].iloc[0]
    else:
        # 向后查找
        mask = df.index > target_date
        if mask.any():
            return df[mask].iloc[0].iloc[0]
    return None

def analyze_year(year, dates, hs300_df, bond_df):
    """分析单年两会表现"""
    try:
        year_str = str(year)
        cppcc_start = pd.Timestamp(f"{year_str}-{dates['cppcc']}")
        npc_start = pd.Timestamp(f"{year_str}-{dates['npc']}")
        lh_end = pd.Timestamp(f"{year_str}-{dates['end']}")
        
        # 计算各时间点
        month_before = cppcc_start - pd.Timedelta(days=30)
        week_before = cppcc_start - pd.Timedelta(days=7)
        week_after = lh_end + pd.Timedelta(days=7)
        month_after = lh_end + pd.Timedelta(days=30)
        
        # 获取沪深300价格
        p_hs300_month_before = get_closest_price(hs300_df, month_before)
        p_hs300_week_before = get_closest_price(hs300_df, week_before)
        p_hs300_cppcc = get_closest_price(hs300_df, cppcc_start)
        p_hs300_end = get_closest_price(hs300_df, lh_end)
        p_hs300_week_after = get_closest_price(hs300_df, week_after)
        p_hs300_month_after = get_closest_price(hs300_df, month_after)
        
        # 获取国债收益率
        p_bond_month_before = get_closest_price(bond_df, month_before)
        p_bond_week_before = get_closest_price(bond_df, week_before)
        p_bond_cppcc = get_closest_price(bond_df, cppcc_start)
        p_bond_end = get_closest_price(bond_df, lh_end)
        p_bond_week_after = get_closest_price(bond_df, week_after)
        p_bond_month_after = get_closest_price(bond_df, month_after)
        
        result = {'年份': year}
        
        # 沪深300涨跌幅
        if all([p_hs300_month_before, p_hs300_cppcc]):
            result['沪深300_前1月'] = round((p_hs300_cppcc - p_hs300_month_before) / p_hs300_month_before * 100, 2)
        if all([p_hs300_week_before, p_hs300_cppcc]):
            result['沪深300_前1周'] = round((p_hs300_cppcc - p_hs300_week_before) / p_hs300_week_before * 100, 2)
        if all([p_hs300_cppcc, p_hs300_end]):
            result['沪深300_两会期间'] = round((p_hs300_end - p_hs300_cppcc) / p_hs300_cppcc * 100, 2)
        if all([p_hs300_end, p_hs300_week_after]):
            result['沪深300_后1周'] = round((p_hs300_week_after - p_hs300_end) / p_hs300_end * 100, 2)
        if all([p_hs300_end, p_hs300_month_after]):
            result['沪深300_后1月'] = round((p_hs300_month_after - p_hs300_end) / p_hs300_end * 100, 2)
        
        # 国债收益率变动 (单位: bp)
        if all([p_bond_month_before, p_bond_cppcc]):
            result['国债10Y_前1月(bp)'] = round((p_bond_cppcc - p_bond_month_before) * 100, 2)
        if all([p_bond_week_before, p_bond_cppcc]):
            result['国债10Y_前1周(bp)'] = round((p_bond_cppcc - p_bond_week_before) * 100, 2)
        if all([p_bond_cppcc, p_bond_end]):
            result['国债10Y_两会期间(bp)'] = round((p_bond_end - p_bond_cppcc) * 100, 2)
        if all([p_bond_end, p_bond_week_after]):
            result['国债10Y_后1周(bp)'] = round((p_bond_week_after - p_bond_end) * 100, 2)
        if all([p_bond_end, p_bond_month_after]):
            result['国债10Y_后1月(bp)'] = round((p_bond_month_after - p_bond_end) * 100, 2)
        
        return result
    except Exception as e:
        print(f"分析 {year} 年出错: {e}")
        return None

# 分析所有年份
print("\n正在分析历年两会表现...")
results = []
for year in sorted(lianghui_dates.keys()):
    result = analyze_year(year, lianghui_dates[year], hs300, bond10y)
    if result:
        results.append(result)

# 创建DataFrame
df_results = pd.DataFrame(results)

# 显示结果
print("\n" + "="*100)
print("历年两会前后市场表现分析 (数据来源: iChoice)")
print("="*100)
print("\n【沪深300指数涨跌幅 %】")
print(df_results[['年份', '沪深300_前1月', '沪深300_前1周', '沪深300_两会期间', '沪深300_后1周', '沪深300_后1月']].to_string(index=False))

print("\n\n【10Y国债收益率变动 (bp)】")
print(df_results[['年份', '国债10Y_前1月(bp)', '国债10Y_前1周(bp)', '国债10Y_两会期间(bp)', '国债10Y_后1周(bp)', '国债10Y_后1月(bp)']].to_string(index=False))

# 计算统计指标
print("\n\n" + "="*100)
print("统计汇总")
print("="*100)

# 沪深300统计
hs300_cols = ['沪深300_前1月', '沪深300_前1周', '沪深300_两会期间', '沪深300_后1周', '沪深300_后1月']
stats_hs300 = pd.DataFrame({
    '指标': ['平均值', '中位数', '最大值', '最小值', '上涨概率'],
    '前1月': [
        round(df_results['沪深300_前1月'].mean(), 2),
        round(df_results['沪深300_前1月'].median(), 2),
        round(df_results['沪深300_前1月'].max(), 2),
        round(df_results['沪深300_前1月'].min(), 2),
        f"{(df_results['沪深300_前1月'] > 0).sum()}/{len(df_results)} ({round((df_results['沪深300_前1月'] > 0).mean()*100, 1)}%)"
    ],
    '前1周': [
        round(df_results['沪深300_前1周'].mean(), 2),
        round(df_results['沪深300_前1周'].median(), 2),
        round(df_results['沪深300_前1周'].max(), 2),
        round(df_results['沪深300_前1周'].min(), 2),
        f"{(df_results['沪深300_前1周'] > 0).sum()}/{len(df_results)} ({round((df_results['沪深300_前1周'] > 0).mean()*100, 1)}%)"
    ],
    '两会期间': [
        round(df_results['沪深300_两会期间'].mean(), 2),
        round(df_results['沪深300_两会期间'].median(), 2),
        round(df_results['沪深300_两会期间'].max(), 2),
        round(df_results['沪深300_两会期间'].min(), 2),
        f"{(df_results['沪深300_两会期间'] > 0).sum()}/{len(df_results)} ({round((df_results['沪深300_两会期间'] > 0).mean()*100, 1)}%)"
    ],
    '后1周': [
        round(df_results['沪深300_后1周'].mean(), 2),
        round(df_results['沪深300_后1周'].median(), 2),
        round(df_results['沪深300_后1周'].max(), 2),
        round(df_results['沪深300_后1周'].min(), 2),
        f"{(df_results['沪深300_后1周'] > 0).sum()}/{len(df_results)} ({round((df_results['沪深300_后1周'] > 0).mean()*100, 1)}%)"
    ],
    '后1月': [
        round(df_results['沪深300_后1月'].mean(), 2),
        round(df_results['沪深300_后1月'].median(), 2),
        round(df_results['沪深300_后1月'].max(), 2),
        round(df_results['沪深300_后1月'].min(), 2),
        f"{(df_results['沪深300_后1月'] > 0).sum()}/{len(df_results)} ({round((df_results['沪深300_后1月'] > 0).mean()*100, 1)}%)"
    ]
})

print("\n【沪深300指数统计 (% )】")
print(stats_hs300.to_string(index=False))

# 国债统计
stats_bond = pd.DataFrame({
    '指标': ['平均值', '中位数', '最大值', '最小值', '上行概率'],
    '前1月': [
        round(df_results['国债10Y_前1月(bp)'].mean(), 2),
        round(df_results['国债10Y_前1月(bp)'].median(), 2),
        round(df_results['国债10Y_前1月(bp)'].max(), 2),
        round(df_results['国债10Y_前1月(bp)'].min(), 2),
        f"{(df_results['国债10Y_前1月(bp)'] > 0).sum()}/{len(df_results)} ({round((df_results['国债10Y_前1月(bp)'] > 0).mean()*100, 1)}%)"
    ],
    '前1周': [
        round(df_results['国债10Y_前1周(bp)'].mean(), 2),
        round(df_results['国债10Y_前1周(bp)'].median(), 2),
        round(df_results['国债10Y_前1周(bp)'].max(), 2),
        round(df_results['国债10Y_前1周(bp)'].min(), 2),
        f"{(df_results['国债10Y_前1周(bp)'] > 0).sum()}/{len(df_results)} ({round((df_results['国债10Y_前1周(bp)'] > 0).mean()*100, 1)}%)"
    ],
    '两会期间': [
        round(df_results['国债10Y_两会期间(bp)'].mean(), 2),
        round(df_results['国债10Y_两会期间(bp)'].median(), 2),
        round(df_results['国债10Y_两会期间(bp)'].max(), 2),
        round(df_results['国债10Y_两会期间(bp)'].min(), 2),
        f"{(df_results['国债10Y_两会期间(bp)'] > 0).sum()}/{len(df_results)} ({round((df_results['国债10Y_两会期间(bp)'] > 0).mean()*100, 1)}%)"
    ],
    '后1周': [
        round(df_results['国债10Y_后1周(bp)'].mean(), 2),
        round(df_results['国债10Y_后1周(bp)'].median(), 2),
        round(df_results['国债10Y_后1周(bp)'].max(), 2),
        round(df_results['国债10Y_后1周(bp)'].min(), 2),
        f"{(df_results['国债10Y_后1周(bp)'] > 0).sum()}/{len(df_results)} ({round((df_results['国债10Y_后1周(bp)'] > 0).mean()*100, 1)}%)"
    ],
    '后1月': [
        round(df_results['国债10Y_后1月(bp)'].mean(), 2),
        round(df_results['国债10Y_后1月(bp)'].median(), 2),
        round(df_results['国债10Y_后1月(bp)'].max(), 2),
        round(df_results['国债10Y_后1月(bp)'].min(), 2),
        f"{(df_results['国债10Y_后1月(bp)'] > 0).sum()}/{len(df_results)} ({round((df_results['国债10Y_后1月(bp)'] > 0).mean()*100, 1)}%)"
    ]
})

print("\n\n【10Y国债收益率变动统计 (bp)】")
print(stats_bond.to_string(index=False))

# 保存到Excel
with pd.ExcelWriter('/Users/fanshengxia/Desktop/lianghui_analysis_ichoice.xlsx', engine='openpyxl') as writer:
    df_results.to_excel(writer, sheet_name='历年数据', index=False)
    stats_hs300.to_excel(writer, sheet_name='沪深300统计', index=False)
    stats_bond.to_excel(writer, sheet_name='国债统计', index=False)

print("\n\n✓ 分析结果已保存到: ~/Desktop/lianghui_analysis_ichoice.xlsx")
print("\n分析完成!")
