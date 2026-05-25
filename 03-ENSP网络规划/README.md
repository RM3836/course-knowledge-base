# 03-ENSP网络规划

本模块包含ENSP网络规划与设计的完整知识体系，涵盖园区网VLAN规划、路由协议配置、NAT配置以及WLAN无线网络规划。

## 目录

### WLAN无线网络规划

校园无线网覆盖项目，采用WLAN二层/三层旁挂组网方式，涵盖：
- **需求分析**：校园无线网络升级背景、覆盖范围与速度提升
- **IP地址规划**：AP管理地址池、用户业务地址池
- **VLAN设计**：AP管理VLAN 100、学生业务VLAN 101、访客业务VLAN 102
- **设备配置**：
  - VLAN划分与DHCP配置
  - AP上线配置
  - SSID模板（GYK_Stu、GYK_Guest）
  - 安全模板（WPA-WPA2加密）
  - VAP模板（隧道转发模式）
  - AP组配置（2.4GHz/5GHz双频）
- **测试验证**：AP上线测试、用户连接与连通性测试

## 核心知识点

| 知识点 | 说明 |
|--------|------|
| 旁挂组网 | AP网关在AC上，用户网关在交换机上，用户流量经过AC |
| DHCP分配 | AC为AP分配IP，SW1为用户分配IP |
| 隧道转发 | 用户数据通过CAPWAP隧道转发到AC |
| 双频配置 | Radio 0为2.4GHz，Radio 1为5GHz |
| 安全策略 | WPA-WPA2 + AES加密 |

## 关键配置示例

```
# AP管理VLAN
vlan 100
 description AP-Management

# 无线业务VLAN
vlan 101
 description Student-WiFi
vlan 102
 description Guest-WiFi

# DHCP地址池
ip pool ap-pool
 gateway-list 10.1.100.1
 network 10.1.100.0 mask 255.255.255.0

# SSID模板
wlan ssid-profile name GYK_Stu
 ssid GYK_Stu_dYB

# 安全模板
wlan security-profile name GYK_Stu
 security wpa-wpa2 psk pass-phrase GKY_Stu@123 aes

# VAP模板
wlan vap-profile name GYK_Stu
 forward-mode tunnel
 service-vlan vlan-id 101
 ssid-profile GYK_Stu
 security-profile GYK_Stu
```

## 参考资料

- 来源：网络规划和设计大作业（实验6）
- 设备：华为AC控制器、AP、交换机
