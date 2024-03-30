import requests
import time
import random
from bs4 import BeautifulSoup
import json
from datetime import datetime
import os
# ref https://blog.jiatool.com/posts/house591_spider/

LINE_NOTIFY_KEY = 'YOUR_NOTIFY_KEY'
def SendMsg(msg):
    my_headers = {'Authorization': 'Bearer ' + LINE_NOTIFY_KEY}

    my_params = {'message': msg}

    response = requests.post('https://notify-api.line.me/api/notify', headers = my_headers, params = my_params)

    print(response.status_code)
    print(datetime.now())

def paramToString(param):
  return ''.join([f'&{key}={value}' for key, value, in filter_params.items()])

def get_house_detail(house_id):
  """ 房屋詳情

  :param house_id: 房屋ID
  :return house_detail: requests 房屋詳細資料
  """
  # 紀錄 Cookie 取得 X-CSRF-TOKEN, deviceid
  headers = {
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.68',
  }
  s = requests.Session()
  url = f'https://rent.591.com.tw/home/{house_id}'
  r = s.get(url, headers=headers)
  soup = BeautifulSoup(r.text, 'html.parser')
  token_item = soup.select_one('meta[name="csrf-token"]')

  headers['X-CSRF-TOKEN'] = token_item.get('content')
  headers['deviceid'] = s.cookies.get_dict()['T591_TOKEN']
  # headers['token'] = s.cookies.get_dict()['PHPSESSID']
  headers['device'] = 'pc'

  url = f'https://bff.591.com.tw/v1/house/rent/detail?id={house_id}'
  r = s.get(url, headers=headers)
  if r.status_code != requests.codes.ok:
      print('請求失敗', r.status_code)
      return
  house_detail = r.json()['data']
  return house_detail

 # 紀錄 Cookie 取得 X-CSRF-TOKEN
def search(filter_params=None, sort_params=None, want_page=1):
  """ 搜尋房屋

  :param filter_params: 篩選參數
  :param sort_params: 排序參數
  :param want_page: 想要抓幾頁
  :return total_count: requests 房屋總數
  :return house_list: requests 搜尋結果房屋資料
  """
  total_count = 0
  house_list = []
  page = 0
  headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.68',
        }

  # 紀錄 Cookie 取得 X-CSRF-TOKEN
  s = requests.Session()
  url = 'https://rent.591.com.tw/'
  r = s.get(url, headers=headers)
  soup = BeautifulSoup(r.text, 'html.parser')
  token_item = soup.select_one('meta[name="csrf-token"]')

  headers['X-CSRF-TOKEN'] = token_item.get('content')

  # 搜尋房屋
  url = 'https://rent.591.com.tw/home/search/rsList'
  params = 'is_format_data=1&is_new_list=1&type=1'
  if filter_params:
      # 加上篩選參數，要先轉換為 URL 參數字串格式
      # params += ''.join([f'&{key}={value}' for key, value, in filter_params.items()])
     params += paramToString(filter_params)
  else:
      params += '&region=1&kind=0'
  # 在 cookie 設定地區縣市，避免某些條件無法取得資料
  s.cookies.set('urlJumpIp', filter_params.get('region', '1') if filter_params else '1', domain='.591.com.tw')

  # 排序參數
  if sort_params:
      params += ''.join([f'&{key}={value}' for key, value, in sort_params.items()])
  row='&firstRow=0'
  while page < want_page:
      # params += f'&firstRow={page*30}'
      r = s.get(url, params=params + row, headers=headers)
      if r.status_code != requests.codes.ok:
          print('請求失敗', r.status_code)
          break

      page += 1
      data = r.json()
      total_count = data['records']
      row =  f'&firstRow={page*30}&totalRows={total_count}'
      house_list.extend(data['data']['data'])
      # print('house_len: ', len(house_list))
      if(len(house_list)>=int(total_count.replace(',',''))):
        break

      # 隨機 delay 一段時間
      time.sleep(random.uniform(2, 5))

  return total_count, house_list

def savePreviousData(data):
  f = open('previousData.json', 'w', encoding='UTF-8')
  f.write(json.dumps(data, indent=4,ensure_ascii=False))
  f.close()

def getPreviousData():
  path = 'previousData.json'
  if(os.path.exists(path)):
    f = open(path, 'r', encoding='UTF-8')
    data = json.load(f)
    f.close()
    return data['data']
  return []

def comparePreviousData(previous, current):
  result = []
  for i in current:
    if(i not in previous):
        result.append(i)
  return result

# main
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
    # 排序依據
sort_params = {
        # 租金由小到大
        'order': 'money',  # posttime, area
        'orderType': 'desc'  # asc
    }
while True:
  total_count, houses = search(filter_params, sort_params, want_page=100)
  print('搜尋結果房屋總數：', total_count)
  prev = getPreviousData()
  curr = list(set([p['post_id'] for p in houses]))
  savePreviousData({'data': list(set(prev+curr))})
  result = comparePreviousData(prev, curr)
  if(len(result) > 0 and len(prev) > 0):
    msg = 'new house:\n'.join([f'https://rent.591.com.tw/home/{value}\n' for value in result])
    if(msg):
      SendMsg(msg)
    print('diff: ', msg)
  else:
    print('no news')
  time.sleep(random.uniform(60 * 2, 60 * 4))