# 載入CSV，繪製「新北市各區域平均房價比較」
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch


file_path = "../data/新北市_不動產實價登錄_買賣案件_FINAL.csv"
df = pd.read_csv(file_path, encoding='utf-8')

plt.rc("font", family="Microsoft JhengHei") # 微軟正黑體
plt.rcParams['axes.unicode_minus'] = False  # 正常顯示負號

district_avg_price = df.groupby('鄉鎮市區')['單價元平方公尺'].mean().sort_values(ascending=False)

# 資料轉成萬元單位
district_avg_price_wan = district_avg_price / 10_000

x_labels = district_avg_price_wan.index.tolist()
y_values = district_avg_price_wan.values.tolist()

# 顏色設定：前 5 名紅色，其餘藍綠色
colors = ['#e63946' if i < 5 else '#69b3a2' for i in range(len(y_values))]

plt.figure(figsize=(12, 6))
bars = plt.bar(x_labels, y_values, color=colors)

plt.title('新北市(2018-2024)各區域平均房價比較', fontsize=16)
plt.xlabel('行政區', fontsize = 12)
plt.ylabel('平均單價( 萬元／平方公尺 )', fontsize = 12)

# 軸字轉斜
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.7)

legend_elements = [
    Patch(facecolor='#e63946', label='前 5 高房價區'),
    Patch(facecolor='#69b3a2', label='其他區域')
]
plt.legend(handles=legend_elements, loc='upper right')

plt.tight_layout()
plt.show()



# # 指定輸出路徑
# output_file_path = "新北市_不動產實價登錄_篩選後.csv"

# # 儲存 CSV
# df_selected.to_csv(output_file_path, index=False, encoding="utf-8-sig")

# 趨勢圖資料判讀
# 1. 價格天花板明確：永和、板橋、中和、三重、新店
# ． 這些區屬於新北的核心生活圈，交通便利、人口密度高
# ． 永和區明顯高出其他區，可能與土地稀缺與高密度使用有關
# ． 這些區域房價高，但可能也反映了需求與便利性
# 2. 中段：林口、土城、新莊、泰山、蘆洲
# ． 中段房價約落在 11~14 萬元／㎡
# ． 多數為交通節點、重劃區或新興住宅區
# ． 林口區因有機場捷運、影視文化園區，長期被看好
# 3. 房價平價區：八里、鶯歌、三芝、石門
# ． 中段房價約落在 11~14 萬元／㎡
# ． 這些區域的單價大多低於 6 萬／㎡，生活機能或距離市中心較遠
# ． 但也可能是退休宅、度假區、或自住型買家選擇的熱點

