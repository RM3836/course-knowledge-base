# 05-编程项目

本模块包含Web服务器设计和Python爬虫两大编程项目的完整知识体系。

## 目录

### [01-WEB服务器设计](01-WEB服务器设计.md)
- **项目类型**：C语言实现的HTTP Web服务器
- **核心内容**：
  - HTTP协议分析（请求/响应报文结构）
  - GET与POST方法对比（8项区别）
  - 套接字通信流程（socket/bind/listen/accept）
  - 守护进程创建（双重fork）
  - 前端HTML页面设计
  - 后端C语言函数架构
- **系统测试**：启动服务器、进程查看、GET/POST测试

### [02-Python爬虫](02-Python爬虫.md)
- **项目类型**：Python网络爬虫
- **基础爬虫**：
  - Requests + BeautifulSoup（获取文字、下载视频）
  - Robots协议解析
- **Selenium自动化**：
  - 元素定位（By.ID、By.CLASS_NAME、By.XPATH等）
  - 鼠标/键盘交互（ActionChains）
  - 下拉框、弹窗、页面切换处理
  - 隐式等待 vs 显式等待
- **实战案例**：
  - **12306余票查询**：JavaScript注入设置站点、WebDriverWait等待登录
  - **动态数据爬取**：英雄数据提取、CSV存储

## 技术栈

| 项目 | 技术 |
|------|------|
| WEB服务器 | C语言、HTTP协议、Socket套接字 |
| 基础爬虫 | Python、Requests、BeautifulSoup |
| 自动化爬虫 | Python、Selenium WebDriver |
| 数据存储 | CSV文件、TXT文件 |

## 学习路径

```
入门
├── HTTP协议基础
├── 套接字通信原理
└── Python requests库

进阶
├── BeautifulSoup解析
├── Selenium自动化
└── 动态页面处理

实战
├── WEB服务器开发
├── 12306查询爬虫
└── 数据分析与存储
```
