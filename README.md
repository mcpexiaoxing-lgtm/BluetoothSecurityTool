# IoT蓝牙安全测试工具 - 使用说明

## 📋 快速开始

### 方法1：本地构建（推荐，最快）

1. **安装Python**（如果还没有）
   - 下载：https://www.python.org/downloads/
   - 选择 Python 3.8 - 3.12 版本
   - ⚠️ **安装时勾选 "Add Python to PATH"**

2. **一键构建**
   - 双击运行 `build_local.bat`
   - 等待几分钟
   - 完成后会打开 `dist` 文件夹
   - 里面就是 `BluetoothSecurityTool.exe`！

### 方法2：GitHub Actions（需要Git推送）

1. 确保你的文件已推送到GitHub
2. 访问：https://github.com/mcpexiaoxing-lgtm/BluetoothSecurityTool/actions
3. 等待构建完成
4. 下载 Artifacts

---

## 📁 文件说明

```
BluetoothSecurityTool/
├── bluetooth_security_app.py    # 主程序
├── requirements.txt             # Python依赖
├── build_local.bat             # 本地一键构建脚本 ⭐
├── .github/workflows/build.yml # GitHub Actions配置
└── README.md                    # 本文件
```

---

## 🎯 工具功能

1. **蓝牙设备扫描**
   - 扫描经典蓝牙和BLE设备
   - 显示设备名称、MAC地址、信号强度

2. **安全评估**
   - 自动分析设备安全性
   - 标记高风险设备

3. **报告导出**
   - JSON格式
   - HTML格式
   - 文本格式

---

## ⚠️ 注意事项

- 需要电脑有蓝牙适配器
- Windows 10/11 系统
- 首次运行可能需要防火墙权限

---

## 🔧 故障排除

### Python未找到
- 重新安装Python，勾选"Add Python to PATH"
- 重启电脑

### 构建失败
- 确保网络连接正常（需要下载依赖）
- 尝试手动运行：
  ```cmd
  pip install bleak pyinstaller
  pyinstaller --onefile bluetooth_security_app.py
  ```

---

## 📞 需要帮助？

查看原始毕业设计文档或联系指导老师。
