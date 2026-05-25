import requests
import re
import openpyxl
def get_station():
    url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9301'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
  }
    resp = requests.get(url,headers=headers)
    resp.encoding='utf8'
    print(resp.text)
    #https://blog.csdn.net/bmjhappy/article/details/80512917
    starions  = re.findall(r'([\u4e00-\u9fa5]+)\|([A-Z]+)',resp.text)
    print(starions)
    return starions


def save(lst):
    wb = openpyxl.Workbook()#创建工作簿对象
    ws = wb.active#使用活动表
    for item in lst:
        ws.append(item)#执行一次append向表格中添加一行
    wb.save('车站代码.xlsx')


if __name__ == '__main__':
    lst = get_station()
    save(lst)













