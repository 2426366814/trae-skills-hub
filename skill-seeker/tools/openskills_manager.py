#!/usr/bin/env python3
"""
OpenSkills管理工具
集成OpenSkills CLI到Skill Seeker
"""
import os
import json
import subprocess
import sys
from typing import List, Dict, Any, Optional
from pathlib import Path

class OpenSkillsManager:
    """OpenSkills管理器"""
    
    def __init__(self):
        """初始化管理器"""
        self.command = "npx openskills"
        self.installed_skills = []
        self._refresh_installed_list()
    
    def _run_command(self, args: List[str]) -> tuple:
        """运行OpenSkills命令"""
        cmd = ["npx", "openskills"] + args
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60,
                check=False
            )
            return result.returncode == 0, result.stdout, result.stderr
        except Exception as e:
            return False, "", str(e)
    
    def _refresh_installed_list(self):
        """刷新已安装技能列表"""
        success, stdout, stderr = self._run_command(["list"])
        if success:
            self.installed_skills = self._parse_list_output(stdout)
    
    def _parse_list_output(self, output: str) -> List[Dict]:
        """解析list命令输出"""
        skills = []
        lines = output.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('-') or line.startswith('Installed'):
                continue
            
            # 解析技能名称和来源
            if ' ' in line:
                parts = line.split()
                skill_name = parts[0]
                source = parts[1] if len(parts) > 1 else "unknown"
                
                skills.append({
                    "name": skill_name,
                    "source": source,
                    "installed": True
                })
        
        return skills
    
    def list_skills(self) -> List[Dict]:
        """列出已安装的技能"""
        self._refresh_installed_list()
        return self.installed_skills
    
    def install_skill(self, source: str) -> Dict:
        """
        安装技能
        
        Args:
            source: 技能来源，如 "owner/repo" 或 Git URL
            
        Returns:
            安装结果
        """
        print(f"📦 正在安装技能: {source}")
        
        success, stdout, stderr = self._run_command(["install", source])
        
        if success:
            self._refresh_installed_list()
            return {
                "success": True,
                "message": f"✅ 成功安装技能: {source}",
                "output": stdout
            }
        else:
            return {
                "success": False,
                "message": f"❌ 安装失败: {source}",
                "error": stderr,
                "output": stdout
            }
    
    def read_skill(self, skill_name: str) -> Dict:
        """
        读取技能内容
        
        Args:
            skill_name: 技能名称
            
        Returns:
            技能内容
        """
        success, stdout, stderr = self._run_command(["read", skill_name])
        
        if success:
            return {
                "success": True,
                "content": stdout,
                "skill_name": skill_name
            }
        else:
            return {
                "success": False,
                "error": stderr,
                "skill_name": skill_name
            }
    
    def update_skills(self, skill_names: List[str] = None) -> Dict:
        """
        更新技能
        
        Args:
            skill_names: 要更新的技能列表，None表示更新所有
            
        Returns:
            更新结果
        """
        if skill_names:
            print(f"🔄 正在更新技能: {', '.join(skill_names)}")
            success, stdout, stderr = self._run_command(["update"] + skill_names)
        else:
            print("🔄 正在更新所有技能...")
            success, stdout, stderr = self._run_command(["update"])
        
        if success:
            self._refresh_installed_list()
            return {
                "success": True,
                "message": "✅ 更新完成",
                "output": stdout
            }
        else:
            return {
                "success": False,
                "message": "❌ 更新失败",
                "error": stderr
            }
    
    def remove_skill(self, skill_name: str) -> Dict:
        """
        移除技能
        
        Args:
            skill_name: 技能名称
            
        Returns:
            移除结果
        """
        print(f"🗑️ 正在移除技能: {skill_name}")
        
        success, stdout, stderr = self._run_command(["remove", skill_name])
        
        if success:
            self._refresh_installed_list()
            return {
                "success": True,
                "message": f"✅ 成功移除技能: {skill_name}",
                "output": stdout
            }
        else:
            return {
                "success": False,
                "message": f"❌ 移除失败: {skill_name}",
                "error": stderr
            }
    
    def sync_agents(self, interactive: bool = True) -> Dict:
        """
        同步AGENTS.md
        
        Args:
            interactive: 是否交互模式
            
        Returns:
            同步结果
        """
        print("🔄 正在同步AGENTS.md...")
        
        args = ["sync"]
        if not interactive:
            args.append("--yes")
        
        success, stdout, stderr = self._run_command(args)
        
        if success:
            return {
                "success": True,
                "message": "✅ AGENTS.md同步完成",
                "output": stdout
            }
        else:
            return {
                "success": False,
                "message": "❌ 同步失败",
                "error": stderr
            }
    
    def search_openskills_repo(self, query: str) -> List[Dict]:
        """
        搜索OpenSkills官方仓库的技能
        
        Args:
            query: 搜索关键词
            
        Returns:
            技能列表
        """
        # OpenSkills官方技能列表
        official_skills = [
            {"name": "pdf", "repo": "anthropics/skills", "description": "PDF编辑和处理"},
            {"name": "docx", "repo": "anthropics/skills", "description": "Word文档处理"},
            {"name": "web-scraping", "repo": "anthropics/skills", "description": "网页抓取"},
            {"name": "data-analysis", "repo": "anthropics/skills", "description": "数据分析"},
            {"name": "react", "repo": "anthropics/webdev-skills", "description": "React开发"},
            {"name": "vue", "repo": "anthropics/webdev-skills", "description": "Vue开发"},
            {"name": "typescript", "repo": "anthropics/webdev-skills", "description": "TypeScript开发"},
            {"name": "css", "repo": "anthropics/webdev-skills", "description": "CSS样式"},
        ]
        
        results = []
        query_lower = query.lower()
        
        for skill in official_skills:
            # 匹配技能名称
            if query_lower in skill["name"].lower():
                results.append(skill)
            # 匹配描述
            elif query_lower in skill["description"].lower():
                results.append(skill)
        
        return results
    
    def get_skill_info(self, skill_name: str) -> Dict:
        """获取技能详细信息"""
        # 检查是否已安装
        installed = any(s["name"] == skill_name for s in self.installed_skills)
        
        # 尝试读取技能内容
        read_result = self.read_skill(skill_name)
        
        return {
            "name": skill_name,
            "installed": installed,
            "content": read_result.get("content", "") if read_result["success"] else None,
            "readable": read_result["success"]
        }
    
    def format_list(self, skills: List[Dict]) -> str:
        """格式化技能列表"""
        if not skills:
            return "❌ 没有已安装的技能"
        
        output = f"📦 OpenSkills已安装技能 ({len(skills)}个)\n"
        output += "=" * 60 + "\n\n"
        
        for i, skill in enumerate(skills, 1):
            output += f"{i}. 📋 {skill['name']}\n"
            if skill.get('source'):
                output += f"   来源: {skill['source']}\n"
            output += "\n"
        
        return output
    
    def format_install_result(self, result: Dict) -> str:
        """格式化安装结果"""
        if result["success"]:
            return f"""✅ 安装成功

{result['message']}

输出:
{result.get('output', '')}
"""
        else:
            return f"""❌ 安装失败

{result['message']}

错误:
{result.get('error', '未知错误')}
"""


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='OpenSkills管理工具')
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # list命令
    list_parser = subparsers.add_parser('list', help='列出已安装技能')
    
    # install命令
    install_parser = subparsers.add_parser('install', help='安装技能')
    install_parser.add_argument('source', help='技能来源 (owner/repo)')
    
    # read命令
    read_parser = subparsers.add_parser('read', help='读取技能内容')
    read_parser.add_argument('skill', help='技能名称')
    
    # update命令
    update_parser = subparsers.add_parser('update', help='更新技能')
    update_parser.add_argument('skills', nargs='*', help='技能名称 (默认更新所有)')
    
    # remove命令
    remove_parser = subparsers.add_parser('remove', help='移除技能')
    remove_parser.add_argument('skill', help='技能名称')
    
    # sync命令
    sync_parser = subparsers.add_parser('sync', help='同步AGENTS.md')
    sync_parser.add_argument('--yes', action='store_true', help='非交互模式')
    
    # search命令
    search_parser = subparsers.add_parser('search', help='搜索官方技能')
    search_parser.add_argument('query', help='搜索关键词')
    
    args = parser.parse_args()
    
    manager = OpenSkillsManager()
    
    if args.command == 'list':
        skills = manager.list_skills()
        print(manager.format_list(skills))
    
    elif args.command == 'install':
        result = manager.install_skill(args.source)
        print(manager.format_install_result(result))
    
    elif args.command == 'read':
        result = manager.read_skill(args.skill)
        if result["success"]:
            print(f"📖 技能内容: {args.skill}\n")
            print(result["content"])
        else:
            print(f"❌ 读取失败: {result.get('error', '')}")
    
    elif args.command == 'update':
        result = manager.update_skills(args.skills if args.skills else None)
        print(result["message"])
        if not result["success"]:
            print(f"错误: {result.get('error', '')}")
    
    elif args.command == 'remove':
        result = manager.remove_skill(args.skill)
        print(result["message"])
    
    elif args.command == 'sync':
        result = manager.sync_agents(interactive=not args.yes)
        print(result["message"])
    
    elif args.command == 'search':
        results = manager.search_openskills_repo(args.query)
        if results:
            print(f"🔍 找到 {len(results)} 个相关技能:\n")
            for skill in results:
                print(f"📦 {skill['name']}")
                print(f"   仓库: {skill['repo']}")
                print(f"   描述: {skill['description']}")
                print(f"   安装: openskills install {skill['repo']}/{skill['name']}")
                print()
        else:
            print(f"❌ 未找到与 '{args.query}' 相关的技能")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
