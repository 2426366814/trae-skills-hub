#!/usr/bin/env python3
"""
自动安装工具
统一安装MCP服务和技能
"""
import os
import json
import subprocess
import shutil
import sys
from typing import Dict, List, Optional
from pathlib import Path


class AutoInstaller:
    """自动安装器"""
    
    def __init__(self):
        """初始化安装器"""
        self.trae_skills_dir = os.path.expanduser("~/.trae-cn/skills")
        self.mcp_dir = "./mcp-servers"
        
    def install_mcp(self, mcp_name: str, source: str = "npm") -> Dict:
        """
        安装MCP服务
        
        Args:
            mcp_name: MCP名称
            source: 来源 (npm/github)
            
        Returns:
            安装结果
        """
        print(f"🚀 安装MCP: {mcp_name}")
        
        # 创建MCP目录
        os.makedirs(self.mcp_dir, exist_ok=True)
        
        install_dir = os.path.join(self.mcp_dir, mcp_name.replace("@", "").replace("/", "-"))
        
        if source == "npm":
            return self._install_npm_package(mcp_name, install_dir)
        elif source == "github":
            return self._install_github_repo(mcp_name, install_dir)
        else:
            return {"success": False, "error": f"未知来源: {source}"}
    
    def _install_npm_package(self, package: str, install_dir: str) -> Dict:
        """安装npm包"""
        try:
            if os.path.exists(install_dir):
                shutil.rmtree(install_dir)
            os.makedirs(install_dir)
            
            # npm init
            subprocess.run(["npm", "init", "-y"], cwd=install_dir, check=True, capture_output=True)
            
            # npm install
            result = subprocess.run(
                ["npm", "install", package],
                cwd=install_dir,
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode == 0:
                return {
                    "success": True,
                    "message": f"✅ 成功安装 {package}",
                    "path": install_dir
                }
            else:
                return {"success": False, "error": result.stderr}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _install_github_repo(self, repo: str, install_dir: str) -> Dict:
        """安装GitHub仓库"""
        try:
            if os.path.exists(install_dir):
                shutil.rmtree(install_dir)
            
            repo_url = f"https://github.com/{repo}.git" if not repo.startswith("https://") else repo
            
            result = subprocess.run(
                ["git", "clone", "--depth", "1", repo_url, install_dir],
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode == 0:
                return {
                    "success": True,
                    "message": f"✅ 成功克隆 {repo}",
                    "path": install_dir
                }
            else:
                return {"success": False, "error": result.stderr}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def install_skill(self, skill_name: str, source: str = "github") -> Dict:
        """
        安装技能到Trae
        
        Args:
            skill_name: 技能名称或仓库
            source: 来源
            
        Returns:
            安装结果
        """
        print(f"🚀 安装技能: {skill_name}")
        
        # 确保Trae技能目录存在
        os.makedirs(self.trae_skills_dir, exist_ok=True)
        
        target_dir = os.path.join(self.trae_skills_dir, skill_name.split("/")[-1])
        
        if source == "github":
            return self._install_skill_from_github(skill_name, target_dir)
        elif source == "local":
            return self._install_skill_from_local(skill_name, target_dir)
        else:
            return {"success": False, "error": f"未知来源: {source}"}
    
    def _install_skill_from_github(self, repo: str, target_dir: str) -> Dict:
        """从GitHub安装技能"""
        try:
            # 备份已存在的技能
            if os.path.exists(target_dir):
                backup_dir = f"{target_dir}.backup"
                if os.path.exists(backup_dir):
                    shutil.rmtree(backup_dir)
                shutil.move(target_dir, backup_dir)
                print(f"📦 已备份到: {backup_dir}")
            
            # 克隆仓库
            repo_url = f"https://github.com/{repo}.git" if not repo.startswith("https://") else repo
            
            result = subprocess.run(
                ["git", "clone", "--depth", "1", repo_url, target_dir],
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode == 0:
                return {
                    "success": True,
                    "message": f"✅ 技能安装成功: {repo}",
                    "path": target_dir
                }
            else:
                return {"success": False, "error": result.stderr}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _install_skill_from_local(self, source_path: str, target_dir: str) -> Dict:
        """从本地安装技能"""
        try:
            if not os.path.exists(source_path):
                return {"success": False, "error": f"源路径不存在: {source_path}"}
            
            # 备份
            if os.path.exists(target_dir):
                backup_dir = f"{target_dir}.backup"
                if os.path.exists(backup_dir):
                    shutil.rmtree(backup_dir)
                shutil.move(target_dir, backup_dir)
            
            # 复制
            shutil.copytree(source_path, target_dir)
            
            return {
                "success": True,
                "message": f"✅ 技能复制成功",
                "path": target_dir
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def install_dependencies(self, project_dir: str) -> Dict:
        """
        安装项目依赖
        
        Args:
            project_dir: 项目目录
            
        Returns:
            安装结果
        """
        print(f"📦 安装依赖: {project_dir}")
        
        results = []
        
        # 检测并安装npm依赖
        if os.path.exists(os.path.join(project_dir, "package.json")):
            result = self._run_command(["npm", "install"], project_dir)
            results.append({"type": "npm", "result": result})
        
        # 检测并安装Python依赖
        if os.path.exists(os.path.join(project_dir, "requirements.txt")):
            result = self._run_command(["pip", "install", "-r", "requirements.txt"], project_dir)
            results.append({"type": "pip", "result": result})
        
        if os.path.exists(os.path.join(project_dir, "pyproject.toml")):
            result = self._run_command(["pip", "install", "-e", "."], project_dir)
            results.append({"type": "pip-e", "result": result})
        
        success = all(r["result"]["success"] for r in results)
        
        return {
            "success": success,
            "results": results
        }
    
    def _run_command(self, cmd: List[str], cwd: str) -> Dict:
        """运行命令"""
        try:
            result = subprocess.run(
                cmd,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=120
            )
            
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def list_installed(self, type: str = "all") -> Dict:
        """
        列出已安装的MCP和技能
        
        Args:
            type: 类型 (mcp/skills/all)
            
        Returns:
            列表结果
        """
        result = {"mcp": [], "skills": []}
        
        if type in ["mcp", "all"]:
            if os.path.exists(self.mcp_dir):
                result["mcp"] = [d for d in os.listdir(self.mcp_dir) 
                                if os.path.isdir(os.path.join(self.mcp_dir, d))]
        
        if type in ["skills", "all"]:
            if os.path.exists(self.trae_skills_dir):
                result["skills"] = [d for d in os.listdir(self.trae_skills_dir)
                                   if os.path.isdir(os.path.join(self.trae_skills_dir, d))]
        
        return result


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='自动安装工具')
    subparsers = parser.add_subparsers(dest='command', help='命令')
    
    # install-mcp
    install_mcp = subparsers.add_parser('install-mcp', help='安装MCP')
    install_mcp.add_argument('name', help='MCP名称')
    install_mcp.add_argument('--source', choices=['npm', 'github'], default='npm', help='来源')
    
    # install-skill
    install_skill = subparsers.add_parser('install-skill', help='安装技能')
    install_skill.add_argument('name', help='技能名称或仓库')
    install_skill.add_argument('--source', choices=['github', 'local'], default='github', help='来源')
    
    # deps
    deps = subparsers.add_parser('deps', help='安装依赖')
    deps.add_argument('dir', help='项目目录')
    
    # list
    list_cmd = subparsers.add_parser('list', help='列出已安装')
    list_cmd.add_argument('--type', choices=['mcp', 'skills', 'all'], default='all', help='类型')
    
    args = parser.parse_args()
    
    installer = AutoInstaller()
    
    if args.command == 'install-mcp':
        result = installer.install_mcp(args.name, args.source)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif args.command == 'install-skill':
        result = installer.install_skill(args.name, args.source)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif args.command == 'deps':
        result = installer.install_dependencies(args.dir)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif args.command == 'list':
        result = installer.list_installed(args.type)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
