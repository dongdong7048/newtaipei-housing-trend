# 用 pandas 分析出各年各區的平均單價
# 用 matplotlib 畫出每年的 Top 10 房價區域的橫向長條圖
# 用 FuncAnimation 把各年的圖組合成一支動畫（MP4）

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

file_path = "../data/新北市_不動產實價登錄_買賣案件_FINAL.csv"
df = pd.read_csv(file_path, encoding='utf-8')

df['單價_萬元'] = df['單價元平方公尺'] / 10_000

# 按年與行政區分組，計算平均單價(萬元)
grouped = df.groupby(['交易年', '鄉鎮市區'])['單價_萬元'].mean().reset_index()

plt.rc("font", family="Microsoft JhengHei") # 微軟正黑體
plt.rcParams['axes.unicode_minus'] = False  # 正常顯示負號

# 年份列表取2019-2025
years = sorted([y for y in df['交易年'].unique() if 2019 <= y <= 2025 ])

# 函式：獲取各區域每年房價
def get_all_districts(year, top_n = 10):
  data = grouped[grouped['交易年'] == year]
  return data.sort_values(by="鄉鎮市區")

# 建立畫布
fig, ax = plt.subplots(figsize = (10, 6))

# 函式： 每一幀要畫的內容
def draw_bars(year):
  ax.clear()
  data = grouped[grouped["交易年"] == year].sort_values(by="鄉鎮市區")

  # 確保資料存在
  if data.empty:
      return

  max_price = data["單價_萬元"].max()
  max_area = data[data["單價_萬元"] == max_price]["鄉鎮市區"].values[0]
  
  # 顏色： 紅色為最高，其餘藍色
  colors = ['#f44336' if area == max_area else '#6fa8dc' for area in data["鄉鎮市區"]]

  # 畫長條
  bars = ax.barh(data["鄉鎮市區"], data["單價_萬元"], color=colors)
  ax.set_yticks([])
  ax.set_title(f"新北市各區平均房價（萬元／平方公尺） - {year}", fontsize=16)
  ax.set_xlabel("平均單價（萬元）")
  ax.set_xlim(0, grouped["單價_萬元"].max() * 1.2)

  for i, (value, name) in enumerate(zip(data["單價_萬元"], data["鄉鎮市區"])):
      # 顯示價格數字
      ax.text(value + 0.2, i, f"{value:.2f}", va='center', fontsize=10)

      # 顯示行政區名稱
      if name == max_area:
          ax.text(0, i, name, va='center', ha='right', color='#b71c1c', fontsize=11, fontweight='bold')
      else:
          ax.text(0, i, name, va='center', ha='right', color='#444444', fontsize=9)

      # ➕ 顯示變化標記
      if year > min(years):  # 有前一年才比較
          prev_year = year - 1
          prev_data = grouped[(grouped["交易年"] == prev_year) & (grouped["鄉鎮市區"] == name)]
          if not prev_data.empty:
              prev_value = prev_data["單價_萬元"].values[0]
              diff = value - prev_value
              color = "#2e7d32" if diff > 0 else "#c62828"
              sign = "+" if diff > 0 else ""
              ax.text(value + 1.8, i, f"{sign}{diff:.2f}", va='center', fontsize=9, color=color)


ani = FuncAnimation(
   fig,
   draw_bars,     # 每一幀呼叫的函式
   frames=years,  # 每一幀的輸入(年份)
   interval=1000, # 每一幀間隔時間(ms)
   repeat=False   # 播完一次就結束
)

# plt.show()

# 儲存為gif，每幀顯示2秒
ani.save("新北市歷年房價變化動畫.gif", writer="pillow", fps=0.4)






