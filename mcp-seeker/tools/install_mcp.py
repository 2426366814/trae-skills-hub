#!/usr/bin/env python3
"""
MCP自动安装工具
一键安装MCP服务，包括下载、配置、测试
"""
import os
import json
import subprocess
import shutil
import sys
from typing import Dict, List, Optional, Tuple
from pathlib import Path


class MCPInstaller:
    """MCP安装器"""
    
    def __init__(self, config_path: str = None):
        """初始化安装器"""
        self.config = self._load_config(config_path)
        self.install_log = []
        
    def _load_config(self, config_path: str = None) -> Dict:
        """加载配置"""
        if config_path is None:
            config_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "config", "settings.json"
            )
        
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # 默认配置
        return {
            "installation": {
                "auto_configure": True,
                "test_connection": True,
                "update_agents_md": True,
                "backup_existing": True
            },
            "paths": {
                "mcp_dir": "./mcp-servers",
                "agents_md": "./AGENTS.md"
            }
        }
    
    def install(self, mcp_name: str, source: str = None, configure: bool = True) -> Dict:
        """
        安装MCP服务
        
        Args:
            mcp_name: MCP名称或npm包名
            source: 来源（npm/github）
            configure: 是否自动配置
            
        Returns:
            安装结果
        """
        print(f"🚀 开始安装MCP: {mcp_name}")
        self.install_log = []
        
        result = {
            "success": False,
            "mcp_name": mcp_name,
            "steps": [],
            "errors": [],
            "config": None
        }
        
        try:
            # 1. 检测安装方式
            install_type = self._detect_install_type(mcp_name, source)
            result["install_type"] = install_type
            
            # 2. 创建安装目录
            install_dir = self._create_install_dir(mcp_name)
            result["install_dir"] = install_dir
            
            # 3. 下载/安装MCP
            if install_type == "npm":
                step_result = self._install_from_npm(mcp_name, install_dir)
            elif install_type == "github":
                step_result = self._install_from_github(mcp_name, install_dir)
            else:
                step_result = {"success": False, "error": "未知的安装类型"}
            
            result["steps"].append({"name": "下载安装", "result": step_result})
            
            if not step_result["success"]:
                result["errors"].append(f"下载安装失败: {step_result.get('error')}")
                return result
            
            # 4. 安装依赖
            deps_result = self._install_dependencies(install_dir)
            result["steps"].append({"name": "安装依赖", "result": deps_result})
            
            if not deps_result["success"]:
                result["errors"].append(f"依赖安装失败: {deps_result.get('error')}")
            
            # 5. 自动配置（如果需要）
            if configure and self.config["installation"]["auto_configure"]:
                config_result = self._configure_mcp(mcp_name, install_dir)
                result["steps"].append({"name": "自动配置", "result": config_result})
                result["config"] = config_result.get("config")
            
            # 6. 测试连接（如果需要）
            if self.config["installation"]["test_connection"]:
                test_result = self._test_connection(mcp_name, install_dir)
                result["steps"].append({"name": "连接测试", "result": test_result})
            
            # 7. 更新AGENTS.md（如果需要）
            if self.config["installation"]["update_agents_md"]:
                agents_result = self._update_agents_md(mcp_name, result.get("config"))
                result["steps"].append({"name": "更新AGENTS.md", "result": agents_result})
            
            result["success"] = len(result["errors"]) == 0
            
        except Exception as e:
            result["errors"].append(f"安装异常: {str(e)}")
        
        return result
    
    def _detect_install_type(self, mcp_name: str, source: str = None) -> str:
        """检测安装类型"""
        if source:
            return source
        
        # 检测npm包格式
        if mcp_name.startswith("@") or "/" not in mcp_name:
            return "npm"
        
        # 检测GitHub格式
        if "/" in mcp_name and not mcp_name.startswith("@"):
            return "github"
        
        return "npm"  # 默认npm
    
    def _create_install_dir(self, mcp_name: str) -> str:
        """创建安装目录"""
        base_dir = self.config["paths"]["mcp_dir"]
        
        # 清理mcp_name作为目录名
        dir_name = mcp_name.replace("@", "").replace("/", "-")
        install_dir = os.path.join(base_dir, dir_name)
        
        # 如果目录已存在，备份或删除
        if os.path.exists(install_dir):
            if self.config["installation"]["backup_existing"]:
                backup_dir = f"{install_dir}.backup"
                if os.path.exists(backup_dir):
                    shutil.rmtree(backup_dir)
                shutil.move(install_dir, backup_dir)
                print(f"📦 已备份现有目录到: {backup_dir}")
            else:
                shutil.rmtree(install_dir)
        
        os.makedirs(install_dir, exist_ok=True)
        return install_dir
    
    def _install_from_npm(self, package_name: str, install_dir: str) -> Dict:
        """从npm安装"""
        print(f"📥 从npm安装: {package_name}")
        
        try:
            # 使用npm init和install
            result = subprocess.run(
                ["npm", "init", "-y"],
                cwd=install_dir,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode != 0:
                return {"success": False, "error": f"npm init失败: {result.stderr}"}
            
            # 安装MCP包
            result = subprocess.run(
                ["npm", "install", package_name],
                cwd=install_dir,
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode == 0:
                return {
                    "success": True,
                    "message": f"成功安装 {package_name}",
                    "output": result.stdout
                }
            else:
                return {"success": False, "error": result.stderr}
                
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "安装超时"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _install_from_github(self, repo: str, install_dir: str) -> Dict:
        """从GitHub安装"""
        print(f"📥 从GitHub克隆: {repo}")
        
        try:
            # 构建GitHub URL
            if not repo.startswith("https://"):
                repo_url = f"https://github.com/{repo}.git"
            else:
                repo_url = repo
            
            # 克隆仓库
            result = subprocess.run(
                ["git", "clone", "--depth", "1", repo_url, "."],
                cwd=install_dir,
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode == 0:
                return {
                    "success": True,
                    "message": f"成功克隆 {repo