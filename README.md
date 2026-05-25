# 📚 课程知识库

> 广州应用科技学院 · 网络工程 · YURM  
> 大二下学期课程资料浓缩整理

## 📖 知识地图

```
course-knowledge-base/
├── README.md                    ← 你在这里
├── cheatsheet.md                ← 一页速查表（考前必看）
│
├── 01-计网路由交换/
│   ├── 01-核心概念.md           ← OSI模型、TCP/IP、关键协议
│   ├── 02-选择题库.md           ← 112道选择题（含答案解析）
│   ├── 03-大题答题模板.md       ← 子网划分、CRC、路由配置
│   ├── 04-华为命令速查.md       ← 路由器/交换机常用命令
│   ├── 05-网络协议分析.md       ← TCP握手、HTTP、ARP
│   └── 06-速记口诀.md           ← 考前速记
│
├── 02-网络安全实验/
│   ├── 01-Metasploitable3攻击.md  ← MS12-020、IIS漏洞
│   ├── 02-防火墙配置.md           ← 安全策略、NAT、双机热备
│   ├── 03-漏洞扫描.md             ← Nmap、Dirb、Nikto
│   └── 04-安全实验速查.md         ← 工具命令速查表
│
├── 03-ENSP网络规划/
│   └── README.md                ← 网络规划大作业（IP/VLAN/设备配置）
│
├── 04-AI机器学习/
│   ├── 01-分类预测.md           ← KNN、决策树、SVM
│   ├── 02-回归分析.md           ← 线性回归、Ridge
│   ├── 03-聚类分析.md           ← K-Means、肘部法则
│   └── 04-代码模板.md           ← sklearn速查模板
│
├── 05-编程项目/
│   ├── 01-WEB服务器设计.md      ← HTTP协议、套接字通信
│   └── 02-Python爬虫.md         ← 12306订票、Bilibili爬虫
│
├── 06-思政与其他/
│   ├── 01-马原复习.md           ← 唯物辩证法、认识论、唯物史观
│   ├── 02-Java面向对象.md       ← 封装继承多态、AWT/Swing
│   └── 03-ENSP基础命令.md       ← VLAN/STP/路由配置速查
│
└── scripts/
    ├── 12306订票_完整.py
    ├── 爬取车站的代号.py
    ├── bilibili_ranking.py
    └── bilibili_download.py
```

## 🎯 模块索引

| # | 模块 | 文件数 | 核心技术 | 来源课程 |
|---|------|--------|----------|----------|
| 01 | 计网路由交换 | 6 | `TCP/IP` `OSPF` `RIP` `VLAN` | 计算机网络、路由交换 |
| 02 | 网络安全实验 | 4 | `Metasploit` `Nmap` `防火墙` | 网络安全技术 |
| 03 | ENSP网络规划 | 1 | `ENSP` `VLAN` `NAT` `ACL` | 网络规划与设计 |
| 04 | AI机器学习 | 4 | `sklearn` `KNN` `SVM` `K-Means` | 人工智能基础 |
| 05 | 编程项目 | 2 | `Python` `Selenium` `HTML/CSS` | WEB开发、Python |
| 06 | 思政与其他 | 3 | `马原` `Java` `面向对象` | 思政课、Java |

**总计**：20 个知识文件 + 4 个 Python 脚本

## 🚀 快速开始

```bash
# 克隆仓库
git clone https://github.com/RM3836/course-knowledge-base.git
cd course-knowledge-base

# 查看速查表（考前必看）
cat cheatsheet.md

# 查看指定模块
cat 01-计网路由交换/02-选择题库.md
```

## 📝 复习建议

| 场景 | 推荐文件 |
|------|----------|
| 考前30分钟速记 | `cheatsheet.md` + 各模块 `06-速记口诀.md` |
| 选择题刷题 | `01-计网路由交换/02-选择题库.md` |
| 大题练习 | `01-计网路由交换/03-大题答题模板.md` |
| 实验报告参考 | `02-网络安全实验/` 各文件 |
| AI实验代码 | `04-AI机器学习/04-代码模板.md` |
| 期末突击 | 按模块顺序通读 |

---

**作者**：YURM ()  
**学校**：广州应用科技学院 · 网络工程  
**GitHub**：[RM3836](https://github.com/RM3836)
