#!/usr/bin/env python3
"""
MCP搜索工具
从多个来源搜索MCP服务
"""
import os
import json
import re
from typing import List, Dict, Any, Optional
from difflib import SequenceMatcher
from datetime import datetime


class MCPSearcher:
    """MCP搜索器"""
    
    def __init__(self, database_path: str = None):
        """初始化搜索器"""
        self.database = self._load_database(database_path)
        self.cache = {}
        
    def _load_database(self, database_path: str = None) -> Dict:
        """加载MCP数据库"""
        if database_path is None:
            database_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "data", "mcp_database.json"
            )
        
        if os.path.exists(database_path):
            with open(database_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # 返回默认数据库
        return self._get_default_database()
    
    def _get_default_database(self) -> Dict:
        """获取默认MCP数据库"""
        return {
            "mcps": [
                # 数据库类
                {
                    "name": "PostgreSQL",
                    "full_name": "@anthropic-ai/mcp-server-postgres",
                    "description": "PostgreSQL数据库连接和查询",
                    "category": "database",
                    "source": "official",
                    "github": "modelcontextprotocol/servers/tree/main/src/postgres",
                    "downloads": 12500,
                    "rating": 4.8,
                    "last_update": "2026-01-30",
                    "features": ["连接池", "SQL查询", "事务管理", "数据迁移"],
                    "keywords": ["postgres", "postgresql", "sql", "database", "db"],
                    "install_cmd": "npx @anthropic-ai/mcp-server-postgres",
                    "language": "typescript"
                },
                {
                    "name": "MySQL",
                    "full_name": "mysql-mcp-server",
                    "description": "MySQL数据库连接和操作",
                    "category": "database",
                    "source": "community",
                    "github": "community/mysql-mcp",
                    "downloads": 8300,
                    "rating": 4.6,
                    "last_update": "2026-01-25",
                    "features": ["连接管理", "查询执行", "存储过程", "备份恢复"],
                    "keywords": ["mysql", "sql", "database", "db", "maria"],
                    "install_cmd": "npm install mysql-mcp-server",
                    "language": "typescript"
                },
                {
                    "name": "MongoDB",
                    "full_name": "mongodb-mcp-server",
                    "description": "MongoDB NoSQL数据库操作",
                    "category": "database",
                    "source": "community",
                    "github": "community/mongodb-mcp",
                    "downloads": 6700,
                    "rating": 4.5,
                    "last_update": "2026-01-20",
                    "features": ["文档操作", "聚合查询", "索引管理", "NoSQL"],
                    "keywords": ["mongodb", "mongo", "nosql", "database", "document"],
                    "install_cmd": "npm install mongodb-mcp-server",
                    "language": "typescript"
                },
                {
                    "name": "SQLite",
                    "full_name": "@anthropic-ai/mcp-server-sqlite",
                    "description": "SQLite轻量级数据库",
                    "category": "database",
                    "source": "official",
                    "github": "modelcontextprotocol/servers/tree/main/src/sqlite",
                    "downloads": 9200,
                    "rating": 4.7,
                    "last_update": "2026-01-28",
                    "features": ["本地数据库", "零配置", "SQL支持", "嵌入式"],
                    "keywords": ["sqlite", "sql", "database", "local", "embedded"],
                    "install_cmd": "npx @anthropic-ai/mcp-server-sqlite",
                    "language": "typescript"
                },
                
                # 文件系统类
                {
                    "name": "Filesystem",
                    "full_name": "@anthropic-ai/mcp-server-filesystem",
                    "description": "文件系统操作和访问",
                    "category": "filesystem",
                    "source": "official",
                    "github": "modelcontextprotocol/servers/tree/main/src/filesystem",
                    "downloads": 25300,
                    "rating": 4.9,
                    "last_update": "2026-02-01",
                    "features": ["文件读写", "目录遍历", "权限管理", "文件搜索"],
                    "keywords": ["filesystem", "file", "directory", "fs", "storage"],
                    "install_cmd": "npx @anthropic-ai/mcp-server-filesystem",
                    "language": "typescript"
                },
                {
                    "name": "PDF",
                    "full_name": "@anthropic-ai/mcp-pdf",
                    "description": "PDF文件读取和处理",
                    "category": "document",
                    "source": "official",
                    "github": "modelcontextprotocol/servers/tree/main/src/pdf",
                    "downloads": 18700,
                    "rating": 4.8,
                    "last_update": "2026-01-29",
                    "features": ["PDF读取", "文本提取", "元数据", "多页处理"],
                    "keywords": ["pdf", "document", "file", "read", "extract"],
                    "install_cmd": "npx @anthropic-ai/mcp-pdf",
                    "language": "typescript"
                },
                
                # Git类
                {
                    "name": "Git",
                    "full_name": "@anthropic-ai/mcp-server-git",
                    "description": "Git版本控制操作",
                    "category": "version-control",
                    "source": "official",
                    "github": "modelcontextprotocol/servers/tree/main/src/git",
                    "downloads": 15600,
                    "rating": 4.7,
                    "last_update": "2026-01-27",
                    "features": ["提交管理", "分支操作", "差异比较", "历史查看"],
                    "keywords": ["git", "version-control", "vcs", "commit", "branch"],
                    "install_cmd": "npx @anthropic-ai/mcp-server-git",
                    "language": "typescript"
                },
                {
                    "name": "GitHub",
                    "full_name": "github-mcp-server",
                    "description": "GitHub API集成",
                    "category": "version-control",
                    "source": "community",
                    "github": "community/github-mcp",
                    "downloads": 11200,
                    "rating": 4.6,
                    "last_update": "2026-01-22",
                    "features": ["Issue管理", "PR操作", "仓库管理", "Webhook"],
                    "keywords": ["github", "git", "api", "repository", "pr"],
                    "install_cmd": "npm install github-mcp-server",
                    "language": "typescript"
                },
                
                # Web/API类
                {
                    "name": "Fetch",
                    "full_name": "@anthropic-ai/mcp-server-fetch",
                    "description": "HTTP请求和API调用",
                    "category": "web",
                    "source": "official",
                    "github": "modelcontextprotocol/servers/tree/main/src/fetch",
                    "downloads": 22100,
                    "rating": 4.8,
                    "last_update": "2026-01-31",
                    "features": ["HTTP请求", "REST API", "JSON处理", "认证支持"],
                    "keywords": ["fetch", "http", "api", "request", "web", "rest"],
                    "install_cmd": "npx @anthropic-ai/mcp-server-fetch",
                    "language": "typescript"
                },
                {
                    "name": "Puppeteer",
                    "full_name": "puppeteer-mcp-server",
                    "description": "浏览器自动化和网页抓取",
                    "category": "web",
                    "source": "community",
                    "github": "community/puppeteer-mcp",
                    "downloads": 8900,
                    "rating": 4.5,
                    "last_update": "2026-01-18",
                    "features": ["浏览器控制", "网页抓取", "截图", "自动化测试"],
                    "keywords": ["puppeteer", "browser", "scraping", "automation", "web"],
                    "install_cmd": "npm install puppeteer-mcp-server",
                    "language": "typescript"
                },
                
                # AI/ML类
                {
                    "name": "OpenAI",
                    "full_name": "openai-mcp-server",
                    "description": "OpenAI API集成",
                    "category": "ai",
                    "source": "community",
                    "github": "community/openai-mcp",
                    "downloads": 14500,
                    "rating": 4.7,
                    "last_update": "2026-01-26",
                    "features": ["GPT调用", "Embedding", "图像生成", "文本补全"],
                    "keywords": ["openai", "gpt", "ai", "llm", "embedding"],
                    "install_cmd": "npm install openai-mcp-server",
                    "language": "typescript"
                },
                {
                    "name": "Hugging Face",
                    "full_name": "huggingface-mcp-server",
                    "description": "Hugging Face模型集成",
                    "category": "ai",
                    "source": "community",
                    "github": "community/huggingface-mcp",
                    "downloads": 6200,
                    "rating": 4.4,
                    "last_update": "2026-01-15",
                    "features": ["模型推理", "文本生成", "图像处理", "Pipeline"],
                    "keywords": ["huggingface", "transformers", "ai", "ml", "model"],
                    "install_cmd": "npm install huggingface-mcp-server",
                    "language": "typescript"
                },
                
                # 搜索类
                {
                    "name": "Brave Search",
                    "full_name": "brave-search-mcp",
                    "description": "Brave搜索引擎集成",
                    "category": "search",
                    "source": "community",
                    "github": "community/brave-search-mcp",
                    "downloads": 7800,
                    "rating": 4.6,
                    "last_update": "2026-01-24",
                    "features": ["网页搜索", "图片搜索", "新闻搜索", "隐私保护"],
                    "keywords": ["brave", "search", "web", "google", "bing"],
                    "install_cmd": "npm install brave-search-mcp",
                    "language": "typescript"
                },
                
                # 办公类
                {
                    "name": "Slack",
                    "full_name": "slack-mcp-server",
                    "description": "Slack消息和频道管理",
                    "category": "communication",
                    "source": "community",
                    "github": "community/slack-mcp",
                    "downloads": 5400,
                    "rating": 4.5,
                    "last_update": "2026-01-19",
                    "features": ["消息发送", "频道管理", "用户查询", "Webhook"],
                    "keywords": ["slack", "chat", "message", "communication", "team"],
                    "install_cmd": "npm install slack-mcp-server",
                    "language": "typescript"
                },
                {
                    "name": "Google Calendar",
                    "full_name": "google-calendar-mcp",
                    "description": "Google日历集成",
                    "category": "productivity",
                    "source": "community",
                    "github": "community/google-calendar-mcp",
                    "downloads": 4800,
                    "rating": 4.4,
                    "last_update": "2026-01-17",
                    "features": ["事件管理", "日程查询", "提醒设置", "日历共享"],
                    "keywords": ["google", "calendar", "schedule", "event", "productivity"],
                    "install_cmd": "npm install google-calendar-mcp",
                    "language": "typescript"
                }
            ],
            "categories": [
                {"id": "database", "name": "数据库", "icon": "🗄️"},
                {"id": "filesystem", "name": "文件系统", "icon": "📁"},
                {"id": "document", "name": "文档处理", "icon": "📄"},
                {"id": "version-control", "name": "版本控制", "icon": "🌿"},
                {"id": "web", "name": "Web/API", "icon": "🌐"},
                {"id": "ai", "name": "AI/ML", "icon": "🤖"},
                {"id": "search", "name": "搜索", "icon": "🔍"},
                {"id": "communication", "name": "通信", "icon": "💬"},
                {"id": "productivity", "name": "生产力", "icon": "⚡"}
            ],
            "last_updated": "2026-02-02"
        }
    
    def search(self, query: str, category: str = None, limit: int = 10) -> List[Dict]:
        """
        搜索MCP服务
        
        Args:
            query: 搜索关键词
            category: 类别筛选
            limit: 返回结果数量
            
        Returns:
            MCP服务列表
        """
        results = []
        query_lower = query.lower()
        query_keywords = set(query_lower.split())
        
        for mcp in self.database.get("mcps", []):
            # 类别筛选
            if category and mcp.get("category") != category:
                continue
            
            # 计算匹配分数
            score = self._calculate_match_score(mcp, query_lower, query_keywords)
            
            if score >= 0.3:  # 最小匹配阈值
                mcp_copy = mcp.copy()
                mcp_copy["match_score"] = score
                results.append(mcp_copy)
        
        # 按匹配分数排序
        results.sort(key=lambda x: x["match_score"], reverse=True)
        
        return results[:limit]
    
    def _calculate_match_score(self, mcp: Dict, query: str, query_keywords: set) -> float:
        """计算匹配分数"""
        scores = []
        
        # 1. 名称匹配 (权重: 0.35)
        name_lower = mcp["name"].lower()
        if query in name_lower:
            scores.append(0.35)
        elif any(kw in name_lower for kw in query_keywords):
            scores.append(0.25)
        else:
            name_similarity = SequenceMatcher(None, name_lower, query).ratio()
            scores.append(name_similarity * 0.2)
        
        # 2. 关键词匹配 (权重: 0.25)
        mcp_keywords = set(kw.lower() for kw in mcp.get("keywords", []))
        keyword_overlap = query_keywords & mcp_keywords
        if keyword_overlap:
            keyword_score = len(keyword_overlap) / len(query_keywords)
            scores.append(keyword_score * 0.25)
        else:
            scores.append(0)
        
        # 3. 描述匹配 (权重: 0.20)
        description = mcp.get("description", "").lower()
        if query in description:
            scores.append(0.20)
        elif any(kw in description for kw in query_keywords):
            scores.append(0.15)
        else:
            scores.append(0)
        
        # 4. 功能匹配 (权重: 0.20)
        features = " ".join(mcp.get("features", [])).lower()
        if any(kw in features for kw in query_keywords):
            scores.append(0.20)
        else:
            scores.append(0)
        
        return sum(scores)
    
    def get_by_category(self, category: str) -> List[Dict]:
        """按类别获取MCP"""
        return [mcp for mcp in self.database.get("mcps", []) 
                if mcp.get("category") == category]
    
    def get_categories(self) -> List[Dict]:
        """获取所有类别"""
        return self.database.get("categories", [])
    
    def get_top_rated(self, limit: int = 10) -> List[Dict]:
        """获取评分最高的MCP"""
        mcps = self.database.get("mcps", [])
        sorted_mcps = sorted(mcps, key=lambda x: x.get("rating", 0), reverse=True)
        return sorted_mcps[:limit]
    
    def get_most_downloaded(self, limit: int = 10) -> List[Dict]:
        """获取下载量最高的MCP"""
        mcps = self.database.get("mcps", [])
        sorted_mcps = sorted(mcps, key=lambda x: x.get("downloads", 0), reverse=True)
        return sorted_mcps[:limit]
    
    def get_recommendations(self, task_description: str, limit: int = 5) -> List[Dict]:
        """
        基于任务描述推荐MCP
        
        Args:
            task_description: 任务描述
            limit: 推荐数量
            
        Returns:
            推荐的MCP列表
        """
        # 分析任务描述，提取关键词
        keywords = self._extract_keywords(task_description)
        
        # 基于关键词搜索
        results = []
        for keyword in keywords:
            search_results = self.search(keyword, limit=limit)
            results.extend(search_results)
        
        # 去重并按匹配度排序
        seen = set()
        unique_results = []
        for r in results:
            if r["name"] not in seen:
                seen.add(r["name"])
                unique_results.append(r)
        
        unique_results.sort(key=lambda x: x.get("match_score", 0), reverse=True)
        
        return unique_results[:limit]
    
    def _extract_keywords(self, text: str) -> List[str]:
        """从文本中提取关键词"""
        # 定义关键词映射
        keyword_mapping = {
            "数据库": ["database", "sql", "postgres", "mysql", "mongo"],
            "database": ["database", "sql", "postgres", "mysql", "mongo"],
            "sql": ["sql", "database", "postgres", "mysql"],
            "文件": ["filesystem", "file", "pdf", "document"],
            "file": ["filesystem", "file", "pdf", "document"],
            "git": ["git", "github", "version-control"],
            "版本控制": ["git", "github", "version-control"],
            "api": ["fetch", "http", "api", "web"],
            "web": ["fetch", "http", "web", "puppeteer"],
            "http": ["fetch", "http", "api", "web"],
            "搜索": ["search", "brave", "google"],
            "search": ["search", "brave", "google"],
            "ai": ["ai", "openai", "huggingface", "gpt"],
            "人工智能": ["ai", "openai", "huggingface", "gpt"],
            "pdf": ["pdf", "document", "file"],
            "文档": ["pdf", "document", "file"],
        }
        
        text_lower = text.lower()
        keywords = []
        
        for key, related in keyword_mapping.items():
            if key in text_lower:
                keywords.extend(related)
        
        # 如果没有匹配到，使用原文作为关键词
        if not keywords:
            keywords = text_lower.split()
        
        return list(set(keywords))  # 去重
    
    def format_results(self, results: List[Dict]) -> str:
        """格式化搜索结果"""
        if not results:
            return "❌ 未找到相关MCP服务"
        
        output = f"🔍 找到 {len(results)} 个相关MCP服务\n\n"
        
        for i, mcp in enumerate(results, 1):
            # 排名图标
            rank_icon = {1: "🥇", 2: "🥈", 3: "🥉"}.get(i, f"{i}.")
            
            # 匹配度条
            score = mcp.get("match_score", 0)
            score_bar = "█" * int(score * 10) + "░" * (10 - int(score * 10))
            
            # 来源图标
            source_icon = {"official": "✅", "community": "👥"}.get(mcp.get("source"), "📦")
            
            output += f"{rank_icon} {mcp['name']} {source_icon}\n"
            output += f"   匹配度: [{score_bar}] {score:.1%}\n"
            output += f"   描述: {mcp['description']}\n"
            output += f"   ⭐ {mcp.get('rating', 0)}/5 | 📥 {mcp.get('downloads', 0):,}下载\n"
            output += f"   功能: {', '.join(mcp.get('features', [])[:3])}\n"
            output += f"   安装: `{mcp.get('install_cmd', 'N/A')}`\n"
            output += "\n"
        
        return output


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='MCP搜索工具')
    parser.add_argument('query', nargs='?', help='搜索关键词')
    parser.add_argument('--category', help='类别筛选')
    parser.add_argument('--limit', type=int, default=10, help='返回结果数量')
    parser.add_argument('--top-rated', action='store_true', help='显示评分最高的MCP')
    parser.add_argument('--most-downloaded', action='store_true', help='显示下载量最高的MCP')
    parser.add_argument('--categories', action='store_true', help='显示所有类别')
    parser.add_argument('--recommend', help='基于任务描述推荐MCP')
    
    args = parser.parse_args()
    
    searcher = MCPSearcher()
    
    if args.categories:
        print("📂 MCP类别:\n")
        for cat in searcher.get_categories():
            count = len(searcher.get_by_category(cat["id"]))
            print(f"{cat['icon']} {cat['name']} ({count}个)")
    
    elif args.top_rated:
        results = searcher.get_top_rated(args.limit)
        print(f"⭐ 评分最高的MCP (Top {len(results)}):\n")
        print(searcher.format_results(results))
    
    elif args.most_downloaded:
        results = searcher.get_most_downloaded(args.limit)
        print(f"📥 下载量最高的MCP (Top {len(results)}):\n")
        print(searcher.format_results(results))
    
    elif args.recommend:
        results = searcher.get_recommendations(args.recommend, args.limit)
        print(f"💡 为任务推荐的MCP: {args.recommend}\n")
        print(searcher.format_results(results))
    
    elif args.query:
        results = searcher.search(args.query, args.category, args.limit)
        print(searcher.format_results(results))
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
