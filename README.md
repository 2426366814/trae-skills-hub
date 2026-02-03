# Trae Skills Hub 🚀

[![GitHub stars](https://img.shields.io/github/stars/2426366814/trae-skills-hub?style=social)](https://github.com/2426366814/trae-skills-hub)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://python.org)
[![Node.js](https://img.shields.io/badge/node.js-18+-green.svg)](https://nodejs.org)

> 一站式Trae技能管理平台 - 搜索、安装、管理、部署，一键搞定！

---

## 📑 目录

- [核心功能](#-核心功能)
- [快速开始](#-快速开始)
- [使用指南](#-使用指南)
- [使用场景](#-使用场景)
- [项目结构](#-项目结构)
- [系统要求](#-系统要求)
- [更新日志](#-更新日志)
- [贡献指南](#-贡献指南)

---

## ✨ 核心功能

### 🔍 智能搜索
- **技能搜索** - 从本地、GitHub、Vercel Skills搜索
- **MCP搜索** - 智能搜索11,790+ MCP服务
- **智能推荐** - 基于需求自动推荐最佳技能/MCP

### ⚡ 一键安装
- **自动安装** - 技能和MCP一键安装
- **依赖管理** - 自动检测和安装依赖
- **环境配置** - 自动配置环境变量

### 🚀 跨机器部署
- **导出配置** - 导出完整环境配置
- **导入部署** - 新机器一键导入安装
- **团队协作** - 共享配置，统一环境

---

## 📦 包含内容

### 核心管理工具

| 工具 | 功能 | 状态 |
|------|------|------|
| **trae-manager** | 统一管理和部署 | ✅ |
| **skill-seeker** | 技能搜索和比较 | ✅ |
| **mcp-seeker** | MCP搜索和安装 | ✅ |

### 文档处理技能

| 技能 | 功能 | 依赖 |
|------|------|------|
| **docx** | Word文档处理 | docx, defusedxml |
| **pdf** | PDF文档处理 | pytesseract, pdf2image |
| **pptx** | PowerPoint处理 | pptxgenjs, python-pptx |
| **xlsx** | Excel表格处理 | openpyxl, pandas |

### 开发技能

| 技能 | 功能 | 依赖 |
|------|------|------|
| **mcp-builder** | 创建MCP服务器 | @modelcontextprotocol/sdk |
| **skill-creator** | 创建自定义技能 | - |
| **frontend-design** | 前端设计 | - |
| **backend-dev-guidelines** | 后端开发指南 | express, flask |
| **frontend-dev-guidelines** | 前端开发指南 | react, typescript |

### MCP服务

| MCP | 功能 | 下载量 | 评分 |
|-----|------|--------|------|
| **Filesystem** | 文件系统访问 | 25.3K | ⭐4.9 |
| **Fetch** | HTTP请求 | 22.1K | ⭐4.8 |
| **PostgreSQL** | 数据库连接 | 12.5K | ⭐4.8 |
| **SQLite** | 轻量级数据库 | 9.2K | ⭐4.7 |
| **Git** | 版本控制 | 15.6K | ⭐4.7 |
| **PDF** | PDF处理 | 18.7K | ⭐4.8 |

---

## 🚀 快速开始

### 前置要求

- **Node.js** >= 18.0.0
- **Python** >= 3.9.0
- **Git** >= 2.30.0

### 安装

```bash
# 克隆仓库
git clone https://github.com/2426366814/trae-skills-hub.git

# 进入目录
cd trae-skills-hub

# 运行安装脚本（Windows）
.\install.ps1

# 或手动安装
python trae-manager/tools/trae_manager.py setup --full --auto-install
```

### 一键安装所有推荐技能

```bash
# 方式1：使用 curl 一键安装
curl -fsSL https://raw.githubusercontent.com/2426366814/trae-skills-hub/master/install.sh | bash

# 方式2：使用 PowerShell 一键安装 (Windows)
iwr -useb https://raw.githubusercontent.com/2426366814/trae-skills-hub/master/install.ps1 | iex

# 方式3：在 Trae IDE 中与 AI 对话
"从 https://github.com/2426366814/trae-skills-hub 安装所有推荐技能"
```

---

## 📖 使用指南

### 基础命令

```bash
# 搜索技能
python trae-manager/tools/skill_search.py --search "文档处理"

# 搜索MCP
python trae-manager/tools/mcp_search.py "database"

# 导出配置
python trae-manager/tools/trae_manager.py export --full > my-config.json

# 导入配置
python trae-manager/tools/trae_manager.py import my-config.json --auto-install
```

### 智能体对话命令

在 Trae IDE 中与 AI 智能体对话，自动安装和管理 skills：

| 操作类型 | 对话命令示例 | 功能说明 |
|---------|-------------|---------|
| **一键安装全部** | `"从 https://github.com/2426366814/trae-skills-hub 安装所有推荐技能"` | 安装本仓库所有推荐的 skills 和 MCP |
| **按项目类型** | `"我开发了 React 项目，安装相关技能"` | 根据项目类型智能安装 |
| **按 GitHub 仓库** | `"我克隆了 https://github.com/xxx/yyy，安装相关技能"` | 分析仓库技术栈后安装 |
| **清理重复** | `"清理重复技能"` | 删除重复安装的技能 |
| **优化组合** | `"优化我的技能组合"` | 分析使用频率，清理冗余 |

---

## 🎯 使用场景

### 场景1：新机器快速部署

```bash
# 源机器导出配置
python trae_manager.py export --full > my-trae-setup.json

# 新机器一键部署
python trae_manager.py import my-trae-setup.json --auto-install
```

### 场景2：团队协作

```bash
# 导出团队配置
python trae_manager.py export --full > team-config.json

# 提交到Git
# 团队成员拉取后导入
python trae_manager.py import team-config.json --auto-install
```

### 场景3：技能搜索和安装

```bash
# 搜索技能
python skill_search.py --search "pdf"

# 安装技能
python trae_manager.py install-skills pdf,docx,xlsx

# 安装MCP
python trae_manager.py install-mcp filesystem,fetch
```

### 场景4：智能体对话自动安装

#### 方式1：从本仓库一键安装全部推荐技能

```bash
# 告诉 AI 从 trae-skills-hub 仓库安装所有推荐技能：
"从 https://github.com/2426366814/trae-skills-hub 安装所有推荐技能"
"安装 trae-skills-hub 中的全部 skills 和 MCP"
"一键安装这个仓库推荐的所有开发工具"

# AI 智能体将自动：
# 1. 访问 https://github.com/2426366814/trae-skills-hub
# 2. 读取推荐的技能清单
# 3. 自动安装所有推荐的 skills 和 MCP
# 4. 配置环境变量和依赖
```

#### 方式2：根据项目类型智能安装

**按项目类型智能安装：**

| 项目类型 | 对话命令 | 自动安装内容 |
|---------|---------|-------------|
| **React/前端项目** | `"我开发了 React 项目"` | frontend-design, frontend-dev-guidelines, artifacts-builder, webapp-testing |
| **Node.js/后端项目** | `"这是 Node.js 后端项目"` | backend-dev-guidelines, error-tracking, systematic-debugging, route-tester |
| **Python/数据分析** | `"Python 数据分析项目"` | xlsx, pdf, docx, canvas-design, theme-factory |
| **AI Agent 应用** | `"开发 AI Agent 应用"` | building-agents, building-agents-using-langchain, mcp-builder, langsmith-fetch |
| **文档处理工具** | `"文档处理工具项目"` | docx, pdf, xlsx, pptx, file-organizer, invoice-organizer |
| **自动化测试** | `"需要自动化测试"` | playwright-cli, webapp-testing, route-tester, test-driven-development |
| **MCP 服务开发** | `"开发 MCP 服务"` | mcp-builder, mcp_with_server, skill-creator |
| **全栈项目** | `"全栈 Web 应用"` | frontend-dev-guidelines, backend-dev-guidelines, connect-apps, error-tracking |

**基于 GitHub 仓库智能安装：**

```bash
# 告诉 AI 你的 GitHub 项目地址：
"我克隆了 https://github.com/username/project-name，安装相关技能"

# AI 自动分析项目并安装：
# 1. 读取 package.json / requirements.txt / Cargo.toml 等
# 2. 分析项目依赖和技术栈
# 3. 匹配并安装对应的 skills 和 MCP
```

#### 方式3：技能管理和优化

| 管理操作 | 对话命令 | 功能说明 |
|---------|---------|---------|
| **清理重复** | `"清理重复技能"` | 扫描并删除重复安装的技能 |
| **优化组合** | `"优化技能组合"` | 分析使用频率，清理冗余 |
| **查看已安装** | `"查看已安装技能"` | 显示所有已安装技能及其版本 |
| **卸载技能** | `"卸载 [技能名]"` | 卸载指定的技能 |
| **更新技能** | `"更新所有技能"` | 检查并更新到最新版本 |
| **备份配置** | `"备份我的技能配置"` | 导出当前配置到文件 |
| **恢复配置** | `"从备份恢复技能"` | 从备份文件恢复配置 |

**使用示例：**

```bash
# 示例1：清理重复技能
用户："清理重复技能"

AI 回复：
🔍 发现重复技能：
   - pdf (v1.0, v1.2, v2.0) -> 保留 v2.0
   - docx (v1.5, v2.1) -> 保留 v2.1
✅ 已清理完成：删除 3 个旧版本，释放 78MB

# 示例2：根据项目优化
用户："我只做前端开发，优化技能组合"

AI 回复：
🎯 已为前端开发优化技能组合：
   保留: 12个核心技能
   删除: 8个不相关技能
   预计释放: 156MB
```

---

## 🛠️ 项目结构

```
trae-skills-hub/
├── README.md                    # 项目说明
├── DEPLOY.md                    # 部署文档
├── LICENSE                      # 许可证
├── install.ps1                  # Windows安装脚本
├── install.sh                   # Linux/Mac安装脚本
├── trae-manager/                # 统一管理工具
│   ├── SKILL.md                # 使用说明
│   ├── INSTALL.md              # 安装指南
│   ├── data/
│   │   └── dependencies.json   # 依赖清单
│   └── tools/
│       ├── trae_manager.py     # 管理脚本
│       ├── install_on_new_machine.ps1
│       └── skill_search.py
├── skill-seeker/               # 技能搜索工具
│   ├── SKILL.md
│   └── tools/
│       └── skill_search.py
├── mcp-seeker/                 # MCP搜索工具
│   ├── SKILL.md
│   └── tools/
│       ├── mcp_search.py
│       └── auto_installer.py
└── .github/
    └── workflows/              # GitHub Actions
        └── release.yml
```

---

## 🔧 系统要求

### 最低配置
- **操作系统**: Windows 10/11, macOS 10.15+, Ubuntu 20.04+
- **内存**: 4GB RAM
- **磁盘**: 1GB 可用空间

### 推荐配置
- **操作系统**: Windows 11, macOS 13+, Ubuntu 22.04+
- **内存**: 8GB RAM
- **磁盘**: 5GB 可用空间

---

## 📝 更新日志

### v1.0.0 (2026-02-02)
- ✅ 初始版本发布
- ✅ 集成skill-seeker技能搜索
- ✅ 集成mcp-seeker MCP搜索
- ✅ 实现trae-manager统一管理
- ✅ 支持导出/导入配置
- ✅ 支持跨机器部署
- ✅ 支持智能体对话自动安装
- ✅ 支持技能管理和优化

---

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

### 贡献步骤
1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

---

## 📚 相关文档

- [部署指南](DEPLOY.md) - 详细部署说明
- [安装指南](trae-manager/INSTALL.md) - 新机器安装指南
- [使用说明](trae-manager/SKILL.md) - 完整使用文档

---

## 🙏 致谢

- [Anthropic](https://www.anthropic.com/) - Claude和MCP协议
- [MCP.so](https://mcp.so/) - MCP服务收录平台
- [Awesome MCP Servers](https://github.com/punkpeye/awesome-mcp-servers)

---

## 📄 许可证

本项目基于 [MIT](LICENSE) 许可证开源。

---

**🌟 如果这个项目对您有帮助，请给我们一个Star！**
