# IoT蓝牙安全测试工具 - Windows版

![Build Status](https://github.com/YOUR_USERNAME/BluetoothSecurityTool/actions/workflows/build.yml/badge.svg)
![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows%2010%2F11-blue.svg)

## 📦 下载已编译的EXE文件

**点击以下链接下载：**

### 🎯 直接下载

| 版本 | 架构 | 下载链接 | 文件大小 |
|------|------|---------|---------|
| **Universal** | 通用版 | [Download](https://github.com/YOUR_USERNAME/BluetoothSecurityTool/releases) | ~25 MB |
| **x86** | 32位 | [Download](https://github.com/YOUR_USERNAME/BluetoothSecurityTool/releases) | ~15 MB |
| **x64** | 64位 | [Download](https://github.com/YOUR_USERNAME/BluetoothSecurityTool/releases) | ~15 MB |

> ⚠️ 如果看不到下载链接，请先阅读下面的"如何使用"部分

---

## 🎯 功能特点

- ✅ **跨架构支持** - 同时提供32位和64位版本
- ✅ **无需安装** - 直接双击运行
- ✅ **中文界面** - 全中文操作界面
- ✅ **安全评估** - 智能风险评估
- ✅ **详细报告** - 支持JSON/HTML/TXT格式导出

---

## 🖥️ 系统要求

| 要求 | 说明 |
|------|------|
| 操作系统 | Windows 10 或 Windows 11 |
| 架构 | x86 (32位) 或 x64 (64位) |
| 内存 | 至少 2GB RAM |
| 蓝牙 | 需要支持蓝牙的适配器（可选） |

---

## 🚀 如何使用

### 方法1：下载Releases（推荐）

1. 点击页面顶部的 **"Releases"** 或 [查看所有Releases](https://github.com/YOUR_USERNAME/BluetoothSecurityTool/releases)
2. 下载最新版本
3. 解压（如果是ZIP）
4. 双击运行 `.exe` 文件

### 方法2：从Actions下载

1. 点击 **"Actions"** 标签
2. 选择最新的构建任务
3. 下载构建产物

---

## 🔧 从源码构建（高级用户）

如果你想自己构建：

```bash
# 1. 克隆仓库
git clone https://github.com/YOUR_USERNAME/BluetoothSecurityTool.git
cd BluetoothSecurityTool

# 2. 安装依赖
pip install -r requirements.txt

# 3. 构建
pyinstaller --onefile bluetooth_security_app.py

# 4. 找到EXE文件
# 位置: dist\bluetooth_security_app.exe
```

---

## 📋 功能列表

1. **设备扫描**
   - 经典蓝牙设备发现
   - BLE低功耗蓝牙设备发现
   - 设备指纹识别

2. **安全评估**
   - 自动风险评估
   - 设备名称分析
   - MAC地址检查

3. **报告生成**
   - JSON格式报告
   - HTML格式报告
   - 文本格式报告

4. **配置建议**
   - 安全加固建议
   - 最佳实践指南

---

## ⚠️ 注意事项

1. **首次运行**可能需要管理员权限
2. **杀毒软件**可能误报，请添加信任
3. **蓝牙功能**需要系统有蓝牙适配器
4. 仅用于**授权的安全测试**

---

## 📜 许可证

本项目仅供学习研究使用。

---

## 👨‍💻 作者

赣州职业技术学院 - 信息安全2312班

---

## 🔗 相关链接

- [毕业设计论文](../thesis/)
- [Android版本](../android_tool/)
- [工具集合](../tools/)

---

**⭐ 如果这个项目对你有帮助，请给个Star！**
