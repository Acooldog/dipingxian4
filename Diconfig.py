# 版本信息
Version = "V1.1.2"

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
             'Xbox Live 网络服务',
             'Peer Networking Grouping']

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


# 微软的非显示服务名
Microsoft_server = ['AdobeUpdateService', 'AdskLicensingService', 'AJRouter', 'ALG', 'AntiCheatExpert Protection', 'AntiCheatExpert Service', 'AppIDSvc', 'Appinfo', 'AppMgmt', 'AppReadiness', 'AppVClient', 'AppXSvc', 'AssignedAccessManagerSvc', 'AudioEndpointBuilder', 'Audiosrv', 'autotimesvc', 'AxInstSV', 'BaiduNetdiskUtility', 'battlenet_helpersvc', 'BDESVC', 'BEService', 'BFE', 'BITS', 'Bonjour Service', 'BrokerInfrastructure', 'BTAGService', 'BthAvctpSvc', 'bthserv', 'camsvc', 'CDPSvc', 'CertPropSvc', 'ClipSVC', 'cloudidsvc', 'COMSysApp', 'CoreMessagingRegistrar', 'CryptSvc', 'CscService', 'DcomLaunch', 'dcsvc', 'debugregsvc', 'defragsvc', 'DeliUSBPnP', 'DeveloperToolsService', 'DeviceAssociationService', 'DeviceInstall', 'DevQueryBroker', 'Dhcp', 'diagnosticshub.standardcollector.service', 'diagsvc', 'DiagTrack', 'DialogBlockingService', 'DispBrokerDesktopSvc', 'DisplayEnhancementService', 'DmEnrollmentSvc', 'dmwappushservice', 'Dnscache', 'DoSvc', 'dot3svc', 'DouyinElevationService', 'DPS', 'DsmSvc', 'DsSvc', 'DusmSvc', 'EAAntiCheatService', 'EABackgroundService', 'EapHost', 'EasyAntiCheat', 'EasyAntiCheat_EOS', 'edgeupdate', 'edgeupdatem', 'EFS', 'embeddedmode', 'EntAppSvc', 'EpicOnlineServices', 'EventLog', 'EventSystem', 'Everything', 'Fax', 'fdPHost', 'FDResPub', 'fhsvc', 'Flash Helper Service', 'FlashCenterSvc', 'FlexNet Licensing Service', 'FontCache', 'FontCache3.0.0.0', 'fp2psrv', 'FrameServer', 'FrameServerMonitor', 'FvSvc', 'GameInput Service', 'GameInputSvc', 'GameViewerService', 'GamingServices', 'GamingServicesNet', 'GoogleChromeElevationService', 'GoogleUpdaterInternalService132.0.6833.0', 'GoogleUpdaterService132.0.6833.0', 'gpsvc', 'GraphicsPerfSvc', 'gupdate', 'gupdatem', 'hidserv', 'HvHost', 'icssvc', 'iGameCenterService', 'IKEEXT', 'InstallService', 'InventorySvc', 'iphlpsvc', 'IpxlatCfgSvc', 'jhi_service', 'KeyIso', 'KtmRm', 'LanmanServer', 'LanmanWorkstation', 'LDPlayerSvr', 'lfsvc', 'LicenseManager', 'lltdsvc', 'lmhosts', 'LSM', 'LxpSvc', 'MapsBroker', 'McpManagementService', 'MicrosoftEdgeElevationService', 'MixedRealityOpenXRSvc', 'mpssvc', 'MSDTC', 'MSiSCSI', 'msiserver', 'MsKeyboardFilter', 'NaturalAuthentication', 'NcaSvc', 'NcbService', 'NcdAutoSetup', 'NefariusVirtualPadDriverService', 'Netlogon', 'Netman', 'netprofm', 'NetSetupSvc', 'NetTcpPortSharing', 'NetworkDaemon', 'NgcCtnrSvc', 'NgcSvc', 'NlaSvc', 'nsi', 'NvBroadcast.ContainerLocalSystem', 'NvContainerLocalSystem', 'NVDisplay.ContainerLocalSystem', 'OVRLibraryService', 'OVRService', 'p2pimsvc', 'p2psvc', 'PcaSvc', 'PCManager Service Store', 'PeerDistSvc', 'perceptionsimulation', 'PerfHost', 'PgyVPNService', 'PhoneSvc', 'phpStudySrv', 'pla', 'PlugPlay', 'PnkBstrA', 'PnkBstrB', 'PNRPAutoReg', 'PNRPsvc', 'PolicyAgent', 'Power', 'PrintNotify', 'ProfSvc', 'PSBCInputService', 'PushToInstall', 'QiyiService', 'QMEmulatorService', 'QQGameService',
                    'QQMicroGameBoxService', 'QWAVE', 'RasAuto', 'RasMan', 'RemoteAccess', 'RemoteRegistry', 'RetailDemo', 'RmSvc', 'Rockstar Service', 'RpcEptMapper', 'RpcLocator', 'RpcSs', 'RtkAudioUniversalService', 'SamSs', 'SCardSvr', 'ScDeviceEnum', 'Schedule', 'SCPolicySvc', 'SDRSVC', 'seclogon', 'SecurityHealthService', 'SEMgrSvc', 'SENS', 'Sense', 'SensorDataService', 'SensorService', 'SensrSvc', 'SessionEnv', 'SgrmBroker', 'SharedAccess', 'SharedRealitySvc', 'ShellHWDetection', 'shpamsvc', 'smphost', 'SmsRouter', 'SNMPTrap', 'spectrum', 'Spooler', 'sppsvc', 'SQLWriter', 'SSDPSRV', 'ssh-agent', 'sshd', 'SshdBroker', 'SstpSvc', 'StateRepository', 'Steam Client Service', 'StiSvc', 'StorSvc', 'SunloginService', 'svsvc', 'swprv', 'SysMain', 'SystemEventsBroker', 'TapiSrv', 'TermService', 'TextInputManagementService', 'Themes', 'TieringEngineService', 'TimeBrokerSvc', 'ToDesk_Service', 'TokenBroker', 'TrkWks', 'TroubleshootingSvc', 'TrustedInstaller', 'tzautoupdate', 'UevAgentService', 'uhssvc', 'UmRdpService', 'Updater', 'upnphost', 'UserManager', 'UsoSvc', 'VacSvc', 'VaultSvc', 'vds', 'vgc', 'VirtualDesktop.Service.exe', 'vivoesService', 'VivoSyncService', 'vivo_remote_watch.exe', 'VMAuthdService', 'vmicguestinterface', 'vmicheartbeat', 'vmickvpexchange', 'vmicrdv', 'vmicshutdown', 'vmictimesync', 'vmicvmsession', 'vmicvss', 'VMnetDHCP', 'VMUSBArbService', 'VMware NAT Service', 'VRLService', 'VSInstallerElevationService', 'VSS', 'VSStandardCollectorService150', 'w32time', 'WaaSMedicSvc', 'WalletService', 'Wallpaper Engine Service', 'WarpJITSvc', 'wbengine', 'WbioSrvc', 'Wcmsvc', 'wcncsvc', 'WDDriveService', 'WdiServiceHost', 'WdiSystemHost', 'WdNisSvc', 'WebClient', 'WebManagement', 'webthreatdefsvc', 'Wecsvc', 'WEPHOSTSVC', 'wercplsupport', 'WerSvc', 'WeType Management Service', 'WFDSConMgrSvc', 'WiaRpc', 'WinDefend', 'WinHttpAutoProxySvc', 'Winmgmt', 'WinRM', 'wisvc', 'WlanSvc', 'wlidsvc', 'wlpasvc', 'WManSvc', 'wmiApSrv', 'WMIRegistrationService', 'WMPNetworkSvc', 'workfolderssvc', 'WpcMonSvc', 'WPDBusEnum', 'WpnService', 'wpscloudsvr', 'wscsvc', 'WSearch', 'wuauserv', 'WwanSvc', 'XblAuthManager', 'XblGameSave', 'XboxGipSvc', 'XboxNetApiSvc', 'XLServicePlatform', 'AarSvc_47637c', 'BcastDVRUserService_47637c', 'BluetoothUserService_47637c', 'CaptureService_47637c', 'cbdhsvc_47637c', 'CDPUserSvc_47637c', 'CloudBackupRestoreSvc_47637c', 'ConsentUxUserSvc_47637c', 'CredentialEnrollmentManagerUserSvc_47637c', 'DeviceAssociationBrokerSvc_47637c', 'DevicePickerUserSvc_47637c', 'DevicesFlowUserSvc_47637c', 'MessagingService_47637c', 'NPSMSvc_47637c', 'OneSyncSvc_47637c', 'P9RdrService_47637c', 'PenService_47637c', 'PimIndexMaintenanceSvc_47637c', 'PrintWorkflowUserSvc_47637c', 'UdkUserSvc_47637c', 'UnistoreSvc_47637c', 'UserDataSvc_47637c', 'WebManagementUser_47637c', 'webthreatdefusersvc_47637c', 'WpnUserService_47637c']

# 微软的显示服务名
Microsoft_display_service = ['AdobeUpdateService', 'Autodesk Desktop Licensing Service', 'AllJoyn Router Service', 'Application Layer Gateway Service', 'AntiCheatExpert Protection', 'AntiCheatExpert Service', 'Application Identity', 'Application Information', 'Application Management', 'App Readiness', 'Microsoft App-V Client', 'AppX Deployment Service (AppXSVC)', 'AssignedAccessManager 服务', 'Windows Audio Endpoint Builder', 'Windows Audio', '手机网络时间', 'ActiveX Installer (AxInstSV)', 'BaiduNetdiskUtility', 'Battle.net Update Helper Svc', 'BitLocker Drive Encryption Service', 'BattlEye Service', 'Base Filtering Engine', 'Background Intelligent Transfer Service', 'Bonjour 服务', 'Background Tasks Infrastructure Service', '蓝牙音频网关服务', 'AVCTP 服务', '蓝牙支持服务', '功能访问管理器服务', '连接设备平台服务', 'Certificate Propagation', 'Client License Service (ClipSVC)', 'Microsoft 云标识服务', 'COM+ System Application', 'CoreMessaging', 'Cryptographic Services', 'Offline Files', 'DCOM Server Process Launcher', '已声明的配置(DC)服务', 'debugregsvc', 'Optimize drives', 'DeliUSBPnP', 'Developer Tools Service', 'Device Association Service', 'Device Install Service', 'DevQuery Background Discovery Broker', 'DHCP Client', 'Microsoft (R) 诊断中心标准收集器服务', 'Diagnostic Execution Service', 'Connected User Experiences and Telemetry', 'DialogBlockingService', '显示策略服务', '显示增强服务', '设备管理注册服务', '设备管理无线应用程序协议 (WAP) 推送消息路由服务', 'DNS Client', 'Delivery Optimization', 'Wired AutoConfig', 'Douyin Elevation Service (DouyinElevationService)', 'Diagnostic Policy Service', 'Device Setup Manager', 'Data Sharing Service', '数据使用量', 'EAAntiCheatService', 'EABackgroundService', 'Extensible Authentication Protocol', 'EasyAntiCheat', 'Easy Anti-Cheat (Epic Online Services)', 'Microsoft Edge Update Service (edgeupdate)', 'Microsoft Edge Update Service (edgeupdatem)', 'Encrypting File System (EFS)', '嵌入模式', 'Enterprise App Management Service', 'Epic Online Services', 'Windows Event Log', 'COM+ Event System', 'Everything', 'Fax', 'Function Discovery Provider Host', 'Function Discovery Resource Publication', 'File History Service', 'Flash Helper Service', 'FlashCenterSvc', 'FlexNet Licensing Service', 'Windows Font Cache Service', 'Windows Presentation Foundation Font Cache 3.0.0.0', 'fp2psrv', 'Windows Camera Frame Server', 'Windows Camera Frame Server Monitor', 'NVIDIA FrameView SDK service', 'GameInput Service', 'GameInput Service', 'GameViewerService', 'Gaming Services', 'Gaming Services', 'Google Chrome Elevation Service (GoogleChromeElevationService)', 'Google 更新程序内部服务 (GoogleUpdaterInternalService132.0.6833.0)', 'Google 更新程序服务 (GoogleUpdaterService132.0.6833.0)', 'Group Policy Client', 'GraphicsPerfSvc', 'Google 更新服务 (gupdate)', 'Google 更新服务 (gupdatem)', 'Human Interface Device Service', 'HV 主机服务', 'Windows 移动热点服务', 'iGameCenter Service', 'IKE and AuthIP IPsec Keying Modules', 'Microsoft Store 安装服务', '清单和兼容性评估服务', 'IP Helper', 'IP 转换配置服务', 'Intel(R) Dynamic Application Loader Host Interface Service', 'CNG Key Isolation', 'KtmRm for Distributed Transaction Coordinator', 'Server', 'Workstation', 'LeiDian', 'Geolocation Service', 'Windows 许可证管理器服务', 'Link-Layer Topology Discovery Mapper', 'TCP/IP NetBIOS Helper', 'Local Session Manager', '语言体验服务', 'Downloaded Maps Manager', 'McpManagementService', 'Microsoft Edge Elevation Service (MicrosoftEdgeElevationService)', 'Windows Mixed Reality OpenXR 服务', 'Windows Defender Firewall', 'Distributed Transaction Coordinator', 'Microsoft iSCSI Initiator Service', 'Windows Installer', 'Microsoft 键盘筛选器', '自然身份验证', 'Network Connectivity Assistant', 'Network Connection Broker', 'Network Connected Devices Auto-Setup', 'Nefarius VirtualPad Driver Service', 'Netlogon', 'Network Connections', 'Network List Service', 'Network Setup Service', 'Net.Tcp Port Sharing Service', 'NetworkDaemon', 'Microsoft Passport Container', 'Microsoft Passport', '网络位置感知', 'Network Store Interface Service', 'NVIDIA Broadcast LocalSystem Container', 'NVIDIA LocalSystem Container', 'NVIDIA Display Container LS', 'Oculus VR Library Service', 'Oculus VR Runtime Service', 'Peer Networking Identity Manager', 'Peer Networking Grouping', 'Program Compatibility Assistant Service', 'MSPCManager Service (Store)', 'BranchCache', 'Windows 感知模拟服务', 'Performance Counter DLL Host', 'PgyVPNService', 'Phone Service', 'phpstudy服务', 'Performance Logs & Alerts', 'Plug and Play', 'PnkBstrA', 'PnkBstrB', 'PNRP Machine Name Publication Service', 'Peer Name Resolution Protocol', 'IPsec Policy Agent', 'Power', 'Printer Extensions and Notifications', 'User Profile Service', 'PSBCInputService',
                             'Windows PushToInstall 服务', 'IQIYI Video Platform Service', 'QMEmulatorService', 'QQGameService', 'QQMicroGameBoxService', 'Quality Windows Audio Video Experience', 'Remote Access Auto Connection Manager', 'Remote Access Connection Manager', 'Routing and Remote Access', 'Remote Registry', '零售演示服务', '无线电管理服务', 'Rockstar Game Library Service', 'RPC Endpoint Mapper', 'Remote Procedure Call (RPC) Locator', 'Remote Procedure Call (RPC)', 'Realtek Audio Universal Service', 'Security Accounts Manager', 'Smart Card', 'Smart Card Device Enumeration Service', 'Task Scheduler', 'Smart Card Removal Policy', 'Windows 备份', 'Secondary Logon', 'Windows 安全中心服务', '付款和 NFC/SE 管理器', 'System Event Notification Service', 'Windows Defender Advanced Threat Protection Service', 'Sensor Data Service', 'Sensor Service', 'Sensor Monitoring Service', 'Remote Desktop Configuration', 'System Guard 运行时监视代理', 'Internet Connection Sharing (ICS)', '空间数据服务', 'Shell Hardware Detection', 'Shared PC Account Manager', 'Microsoft Storage Spaces SMP', 'Microsoft Windows SMS 路由器服务。', 'SNMP 陷阱', 'Windows 感知服务', 'Print Spooler', 'Software Protection', 'SQL Server VSS Writer', 'SSDP Discovery', 'OpenSSH Authentication Agent', 'OpenSSH SSH Server', 'SshdBroker', 'Secure Socket Tunneling Protocol Service', 'State Repository Service', 'Steam Client Service', 'Windows Image Acquisition (WIA)', 'Storage Service', 'SunloginService', 'Spot Verifier', 'Microsoft Software Shadow Copy Provider', 'SysMain', 'System Events Broker', 'Telephony', 'Remote Desktop Services', 'Text Input Management Service', 'Themes', 'Storage Tiers Management', 'Time Broker', 'ToDesk Service', 'Web 帐户管理器', 'Distributed Link Tracking Client', '建议疑难解答服务', 'Windows Modules Installer', '自动时区更新程序', 'User Experience Virtualization Service', 'Microsoft Update Health Service', 'Remote Desktop Services UserMode Port Redirector', 'Updater', 'UPnP Device Host', 'User Manager', '更新 Orchestrator 服务', '立 体音频组合器服务', 'Credential Manager', 'Virtual Disk', 'vgc', 'Virtual Desktop Service', 'vivoesService', 'VivoSyncService', 'vivo_remote_watch', 'VMware Authorization Service', 'Hyper-V Guest Service Interface', 'Hyper-V Heartbeat Service', 'Hyper-V Data Exchange Service', 'Hyper-V 远程桌面 虚拟化服务', 'Hyper-V Guest Shutdown Service', 'Hyper-V Time Synchronization Service', 'Hyper-V PowerShell Direct Service', 'Hyper-V 卷影复制请求程序', 'VMware DHCP Service', 'VMware USB Arbitration Service', 'VMware NAT Service', 'VRLService', 'Visual Studio Installer Elevation Service', 'Volume Shadow Copy', 'Visual Studio Standard Collector Service 150', 'Windows Time', 'WaaSMedicSvc', 'WalletService', 'Wallpaper Engine Service', 'Warp JIT Service', 'Block Level Backup Engine Service', 'Windows Biometric Service', 'Windows Connection Manager', 'Windows Connect Now - Config Registrar', 'WD Drive Manager', 'Diagnostic Service Host', 'Diagnostic System Host', 'Microsoft Defender Antivirus Network Inspection Service', 'WebClient', 'Web Management', 'Web 威胁防御服务', 'Windows Event Collector', 'Windows Encryption Provider Host Service', 'Problem Reports Control Panel Support', 'Windows Error Reporting Service', 'WeType Management Service', 'WLAN Direct 服务连接管理器服务', 'Still Image Acquisition Events', 'Microsoft Defender Antivirus Service', 'WinHTTP Web Proxy Auto-Discovery Service', 'Windows Management Instrumentation', 'Windows Remote Management (WS-Management)', 'Windows 预览体验成员服务', 'WLAN AutoConfig', 'Microsoft Account Sign-in Assistant', '本地配置文件助手服务', 'Windows 管理服务', 'WMI Performance Adapter', 'Intel(R) Management Engine WMI Provider Registration', 'Windows Media Player Network Sharing Service', 'Work Folders', '家长控制', 'Portable Device Enumerator Service', 'Windows 推送通知系统服务', 'WPS Office Cloud Service', '安全中心', 'Windows Search', 'Windows 更新', 'WWAN AutoConfig', 'Xbox Live 身份验证管理器', 'Xbox Live 游戏保存', 'Xbox Accessory Management Service', 'Xbox Live 网络服务', '迅雷下载基础服务（用于 快速申请磁盘空间及接管浏览器下载请求）', 'Agent Activation Runtime_47637c', 'GameDVR 和广播用户服务_47637c', '蓝牙用户支持服务_47637c', 'CaptureService_47637c', '剪贴板用户服务_47637c', '连接设备平台用户服务_47637c', '云备份和还原服务_47637c', 'ConsentUX 用户服务_47637c', 'CredentialEnrollmentManagerUserSvc_47637c', 'DeviceAssociationBroker_47637c', 'DevicePicker_47637c', 'DevicesFlow_47637c', 'MessagingService_47637c', 'NPSMSvc_47637c', '同步主机_47637c', 'P9RdrService_47637c', 'PenService_47637c', 'Contact Data_47637c', 'PrintWorkflow_47637c', 'Udk 用户服务_47637c', 'User Data Storage_47637c', 'User Data Access_47637c', 'WebManagementUser_47637c', 'Web 威胁防御用户服务_47637c', 'Windows Push Notifications User Service_47637c']

# 非微软服务 我自己的
my_services = [
    "AdobeUpdateService",
    "Autodesk Desktop Licensing Service",
    "AntiCheatExpert Protection",
    "AntiCheatExpert Service",
    "BaiduNetdiskUtility",
    "Battle.net Update Helper Svc",
    "BattlEye Service",
    "Bonjour 服务",
    "DeliUSBPNP",
    "Douyin Elevation Service (DouyinElevationService)",
    "EAAntiCheatService",
    "EABackgroundService",
    "EasyAntiCheat",
    "Easy Anti - Cheat (Epic Online services)",
    "Epic Online Services",
    "Everything",
    "Flash Helper Service",
    "FlashCenterSvc",
    "FlexNet Licensing Service",
    "fp2psrv",
    "NVIDIA FrameView SDK service",
    "GameViewerService",
    "Google Chrome Elevation Service (GoogleChromeElevationService)",
    "Google 更新程序内部服务 (GoogleUpdaterinternalService132.0.6833.0)",
    "Google 更新程序服务 (GoogleUpdaterService132.0.6833.0)",
    "Google 更新服务 (gupdate)",
    "Google 更新服务 (gupdatem)",
    "iGameCenter Service",
    "Intel(R) Dynamic Application Loader Host Interface Service",
    "LeiDian",
    "Nefarius VirtualPad Driver Service",
    "NVIDIA Broadcast LocalSystem Container",
    "NVIDIA LocalSystem Container",
    "NVIDIA Display Container LS",
    "Oculus VR Library Service",
    "Oculus VR Runtime Service",
    "MSPCManager Service (Store)",
    "phpstudy服务",
    "PSBCInputService",
    "IQIYI Video Platform Service",
    "QMEmulatorService",
    "QQGameService",
    "QQMicroGameBoxService",
    "Rockstar Game Library Service",
    "Realtek Audio Universal Service",
    "OpenSSH SSH Server",
    "Steam Client Service",
    "SunloginService",
    "ToDesk Service",
    "Updater",
    "vgc",
    "Virtual Desktop Service",
    "vivoesService",
    "VivoSyncService",
    "vivo_remote_watch",
    "VMware Authorization Service",
    "VMware DHCP Service",
    "VMware USB Arbitration Service",
    "VMware NAT Service",
    "VRLService",
    "Wallpaper Engine Service",
    "WD Drive Manager",
    "WeType Management Service",
    "Intel(R) Management Engine WMI Provider Registration",
    "WPS Office Cloud Service"
]