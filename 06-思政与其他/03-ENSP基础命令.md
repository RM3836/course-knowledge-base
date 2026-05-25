# 03-ENSP基础命令

## 一、VLAN配置

### 创建VLAN
```
[Switch] vlan 10
[Switch-vlan10] description Student-WiFi
[Switch-vlan10] quit

[Switch] vlan 20
[Switch-vlan20] description Guest-WiFi
```

### 配置Trunk链路
```
[Switch] interface GigabitEthernet 0/0/1
[Switch-GigabitEthernet0/0/1] port link-type trunk
[Switch-GigabitEthernet0/0/1] port trunk allow-pass vlan 10 20
```

### 配置Access端口
```
[Switch] interface Ethernet 0/0/1
[Switch-Ethernet0/0/1] port link-type access
[Switch-Ethernet0/0/1] port default vlan 10
```

### 配置VLANIF接口（三层交换机）
```
[Switch] interface Vlanif 10
[Switch-Vlanif10] ip address 10.30.10.254 255.255.255.0
[Switch-Vlanif10] quit

[Switch] interface Vlanif 20
[Switch-Vlanif20] ip address 10.30.20.254 255.255.255.0
```

## 二、STP配置

### 设置根桥
```
[Switch] stp root primary
```

### 设置优先级
```
[Switch] stp priority 4096
```

## 三、静态路由

### 配置静态路由
```
[Router] ip route-static 10.30.20.0 255.255.255.0 10.30.40.253
```

### 配置默认路由
```
[Router] ip route-static 0.0.0.0 0.0.0.0 10.30.40.254
```

### 配置浮动路由（备份链路）
```
[Router] ip route-static 0.0.0.0 0.0.0.0 10.30.40.253 preference 60
[Router] ip route-static 0.0.0.0 0.0.0.0 10.30.50.253 preference 80
```

## 四、RIP路由协议

### 启用RIP
```
[Router] rip 1
[Router-rip-1] version 2
[Router-rip-1] network 10.0.0.0
```

### 重发布默认路由到RIP
```
[Router] rip 1
[Router-rip-1] default-route originate
```

## 五、OSPF路由协议

### 启用OSPF
```
[Router] ospf 1 router-id 1.1.1.1
[Router-ospf-1] area 0
[Router-ospf-1-area-0.0.0.0] network 10.30.10.0 0.0.0.255
[Router-ospf-1-area-0.0.0.0] network 10.30.20.0 0.0.0.255
```

### 重发布默认路由到OSPF
```
[Router] ospf 1
[Router-ospf-1] default-route-advertise always
```

## 六、NAT配置

### 配置ACL
```
[Router] acl number 2000
[Router-acl-basic-2000] rule 5 permit source any
```

### 配置NAT地址池
```
[Router] nat address-group 1 100.255.2.2 100.255.2.10
```

### 配置NAT outbound（源地址转换）
```
[Router] interface GigabitEthernet 0/0/2
[Router-GigabitEthernet0/0/2] nat outbound 2000 address-group 1
```

### 配置NAT server（目的地址转换/端口映射）
```
# FTP服务映射
[Router] nat server protocol tcp global 100.255.2.100 21 inside 10.76.10.100 21

# HTTP服务映射
[Router] nat server protocol tcp global 100.255.2.101 80 inside 10.76.10.101 80
```

### 使用接口IP作为NAT转换地址
```
[Router] interface GigabitEthernet 0/0/2
[Router-GigabitEthernet0/0/2] nat outbound 2000
```

## 七、防火墙NAT配置

```
# 配置安全策略
[FW] security-policy
[FW-policy-security] rule name trust_to_untrust
[FW-policy-security-rule-trust_to_untrust] source-zone trust
[FW-policy-security-rule-trust_to_untrust] destination-zone untrust
[FW-policy-security-rule-trust_to_untrust] action permit

[FW-policy-security] rule name untrust_to_trust
[FW-policy-security-rule-untrust_to_trust] source-zone untrust
[FW-policy-security-rule-untrust_to_trust] destination-zone trust
[FW-policy-security-rule-untrust_to_trust] action permit

# 配置NAT
[FW] acl number 2000
[FW-acl-basic-2000] rule 5 permit source any
[FW] nat address-group 1 100.255.2.2 100.255.2.10
[FW] interface GigabitEthernet 1/0/2
[FW-GigabitEthernet1/0/2] nat outbound 2000 address-group 1
```

## 八、WLAN配置

### VLAN划分
```
[AC] vlan 100
[AC-vlan100] description AP-Management

[AC] vlan 101
[AC-vlan101] description Student-WiFi

[AC] vlan 102
[AC-vlan102] description Guest-WiFi
```

### DHCP配置
```
[AC] dhcp enable
[AC] ip pool ap-pool
[AC-ip-pool-ap-pool] gateway-list 10.1.100.1
[AC-ip-pool-ap-pool] network 10.1.100.0 mask 255.255.255.0
[AC-ip-pool-ap-pool] dns-list 8.8.8.8

[AC] interface Vlanif 100
[AC-Vlanif100] ip address 10.1.100.1 255.255.255.0
[AC-Vlanif100] dhcp select interface
```

### WLAN模板配置
```
# 域管理模板
[AC] wlan
[AC-wlan-view] regulatory-domain-profile name GYK
[AC-wlan-regulate-domain-GYK] country-code CN

# SSID模板
[AC-wlan-view] ssid-profile name GYK_Stu
[AC-wlan-ssid-prof-GYK_Stu] ssid GYK_Stu_dYB

[AC-wlan-view] ssid-profile name GYK_Guest
[AC-wlan-ssid-prof-GYK_Guest] ssid GYK_Guest

# 安全模板
[AC-wlan-view] security-profile name GYK_Stu
[AC-wlan-sec-prof-GYK_Stu] security wpa-wpa2 psk pass-phrase GKY_Stu@123 aes

[AC-wlan-view] security-profile name GYK_Guest
[AC-wlan-sec-prof-GYK_Guest] security wpa-wpa2 psk pass-phrase GKY_Guest@123 aes

# VAP模板
[AC-wlan-view] vap-profile name GYK_Stu
[AC-wlan-vap-prof-GYK_Stu] forward-mode tunnel
[AC-wlan-vap-prof-GYK_Stu] service-vlan vlan-id 101
[AC-wlan-vap-prof-GYK_Stu] ssid-profile GYK_Stu
[AC-wlan-vap-prof-GYK_Stu] security-profile GYK_Stu

[AC-wlan-view] vap-profile name GYK_Guest
[AC-wlan-vap-prof-GYK_Guest] forward-mode tunnel
[AC-wlan-vap-prof-GYK_Guest] service-vlan vlan-id 102
[AC-wlan-vap-prof-GYK_Guest] ssid-profile GYK_Guest
[AC-wlan-vap-prof-GYK_Guest] security-profile GYK_Guest

# AP组
[AC-wlan-view] ap-group name GYK
[AC-wlan-ap-group-GYK] vap-profile GYK_Stu wlan 1 radio 0
[AC-wlan-ap-group-GYK] vap-profile GYK_Guest wlan 2 radio 1
[AC-wlan-ap-group-GYK] regulatory-domain-profile GYK
```

## 九、常用查看命令

```
# 查看VLAN
display vlan

# 查看接口IP地址
display ip interface brief

# 查看路由表
display ip routing-table

# 查看NAT会话
display nat session

# 查看OSPF邻居
display ospf peer

# 查看RIP路由
display rip 1 route

# 查看AP状态
display ap all
```

## 十、验证测试

```
# 测试连通性
ping 10.30.20.1

# 追踪路由
tracert 8.8.8.8
```
