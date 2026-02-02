#!/usr/bin/env python3
"""
技能搜索工具
支持本地、GitHub和Vercel Skills商店搜索
"""
import os
import json
import re
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional
from difflib import SequenceMatcher
import sys

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class SkillSearcher:
    """技能搜索器"""
    
    def __init__(self, config_path: str = None):
        """初始化搜索器"""
        self.config = self._load_config(config_path)
        self.cache = {}
        self.local_skills_dir = os.path.expanduser("~/.trae-cn/skills")
        
    def _load_config(self, config_path: str = None) -> Dict:
        """加载配置"""
        if config_path is None:
            config_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "config", "sources.json"
            )
        
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # 默认配置
        return {
            "sources": {
                "local": {"enabled": True, "path": "~/.trae-cn/skills"},
                "github": {"enabled": True, "api_url": "https://api.github.com"},
                "vercel": {"enabled": True, "api_url": "https://skills.sh/api"}
            },
            "search": {
                "default_limit": 10,
                "cache_duration": 3600,
                "min_score": 0.3
            }
        }
    
    def search(self, query: str, source: str = "all", limit: int = 10) -> List[Dict]:
        """
        搜索技能
        
        Args:
            query: 搜索关键词
            source: 搜索源 (local/github/vercel/all)
            limit: 返回结果数量
            
        Returns:
            技能列表
        """
        results = []
        
        if source in ["local", "all"]:
            local_results = self._search_local(query, limit)
            results.extend(local_results)
        
        if source in ["github", "all"]:
            github_results = self._search_github(query, limit)
            results.extend(github_results)
        
        if source in ["vercel", "all"]:
            vercel_results = self._search_vercel(query, limit)
            results.extend(vercel_results)
        
        # 去重和排序
        results = self._deduplicate_and_sort(results, query)
        
        return results[:limit]
    
    def _search_local(self, query: str, limit: int) -> List[Dict]:
        """搜索本地技能"""
        results = []
        
        if not os.path.exists(self.local_skills_dir):
            return results
        
        query_lower = query.lower()
        query_keywords = set(query_lower.split())
        
        for skill_name in os.listdir(self.local_skills_dir):
            skill_path = os.path.join(self.local_skills_dir, skill_name)
            
            if not os.path.isdir(skill_path):
                continue
            
            # 计算匹配分数
            score = self._calculate_match_score(skill_name, query, skill_path)
            
            if score >= self.config["search"]["min_score"]:
                skill_info = self._get_skill_info(skill_path, skill_name)
                skill_info["score"] = score
                skill_info["source"] = "local"
                results.append(skill_info)
        
        return sorted(results, key=lambda x: x["score"], reverse=True)[:limit]
    
    def _search_github(self, query: str, limit: int) -> List[Dict]:
        """搜索GitHub技能仓库"""
        results = []
        
        # 预定义的高质量技能仓库
        github_skills = [
            {"name": "awesome-claude-skills", "owner": "ComposioHQ", "stars": 12000},
            {"name": "claude-code-infrastructure-showcase", "owner": "diet103", "stars": 7000},
            {"name": "superpowers", "owner": "obra", "stars": 12000},
            {"name": "Skill_Seekers", "owner": "yusufkaraaslan", "stars": 500},
        ]
        
        query_lower = query.lower()
        
        for skill in github_skills:
            # 计算匹配分数
            name_score = self._calculate_match_score(skill["name"], query)
            
            if name_score >= self.config["search"]["min_score"]:
                results.append({
                    "name": skill["name"],
                    "full_name": f"{skill['owner']}/{skill['name']}",
                    "description": f"GitHub skill repository by {skill['owner']}",
                    "stars": skill["stars"],
                    "score": name_score,
                    "source": "github",
                    "url": f"https://github.com/{skill['owner']}/{skill['name']}"
                })
        
        return sorted(results, key=lambda x: x["score"], reverse=True)[:limit]
    
    def _search_vercel(self, query: str, limit: int) -> List[Dict]:
        """搜索Vercel Skills商店"""
        results = []
        
        # 预定义的热门Vercel技能
        vercel_skills = [
            {"name": "vercel-react-best-practices", "downloads": 39600, "rank": 1},
            {"name": "web-design-guidelines", "downloads": 30100, "rank": 2},
            {"name": "remotion-best-practices", "downloads": 21500, "rank": 3},
            {"name": "frontend-design", "downloads": 8600, "rank": 4},
            {"name": "skill-creator", "downloads": 4300, "rank": 5},
            {"name": "agent-browser", "downloads": 3100, "rank": 6},
            {"name": "building-native-ui", "downloads": 3000, "rank": 7},
            {"name": "seo-audit", "downloads": 2600, "rank": 8},
            {"name": "better-auth-best-practices", "downloads": 2600, "rank": 9},
            {"name": "audit-website", "downloads": 2500, "rank": 10},
        ]
        
        query_lower = query.lower()
        
        for skill in vercel_skills:
            # 计算匹配分数
            name_score = self._calculate_match_score(skill["name"], query)
            
            # 考虑下载量和排名
            popularity_score = min(skill["downloads"] / 50000, 1.0) * 0.3
            rank_score = (11 - skill["rank"]) / 10 * 0.2 if skill["rank"] else 0
            
            total_score = name_score * 0.5 + popularity_score + rank_score
            
            if total_score >= self.config["search"]["min_score"]:
                results.append({
                    "name": skill["name"],
                    "description": f"Vercel Skills Store - Rank #{skill['rank']}",
                    "downloads": skill["downloads"],
                    "rank": skill["rank"],
                    "score": total_score,
                    "source": "vercel",
                    "url": f"https://skills.sh/s/{skill['name']}"
                })
        
        return sorted(results, key=lambda x: x["score"], reverse=True)[:limit]
    
    def _calculate_match_score(self, skill_name: str, query: str, skill_path: str = None) -> float:
        """计算匹配分数"""
        skill_lower = skill_name.lower()
        query_lower = query.lower()
        
        # 精确匹配
        if skill_lower == query_lower:
            return 1.0
        
        # 包含匹配
        if query_lower in skill_lower:
            return 0.9
        
        if skill_lower in query_lower:
            return 0.8
        
        # 相似度匹配
        similarity = SequenceMatcher(None, skill_lower, query_lower).ratio()
        
        # 关键词匹配
        query_keywords = set(query_lower.split())
        skill_keywords = set(skill_lower.replace("-", " ").replace("_", " ").split())
        
        if query_keywords & skill_keywords:
            keyword_score = len(query_keywords & skill_keywords) / len(query_keywords)
            similarity = max(similarity, keyword_score * 0.7)
        
        # 如果提供了技能路径，读取SKILL.md进行语义匹配
        if skill_path and os.path.exists(skill_path):
            semantic_score = self._semantic_match(skill_path, query_lower)
            similarity = max(similarity, semantic_score)
        
        return similarity
    
    def _semantic_match(self, skill_path: str, query: str) -> float:
        """语义匹配"""
        skill_md = os.path.join(skill_path, "SKILL.md")
        
        if not os.path.exists(skill_md):
            return 0.0
        
        try:
            with open(skill_md, 'r', encoding='utf-8') as f:
                content = f.read().lower()
            
            # 检查描述和关键词
            query_keywords = set(query.split())
            content_words = set(content.split())
            
            overlap = query_keywords & content_words
            if overlap:
                return len(overlap) / len(query_keywords) * 0.6
            
            return 0.0
        except:
            return 0.0
    
    def _get_skill_info(self, skill_path: str, skill_name: str) -> Dict:
        """获取技能信息"""
        info = {
            "name": skill_name,
            "path": skill_path,
            "description": "",
            "installed": True
        }
        
        # 读取SKILL.md
        skill_md = os.path.join(skill_path, "SKILL.md")
        if os.path.exists(skill_md):
            try:
                with open(skill_md, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # 提取描述（假设第一行是标题，第二行是描述）
                    lines = content.split('\n')
                    for line in lines[1:10]:
                        if line.strip() and not line.startswith('#'):
                            info["description"] = line.strip()[:200]
                            break
            except:
                pass
        
        return info
    
    def _deduplicate_and_sort(self, results: List[Dict], query: str) -> List[Dict]:
        """去重和排序"""
        seen = set()
        unique_results = []
        
        for result in results:
            name = result["name"]
            if name not in seen:
                seen.add(name)
                unique_results.append(result)
        
        # 按分数排序
        return sorted(unique_results, key=lambda x: x.get("score", 0), reverse=True)
    
    def format_results(self, results: List[Dict]) -> str:
        """格式化搜索结果"""
        if not results:
            return "❌ 未找到相关技能"
        
        output = f"🔍 找到 {len(results)} 个相关技能\n\n"
        
        for i, skill in enumerate(results, 1):
            source_icon = {
                "local": "📁",
                "github": "🐙",
                "vercel": "▲"
            }.get(skill.get("source", "local"), "📦")
            
            score = skill.get("score", 0)
            score_bar = "█" * int(score * 10) + "░" * (10 - int(score * 10))
            
            output += f"{i}. {source_icon} {skill['name']}\n"
            output += f"   匹配度: [{score_bar}] {score:.1%}\n"
            
            if skill.get("description"):
                output += f"   描述: {skill['description'][:100]}\n"
            
            if skill.get("stars"):
                output += f"   ⭐ {skill['stars']:,}\n"
            
            if skill.get("downloads"):
                output += f"   📥 {skill['downloads']:,} 下载\n"
            
            if skill.get("source") == "local":
                output += f"   ✅ 已安装\n"
            elif skill.get("url"):
                output += f"   🔗 {skill['url']}\n"
            
            output += "\n"
        
        return output


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='技能搜索工具')
    parser.add_argument('query', help='搜索关键词')
    parser.add_argument('--source', choices=['local', 'github', 'vercel', 'all'], 
                       default='all', help='搜索源')
    parser.add_argument('--limit', type=int, default=10, help='返回结果数量')
    parser.add_argument('--json', action='store_true', help='以JSON格式输出')
    
    args = parser.parse_args()
    
    searcher = SkillSearcher()
    results = searcher.search(args.query, args.source, args.limit)
    
    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        print(searcher.format_results(results))


if __name__ == "__main__":
    main()
