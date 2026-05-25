import requests
import json
import os

# 读取之前保存的数据
with open('bilibili_rank.json', 'r', encoding='utf-8') as f:
    videos = json.load(f)

# 创建图片文件夹（如果不存在）
image_folder = "Bilibili全站排行榜封面图片"
if not os.path.exists(image_folder):
    os.makedirs(image_folder)

print("开始下载封面图片...")

# 遍历所有视频数据
for index, video in enumerate(videos):
    pic_url = video.get('pic_url', '')
    if pic_url:  # 确保URL不为空
        try:
            # 发送请求获取图片
            response = requests.get(pic_url, timeout=10)
            response.raise_for_status()
            
            # 构建保存路径
            file_name = f"图片{index + 1}.jpg"
            file_path = os.path.join(image_folder, file_name)
            
            # 保存图片
            with open(file_path, 'wb') as f:
                f.write(response.content)
            
            print(f"图片{index + 1}下载成功！")
            
        except requests.exceptions.RequestException as e:
            print(f"下载图片{index + 1}时出错: {e}")
        except Exception as e:
            print(f"保存图片{index + 1}时出错: {e}")
    else:
        print(f"视频{index + 1}没有封面URL")

print("所有图片下载完成！")