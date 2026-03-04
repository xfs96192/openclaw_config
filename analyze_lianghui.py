import csv
from datetime import datetime, timedelta
from collections import defaultdict

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

# 读取沪深300数据
hs300_data = {}
with open('/Users/fanshengxia/clawd/hs300_history.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        date = row['date']
        hs300_data[date] = {
            'open': float(row['open']),
            'close': float(row['close']),
            'high': float(row['high']),
            'low': float(row['low'])
        }

print(f"沪深300数据: {len(hs300_data)} 条")

# 读取国债期货数据
bond_data = {}
try:
    with open('/Users/fanshengxia/clawd/bond10y_history.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            date = row['date']
            bond_data[date] = {
                'open': float(row['open']),
                'close': float(row['close']),
                'high': float(row['high']),
                'low': float(row['low'])
            }
    print(f"国债期货数据: {len(bond_data)} 条")
except:
    print("国债期货数据读取失败")

def get_price(data_dict, date_str, field='close'):
    """获取某日期价格，如果当天无数据则向前查找最近交易日"""
    if date_str in data_dict:
        return data_dict[date_str][field]
    # 向前查找最近交易日
    d = datetime.strptime(date_str, '%Y-%m-%d')
    for i in range(1, 10):  # 向前查找最多10天
        prev_date = (d - timedelta(days=i)).strftime('%Y-%m-%d')
        if prev_date in data_dict:
            return data_dict[prev_date][field]
    return None

def analyze_lianghui(year, dates, data_dict, name="沪深300"):
    """分析单年两会前后表现"""
    try:
        cppcc_start = f"{year}-{dates['cppcc']}"
        npc_start = f"{year}-{dates['npc']}"
        lh_end = f"{year}-{dates['end']}"
        
        # 计算各时间点
        cppcc_dt = datetime.strptime(cppcc_start, '%Y-%m-%d')
        npc_dt = datetime.strptime(npc_start, '%Y-%m-%d')
        end_dt = datetime.strptime(lh_end, '%Y-%m-%d')
        
        # 前一周、前一月、期间、后一周、后一月
        week_before = (cppcc_dt - timedelta(days=7)).strftime('%Y-%m-%d')
        month_before = (cppcc_dt - timedelta(days=30)).strftime('%Y-%m-%d')
        week_after = (end_dt + timedelta(days=7)).strftime('%Y-%m-%d')
        month_after = (end_dt + timedelta(days=30)).strftime('%Y-%m-%d')
        
        # 获取价格
        p_month_before = get_price(data_dict, month_before)
        p_week_before = get_price(data_dict, week_before)
        p_cppcc = get_price(data_dict, cppcc_start)
        p_end = get_price(data_dict, lh_end)
        p_week_after = get_price(data_dict, week_after)
        p_month_after = get_price(data_dict, month_after)
        
        if None in [p_month_before, p_week_before, p_cppcc, p_end]:
            return None
        
        return {
            'year': year,
            'month_before': round((p_cppcc - p_month_before) / p_month_before * 100, 2) if p_month_before else None,
            'week_before': round((p_cppcc - p_week_before) / p_week_before * 100, 2) if p_week_before else None,
            'during': round((p_end - p_cppcc) / p_cppcc * 100, 2) if p_cppcc else None,
            'week_after': round((p_week_after - p_end) / p_end * 100, 2) if p_end and p_week_after else None,
            'month_after': round((p_month_after - p_end) / p_end * 100, 2) if p_end and p_month_after else None,
        }
    except Exception as e:
        print(f"分析 {year} 年出错: {e}")
        return None

# 分析沪深300
print("\n" + "="*80)
print("沪深300指数 历年两会前后表现分析")
print("="*80)

results_hs300 = []
for year in sorted(lianghui_dates.keys()):
    result = analyze_lianghui(year, lianghui_dates[year], hs300_data, "沪深300")
    if result:
        results_hs300.append(result)

# 打印结果
print(f"\n{'年份':<8}{'前1月%':<10}{'前1周%':<10}{'两会期间%':<12}{'后1周%':<10}{'后1月%':<10}")
print("-"*70)

for r in results_hs300:
    print(f"{r['year']:<8}{r['month_before']:<10}{r['week_before']:<10}{r['during']:<12}{r['week_after']:<10}{r['month_after']:<10}")

# 计算统计指标
def calc_stats(data_list, field):
    values = [d[field] for d in data_list if d[field] is not None]
    if not values:
        return None, None, None
    return round(sum(values)/len(values), 2), round(max(values), 2), round(min(values), 2)

print("\n" + "="*70)
print("统计汇总 (沪深300)")
print("="*70)
print(f"{'指标':<12}{'平均值%':<12}{'最大值%':<12}{'最小值%':<12}")
print("-"*50)

for field in ['month_before', 'week_before', 'during', 'week_after', 'month_after']:
    avg, maxv, minv = calc_stats(results_hs300, field)
    label = {'month_before': '前1月', 'week_before': '前1周', 'during': '两会期间', 
             'week_after': '后1周', 'month_after': '后1月'}[field]
    print(f"{label:<12}{avg:<12}{maxv:<12}{minv:<12}")

# 计算上涨概率
print("\n上涨概率:")
for field in ['month_before', 'week_before', 'during', 'week_after', 'month_after']:
    values = [d[field] for d in results_hs300 if d[field] is not None]
    up_count = sum(1 for v in values if v > 0)
    prob = round(up_count / len(values) * 100, 1) if values else 0
    label = {'month_before': '前1月', 'week_before': '前1周', 'during': '两会期间', 
             'week_after': '后1周', 'month_after': '后1月'}[field]
    print(f"  {label}: {prob}% ({up_count}/{len(values)})")

# 分析国债期货
print("\n\n" + "="*80)
print("10Y国债期货 历年两会前后表现分析")
print("="*80)

results_bond = []
for year in sorted(lianghui_dates.keys()):
    if year >= 2016:  # 国债期货数据从2016年开始
        result = analyze_lianghui(year, lianghui_dates[year], bond_data, "国债期货")
        if result:
            results_bond.append(result)

print(f"\n{'年份':<8}{'前1月%':<10}{'前1周%':<10}{'两会期间%':<12}{'后1周%':<10}{'后1月%':<10}")
print("-"*70)

for r in results_bond:
    print(f"{r['year']:<8}{r['month_before']:<10}{r['week_before']:<10}{r['during']:<12}{r['week_after']:<10}{r['month_after']:<10}")

print("\n" + "="*70)
print("统计汇总 (10Y国债期货 - 注: 价格上涨=收益率下降)")
print("="*70)
print(f"{'指标':<12}{'平均值%':<12}{'最大值%':<12}{'最小值%':<12}")
print("-"*50)

for field in ['month_before', 'week_before', 'during', 'week_after', 'month_after']:
    avg, maxv, minv = calc_stats(results_bond, field)
    label = {'month_before': '前1月', 'week_before': '前1周', 'during': '两会期间', 
             'week_after': '后1周', 'month_after': '后1月'}[field]
    print(f"{label:<12}{avg:<12}{maxv:<12}{minv:<12}")

print("\n上涨概率 (价格上涨=收益率下降):")
for field in ['month_before', 'week_before', 'during', 'week_after', 'month_after']:
    values = [d[field] for d in results_bond if d[field] is not None]
    up_count = sum(1 for v in values if v > 0)
    prob = round(up_count / len(values) * 100, 1) if values else 0
    label = {'month_before': '前1月', 'week_before': '前1周', 'during': '两会期间', 
             'week_after': '后1周', 'month_after': '后1月'}[field]
    print(f"  {label}: {prob}% ({up_count}/{len(values)})")

print("\n\n分析完成!")
