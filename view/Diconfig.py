# 版本信息
Version = "V1.0.0"

# 电路仿真软件服务名称
disName = ["NI Application Web Server",
           "NI System Web Server",
           "NI Authentication Service",
           "NI Citadel 4 Service",
           "NI Variable Engine",
           "NI Device Loader",
           "NI Configuration Manager",
           "NI Domain Service",
           "NI Network Discovery",
           "NI mDNS Responder Service",
           "NI Time Synchronization",
           "NI PSP Service Locator",
           "NI PXI Resource Manager",
           "NI Service Locator",
           "NI System Web Server"]

# 必要开启服务名称
# 手动
man_safe = ['IP Helper',
            'Xbox Live 游戏保存']
# 自动
auto_safe = ['IKE and AuthIP IPsec Keying Modules',
             'TCP/IP NetBIOS Helper',
             'Xbox Accessory Management Service',
             'Xbox Live 身份验证管理器',
             'Xbox Live 网络服务']

# 注册表名称
para = ['AddrConfigControl',
        'DisabledComponents']

# 注册表地址
path = r'SYSTEM\CurrentControlSet\Services\Dnscache\Parameters'

# ping 列表
teredo_servers = [
    "win1910.ipv6.microsoft.com",
    "teredo.remlab.net",
    "teredo-debian.remlab.net",
    "teredo.autotrans.consulintel.com",
    "teredo.ipv6.microsoft.com",
    "teredo.ngix.ne.kr",
    "teredo.managemydedi.com",
    "teredo.trex.fi",
    "teredo.iks-jena.de"
]

# 命令
commands = [
    "Netsh int ter set state enterpriseclient",
    "netsh int teredo show state"
]

zhuce_commands = ["reg query HKLM\\System\\CurrentControlSet\\Services\\TcpIp6\\Parameters", 
                  "reg add HKLM\\System\\CurrentControlSet\\Services\\Tcpip6\\Parameters /v DisabledComponents /t REG_DWORD /d 0x0"]