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
