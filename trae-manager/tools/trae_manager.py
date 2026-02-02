#!/usr/bin/env python3
"""
Trae Manager - 统一管理和部署工具
包含今天所有需求：技能搜索、MCP安装、自动安装、跨机器部署
"""
import os
import json
import shutil
import subprocess
import sys
from typing import Dict, List, Optional
from pathlib import Path
from datetime import datetime


class TraeManager:
    """Trae管理器"""
    
    def __init__(self):
        """初始化管理器"""
        self.trae_skills_dir = os.path.expanduser("~/.trae-cn/skills")
        self.mcp_dir = "./mcp-servers"
        self.config_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.deps_file = os.path.join(self.config_dir, "data", "dependencies.json")
        
        # 加载依赖配置
        self.dependencies = self._load_dependencies()
    
    def _load_dependencies(self) -> Dict:
        """加载依赖配置"""
        if os.path.exists(self.deps_file):
            with open(self.deps_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def setup(self, mode: str = "full", auto_install: bool = False) -> Dict:
        """
        设置完整环境
        
        Args:
            mode: 设置模式 (full/skills/mcp/deps)
            auto_install: 是否自动安装
            
        Returns:
            设置结果
        """
        print(f"🚀 开始设置Trae环境 [模式: {mode}]")
        
        results = {
            "mode": mode,
            "timestamp": datetime.now().isoformat(),
            "steps": [],
            "success": False
        }
        
        # 1. 检查环境
        if mode in ["full", "deps"]:
            env_result = self.check_env()
            results["steps"].append({"name": "环境检查", "result": env_result})
        
        # 2. 安装技能
        if mode in ["full", "skills"]:
            skills_result = self.install_skills("--all" if auto_install else "core")
            results["steps"].append({"name": "技能安装", "result": skills_result})
        
        # 3. 安装MCP
        if mode in ["full", "mcp"]:
            mcp_result = self.install_mcp("--recommended" if auto_install else "")
            results["steps"].append({"name": "MCP安装", "result": mcp_result})
        
        # 4. 安装依赖
        if mode in ["full", "deps"]:
            deps_result = self._install_all_dependencies()
            results["steps"].append({"name": "依赖安装", "result": deps_result})
        
        results["success"] = all(s["result"].get("success", False) for s in results["steps"])
        
        return results
    
    def install_skills(self, skills: str) -> Dict:
        """
        安装技能
        
        Args:
            skills: 技能名称或--all/core
            
        Returns:
            安装结果
        """
        print(f"📦 安装技能: {skills}")
        
        if skills == "--all":
            # 安装所有技能
            all_skills = []
            for category in ["core_skills", "document_skills", "development_skills", "tool_skills"]:
                all_skills.extend(self.dependencies.get(category, {}).keys())
            skill_list = all_skills
        elif skills == "core":
            # 安装核心技能
            skill_list = list(self.dependencies.get("core_skills", {}).keys())
        else:
            # 安装指定技能
            skill_list = skills.split(",")
        
        results = []
        for skill in skill_list:
            skill = skill.strip()
            result = self._install_single_skill(skill)
            results.append({"skill": skill, "result": result})
        
        success = all(r["result"].get("success", False) for r in results)
        
        return {
            "success": success,
            "installed": len([r for r in results if r["result"].get("success")]),
            "failed": len([r for r in results if not r["result"].get("success")]),
            "details": results
        }
    
    def _install_single_skill(self, skill_name: str) -> Dict:
        """安装单个技能"""
        # 查找技能配置
        skill_config = None
        for category in ["core_skills", "document_skills", "development_skills", "tool_skills"]:
            if skill_name in self.dependencies.get(category, {}):
                skill_config = self.dependencies[category][skill_name]
                break
        
        if not skill_config:
            return {"success": False, "error": f"未找到技能配置: {skill_name}"}
        
        # 根据来源安装
        source = skill_config.get("source", "local")
        
        if source == "local":
            return self._install_local_skill(skill_name, skill_config)
        elif source == "core":
            return self._install_core_skill(skill_name, skill_config)
        else:
            return {"success": False, "error": f"未知的技能来源: {source}"}
    
    def _install_local_skill(self, skill_name: str, config: Dict) -> Dict:
        """安装本地技能"""
        try:
            source_path = config.get("path", skill_name)
            target_dir = os.path.join(self.trae_skills_dir, skill_name)
            
            # 确保目标目录存在
            os.makedirs(self.trae_skills_dir, exist_ok=True)
            
            # 备份已存在的技能
            if os.path.exists(target_dir):
                backup_dir = f"{target_dir}.backup"
                if os.path.exists(backup_dir):
                    shutil.rmtree(backup_dir)
                shutil.move(target_dir, backup_dir)
                print(f"  📦 已备份: {skill_name}")
            
            # 复制技能
            if os.path.exists(source_path):
                shutil.copytree(source_path, target_dir)
                
                # 安装依赖
                self._install_skill_dependencies(target_dir, config.get("dependencies", {}))
                
                return {"success": True, "message": f"✅ 技能安装成功: {skill_name}"}
            else:
                return {"success": False, "error": f"源路径不存在: {source_path}"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _install_core_skill(self, skill_name: str, config: Dict) -> Dict:
        """安装核心技能"""
        # 核心技能假设已存在，只需安装依赖
        try:
            target_dir = os.path.join(self.trae_skills_dir, skill_name)
            
            if os.path.exists(target_dir):
                self._install_skill_dependencies(target_dir, config.get("dependencies", {}))
                return {"success": True, "message": f"✅ 核心技能已配置: {skill_name}"}
            else:
                return {"success": False, "error": f"核心技能未找到: {skill_name}"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _install_skill_dependencies(self, skill_dir: str, dependencies: Dict):
        """安装技能依赖"""
        # npm依赖
        if "npm" in dependencies and dependencies["npm"]:
            for pkg in dependencies["npm"]:
                subprocess.run(["npm", "install", "-g", pkg], capture_output=True)
        
        # pip依赖
        if "pip" in dependencies and dependencies["pip"]:
            for pkg in dependencies["pip"]:
                subprocess.run([sys.executable, "-m", "pip", "install", pkg], capture_output=True)
    
    def install_mcp(self, mcp: str) -> Dict:
        """
        安装MCP服务
        
        Args:
            mcp: MCP名称或--recommended
            
        Returns:
            安装结果
        """
        print(f"🔌 安装MCP: {mcp}")
        
        if mcp == "--recommended":
            # 安装推荐的MCP
            mcp_list = ["filesystem", "fetch", "git", "pdf"]
        elif mcp:
            mcp_list = mcp.split(",")
        else:
            return {"success": False, "error": "未指定MCP"}
        
        results = []
        for mcp_name in mcp_list:
            mcp_name = mcp_name.strip()
            result = self._install_single_mcp(mcp_name)
            results.append({"mcp": mcp_name, "result": result})
        
        success = all(r["result"].get("success", False) for r in results)
        
        return {
            "success": success,
            "installed": len([r for r in results if r["result"].get("success")]),
            "details": results
        }
    
    def _install_single_mcp(self, mcp_name: str) -> Dict:
        """安装单个MCP"""
        mcp_config = self.dependencies.get("mcp_servers", {}).get(mcp_name)
        
        if not mcp_config:
            return {"success": False, "error": f"未找到MCP配置: {mcp_name}"}
        
        try:
            package = mcp_config.get("package")
            source = mcp_config.get("source", "npm")
            
            # 创建MCP目录
            os.makedirs(self.mcp_dir, exist_ok=True)
            install_dir = os.path.join(self.mcp_dir, mcp_name)
            
            if os.path.exists(install_dir):
                shutil.rmtree(install_dir)
            os.makedirs(install_dir)
            
            if source == "npm":
                # npm安装
                subprocess.run(["npm", "init", "-y"], cwd=install_dir, check=True, capture_output=True)
                result = subprocess.run(
                    ["npm", "install", package],
                    cwd=install_dir,
                    capture_output=True,
                    text=True,
                    timeout=120
                )
                
                if result.returncode == 0:
                    return {"success": True, "message": f"✅ MCP安装成功: {mcp_name}"}
                else:
                    return {"success": False, "error": result.stderr}
            else:
                return {"success": False, "error": f"不支持的MCP来源: {source}"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def check_env(self) -> Dict:
        """检查环境"""
        print("🔍 检查环境...")
        
        checks = {
            "node": self._check_command("node", "--version"),
            "npm": self._check_command("npm", "--version"),
            "python": self._check_command(sys.executable, "--version"),
            "git": self._check_command("git", "--version"),
        }
        
        all_ok = all(c["ok"] for c in checks.values())
        
        return {
            "success": all_ok,
            "checks": checks,
            "message": "✅ 环境检查通过" if all_ok else "❌ 环境检查失败"
        }
    
    def _check_command(self, cmd: str, arg: str) -> Dict:
        """检查命令是否存在"""
        try:
            result = subprocess.run(
                [cmd, arg],
                capture_output=True,
                text=True,
                timeout=10
            )
            return {
                "ok": result.returncode == 0,
                "version": result.stdout.strip() if result.returncode == 0 else None
            }
        except:
            return {"ok": False, "version": None}
    
    def _install_all_dependencies(self) -> Dict:
        """安装所有依赖"""
        print("📦 安装所有依赖...")
        
        # 收集所有依赖
        npm_deps = set()
        pip_deps = set()
        
        for category in ["core_skills", "document_skills", "development_skills", "tool_skills"]:
            for skill_name, skill_config in self.dependencies.get(category, {}).items():
                deps = skill_config.get("dependencies", {})
                npm_deps.update(deps.get("npm", []))
                pip_deps.update(deps.get("pip", []))
        
        # 安装npm依赖
        npm_results = []
        for pkg in npm_deps:
            result = subprocess.run(
                ["npm", "install", "-g", pkg],
                capture_output=True,
                text=True
            )
            npm_results.append({"package": pkg, "success": result.returncode == 0})
        
        # 安装pip依赖
        pip_results = []
        for pkg in pip_deps:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", pkg],
                capture_output=True,
                text=True
            )
            pip_results.append({"package": pkg, "success": result.returncode == 0})
        
        return {
            "success": all(r["success"] for r in npm_results + pip_results),
            "npm": npm_results,
            "pip": pip_results
        }
    
    def export_config(self, full: bool = False) -> Dict:
        """
        导出配置
        
        Args:
            full: 是否导出完整配置
            
        Returns:
            配置数据
        """
        config = {
            "version": "1.0.0",
            "timestamp": datetime.now().isoformat(),
            "export_type": "full" if full else "minimal"
        }
        
        if full:
            # 导出已安装的技能
            config["installed_skills"] = self._get_installed_skills()
            config["installed_mcp"] = self._get_installed_mcp()
            config["dependencies"] = self.dependencies
        
        return config
    
    def _get_installed_skills(self) -> List[str]:
        """获取已安装的技能"""
        if os.path.exists(self.trae_skills_dir):
            return [d for d in os.listdir(self.trae_skills_dir) 
                   if os.path.isdir(os.path.join(self.trae_skills_dir, d))]
        return []
    
    def _get_installed_mcp(self) -> List[str]:
        """获取已安装的MCP"""
        if os.path.exists(self.mcp_dir):
            return [d for d in os.listdir(self.mcp_dir)
                   if os.path.isdir(os.path.join(self.mcp_dir, d))]
        return []
    
    def import_config(self, config_file: str, auto_install: bool = False) -> Dict:
        """
        导入配置
        
        Args:
            config_file: 配置文件路径
            auto_install: 是否自动安装
            
        Returns:
            导入结果
        """
        print(f"📥 导入配置: {config_file}")
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            results = {"success": True, "steps": []}
            
            # 安装技能
            if auto_install and "installed_skills" in config:
                skills = ",".join(config["installed_skills"])
                result = self.install_skills(skills)
                results["steps"].append({"name": "安装技能", "result": result})
            
            # 安装MCP
            if auto_install and "installed_mcp" in config:
                mcp = ",".join(config["installed_mcp"])
                result = self.install_mcp(mcp)
                results["steps"].append({"name": "安装MCP", "result": result})
            
            return results
            
        except Exception as e:
            return {"success": False, "error": str(e)}


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Trae Manager - 统一管理和部署工具')
    subparsers = parser.add_subparsers(dest='command', help='命令')
    
    # setup
    setup_cmd = subparsers.add_parser('setup', help='设置完整环境')
    setup_cmd.add_argument('--mode', choices=['full', 'skills', 'mcp', 'deps'], 
                          default='full', help='设置模式')
    setup_cmd.add_argument('--auto-install', action='store_true', help='自动安装')
    
    # install-skills
    install_skills_cmd = subparsers.add_parser('install-skills', help='安装技能')
    install_skills_cmd.add_argument('skills', help='技能名称或--all/core')
    
    # install-mcp
    install_mcp_cmd = subparsers.add_parser('install-mcp', help='安装MCP')
    install_mcp_cmd.add_argument('mcp', help='MCP名称或--recommended')
    
    # check-env
    subparsers.add_parser('check-env', help='检查环境')
    
    # export
    export_cmd = subparsers.add_parser('export', help='导出配置')
    export_cmd.add_argument('--full', action='store_true', help='导出完整配置')
    
    # import
    import_cmd = subparsers.add_parser('import', help='导入配置')
    import_cmd.add_argument('file', help='配置文件路径')
    import_cmd.add_argument('--auto-install', action='store_true', help='自动安装')
    
    args = parser.parse_args()
    
    manager = TraeManager()
    
    if args.command == 'setup':
        result = manager.setup(args.mode, args.auto_install)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif args.command == 'install-skills':
        result = manager.install_skills(args.skills)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif args.command == 'install-mcp':
        result = manager.install_mcp(args.mcp)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif args.command == 'check-env':
        result = manager.check_env()
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif args.command == 'export':
        result = manager.export_config(args.full)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif args.command == 'import':
        result = manager.import_config(args.file, args.auto_install)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
