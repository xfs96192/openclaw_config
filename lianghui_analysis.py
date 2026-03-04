import requests
import json
from datetime import datetime, timedelta

# 两会时间数据 (2008-2025)
lianghui_dates = {
    2008: {"npc": "03-05", "cppcc": "03-03", "end": "03-18"},
    2009: {"npc": "03-05", "cppcc": "03-03", "end": "03-13"},
    2010: {"npc": "03-05", "cppcc": "03-03", "end": "03-14"},
    2011: {"npc": "03-05", "cppcc": "03-03", "end": "03-14"},
    2012: {"npc": "03-05", "cppcc": "03-03", "end": "03-14"},
    2013: {"npc": "03-05", "cppcc": "03-03", "end": "03-17"},
    2014: {"npc": "03-05", "cppcc": "03-03", "end": "03-13"},
    2015: {"npc": "03-05", "cppcc": "03-03", "end": "03-15"},
    2016: {"npc": "03-05", "cppcc": "03-03", "end": "03-16"},
    2017: {"npc": "03-05", "cppcc": "03-03", "end": "03-15"},
    2018: {"npc": "03-05", "cppcc": "03-03", "end": "03-20"},
    2019: {"npc": "03-05", "cppcc": "03-03", "end": "03-15"},
    2020: {"npc": "05-22", "cppcc": "05-21", "end": "05-28"},  # 疫情推迟
    2021: {"npc": "03-05", "cppcc": "03-04", "end": "03-11"},
    2022: {"npc": "03-05", "cppcc": "03-04", "end": "03-11"},
    2023: {"npc": "03-05", "cppcc": "03-04", "end": "03-13"},
    2024: {"npc": "03-05", "cppcc": "03-04", "end": "03-11"},
    2025: {"npc": "03-05", "cppcc": "03-04", "end": "03-11"},
}

print("历年两会时间数据已准备")
print(f"数据范围: {min(lianghui_dates.keys())} - {max(lianghui_dates.keys())}")
print(f"共 {len(lianghui_dates)} 年数据")
print("\n示例数据:")
for year in [2008, 2020, 2025]:
    d = lianghui_dates[year]
    print(f"  {year}年: 政协{d['cppcc']}, 人大{d['npc']}, 结束{d['end']}")
