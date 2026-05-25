# ENSP网络规划模块

## 一、知识点总结

### 1. 网络规划核心要素
- **需求分析**：明确企业/校园网络的用户规模、业务类型、安全要求
- **IP地址规划**：按部门/功能划分子网，预留扩展空间
- **VLAN设计**：隔离广播域，按部门/业务划分VLAN
- **设备选型**：核心层、汇聚层、接入层三层架构

### 2. WLAN无线网络规划（实验六）
- **组网方式**：二层/三层旁挂组网，AP网关在AC上，用户网关在交换机上
- **隧道转发模式**：用户流量经过AC，便于统一管理和安全控制
- **DHCP分配**：AC为AP分配地址，SW1为用户分配地址
- **安全策略**：WPA-WPA2加密，SSID隔离不同用户群体

### 3. NAT网络地址转换（实验四）
- **目的**：解决IPv4地址短缺，隐藏内网结构
- **源NAT**：内网访问外网时替换源IP（地址池方式/接口方式）
- **目的NAT（服务器映射）**：外网访问内网服务器，端口映射
- **ACL控制**：通过ACL规则控制哪些内网地址可以NAT转换

### 4. 核心协议与技术
- **OSPF**：动态路由协议，自动学习路由
- **VLANIF**：三层交换机虚拟接口，充当VLAN网关
- **静态路由**：手动配置路由条目，适用于小型网络
- **DHCP**：自动分配IP地址，减少手动配置

---

## 二、实操步骤

### A. 企业网络规划大作业步骤

#### 步骤1：需求分析与拓扑设计
1. 确定网络规模（多少部门、多少用户）
2. 设计三层架构：核心层→汇聚层→接入层
3. 画出网络拓扑图（使用ENSP模拟器）

#### 步骤2：IP地址规划
```
示例规划：
部门        VLAN    网段              网关
市场部      VLAN20  10.30.20.0/24    10.30.20.254
销售部      VLAN30  10.30.30.0/24    10.30.30.254
服务器区    VLAN10  10.30.10.0/24    10.30.10.254
互联链路    VLAN40  10.30.40.0/24    -
```

#### 步骤3：VLAN划分配置
```
# 三层交换机ACC1配置
[ACC1] vlan batch 10 20 30 40
[ACC1] interface Vlanif10
[ACC1-Vlanif10] ip address 10.30.10.254 255.255.255.0
[ACC1] interface Vlanif20
[ACC1-Vlanif20] ip address 10.30.20.254 255.255.255.0
[ACC1] interface Vlanif30
[ACC1-Vlanif30] ip address 10.30.30.254 255.255.255.0
[ACC1] interface Vlanif40
[ACC1-Vlanif40] ip address 10.30.40.254 255.255.255.0
```

#### 步骤4：静态路由配置
```
# ACC1 → Export（默认路由）
[ACC1] ip route-static 0.0.0.0 0.0.0.0 10.30.40.253

# Export → ACC1（回程路由）
[Export2] ip route-static 10.30.10.0 255.255.255.0 10.30.40.254
[Export2] ip route-static 10.30.20.0 255.255.255.0 10.30.40.254
[Export2] ip route-static 10.30.30.0 255.255.255.0 10.30.40.254

# Export → ISP（默认路由）
[Export2] ip route-static 0.0.0.0 0.0.0.0 1.30.1.254
```

#### 步骤5：NAT配置
```
# 创建ACL
[Export2] acl number 2000
[Export2-acl-basic-2000] rule 5 permit source any

# 地址池方式NAT
[Export2] nat address-group 1 100.255.2.2 100.255.2.10
[Export2] interface GigabitEthernet0/0/2
[Export2-GigabitEthernet0/0/2] nat outbound 2000 address-group 1

# 服务器端口映射
[Export2] nat server protocol tcp global 100.255.2.100 21 inside 10.30.10.100 21
[Export2] nat server protocol tcp global 100.255.2.101 80 inside 10.30.10.101 80
```

### B. WLAN配置步骤

#### 步骤1：VLAN与DHCP
```
# 配置AP管理VLAN100，AC作为DHCP服务器
[AC] dhcp enable
[AC] ip pool ap_pool
[AC-ip-pool-ap_pool] network 10.1.100.0 mask 255.255.255.0
[AC-ip-pool-ap_pool] gateway-list 10.1.100.1

# 无线业务VLAN101、102，SW1作为DHCP服务器
```

#### 步骤2：配置AP上线
```
# 创建AP组
[AC] wlan
[AC-wlan-view] ap-group name GYK
```

#### 步骤3：配置SSID和安全模板
```
# SSID模板
[AC-wlan-view] ssid-profile name GYK_Stu_dYB
[AC-wlan-ssid-prof-GYK_Stu_dYB] ssid GYK_Stu_dYB

# 安全模板
[AC-wlan-view] security-profile name GYK_Stu_dYB
[AC-wlan-sec-prof-GYK_Stu_dYB] security wpa-wpa2 pass-phrase GYK_Stu@123 aes
```

#### 步骤4：配置VAP模板并绑定
```
# VAP模板（隧道转发模式）
[AC-wlan-view] vap-profile name GYK_Stu_dYB
[AC-wlan-vap-prof-GYK_Stu_dYB] forward-mode tunnel
[AC-wlan-vap-prof-GYK_Stu_dYB] service-vlan vlan-id 101
[AC-wlan-vap-prof-GYK_Stu_dYB] ssid-profile GYK_Stu_dYB
[AC-wlan-vap-prof-GYK_Stu_dYB] security-profile GYK_Stu_dYB

# 绑定到AP组
[AC-wlan-view] ap-group name GYK
[AC-wlan-ap-group-GYK] vap-profile GYK_Stu_dYB wlan 1 radio 0
[AC-wlan-ap-group-GYK] vap-profile GYK_Stu_dYB wlan 1 radio 1
```

---

## 三、拓扑设计思路

### 1. 三层架构设计
```
核心层（Core）
  ├── 高速转发，冗余设计
  ├── 核心交换机/路由器
  │
汇聚层（Distribution）
  ├── VLAN间路由
  ├── 策略控制（ACL/QoS）
  ├── 三层交换机
  │
接入层（Access）
  ├── 用户接入
  ├── VLAN划分
  ├── 二层交换机/AP
```

### 2. WLAN旁挂组网
```
        互联网
          │
       出口路由器(AR1)
          │
    ┌─────┴─────┐
    │           │
   SW1        AC1
    │      (旁挂，管理AP)
    │           │
   AP ←─────────┘
    │
  用户(STA)
```

### 3. 设计要点
- **冗余性**：关键设备双链路、双电源
- **可扩展性**：IP地址预留空间，VLAN编号留余量
- **安全性**：VLAN隔离、ACL控制、NAT隐藏内网
- **性能**：核心层用三层交换机，避免瓶颈

---

## 四、配置要点速查

### 关键命令速查表

| 功能 | 命令 |
|------|------|
| 创建VLAN | `vlan batch 10 20 30` |
| 配置VLANIF地址 | `interface Vlanif10` → `ip address x.x.x.x mask` |
| 静态路由 | `ip route-static 目标网段 掩码 下一跳` |
| NAT地址池 | `nat address-group 1 起始IP 结束IP` |
| NAT出接口 | `interface G0/0/x` → `nat outbound 2000 address-group 1` |
| 服务器映射 | `nat server protocol tcp global 公网IP 端口 inside 内网IP 端口` |
| 查看NAT会话 | `display nat session` |
| 查看路由表 | `display ip routing-table` |
| 查看VLAN | `display vlan` |

---

## 五、常见问题

### Q1：三层交换机VLANIF接口ping不通？
**A**：检查VLAN是否创建、接口是否加入对应VLAN、VLANIF是否已开启（undo shutdown）。

### Q2：NAT配置后内网能上网但外网访问不了内网服务器？
**A**：检查`nat server`命令是否正确配置，确认公网IP是否在出口接口网段内，检查回程路由是否存在。

### Q3：AP无法上线？
**A**：检查AP能否通过DHCP获取IP地址，确认AC的源接口配置是否正确，检查AP序列号是否录入。

### Q4：静态路由配置后部分网段不通？
**A**：静态路由需要双向配置，不仅需要去程路由，也需要回程路由。使用`display ip routing-table`逐跳检查。

### Q5：无线用户能连接但无法上网？
**A**：检查用户VLAN的DHCP配置、网关配置，确认VAP模板中业务VLAN是否正确绑定。

---

## 六、速记口诀

### IP规划口诀
```
先定部门后分段，VLAN对应网段配；
网关地址取末尾，互联地址单独划；
预留空间好扩展，文档记录不能差。
```

### NAT配置口诀
```
ACL先开路，地址池来备；
出接口绑定它，映射靠nat server；
内转外用outbound，外转内用server；
测试先ping后访问，display session查会话。
```

### WLAN配置口诀
```
先建VLAN配DHCP，AP管理业务分；
SSID模板起名字，安全模板设密码；
VAP绑定三件套（SSID+安全+VLAN），AP组里radio配；
隧道转发保安全，测试上线看状态。
```

### 排错口诀
```
不通先查物理层，线缆接口要看清；
二层查VLAN和MAC，三层查路由和ACL；
逐跳ping来定位，display命令帮大忙。
```
