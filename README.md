# TWD97toWGS84

政府開放資料集大多會採用twd97座標系，
而想要將資料應用到google map api上就必須經過轉換，
將twd97轉亂成wgs84。

# 使用方式

將要轉換的資料集檔名改成source.geojson，
在command line中輸入 python TWD97toWGS84.py (注意自己所在的位置)
最後會輸出一個result.json為轉換後的結果
