# 如何使用

1.去[Line Notify](https://notify-bot.line.me/zh_TW/)申請一組你專屬的Key \
2.調整你希望搜尋的租屋類型

```
filter_params = {
        'region': '1',  # (地區) 台北
        'section': '5,7', # 信義區和大安區
        'searchtype': '1',  # (位置1) 按捷運
        # 'mrtline': '125',  # (位置2) 淡水信義線
        # 'mrtcoods': '4198,4163',  # (位置3) 新北投 & 淡水
        # 'kind': '2',  # (類型) 獨立套房
        # 'multiPrice': '20000_30000',  # (租金) 5000元以下 & 5000-10000元
        # 'rentprice': '3000,6000',  # (自訂租金範圍) 3000~6000元
        # 'multiRoom': '2,3',  # (格局) 2房 & 3房
        # 'other': 'near_subway,cook,lease',  # (特色) 近捷運 & 可開伙 & 可短期租賃
        # --- 以下要加 showMore=1 ---
        'showMore': '1',
        # 'shape': '3',  # (型態) 透天厝
        # 'multiArea': '10_20,20_30,30_40',  # (坪數) 10-20坪 & 20-30坪 & 30-40坪
        
        # 'multiFloor': '2_6',  # (樓層) 2-6層
        # 'option': 'cold,washer,bed',  # (設備) 有冷氣 & 有洗衣機 & 床
        # 'multiNotice': 'all_sex',  # (須知) 男女皆可
        # 'other':'pet',
        'area': '10,',  # (自訂坪數範圍) 20~50坪
        'recom_community':'1',
    }
```

3. 下 `python rent.py`或是`python3 rent.py`
4. 耐心等待結果,因為591一次只能搜尋30筆,如果資料量比較多就要慢慢搜尋, 避免被Ban
