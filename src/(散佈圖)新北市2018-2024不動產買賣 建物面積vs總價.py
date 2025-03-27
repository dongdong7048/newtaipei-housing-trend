# 載入CSV，繪製新北市歷年房價趨勢圖

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


file_path = "../data/不動產實價登錄資訊-買賣案件-新北市.csv"
df = pd.read_csv(file_path, encoding='utf-8')

# 篩選需要的欄位：
# rps07 交易年月日 -> 需要轉換為西元
# district 鄉鎮市區
# rps15 建物移轉總面積公尺
# rps21 總價元
# rps22 單價元平方公尺

df['交易年'] = df['rps07'].astype(str).str[:3].astype(int) + 1911 #民國年轉西元年

selected_columns = {
  "district" : "鄉鎮市區",
  "交易年": "交易年",
  "rps21" : "總價元",
  "rps15" : "建物移轉總面積平方公尺",
  "rps22" : "單價元平方公尺",
}

df_selected = df[list(selected_columns.keys())].rename(columns=selected_columns)

# 篩選出 建物移轉總面積平方公尺 和 單價元平方公尺 兩欄數值皆大於 0 的資料
# 使用 dropna() 刪除這兩個欄位為 NaN (空值) 的行
df_selected = df_selected[
  (df_selected['建物移轉總面積平方公尺'] > 0) &
  (df_selected['單價元平方公尺'] > 0)
].dropna(subset=['建物移轉總面積平方公尺', '單價元平方公尺'])

plt.rc("font", family="Microsoft JhengHei") # 微軟正黑體
plt.rcParams['axes.unicode_minus'] = False  # 正常顯示負號

df_focus = df_selected[
  (df_selected['建物移轉總面積平方公尺'] < 250) &
  (df_selected['單價元平方公尺'] < 60_000_000)
]

x = df_focus['建物移轉總面積平方公尺']
y = df_focus['總價元'] / 1_000_1000

# 一次多項式擬和
slope, intercept = np.polyfit(x, y, 1)

# y = ax + b
y_pred = slope * x + intercept

plt.figure(figsize=(10, 6))
plt.scatter(
  x, 
  y, 
  alpha=0.2,
  s=2,
  color="#4c4c4c",
  label = '交易資料'
)
plt.plot(
  x, 
  y_pred, 
  color = "#e63946", 
  linewidth = 2,
  label = f'趨勢線: y = {slope:.2f}x + {intercept:.2f}' 
)
plt.title('新北市(2018-2024)不動產買賣  建物面積 vs 總價', fontsize=16)
plt.xlabel('建物面積(平方公尺)', fontsize=12)
plt.ylabel('總價(百萬元)', fontsize=12)
plt.legend()
plt.grid(True) 
plt.tight_layout()
plt.show()

# 趨勢圖資料判讀
# 1. 趨勢線的斜率為正（0.01x），表示建物面積越大，總價越高
# 2. 這是房價中常見的趨勢，但它不是完全線性：
#    ．小面積的價格落在較窄範圍內（點集中）
#    ．面積一旦變大，價格變異變大（點分得較散）
#    ．說明有些大坪數建物總價很便宜，有些則很貴，和地點、建材、用途等因素有關
# 3. 每增加 1 平方公尺，平均只提升總價 1 萬元（= 百萬 * 0.01），
#    說明「每坪增加單價穩定，不會暴漲」

# # 指定輸出路徑
# output_file_path = "新北市_不動產實價登錄_篩選後.csv"

# # 儲存 CSV
# df_selected.to_csv(output_file_path, index=False, encoding="utf-8-sig")