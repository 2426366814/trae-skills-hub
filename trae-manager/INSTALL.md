# Trae环境新机器安装指南

## 快速开始（推荐）

### 方式1：使用配置文件自动安装（最简单）

#### 第一步：在源机器导出配置

```powershell
# 进入trae-manager目录
cd "C:\Users\Administrator\.trae-cn\skills\trae-manager\tools"

# 导出完整配置
python trae_manager.py export --full > my-trae-setup.json

# 复制配置文件到新机器（通过U盘、网盘、邮件等）
```

#### 第二步：在新机器上运行安装脚本

```powershell
# 1. 复制trae-manager文件夹和my-trae-setup.json到新机器
# 2. 进入trae-manager/tools目录
cd trae-manager\tools

# 3. 运行安装脚本（使用配置文件）
.\install_on_new_machine.ps1 -ConfigFile "my-trae-setup.json"
```

### 方式2：只安装核心技能

```powershell
# 如果不需要完整环境，只安装核心技能
.\install_on_new_machine.ps1 -InstallCoreOnly
```

### 方式3：手动安装

```powershell
# 1. 检查环境
python trae_manager.py check-env

# 2. 安装核心技能
python trae_manager.py install-skills core

# 3. 安装推荐MCP
python trae_manager.py install-mcp --recommended
```

---

## 详细步骤

### 前置要求

新机器必须安装以下软件：

1. **Node.js** >= 18.0.0
   - 下载：https://nodejs.org/
   - 验证：`node --version`

2. **Python** >= 3.9.0
   - 下载：https://python.org/
   - 验证：`python --version`

3. **Git** >= 2.30.0
   - 下载：https://git-scm.com/
   - 验证：`git --version`

### 安装流程

```
┌─────────────────────────────────────────────────────────┐
│  1. 安装Node.js、Python、Git（如果尚未安装）              │
│     ↓                                                   │
│  2. 复制trae-manager文件夹到新机器                        │
│     ↓                                                   │
│  3. 运行安装脚本 install_on_new_machine.ps1              │
│     ↓                                                   │
│  4. 等待自动安装完成（5-10分钟）                          │
│     ↓                                                   │
│  5. 验证安装并开始使用                                   │
└─────────────────────────────────────────────────────────┘
```

### 需要复制的文件

**最小安装（推荐）：**
```
trae-manager/
├── SKILL.md
├── INSTALL.md（本文件）
├── data/
│   └── dependencies.json
└── tools/
    ├── trae_manager.py
    └── install_on_new_machine.ps1
```

**完整安装（包含所有技能）：**
```
.trae-cn/skills/          # 整个目录（170+个技能）
├── trae-manager/
├── skill-seeker/
├── mcp-seeker/
├── docx/
├── pdf/
├── ...（其他所有技能）
```

---

## 脚本参数说明

### install_on_new_machine.ps1

| 参数 | 说明 | 示例 |
|------|------|------|
| `-ConfigFile` | 使用配置文件安装 | `-ConfigFile "my-trae-setup.json"` |
| `-InstallCoreOnly` | 只安装核心技能 | `-InstallCoreOnly` |
| `-SkipEnvCheck` | 跳过环境检查 | `-SkipEnvCheck` |

### 使用示例

```powershell
# 使用配置文件完整安装
.\install_on_new_machine.ps1 -ConfigFile "my-trae-setup.json"

# 只安装核心技能
.\install_on_new_machine.ps1 -InstallCoreOnly

# 跳过环境检查（如果确定环境已准备好）
.\install_on_new_machine.ps1 -ConfigFile "my-trae-setup.json" -SkipEnvCheck
```

---

## 验证安装

安装完成后，运行以下命令验证：

```powershell
# 1. 检查环境
python "$HOME\.trae-cn\skills\trae-manager\tools\trae_manager.py" check-env

# 2. 列出已安装技能
python "$HOME\.trae-cn\skills\trae-manager\tools\trae_manager.py" export

# 3. 测试skill-seeker
python "$HOME\.trae-cn\skills\skill-seeker\tools\skill_search.py" --local

# 4. 测试mcp-seeker
python "$HOME\.trae-cn\skills\mcp-seeker\tools\mcp_search.py" --categories
```

---

## 常见问题

### Q: 安装脚本运行失败？

**A:** 检查以下几点：
1. 是否以管理员权限运行PowerShell
2. 是否已安装Node.js、Python、Git
3. 脚本路径是否正确

### Q: 如何只安装部分技能？

**A:** 编辑配置文件，删除不需要的技能：
```powershell
# 1. 导出配置
python trae_manager.py export --full > my-config.json

# 2. 编辑my-config.json，删除不需要的技能

# 3. 导入修改后的配置
python trae_manager.py import my-config.json --auto-install
```

### Q: 新机器没有网络怎么办？

**A:** 使用离线安装：
1. 在源机器上压缩整个`.trae-cn/skills/`目录
2. 复制到新机器解压
3. 手动安装依赖（查看各SKILL.md）

### Q: 如何更新已安装的技能？

**A:** 使用trae-manager更新：
```powershell
python trae_manager.py update-all
```

### Q: 安装过程中断怎么办？

**A:** 重新运行安装脚本即可，会自动跳过已安装的部分。

---

## 故障排除

### 环境检查失败

```powershell
# 检查Node.js
node --version

# 检查Python
python --version

# 检查Git
git --version
```

### Python依赖安装失败

```powershell
# 手动安装pyyaml
python -m pip install pyyaml

# 或
pip3 install pyyaml
```

### 权限问题

```powershell
# 以管理员身份运行PowerShell
# 右键点击PowerShell -> 以管理员身份运行
```

---

## 安装后配置

### 配置环境变量（可选）

```powershell
# 添加trae-manager到PATH
[Environment]::SetEnvironmentVariable(
    "Path",
    [Environment]::GetEnvironmentVariable("Path", "User") + ";$HOME\.trae-cn\skills\trae-manager\tools",
    "User"
)
```

### 创建快捷命令（可选）

```powershell
# 在PowerShell配置文件中添加别名
notepad $PROFILE

# 添加以下内容：
function trae-check { python "$HOME\.trae-cn\skills\trae-manager\tools\trae_manager.py" check-env }
function trae-export { python "$HOME\.trae-cn\skills\trae-manager\tools\trae_manager.py" export --full }
function trae-install { python "$HOME\.trae-cn\skills\trae-manager\tools\trae_manager.py" install-skills $args }
```

---

## 总结

**最简单的安装方式：**

1. 源机器：`python trae_manager.py export --full > my-config.json`
2. 复制`trae-manager`文件夹和`my-config.json`到新机器
3. 新机器：`.
stall_on_new_machine.ps1 -ConfigFile "my-config.json"`
4. 等待5-10分钟完成安装

**预计时间：**
- 最小安装（核心技能）：2-3分钟
- 完整安装（所有技能）：10-15分钟

**安装完成后即可使用所有Trae功能！** 🎉
