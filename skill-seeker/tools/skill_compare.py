#!/usr/bin/env python3
"""
技能比较工具
比较多个技能的功能、流行度和适用性
"""
import os
import json
import sys
from typing import List, Dict, Any
from datetime import datetime

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class SkillComparer:
    """技能比较器"""
    
    def __init__(self):
        """初始化比较器"""
        self.comparison_cache = {}
    
    def compare(self, skills: List[str], criteria: List[str] = None) -> Dict:
        """
        比较多个技能
        
        Args:
            skills: 技能名称列表
            criteria: 比较维度 (downloads/features/ratings/popularity/updated)
            
        Returns:
            比较结果
        """
        if criteria is None:
            criteria = ["downloads", "features", "ratings", "popularity"]
        
        # 获取技能信息
        skill_infos = []
        for skill_name in skills:
            info = self._get_skill_info(skill_name)
            if info:
                skill_infos.append(info)
        
        if len(skill_infos) < 2:
            return {
                "error": "需要至少2个有效技能进行比较",
                "skills_found": len(skill_infos)
            }
        
        # 进行比较
        comparison = {
            "timestamp": datetime.now().isoformat(),
            "skills_compared": [s["name"] for s in skill_infos],
            "criteria": criteria,
            "summary": {},
            "detailed_comparison": {},
            "recommendation": ""
        }
        
        # 按维度比较
        for criterion in criteria:
            comparison["detailed_comparison"][criterion] = self._compare_by_criterion(
                skill_infos, criterion
            )
        
        # 生成总结
        comparison["summary"] = self._generate_summary(skill_infos, criteria)
        
        # 生成推荐
        comparison["recommendation"] = self._generate_recommendation(
            skill_infos, comparison["summary"]
        )
        
        return comparison
    
    def _get_skill_info(self, skill_name: str) -> Dict:
        """获取技能信息"""
        # 预定义的技能数据库
        skill_database = {
            # awesome-claude-skills
            "docx": {
                "name": "docx",
                "source": "awesome-claude-skills",
                "description": "Word文档处理",
                "downloads": 28100,
                "features": ["创建文档", "编辑文档", "格式设置", "表格处理"],
                "ratings": 4.8,
                "use_cases": ["办公文档", "报告生成", "合同处理"],
                "pros": ["功能全面", "易于使用", "格式支持好"],
                "cons": ["仅支持Word格式"]
            },
            "pdf": {
                "name": "pdf",
                "source": "awesome-claude-skills",
                "description": "PDF文档处理",
                "downloads": 25300,
                "features": ["PDF读取", "PDF编辑", "PDF合并", "PDF转换"],
                "ratings": 4.7,
                "use_cases": ["文档查看", "PDF编辑", "文档归档"],
                "pros": ["格式稳定", "跨平台", "安全性高"],
                "cons": ["编辑功能有限"]
            },
            "pptx": {
                "name": "pptx",
                "source": "awesome-claude-skills",
                "description": "PowerPoint处理",
                "downloads": 22400,
                "features": ["创建幻灯片", "编辑演示文稿", "图表生成", "模板应用"],
                "ratings": 4.6,
                "use_cases": ["演示文稿", "报告展示", "培训材料"],
                "pros": ["视觉效果佳", "模板丰富", "动画支持"],
                "cons": ["文件较大"]
            },
            "xlsx": {
                "name": "xlsx",
                "source": "awesome-claude-skills",
                "description": "Excel表格处理",
                "downloads": 26500,
                "features": ["数据处理", "公式计算", "图表生成", "数据透视"],
                "ratings": 4.7,
                "use_cases": ["数据分析", "财务报表", "数据整理"],
                "pros": ["计算功能强", "图表丰富", "数据处理高效"],
                "cons": ["学习曲线较陡"]
            },
            "mcp-builder": {
                "name": "mcp-builder",
                "source": "awesome-claude-skills",
                "description": "创建MCP服务器",
                "downloads": 18500,
                "features": ["MCP服务器生成", "API集成", "协议实现", "模板创建"],
                "ratings": 4.9,
                "use_cases": ["MCP开发", "API封装", "服务集成"],
                "pros": ["自动化程度高", "模板丰富", "文档完善"],
                "cons": ["需要编程基础"]
            },
            "skill-creator": {
                "name": "skill-creator",
                "source": "awesome-claude-skills",
                "description": "创建自定义技能",
                "downloads": 15600,
                "features": ["技能模板", "代码生成", "文档创建", "测试工具"],
                "ratings": 4.8,
                "use_cases": ["技能开发", "自定义工具", "工作流创建"],
                "pros": ["降低开发门槛", "模板丰富", "社区支持"],
                "cons": ["需要理解技能架构"]
            },
            "webapp-testing": {
                "name": "webapp-testing",
                "source": "awesome-claude-skills",
                "description": "Web应用测试",
                "downloads": 14200,
                "features": ["自动化测试", "性能测试", "UI测试", "API测试"],
                "ratings": 4.7,
                "use_cases": ["Web测试", "质量保证", "CI/CD集成"],
                "pros": ["测试覆盖全面", "自动化程度高", "报告详细"],
                "cons": ["配置较复杂"]
            },
            "frontend-design": {
                "name": "frontend-design",
                "source": "awesome-claude-skills",
                "description": "前端设计",
                "downloads": 8600,
                "features": ["UI设计", "响应式布局", "组件设计", "样式优化"],
                "ratings": 4.6,
                "use_cases": ["Web设计", "UI优化", "前端开发"],
                "pros": ["设计规范", "组件丰富", "易于实现"],
                "cons": ["设计主观性强"]
            },
            "connect-apps": {
                "name": "connect-apps",
                "source": "awesome-claude-skills",
                "description": "连接应用程序",
                "downloads": 12300,
                "features": ["应用集成", "API连接", "数据同步", "自动化工作流"],
                "ratings": 4.8,
                "use_cases": ["系统集成", "数据同步", "自动化"],
                "pros": ["集成能力强", "支持应用多", "配置简单"],
                "cons": ["依赖第三方API"]
            },
            "file-organizer": {
                "name": "file-organizer",
                "source": "awesome-claude-skills",
                "description": "文件整理",
                "downloads": 19800,
                "features": ["文件分类", "重复检测", "自动整理", "批量重命名"],
                "ratings": 4.7,
                "use_cases": ["文件管理", "磁盘整理", "归档处理"],
                "pros": ["自动化程度高", "智能分类", "节省时间"],
                "cons": ["需要初始配置"]
            },
            
            # claude-code-infrastructure
            "backend-dev-guidelines": {
                "name": "backend-dev-guidelines",
                "source": "claude-code-infrastructure",
                "description": "后端开发指南",
                "downloads": 8900,
                "features": ["API设计", "数据库操作", "安全最佳实践", "性能优化"],
                "ratings": 4.9,
                "use_cases": ["后端开发", "API开发", "企业应用"],
                "pros": ["生产验证", "最佳实践", "架构清晰"],
                "cons": ["主要针对Node.js"]
            },
            "frontend-dev-guidelines": {
                "name": "frontend-dev-guidelines",
                "source": "claude-code-infrastructure",
                "description": "前端开发指南",
                "downloads": 9200,
                "features": ["React模式", "TypeScript规范", "MUI组件", "状态管理"],
                "ratings": 4.8,
                "use_cases": ["前端开发", "React项目", "企业应用"],
                "pros": ["组件丰富", "类型安全", "性能优化"],
                "cons": ["依赖React生态"]
            },
            "skill-developer": {
                "name": "skill-developer",
                "source": "claude-code-infrastructure",
                "description": "技能开发元技能",
                "downloads": 7600,
                "features": ["技能架构", "开发流程", "测试方法", "发布指南"],
                "ratings": 4.9,
                "use_cases": ["技能开发", "元编程", "工具创建"],
                "pros": ["系统化方法", "最佳实践", "社区标准"],
                "cons": ["需要深入理解"]
            },
            "route-tester": {
                "name": "route-tester",
                "source": "claude-code-infrastructure",
                "description": "API路由测试",
                "downloads": 6800,
                "features": ["路由测试", "认证测试", "性能测试", "自动化"],
                "ratings": 4.7,
                "use_cases": ["API测试", "后端验证", "质量保证"],
                "pros": ["测试全面", "自动化", "报告详细"],
                "cons": ["需要API文档"]
            },
            "error-tracking": {
                "name": "error-tracking",
                "source": "claude-code-infrastructure",
                "description": "错误追踪",
                "downloads": 8100,
                "features": ["Sentry集成", "错误监控", "性能追踪", "告警通知"],
                "ratings": 4.8,
                "use_cases": ["错误监控", "生产环境", "质量保障"],
                "pros": ["实时监控", "详细报告", "集成简单"],
                "cons": ["依赖Sentry服务"]
            },
            
            # superpowers
            "brainstorming": {
                "name": "brainstorming",
                "source": "superpowers",
                "description": "需求头脑风暴",
                "downloads": 11200,
                "features": ["需求分析", "方案探索", "设计完善", "风险评估"],
                "ratings": 4.9,
                "use_cases": ["项目启动", "需求分析", "方案设计"],
                "pros": ["系统化方法", "全面考虑", "降低风险"],
                "cons": ["需要更多时间"]
            },
            "writing-plans": {
                "name": "writing-plans",
                "source": "superpowers",
                "description": "制定实施计划",
                "downloads": 10500,
                "features": ["任务分解", "时间规划", "依赖分析", "里程碑设置"],
                "ratings": 4.8,
                "use_cases": ["项目管理", "开发规划", "进度跟踪"],
                "pros": ["计划详细", "可执行性强", "易于跟踪"],
                "cons": ["需要维护更新"]
            },
            "test-driven-development": {
                "name": "test-driven-development",
                "source": "superpowers",
                "description": "测试驱动开发",
                "downloads": 9800,
                "features": ["TDD流程", "测试编写", "代码重构", "质量保证"],
                "ratings": 4.9,
                "use_cases": ["高质量开发", "代码重构", "Bug预防"],
                "pros": ["代码质量高", "Bug少", "设计更好"],
                "cons": ["初期开发较慢"]
            },
            "subagent-driven-development": {
                "name": "subagent-driven-development",
                "source": "superpowers",
                "description": "子代理驱动开发",
                "downloads": 8700,
                "features": ["子任务分配", "并行开发", "代码审查", "进度跟踪"],
                "ratings": 4.8,
                "use_cases": ["大型项目", "团队协作", "快速开发"],
                "pros": ["开发速度快", "并行处理", "质量可控"],
                "cons": ["需要协调管理"]
            },
            
            # Vercel Skills
            "vercel-react-best-practices": {
                "name": "vercel-react-best-practices",
                "source": "vercel",
                "description": "React最佳实践",
                "downloads": 39600,
                "features": ["组件模式", "状态管理", "性能优化", "TypeScript"],
                "ratings": 4.9,
                "use_cases": ["React开发", "前端项目", "企业应用"],
                "pros": ["行业标准", "性能优秀", "类型安全"],
                "cons": ["学习曲线较陡"]
            },
            "web-design-guidelines": {
                "name": "web-design-guidelines",
                "source": "vercel",
                "description": "网页设计规范",
                "downloads": 30100,
                "features": ["设计系统", "响应式设计", "可访问性", "UI组件"],
                "ratings": 4.8,
                "use_cases": ["Web设计", "UI/UX", "设计系统"],
                "pros": ["设计规范", "系统全面", "易于维护"],
                "cons": ["设计主观性"]
            },
            "seo-audit": {
                "name": "seo-audit",
                "source": "vercel",
                "description": "SEO诊断",
                "downloads": 2600,
                "features": ["SEO分析", "排名诊断", "优化建议", "竞品分析"],
                "ratings": 4.7,
                "use_cases": ["SEO优化", "网站推广", "流量提升"],
                "pros": ["分析全面", "建议实用", "效果显著"],
                "cons": ["需要持续优化"]
            },
            "agent-browser": {
                "name": "agent-browser",
                "source": "vercel",
                "description": "AI操作浏览器",
                "downloads": 3100,
                "features": ["浏览器自动化", "网页测试", "数据抓取", "UI测试"],
                "ratings": 4.6,
                "use_cases": ["自动化测试", "网页抓取", "UI验证"],
                "pros": ["自动化程度高", "测试全面", "节省时间"],
                "cons": ["需要维护脚本"]
            }
        }
        
        # 查找技能（支持模糊匹配）
        skill_lower = skill_name.lower()
        
        # 精确匹配
        if skill_name in skill_database:
            return skill_database[skill_name]
        
        # 模糊匹配
        for key, value in skill_database.items():
            if skill_lower in key.lower() or key.lower() in skill_lower:
                return value
        
        # 未找到
        return {
            "name": skill_name,
            "source": "unknown",
            "description": "未知技能",
            "downloads": 0,
            "features": [],
            "ratings": 0,
            "use_cases": [],
            "pros": [],
            "cons": []
        }
    
    def _compare_by_criterion(self, skills: List[Dict], criterion: str) -> Dict:
        """按特定维度比较"""
        comparison = {
            "criterion": criterion,
            "winner": "",
            "rankings": []
        }
        
        if criterion == "downloads":
            sorted_skills = sorted(skills, key=lambda x: x.get("downloads", 0), reverse=True)
            comparison["winner"] = sorted_skills[0]["name"] if sorted_skills else ""
            comparison["rankings"] = [
                {"name": s["name"], "value": s.get("downloads", 0)} 
                for s in sorted_skills
            ]
            
        elif criterion == "features":
            sorted_skills = sorted(skills, key=lambda x: len(x.get("features", [])), reverse=True)
            comparison["winner"] = sorted_skills[0]["name"] if sorted_skills else ""
            comparison["rankings"] = [
                {"name": s["name"], "value": len(s.get("features", [])), "features": s.get("features", [])} 
                for s in sorted_skills
            ]
            
        elif criterion == "ratings":
            sorted_skills = sorted(skills, key=lambda x: x.get("ratings", 0), reverse=True)
            comparison["winner"] = sorted_skills[0]["name"] if sorted_skills else ""
            comparison["rankings"] = [
                {"name": s["name"], "value": s.get("ratings", 0)} 
                for s in sorted_skills
            ]
            
        elif criterion == "popularity":
            # 综合考虑下载量和评分
            def popularity_score(skill):
                downloads = skill.get("downloads", 0)
                ratings = skill.get("ratings", 0)
                return downloads * ratings
            
            sorted_skills = sorted(skills, key=popularity_score, reverse=True)
            comparison["winner"] = sorted_skills[0]["name"] if sorted_skills else ""
            comparison["rankings"] = [
                {"name": s["name"], "value": popularity_score(s)} 
                for s in sorted_skills
            ]
        
        return comparison
    
    def _generate_summary(self, skills: List[Dict], criteria: List[str]) -> Dict:
        """生成比较总结"""
        summary = {
            "total_skills": len(skills),
            "best_overall": "",
            "best_by_criterion": {},
            "feature_comparison": {},
            "use_case_overlap": []
        }
        
        # 找出每个维度的最佳技能
        for criterion in criteria:
            if criterion == "downloads":
                best = max(skills, key=lambda x: x.get("downloads", 0))
                summary["best_by_criterion"]["downloads"] = {
                    "skill": best["name"],
                    "value": best.get("downloads", 0)
                }
            elif criterion == "ratings":
                best = max(skills, key=lambda x: x.get("ratings", 0))
                summary["best_by_criterion"]["ratings"] = {
                    "skill": best["name"],
                    "value": best.get("ratings", 0)
                }
        
        # 功能对比
        all_features = set()
        for skill in skills:
            all_features.update(skill.get("features", []))
        
        for feature in all_features:
            supporting_skills = [
                s["name"] for s in skills 
                if feature in s.get("features", [])
            ]
            summary["feature_comparison"][feature] = supporting_skills
        
        # 使用场景重叠
        use_cases = [set(s.get("use_cases", [])) for s in skills]
        if use_cases:
            overlap = use_cases[0]
            for uc in use_cases[1:]:
                overlap &= uc
            summary["use_case_overlap"] = list(overlap)
        
        # 综合最佳（下载量 * 评分）
        best_overall = max(skills, key=lambda x: x.get("downloads", 0) * x.get("ratings", 0))
        summary["best_overall"] = best_overall["name"]
        
        return summary
    
    def _generate_recommendation(self, skills: List[Dict], summary: Dict) -> str:
        """生成推荐"""
        if len(skills) == 2:
            skill1, skill2 = skills[0], skills[1]
            
            recommendation = f"""📊 比较结论：

**{skill1['name']} vs {skill2['name']}**

| 维度 | {skill1['name']} | {skill2['name']} | 胜出 |
|------|------------------|------------------|------|
| 下载量 | {skill1.get('downloads', 0):,} | {skill2.get('downloads', 0):,} | {'⬅️' if skill1.get('downloads', 0) > skill2.get('downloads', 0) else '➡️'} |
| 评分 | {skill1.get('ratings', 0)} | {skill2.get('ratings', 0)} | {'⬅️' if skill1.get('ratings', 0) > skill2.get('ratings', 0) else '➡️'} |
| 功能数 | {len(skill1.get('features', []))} | {len(skill2.get('features', []))} | {'⬅️' if len(skill1.get('features', [])) > len(skill2.get('features', [])) else '➡️'} |

**推荐选择：**
"""
            
            # 根据使用场景推荐
            if summary.get("use_case_overlap"):
                recommendation += f"\n✅ 两个技能都适用于：{', '.join(summary['use_case_overlap'])}\n"
            
            # 综合推荐
            best = summary.get("best_overall", "")
            if best:
                recommendation += f"\n🏆 **综合推荐：{best}**\n"
                recommendation += f"   理由：下载量和评分综合最高\n"
            
            # 特定场景推荐
            recommendation += "\n📌 **场景建议：**\n"
            for skill in skills:
                if skill.get("pros"):
                    recommendation += f"\n选择 {skill['name']} 如果你需要：\n"
                    for pro in skill["pros"][:3]:
                        recommendation += f"  • {pro}\n"
            
            return recommendation
        
        else:
            # 多个技能比较
            recommendation = f"📊 比较了 {len(skills)} 个技能\n\n"
            recommendation += f"🏆 **综合最佳：{summary.get('best_overall', 'N/A')}**\n\n"
            
            for criterion, result in summary.get("best_by_criterion", {}).items():
                recommendation += f"✅ {criterion}最佳：{result['skill']} ({result['value']})\n"
            
            return recommendation
    
    def format_comparison(self, comparison: Dict) -> str:
        """格式化比较结果"""
        if "error" in comparison:
            return f"❌ 错误：{comparison['error']}"
        
        output = f"""📊 技能比较报告
{'=' * 60}

比较技能：{', '.join(comparison['skills_compared'])}
比较维度：{', '.join(comparison['criteria'])}

"""
        
        # 详细比较
        for criterion, details in comparison.get("detailed_comparison", {}).items():
            output += f"\n**{criterion.upper()} 对比**\n"
            output += f"胜出者：{details.get('winner', 'N/A')}\n"
            output += "排名：\n"
            for rank in details.get("rankings", []):
                output += f"  {rank['name']}: {rank['value']}\n"
        
        # 总结
        summary = comparison.get("summary", {})
        output += f"\n{'=' * 60}\n📈 总结\n{'=' * 60}\n"
        output += f"综合最佳：{summary.get('best_overall', 'N/A')}\n"
        
        # 推荐
        output += f"\n{'=' * 60}\n"
        output += comparison.get("recommendation", "")
        
        return output


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='技能比较工具')
    parser.add_argument('skills', nargs='+', help='要比较的技能名称')
    parser.add_argument('--criteria', nargs='+', 
                       choices=['downloads', 'features', 'ratings', 'popularity'],
                       default=['downloads', 'features', 'ratings'],
                       help='比较维度')
    parser.add_argument('--json', action='store_true', help='以JSON格式输出')
    
    args = parser.parse_args()
    
    comparer = SkillComparer()
    result = comparer.compare(args.skills, args.criteria)
    
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(comparer.format_comparison(result))


if __name__ == "__main__":
    main()
