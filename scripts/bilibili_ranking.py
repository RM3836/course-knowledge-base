import requests
import json

# B站排行榜API地址
rank_api_url = "https://api.bilibili.com/x/web-interface/ranking/v2?rid=0&type=all"

# 模拟浏览器请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

print("正在获取Bilibili全站排行榜数据...")

try:
    # 发送请求
    response = requests.get(rank_api_url, headers=headers)
    response.raise_for_status()  # 检查HTTP状态码
    
    # 解析JSON数据
    data = response.json()
    
    # 打印数据结构（调试用）
    print("---原始JSON数据结构预览---")
    print(json.dumps(data, indent=2, ensure_ascii=False))
    
except requests.exceptions.RequestException as e:
    print(f"网络请求错误: {e}")
    data = None
except json.JSONDecodeError as e:
    print(f"JSON解析错误: {e}")
    data = None

# 校验数据并提取信息
if data and data.get('code') == 0:
    print("\n获取成功！开始解析并保存数据...")
    
    # 安全获取视频列表
    video_list = data.get('data', {}).get('list', [])
    
    if video_list:
        print("\n---Bilibili全站排行榜Top视频信息---")
        
        # 清空或创建新文件
        with open('bilibili_rank.json', 'w', encoding='utf-8') as f:
            f.write('[\n')  # 开始JSON数组
        
        for index, video in enumerate(video_list):
            # 安全获取数据
            title = video.get('title', '未知标题')
            author = video.get('owner', {}).get('name', '未知UP主')
            pic_url = video.get('pic', '')  # 获取封面URL
            
            # 获取播放量
            stats = video.get('stat', {})
            views = stats.get('view', 0)
            
            print(f"排名{index + 1}: {title} | UP主: {author} | 播放量: {views}")
            
            # 准备数据
            video_data = {
                'rank': index + 1,
                'title': title,
                'author': author,
                'views': views,
                'pic_url': pic_url  # 添加封面URL
            }
            
            # 写入文件
            with open('bilibili_rank.json', 'a', encoding='utf-8') as f:
                if index > 0:
                    f.write(',\n')
                json.dump(video_data, f, ensure_ascii=False, indent=4)
        
        # 结束JSON数组
        with open('bilibili_rank.json', 'a', encoding='utf-8') as f:
            f.write('\n]')
        
        print("\n数据已保存到 bilibili_rank.json 文件")
    else:
        print("未能从返回的数据中找到视频列表。")
else:
    print("\nAPI返回错误或数据格式不正确。")