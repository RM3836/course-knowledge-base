# 02-Python爬虫

## 一、爬虫基础

### 爬虫基本流程
1. **分析**：确定要爬取的网站和数据
2. **发送请求**：使用requests或urllib发送HTTP请求
3. **获取响应**：接收服务器返回的HTML/JSON数据
4. **解析数据**：使用BeautifulSoup、lxml或正则表达式提取信息
5. **存储数据**：保存到文件（TXT/CSV）或数据库
6. **遵守规则**：检查robots.txt，避免频繁请求

### Robots协议
```
# 示例：豆瓣robots.txt
User-agent: *           # 适用于所有爬虫
Disallow: /search       # 禁止爬取搜索页面
Disallow: /accounts/    # 禁止爬取用户账户页面
Disallow: /forum/       # 禁止爬取论坛页面
```

## 二、Requests + BeautifulSoup基础爬虫

### 环境安装
```bash
pip install requests beautifulsoup4 lxml
```

### 获取网页文字

```python
import requests
from bs4 import BeautifulSoup

# 1. 发送请求
url = "https://example.com"
response = requests.get(url)

# 2. 解析HTML
soup = BeautifulSoup(response.text, 'html.parser')

# 3. 提取数据
title = soup.title
print(f"页面标题: {title.string}")

# 提取所有链接
links = soup.find_all('a')
for link in links:
    print(link.get('href'), link.text)
```

### 下载视频

```python
import requests

def download_video(url, filename):
    """下载视频文件"""
    response = requests.get(url, stream=True)
    with open(filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    print(f"下载完成: {filename}")

# 使用示例
video_url = "https://example.com/video.mp4"
download_video(video_url, "video.mp4")
```

## 三、Selenium自动化爬虫

### 环境安装
```bash
pip install selenium
# 下载对应浏览器的WebDriver
```

### 基础操作

#### 元素定位

```python
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://example.com")

# By.ID定位
element_by_id = driver.find_element(By.ID, "element-id")

# By.CLASS_NAME定位
element_by_class = driver.find_element(By.CLASS_NAME, "class-name")

# By.XPATH定位
element_by_xpath = driver.find_element(By.XPATH, "//div[@class='example']")

# By.CSS_SELECTOR定位
element_by_css = driver.find_element(By.CSS_SELECTOR, "#id > .class")

# find_elements返回列表
elements = driver.find_elements(By.CLASS_NAME, "item")
print(type(elements))  # <class 'list'>
```

**By.ID vs By.CLASS_NAME**：
- By.ID：通过元素的id属性定位，id在页面中唯一
- By.CLASS_NAME：通过class属性定位，class可以有多个匹配

#### 鼠标操作

```python
from selenium.webdriver.common.action_chains import ActionChains

# 复杂操作需要ActionChains
element = driver.find_element(By.ID, "button")
actions = ActionChains(driver)
actions.click(element).perform()  # 必须调用perform()

# 为什么需要ActionChains？
# ActionChains将多个操作存储在队列中，调用perform()时按顺序执行
# 适用于悬停、拖拽、右键等复杂交互
```

#### 下拉框处理

```python
from selenium.webdriver.support.ui import Select

select_element = driver.find_element(By.ID, "dropdown")
select = Select(select_element)  # 必须用Select包装

select.select_by_index(0)      # 按索引选择（从0开始）
select.select_by_value("value") # 按value属性选择
select.select_by_visible_text("文本")  # 按显示文本选择
```

#### 弹窗处理

```python
# 不能用find_element处理弹窗，因为弹窗属于浏览器而非页面
alert = driver.switch_to.alert  # 切换到弹窗
print(alert.text)               # 获取弹窗文本
alert.accept()                  # 点击确定
alert.dismiss()                 # 点击取消
alert.send_keys("输入内容")      # 输入文本（prompt弹窗）
```

#### 页面切换（窗口句柄）

```python
# 窗口句柄是浏览器为每个标签页/窗口分配的唯一标识
handles = driver.window_handles  # 获取所有窗口句柄
driver.switch_to.window(handles[-1])  # 切换到最新窗口

# 为什么要切换？
# 新标签页打开后，driver仍指向原页面
# 必须switch_to.window()才能操作新页面
```

#### 等待操作

```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 隐式等待：全局设置，每次查找元素时最多等待N秒
driver.implicitly_wait(10)

# 显式等待：针对特定条件等待
element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "button"))
)

# 区别：
# - 隐式等待：对所有find_element生效，等待元素出现
# - 显式等待：针对特定条件（可点击、可见等），更精确可靠
```

## 四、实战：12306余票查询

### 关键技术

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
driver.get("https://www.12306.cn/index/")

# 1. 等待用户手动登录
WebDriverWait(driver, 300).until(
    EC.presence_of_element_located((By.ID, "loginUser"))
)
print("登录成功")

# 2. 使用JavaScript注入设置出发站（为什么不用send_keys？）
# 因为12306的输入框是特殊组件，send_keys会触发联想干扰
from_station = driver.find_element(By.ID, "fromStationText")
from_station_code = "BJP"  # 北京站代码

driver.execute_script(
    "arguments[0].value=arguments[1];",
    from_station,
    from_station_code
)
# execute_script直接修改DOM的value属性，绕过前端事件触发

# 3. 设置到达站
to_station = driver.find_element(By.ID, "toStationText")
to_station_code = "SHH"  # 上海站代码
driver.execute_script(
    "arguments[0].value=arguments[1];",
    to_station,
    to_station_code
)

# 4. 点击查询
search_btn = driver.find_element(By.ID, "search_one")
search_btn.click()

# 5. 等待结果加载并提取
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "ticket-info"))
)

# 提取余票信息
trains = driver.find_elements(By.XPATH, "//tbody[@id='queryLeftTable']/tr")
for train in infos:
    # 提取车次、出发站、到达站、历时、余票等信息
    print(train.text)
```

### 关键技术解释

**WebDriverWait**：显式等待方式，确保元素可交互后再操作，比sleep更可靠。

**execute_script注入**：12306输入框是特殊组件，`send_keys()`会触发前端JS事件导致联想干扰。`execute_script`直接修改DOM的value属性，绕过前端事件，更稳定可靠。

## 五、实战：动态数据爬取

### 英雄数据爬取示例

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import time

driver = webdriver.Chrome()
driver.get("https://lol.qq.com/data/info-def498.shtml")

# 等待页面加载
time.sleep(3)

# 提取英雄数据
heros = driver.find_elements(By.CLASS_NAME, "l_ol_item")

# 保存到CSV
with open('英雄数据.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['英雄名', '定位', '价格'])
    for hero in heros:
        name = hero.find_element(By.CLASS_NAME, "name").text
        # ... 提取其他信息
        writer.writerow([name])

driver.quit()
```

## 六、常见问题与解决

| 问题 | 解决方案 |
|------|----------|
| 中文显示乱码 | `response.encoding = 'utf-8'` |
| 元素找不到 | 增加等待时间，使用显式等待 |
| 反爬机制 | 添加请求头、使用代理、降低频率 |
| 动态页面 | 使用Selenium而非requests |
| 编码问题 | 检查网页charset，设置正确编码 |
