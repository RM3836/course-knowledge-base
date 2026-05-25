# 网络安全实验 知识库

本目录收录网络安全课程实验的核心知识点、实操步骤与速查手册。

## 文件列表

| 文件名 | 内容概要 |
|--------|----------|
| [01-Metasploitable3攻击.md](01-Metasploitable3攻击.md) | MS12-020 RDP漏洞、IIS重复参数请求DoS漏洞利用步骤 |
| [02-防火墙配置.md](02-防火墙配置.md) | 华为防火墙安全策略、NAT、双机热备、虚拟化防火墙配置 |
| [03-漏洞扫描.md](03-漏洞扫描.md) | Nmap/Dirb/Nikto等扫描工具使用、渗透测试信息收集、ShellShock漏洞利用 |
| [04-安全实验速查.md](04-安全实验速查.md) | 所有安全工具命令速查表，覆盖MSF、Nmap、防火墙CLI等 |

## 实验覆盖范围

- **Metasploitable3 靶机攻击**：MS12-020（RDP蓝屏）、MS10-065（IIS DoS）、ShellShock
- **防火墙配置**：安全区域划分、安全策略、源NAT/目的NAT/NAT Server、ASPF/ALG、双机热备（VRRP/HRP）、虚拟化防火墙（vsys）
- **漏洞扫描与信息收集**：Nmap端口扫描、Dirb目录爆破、enum4linux SMB枚举、Whois/DNS查询
- **渗透测试工具链**：Metasploit Framework、BurpSuite、Nikto、Amap、DirBuster

## 学习建议

1. 先通读 `04-安全实验速查.md`，建立工具命令全局认知
2. 按 `03 → 01 → 02` 的顺序学习，从信息收集到漏洞利用再到防御配置
3. 实验前确认靶机环境（Metasploitable3 / 华为eNSP）已就绪
