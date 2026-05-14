# GitHub 在线编译 - 完整操作指南

## 📋 概述

通过GitHub Actions自动编译，你将获得：
- ✅ BluetoothSecurity_x86.exe (32位)
- ✅ BluetoothSecurity_x64.exe (64位)
- ✅ BluetoothSecurity_Universal.exe (通用版)

---

## 🚀 5分钟快速上手

### 第一步：创建GitHub账号

1. 访问 https://github.com/
2. 点击 "Sign up"
3. 完成注册和邮箱验证

---

### 第二步：创建新仓库

1. 登录后，点击右上角 "+" → "New repository"
2. 填写信息：
   - **Repository name**: `BluetoothSecurityTool`
   - **Description**: `IoT蓝牙安全测试工具`
   - **Private/Public**: 选择 Private（私有）或者 Public（公开）
3. 点击 "Create repository"

---

### 第三步：上传文件

**方法A：网页上传（最简单）**

1. 在仓库页面，点击 "uploading an existing file"
2. 将我创建的所有文件拖入上传区域
3. 需要的文件：
   ```
   bluetooth_security_app.py
   requirements.txt
   .github/workflows/build.yml
   ```
4. 点击 "Commit changes"

**方法B：使用Git命令**

```bash
# 1. 克隆空仓库
git clone https://github.com/YOUR_USERNAME/BluetoothSecurityTool.git
cd BluetoothSecurityTool

# 2. 复制文件
# 将 bluetooth_security_app.py, requirements.txt 复制到此处

# 3. 创建.github/workflows目录
mkdir -p .github/workflows

# 4. 复制build.yml到该目录
# 将build.yml复制到 .github/workflows/ 目录

# 5. 提交并推送
git add .
git commit -m "Initial commit"
git push origin main
```

---

### 第四步：触发自动构建

推送代码后，GitHub Actions会自动开始构建！

1. 进入仓库页面
2. 点击 **"Actions"** 标签
3. 看到 "Build Windows Executables" 工作流正在运行
4. 等待 3-5 分钟构建完成

---

### 第五步：下载EXE文件

**方法1：从Releases下载（推荐）**

1. 进入仓库 → 点击 **"Releases"** (右侧边栏)
2. 点击 "Create a new release"（如果没有自动创建）
3. 填写：
   - **Tag version**: `v1.0`
   - **Release title**: `IoT蓝牙安全测试工具 v1.0`
4. 点击 "Publish release"
5. 在 "Assets" 部分下载EXE文件

**方法2：从Artifacts下载**

1. 点击 **"Actions"** 标签
2. 点击构建任务名称
3. 点击 Artifacts 部分
4. 下载ZIP文件

---

## 🎯 完整操作流程图

```
创建GitHub账号
     ↓
创建新仓库 (BluetoothSecurityTool)
     ↓
上传3个文件
  - bluetooth_security_app.py
  - requirements.txt
  - .github/workflows/build.yml
     ↓
自动触发构建 (Actions)
     ↓
等待3-5分钟
     ↓
下载EXE文件
  ✅ x86版本
  ✅ x64版本
  ✅ Universal版本
```

---

## 🔧 自定义配置

### 修改仓库名称

如果你想用其他名称：
1. 仓库设置 → Options → Repository name
2. 改名为你想要的名称
3. 更新 `README.md` 中的链接

### 更新下载链接

在 `README.md` 中搜索 `YOUR_USERNAME`，替换为你的GitHub用户名：
```markdown
# 把这个
https://github.com/YOUR_USERNAME/BluetoothSecurityTool/releases

# 改成这样
https://github.com/你的用户名/BluetoothSecurityTool/releases
```

---

## ❓ 常见问题

### Q: 构建失败了怎么办？

**A:** 检查以下几点：
1. 是否正确上传了所有文件？
2. 文件路径是否正确？
3. 查看 Actions 日志中的错误信息

### Q: 找不到下载链接？

**A:** 
1. 确认构建是否成功（绿色勾选）
2. 可能需要手动创建Release
3. 或者直接从Artifacts下载

### Q: 构建时间太长？

**A:** 正常构建需要3-5分钟，耐心等待即可。

### Q: 如何更新程序？

**A:**
1. 修改 `bluetooth_security_app.py`
2. 提交并推送
3. GitHub会自动重新构建

---

## 📞 获取帮助

如果遇到问题：
1. 查看 Actions 日志
2. 检查文件是否正确上传
3. 搜索GitHub相关问题

---

## 🎉 完成后

你将拥有：
- ✅ 32位EXE文件
- ✅ 64位EXE文件
- ✅ 通用EXE文件
- ✅ 在线自动构建服务

以后更新代码只需要：
1. 修改代码
2. 推送
3. 自动生成新EXE

祝你成功！🎓
