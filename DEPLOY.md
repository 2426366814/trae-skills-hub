# Trae Skills Hub 部署指南

> 详细的部署说明，支持本地部署、新机器部署和团队协作部署

## 📋 目录

1. [快速部署](#快速部署)
2. [本地部署](#本地部署)
3. [新机器部署](#新机器部署)
4. [团队协作部署](#团队协作部署)
5. [Docker部署](#docker部署)
6. [故障排除](#故障排除)

---

## 快速部署

### 5分钟快速开始

```bash
# 1. 克隆仓库
git clone https://github.com/yourusername/trae-skills-hub.git
cd trae-skills-hub

# 2. 运行安装脚本
# Windows:
.\install.ps1

# Linux/Mac:
bash install.sh

# 3. 验证安装
python trae-manager/tools/trae_manager.py check-env
```

**✅ 完成！现在可以使用所有Trae功能了。**

---

## 本地部署

### 环境准备

#### Windows

```powershell
# 1. 安装Chocolatey（如果尚未安装）
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# 2. 使用Chocolatey安装依赖
choco install nodejs python git -y

# 3. 验证安装
node --version  # v18+
python --version  # 3.9+
git --version  # 2.30+
```

#### macOS

```bash
# 1. 安装Homebrew（如果尚未安装）
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. 使用Homebrew安装依赖
brew install node python git

# 3. 验证安装
node --version
python3 --version
git --version
```

#### Linux (Ubuntu/Debian)

```bash
# 1. 更新包列表
sudo apt update

# 2. 安装依赖
sudo apt install -y nodejs npm python3 python3-pip git

# 3. 验证安装
node --version
python3 --version
git --version
```

### 安装步骤

```bash
# 1. 克隆仓库
git clone https://github.com/yourusername/trae-skills-hub.git
cd trae-skills-hub

# 2. 安装Python依赖
pip install pyyaml

# 3. 运行安装脚本
python trae-manager/tools/trae_manager.py setup --full --auto-install

# 4. 验证安装
python trae-manager/tools/trae_manager.py check-env
```

---

## 新机器部署

### 方案1：使用GitHub仓库（推荐）

#### 源机器（导出配置）

```bash
# 1. 进入trae-manager目录
cd ~/.trae-cn/skills/trae-manager/tools

# 2. 导出完整配置
python trae_manager.py export --full > my-trae-setup.json

# 3. 复制配置文件到新机器
# 方式A：通过GitHub Gist
cat my-trae-setup.json | gh gist create -d "Trae环境配置"

# 方式B：通过文件传输（U盘、网盘等）
cp my-trae-setup.json /path/to/transfer/
```

#### 新机器（导入配置）

```bash
# 1. 克隆仓库
git clone https://github.com/yourusername/trae-skills-hub.git
cd trae-skills-hub

# 2. 复制配置文件到目录
# 如果通过Gist下载：
curl -o my-trae-setup.json https://gist.githubusercontent.com/.../raw

# 3. 运行安装脚本
.\install.ps1 -ConfigFile my-trae-setup.json

# 或手动导入
python trae-manager/tools/trae_manager.py import my-trae-setup.json --auto-install
```

### 方案2：离线部署

#### 源机器（打包）

```powershell
# Windows
Compress-Archive -Path "$env:USERPROFILE\.trae-cn\skills\*" -DestinationPath "trae-skills.zip"

# Linux/Mac
tar -czvf trae-skills.tar.gz ~/.trae-cn/skills/
```

#### 新机器（解压）

```powershell
# Windows
Expand-Archive -Path "trae-skills.zip" -DestinationPath "$env:USERPROFILE\.trae-cn\skills"

# Linux/Mac
tar -xzvf trae-skills.tar.gz -C ~/
```

### 方案3：最小化部署

如果只需要核心功能：

```bash
# 1. 克隆仓库
git clone https://github.com/yourusername/trae-skills-hub.git
cd trae-skills-hub

# 2. 只安装核心技能
.\install.ps1 -InstallCoreOnly

# 或手动安装
python trae-manager/tools/trae_manager.py install-skills core
python trae-manager/tools/trae_manager.py install-mcp --recommended
```

---

## 团队协作部署

### 共享配置

#### 创建团队配置

```bash
# 1. 导出配置
python trae-manager/tools/trae_manager.py export --full > team-config.json

# 2. 提交到Git仓库
git add team-config.json
git commit -m "添加团队Trae配置"
git push
```

#### 团队成员使用

```bash
# 1. 拉取最新配置
git pull

# 2. 导入配置
python trae-manager/tools/trae_manager.py import team-config.json --auto-install
```

### Git Submodule方式

```bash
# 1. 将trae-skills-hub作为子模块添加
git submodule add https://github.com/yourusername/trae-skills-hub.git trae-skills

# 2. 初始化子模块
git submodule update --init --recursive

# 3. 安装
cd trae-skills
.\install.ps1
```

### Docker Compose方式

```yaml
# docker-compose.yml
version: '3.8'

services:
  trae-skills:
    build: .
    volumes:
      - ./trae-config.json:/app/config.json
      - trae-skills:/root/.trae-cn/skills
    command: python trae-manager/tools/trae_manager.py import /app/config.json --auto-install

volumes:
  trae-skills:
```

---

## Docker部署

### 构建Docker镜像

```dockerfile
# Dockerfile
FROM python:3.11-slim

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    nodejs \
    npm \
    git \
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 复制项目文件
COPY . .

# 安装Python依赖
RUN pip install pyyaml

# 安装Trae环境
RUN python trae-manager/tools/trae_manager.py setup --full --auto-install

# 设置环境变量
ENV PATH="/root/.trae-cn/skills/trae-manager/tools:${PATH}"

# 默认命令
CMD ["python", "trae-manager/tools/trae_manager.py", "check-env"]
```

### 构建和运行

```bash
# 构建镜像
docker build -t trae-skills-hub .

# 运行容器
docker run -it trae-skills-hub

# 带配置运行
docker run -it -v $(pwd)/my-config.json:/app/config.json trae-skills-hub python trae-manager/tools/trae_manager.py import /app/config.json --auto-install
```

---

## 故障排除

### 环境检查失败

```bash
# 检查Node.js
node --version
which node

# 检查Python
python --version
which python

# 检查Git
git --version
which git
```

### Python依赖安装失败

```bash
# 升级pip
python -m pip install --upgrade pip

# 安装pyyaml
python -m pip install pyyaml

# 或使用conda
conda install pyyaml
```

### npm安装失败

```bash
# 清除npm缓存
npm cache clean --force

# 使用淘宝镜像
npm config set registry https://registry.npmmirror.com

# 重新安装
npm install
```

### 权限问题

```bash
# Windows - 以管理员身份运行PowerShell
# 右键点击PowerShell -> 以管理员身份运行

# Linux/Mac - 使用sudo
sudo python trae-manager/tools/trae_manager.py setup --full

# 或更改目录权限
sudo chown -R $(whoami) ~/.trae-cn
```

### 网络问题

```bash
# 设置代理
export HTTP_PROXY=http://proxy.example.com:8080
export HTTPS_PROXY=http://proxy.example.com:8080

# 或使用镜像
npm config set registry https://registry.npmmirror.com
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

---

## 验证部署

### 检查环境

```bash
python trae-manager/tools/trae_manager.py check-env
```

预期输出：
```json
{
  "success": true,
  "checks": {
    "node": {"ok": true, "version": "v18.x.x"},
    "python": {"ok": true, "version": "Python 3.x.x"},
    "git": {"ok": true, "version": "git version 2.x.x"}
  }
}
```

### 检查已安装技能

```bash
python trae-manager/tools/trae_manager.py export
```

### 测试功能

```bash
# 测试技能搜索
python skill-seeker/tools/skill_search.py --local

# 测试MCP搜索
python mcp-seeker/tools/mcp_search.py --categories

# 测试trae-manager
python trae-manager/tools/trae_manager.py list
```

---

## 更新和维护

### 更新技能

```bash
# 拉取最新代码
git pull

# 更新所有技能
python trae-manager/tools/trae_manager.py update-all

# 或更新特定技能
python trae-manager/tools/trae_manager.py update skill-seeker
```

### 备份配置

```bash
# 导出配置
python trae-manager/tools/trae_manager.py export --full > backup-$(date +%Y%m%d).json

# 备份技能目录
tar -czvf trae-skills-backup-$(date +%Y%m%d).tar.gz ~/.trae-cn/skills/
```

### 恢复配置

```bash
# 导入配置
python trae-manager/tools/trae_manager.py import backup-20260202.json --auto-install

# 解压备份
tar -xzvf trae-skills-backup-20260202.tar.gz -C ~/
```

---

## 性能优化

### 加速安装

```bash
# 使用国内镜像
npm config set registry https://registry.npmmirror.com
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 并行安装
export PIP_DISABLE_PIP_VERSION_CHECK=1
export PIP_NO_CACHE_DIR=1
```

### 磁盘空间优化

```bash
# 清理npm缓存
npm cache clean --force

# 清理pip缓存
pip cache purge

# 删除旧备份
find ~/.trae-cn/skills -name "*.backup.*" -mtime +30 -delete
```

---

## 安全建议

1. **定期更新依赖**
   ```bash
   npm audit fix
   pip list --outdated
   ```

2. **使用虚拟环境**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # 或
   venv\Scripts\activate  # Windows
   ```

3. **限制权限**
   ```bash
   # 不要以root运行
   # 使用普通用户安装
   ```

---

## 总结

| 部署方式 | 适用场景 | 难度 | 时间 |
|---------|---------|------|------|
| **GitHub仓库** | 有网络的机器 | ⭐ | 5-10分钟 |
| **离线部署** | 无网络的机器 | ⭐⭐ | 10-15分钟 |
| **Docker部署** | 容器化环境 | ⭐⭐ | 10-20分钟 |
| **团队协作** | 团队共享 | ⭐⭐ | 5分钟/人 |

**推荐方案：** 使用GitHub仓库 + 配置文件方式，最简单高效！

---

**🎉 部署完成！开始使用Trae Skills Hub吧！**
