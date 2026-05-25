# 📋 课程知识库速查表

## 计算机网络

| 命令/概念 | 说明 |
|-----------|------|
| `ipconfig /all` | 查看本机 IP 配置 |
| `ping X.X.X.X` | 测试连通性 |
| `netstat` | 查看网络连接状态 |
| `arp -a` | 查看 ARP 缓存表 |
| `nslookup domain` | DNS 查询 |
| `tracert X.X.X.X` | 路由追踪（Windows） |

## 华为路由器

| 命令 | 说明 |
|------|------|
| `system-view` | 用户视图→系统视图 |
| `display ip routing-table` | 查看路由表 |
| `display current-configuration` | 查看当前配置 |
| `display ip interface brief` | 查看接口 IP 摘要 |
| `ip route-static 目标网段 掩码 下一跳` | 配置静态路由 |
| `rip 1` → `version 2` → `network X.X.0.0` | 配置 RIP |
| `ospf 1` → `area 0` → `network X.X.X.X 反掩码` | 配置 OSPF |
| `save` | 保存配置 |

## 路由优先级

| 来源 | 默认优先级 |
|------|------------|
| 直连路由 | 0 |
| 静态路由 | 60 |
| OSPF | 10 |
| RIP | 100 |

## 线缆速查

| 场景 | 线缆类型 |
|------|----------|
| PC ↔ 交换机 | 直通线 |
| PC ↔ 路由器 | 交叉线 |
| 交换机 ↔ 交换机 | 交叉线 |
| 路由器 ↔ 交换机 | 直通线 |

## Python sklearn 速查

```python
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
from sklearn.metrics import accuracy_score, classification_report

# 分类流程
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
model = KNeighborsClassifier(n_neighbors=5)
model.fit(X_train, y_train)
pred = model.predict(X_test)
print(accuracy_score(y_test, pred))
```

## 子网划分公式

```
子网数 = 2^n（n = 借位数）
每子网主机数 = 2^m - 2（m = 剩余主机位）
子网掩码 = 原掩码 + n 位
子网大小 = 2^m
```

## DNS 解析顺序

```
本地缓存 → 本地DNS → 根DNS → 顶级DNS → 权威DNS
```

## ENSP VLAN 配置

```bash
# 创建 VLAN
[Huawei]vlan 10
[Huawei-vlan10]description Department

# 端口加入 VLAN（Access）
[Huawei]int g0/0/1
[Huawei-GigabitEthernet0/0/1]port link-type access
[Huawei-GigabitEthernet0/0/1]port default vlan 10

# Trunk 端口
[Huawei]int g0/0/24
[Huawei-GigabitEthernet0/0/24]port link-type trunk
[Huawei-GigabitEthernet0/0/24]port trunk allow-pass vlan 10 20
```
