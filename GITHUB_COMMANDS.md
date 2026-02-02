# GitHub 命令指南

> 完整的GitHub仓库操作命令，用于上传项目和管理代码

## 📋 目录

1. [首次上传](#首次上传)
2. [日常操作](#日常操作)
3. [新机器克隆](#新机器克隆)
4. [团队协作](#团队协作)
5. [常见问题](#常见问题)

---

## 首次上传

### 1. 创建GitHub仓库

在GitHub网站上创建新仓库：
- 访问：https://github.com/new
- 仓库名称：`trae-skills-hub`
- 描述：`一站式Trae技能管理平台`
- 选择：`Public` 或 `Private`
- 不要初始化README（我们已有README.md）

### 2. 本地初始化并上传

```bash
# 进入项目目录
cd trae-skills-hub

# 初始化Git仓库
git init

# 添加所有文件
git add .

# 提交更改
git commit -m "初始提交：Trae Skills Hub v1.0.0

- 集成skill-seeker技能搜索
- 集成mcp-seeker MCP搜索
- 实现trae-manager统一管理
- 支持导出/导入配置
- 支持跨机器部署"

# 添加远程仓库（替换yourusername为你的GitHub用户名）
git remote add origin https://github.com/yourusername/trae-skills-hub.git

# 推送到GitHub
git push -u origin main

# 如果main分支推送失败，尝试master分支：
# git push -u origin master
```

### 3. 验证上传

```bash
# 查看远程仓库
git remote -v

# 查看分支状态
git status

# 查看提交历史
git log --oneline
```

---

## 日常操作

### 更新代码

```bash
# 查看更改
git status

# 添加更改的文件
git add filename
# 或添加所有更改
git add .

# 提交更改
git commit -m "描述你的更改"

# 推送到GitHub
git push
```

### 创建分支

```bash
# 创建并切换到新分支
git checkout -b feature/new-feature

# 在新分支上工作...
# ...

# 提交更改
git add .
git commit -m "添加新功能"

# 推送到远程分支
git push -u origin feature/new-feature

# 在GitHub上创建Pull Request合并到main分支
```

### 同步更新

```bash
# 拉取远程更新
git pull origin main

# 如果有冲突，解决冲突后：
git add .
git commit -m "解决合并冲突"
git push
```

---

## 新机器克隆

### 方式1：使用HTTPS（推荐新手）

```bash
# 克隆仓库
git clone https://github.com/yourusername/trae-skills-hub.git

# 进入目录
cd trae-skills-hub

# 运行安装脚本
.\install.ps1
```

### 方式2：使用SSH（需要配置SSH密钥）

```bash
# 生成SSH密钥（如果尚未生成）
ssh-keygen -t ed25519 -C "your.email@example.com"

# 添加SSH密钥到ssh-agent
ssh-add ~/.ssh/id_ed25519

# 复制公钥到GitHub
# 访问：https://github.com/settings/keys
# 点击 "New SSH key"
# 粘贴 ~/.ssh/id_ed25519.pub 的内容

# 克隆仓库
git clone git@github.com:yourusername/trae-skills-hub.git

# 进入目录并安装
cd trae-skills-hub
.\install.ps1
```

### 方式3：使用GitHub CLI

```bash
# 安装GitHub CLI
# Windows: winget install --id GitHub.cli
# macOS: brew install gh
# Linux: sudo apt install gh

# 登录GitHub
gh auth login

# 克隆仓库
gh repo clone yourusername/trae-skills-hub

# 进入目录并安装
cd trae-skills-hub
.\install.ps1
```

---

## 团队协作

### 添加协作者

在GitHub网站上：
1. 访问仓库页面
2. 点击 `Settings` → `Manage access`
3. 点击 `Invite a collaborator`
4. 输入协作者的GitHub用户名

### 协作者工作流程

```bash
# 1. 克隆仓库
git clone https://github.com/yourusername/trae-skills-hub.git
cd trae-skills-hub

# 2. 创建功能分支
git checkout -b feature/my-feature

# 3. 进行更改
# ... 编辑文件 ...

# 4. 提交更改
git add .
git commit -m "添加新功能：xxx"

# 5. 推送到远程
git push -u origin feature/my-feature

# 6. 在GitHub上创建Pull Request
# 访问：https://github.com/yourusername/trae-skills-hub/pulls
# 点击 "New Pull Request"
```

### 代码审查

```bash
# 查看待审查的PR
gh pr list

# 查看特定PR
gh pr view 123

# 检出PR进行本地测试
gh pr checkout 123

# 批准PR
gh pr review 123 --approve

# 合并PR
gh pr merge 123
```

---

## 发布版本

### 创建Release

```bash
# 创建标签
git tag -a v1.0.0 -m "发布v1.0.0"

# 推送标签到GitHub
git push origin v1.0.0

# 使用GitHub CLI创建Release
gh release create v1.0.0 \
  --title "Trae Skills Hub v1.0.0" \
  --notes "初始版本发布

## 新功能
- 技能搜索和比较
- MCP搜索和安装
- 统一管理和部署
- 跨机器部署支持

## 安装
\`\`\`bash
git clone https://github.com/yourusername/trae-skills-hub.git
.\install.ps1
\`\`\`"
```

### 自动发布（GitHub Actions）

创建 `.github/workflows/release.yml`：

```yaml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Create Release
        uses: actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tag_name: ${{ github.ref }}
          release_name: Release ${{ github.ref }}
          draft: false
          prerelease: false
```

---

## 常见问题

### Q: 推送失败，提示权限错误？

**A:** 检查远程仓库URL：
```bash
# 查看当前远程仓库
git remote -v

# 如果使用的是HTTPS，改为SSH：
git remote set-url origin git@github.com:yourusername/trae-skills-hub.git

# 或配置Git凭据管理器：
git config --global credential.helper manager
```

### Q: 提交时提示需要配置用户名和邮箱？

**A:** 配置Git用户信息：
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Q: 如何撤销上次的提交？

**A:** 
```bash
# 撤销提交但保留更改
git reset --soft HEAD~1

# 撤销提交并丢弃更改（谨慎使用）
git reset --hard HEAD~1

# 撤销已推送的提交
git revert HEAD
git push
```

### Q: 如何忽略某些文件？

**A:** 编辑 `.gitignore` 文件：
```gitignore
# 忽略配置文件
*.config.json
my-trae-setup.json

# 忽略日志
*.log

# 忽略临时文件
*.tmp
*.backup.*

# 忽略IDE文件
.vscode/
.idea/
```

### Q: 仓库太大，如何减小体积？

**A:**
```bash
# 查看大文件
git rev-list --objects --all | git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' | awk '/^blob/ {print $3 " " $4}' | sort -rn | head -20

# 清理历史（谨慎使用）
git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch 大文件路径' HEAD
```

---

## 完整命令速查表

| 操作 | 命令 |
|------|------|
| **初始化** | |
| 初始化仓库 | `git init` |
| 添加远程仓库 | `git remote add origin <url>` |
| 克隆仓库 | `git clone <url>` |
| **基本操作** | |
| 查看状态 | `git status` |
| 添加文件 | `git add <file>` 或 `git add .` |
| 提交更改 | `git commit -m "message"` |
| 推送更改 | `git push` |
| 拉取更新 | `git pull` |
| **分支操作** | |
| 查看分支 | `git branch` |
| 创建分支 | `git checkout -b <branch>` |
| 切换分支 | `git checkout <branch>` |
| 合并分支 | `git merge <branch>` |
| 删除分支 | `git branch -d <branch>` |
| **标签操作** | |
| 创建标签 | `git tag -a v1.0 -m "message"` |
| 推送标签 | `git push origin <tag>` |
| 推送所有标签 | `git push origin --tags` |
| **撤销操作** | |
| 撤销add | `git reset HEAD <file>` |
| 撤销commit | `git reset --soft HEAD~1` |
| 撤销修改 | `git checkout -- <file>` |
| **查看历史** | |
| 查看日志 | `git log` |
| 简洁日志 | `git log --oneline` |
| 图形化日志 | `git log --graph --oneline` |

---

## 新机器完整部署流程

```bash
# ===== 第1步：安装基础环境 =====
# Windows: 安装Git、Node.js、Python
# macOS: brew install git node python
# Linux: sudo apt install git nodejs npm python3

# ===== 第2步：克隆仓库 =====
git clone https://github.com/yourusername/trae-skills-hub.git
cd trae-skills-hub

# ===== 第3步：运行安装脚本 =====
# Windows:
.\install.ps1

# 或使用配置文件：
# .\install.ps1 -ConfigFile "my-config.json"

# ===== 第4步：验证安装 =====
python trae-manager/tools/trae_manager.py check-env

# ===== 完成！=====
```

---

**🎉 现在您可以将项目上传到GitHub，并在任何机器上轻松部署了！**
