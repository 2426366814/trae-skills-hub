# Trae Skills Hub 🚀

[![GitHub stars](https://img.shields.io/github/stars/yourusername/trae-skills-hub?style=social)](https://github.com/yourusername/trae-skills-hub)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://python.org)
[![Node.js](https://img.shields.io/badge/node.js-18+-green.svg)](https://nodejs.org)

> 一站式Trae技能管理平台 - 搜索、安装、管理、部署，一键搞定！

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

## 🚀 快速开始

### 前置要求

- **Node.js** >= 18.0.0
- **Python** >= 3.9.0
- **Git** >= 2.30.0

### 安装

```bash
# 克隆仓库
git clone https://github.com/yourusername/trae-skills-hub.git

# 进入目录
cd trae-skills-hub

# 运行安装脚本（Windows）
.\install.ps1

# 或手动安装
python trae-manager/tools/trae_manager.py setup --full --auto-install
```

### 使用

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

## 📚 文档

- [部署指南](DEPLOY.md) - 详细部署说明
- [安装指南](trae-manager/INSTALL.md) - 新机器安装指南
- [使用说明](trae-manager/SKILL.md) - 完整使用文档

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

根据你的 GitHub 项目类型，AI 智能体会自动分析并安装所需的 skills 和 MCP：

```bash
# 在 Trae IDE 中，直接告诉 AI 你的项目：

"我克隆了一个 React 前端项目，帮我安装相关技能"
"这是一个 Python 数据分析项目，需要哪些技能？"
"我在开发一个 AI Agent 应用，安装相关工具"
"这是一个文档处理工具项目"

# AI 智能体将自动：
# 1. 分析项目类型（package.json、requirements.txt、代码结构等）
# 2. 识别项目所需的技术栈
# 3. 自动安装匹配的 skills 和 MCP
# 4. 配置环境变量和依赖
```

**按项目类型智能安装：**

| 项目类型 | 对话命令 | 自动安装内容 |
|---------|---------|-------------|
| **React/前端项目** | "我开发了 React 项目" | frontend-design, frontend-dev-guidelines, artifacts-builder, webapp-testing |
| **Node.js/后端项目** | "这是 Node.js 后端项目" | backend-dev-guidelines, error-tracking, systematic-debugging, route-tester |
| **Python/数据分析** | "Python 数据分析项目" | xlsx, pdf, docx, canvas-design, theme-factory |
| **AI Agent 应用** | "开发 AI Agent 应用" | building-agents, building-agents-using-langchain, mcp-builder, langsmith-fetch |
| **文档处理工具** | "文档处理工具项目" | docx, pdf, xlsx, pptx, file-organizer, invoice-organizer |
| **自动化测试** | "需要自动化测试" | playwright-cli, webapp-testing, route-tester, test-driven-development |
| **MCP 服务开发** | "开发 MCP 服务" | mcp-builder, mcp_with_server, skill-creator |
| **全栈项目** | "全栈 Web 应用" | frontend-dev-guidelines, backend-dev-guidelines, connect-apps, error-tracking |

**基于 GitHub 仓库智能安装：**

```bash
# 告诉 AI 你的 GitHub 项目地址：
"我克隆了 https://github.com/username/project-name，安装相关技能"

# AI 自动分析项目并安装：
# 1. 读取 package.json / requirements.txt / Cargo.toml 等
# 2. 分析项目依赖和技术栈
# 3. 匹配并安装对应的 skills 和 MCP

# 示例：
# 检测到 React + TypeScript -> 安装 frontend-dev-guidelines, frontend-design
# 检测到 Python + FastAPI -> 安装 backend-dev-guidelines, error-tracking
# 检测到 Playwright 测试 -> 安装 webapp-testing, playwright-cli
```

**一键安装项目所需全部环境：**

```bash
# 完整项目环境安装命令：

# 前端项目环境
"为我的前端项目安装全部所需技能"
python trae_manager.py install-skills frontend-design,frontend-dev-guidelines,artifacts-builder,web-artifacts-builder,canvas-design,theme-factory,webapp-testing,skill-creator

# 后端项目环境  
"为我的后端项目安装全部所需技能"
python trae_manager.py install-skills backend-dev-guidelines,error-tracking,systematic-debugging,route-tester,requesting-code-review,finishing-a-development-branch,writing-plans,executing-plans

# AI 项目环境
"为我的 AI 项目安装全部所需技能"
python trae_manager.py install-skills building-agents,building-agents-using-langchain,building-agents-using-crewai,building-agents-using-llamaindex,mcp-builder,langsmith-fetch,content-research-writer,brainstorming

# 数据/文档处理环境
"为我的数据处理项目安装全部所需技能"
python trae_manager.py install-skills docx,pdf,xlsx,pptx,file-organizer,invoice-organizer,canvas-design,theme-factory

# 完整开发环境（全部安装）
"安装全部 skills 和 MCP"
python trae_manager.py install-skills docx,pdf,pptx,xlsx,skill-creator,mcp-builder,frontend-design,backend-dev-guidelines,frontend-dev-guidelines,canvas-design,theme-factory,artifacts-builder,web-artifacts-builder,brainstorming,systematic-debugging,writing-plans,executing-plans,using-superpowers,using-git-worktrees,content-research-writer,doc-coauthoring,skill-share,requesting-code-review,finishing-a-development-branch,subagent-driven-development,test-driven-development,building-agents,building-agents-using-langchain,building-agents-using-crewai,building-agents-using-llamaindex,building-agents-using-vercel,connect-apps,connect,langsmith-fetch,developer-growth-analysis,meeting-insights-analyzer,lead-research-assistant,tailored-resume-generator,twitter-algorithm-optimizer,competitive-ads-extractor,domain-name-brainstormer,file-organizer,invoice-organizer,internal-comms,route-tester,skill-developer,error-tracking,playwright-cli,playwright-mcp-dev,webapp-testing
python trae_manager.py install-mcp filesystem,fetch,sqlite,postgresql,git,pdf
```

**实际使用示例：**

```bash
# 场景1：刚克隆了一个项目
用户："我刚克隆了 https://github.com/vercel/next.js，需要安装什么技能？"

AI 分析：
- 检测到 Next.js 框架
- 检测到 React + TypeScript
- 检测到前端项目结构

AI 自动执行：
python trae_manager.py install-skills frontend-dev-guidelines,frontend-design,artifacts-builder,webapp-testing

AI 回复：
✅ 已为 Next.js 项目安装以下技能：
   - frontend-dev-guidelines (前端开发指南)
   - frontend-design (前端设计)
   - artifacts-builder (构建工具)
   - webapp-testing (Web 应用测试)

# 场景2：开始新项目
用户："我要开发一个 Python 数据分析工具"

AI 自动执行：
python trae_manager.py install-skills xlsx,pdf,docx,canvas-design,theme-factory,file-organizer

AI 回复：
✅ 已为数据分析项目安装以下技能：
   - xlsx (Excel 处理)
   - pdf (PDF 处理)  
   - docx (Word 处理)
   - canvas-design (可视化设计)
   - theme-factory (主题工厂)
   - file-organizer (文件整理)
```

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

## 🔧 系统要求

### 最低配置
- **操作系统**: Windows 10/11, macOS 10.15+, Ubuntu 20.04+
- **内存**: 4GB RAM
- **磁盘**: 1GB 可用空间

### 推荐配置
- **操作系统**: Windows 11, macOS 13+, Ubuntu 22.04+
- **内存**: 8GB RAM
- **磁盘**: 5GB 可用空间

## 📝 更新日志

### v1.0.0 (2026-02-02)
- ✅ 初始版本发布
- ✅ 集成skill-seeker技能搜索
- ✅ 集成mcp-seeker MCP搜索
- ✅ 实现trae-manager统一管理
- ✅ 支持导出/导入配置
- ✅ 支持跨机器部署

## 🤝 贡献

欢迎提交Issue和Pull Request！

### 贡献步骤
1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目基于 [MIT](LICENSE) 许可证开源。

## 🙏 致谢

- [Anthropic](https://www.anthropic.com/) - Claude和MCP协议
- [MCP.so](https://mcp.so/) - MCP服务收录平台
- [Awesome MCP Servers](https://github.com/punkpeye/awesome-mcp-servers)

## 📞 联系我们

- **GitHub Issues**: [提交问题](https://github.com/yourusername/trae-skills-hub/issues)
- **Email**: your.email@example.com

---

**🌟 如果这个项目对您有帮助，请给我们一个Star！**
