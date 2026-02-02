#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Trae Skills Hub - Windows安装脚本
.DESCRIPTION
    一键安装完整的Trae Skills Hub环境
.EXAMPLE
    .\install.ps1
    .\install.ps1 -ConfigFile "my-config.json"
    .\install.ps1 -InstallCoreOnly
#>

param(
    [Parameter(Mandatory=$false)]
    [string]$ConfigFile = "",
    
    [Parameter(Mandatory=$false)]
    [switch]$InstallCoreOnly,
    
    [Parameter(Mandatory=$false)]
    [switch]$SkipEnvCheck
)

$ErrorActionPreference = "Stop"

# 颜色输出函数
function Write-ColorOutput($ForegroundColor) {
    $fc = $host.UI.RawUI.ForegroundColor
    $host.UI.RawUI.ForegroundColor = $ForegroundColor
    if ($args) { Write-Output $args }
    $host.UI.RawUI.ForegroundColor = $fc
}

function Write-Success($message) { Write-ColorOutput Green "✅ $message" }
function Write-Info($message) { Write-ColorOutput Cyan "ℹ️  $message" }
function Write-Warning($message) { Write-ColorOutput Yellow "⚠️  $message" }
function Write-Error($message) { Write-ColorOutput Red "❌ $message" }

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                                                            ║" -ForegroundColor Cyan
Write-Host "║           🚀 Trae Skills Hub 安装程序                      ║" -ForegroundColor Cyan
Write-Host "║                                                            ║" -ForegroundColor Cyan
Write-Host "║   一站式Trae技能管理平台 - 搜索、安装、管理、部署          ║" -ForegroundColor Cyan
Write-Host "║                                                            ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# 1. 检查环境
if (-not $SkipEnvCheck) {
    Write-Info "步骤 1/5: 检查系统环境..."
    
    $checks = @{
        "Node.js" = @{ Command = "node"; Args = "--version" }
        "npm" = @{ Command = "npm"; Args = "--version" }
        "Python" = @{ Command = "python"; Args = "--version" }
        "Git" = @{ Command = "git"; Args = "--version" }
    }
    
    $allOk = $true
    foreach ($name in $checks.Keys) {
        $check = $checks[$name]
        try {
            $result = & $check.Command $check.Args 2>&1
            Write-Success "$name 已安装: $result"
        } catch {
            Write-Error "$name 未安装或不在PATH中"
            $allOk = $false
        }
    }
    
    if (-not $allOk) {
        Write-Error "环境检查失败，请先安装缺失的组件"
        Write-Info ""
        Write-Info "📥 下载地址："
        Write-Info "  • Node.js: https://nodejs.org/"
        Write-Info "  • Python: https://python.org/"
        Write-Info "  • Git: https://git-scm.com/"
        Write-Info ""
        exit 1
    }
} else {
    Write-Warning "跳过环境检查"
}

# 2. 创建Trae技能目录
Write-Info "步骤 2/5: 创建Trae技能目录..."
$traeSkillsDir = "$env:USERPROFILE\.trae-cn\skills"
if (-not (Test-Path $traeSkillsDir)) {
    New-Item -ItemType Directory -Force -Path $traeSkillsDir | Out-Null
    Write-Success "创建目录: $traeSkillsDir"
} else {
    Write-Info "目录已存在: $traeSkillsDir"
}

# 3. 安装核心技能
Write-Info "步骤 3/5: 安装核心技能..."
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$coreSkills = @("trae-manager", "skill-seeker", "mcp-seeker")

foreach ($skill in $coreSkills) {
    $sourceDir = Join-Path $scriptDir $skill
    $targetDir = Join-Path $traeSkillsDir $skill
    
    if (Test-Path $sourceDir) {
        if (Test-Path $targetDir) {
            $backupDir = "$targetDir.backup.$(Get-Date -Format 'yyyyMMddHHmmss')"
            Move-Item $targetDir $backupDir
            Write-Info "已备份 $skill 到: $backupDir"
        }
        
        Copy-Item -Recurse -Force $sourceDir $targetDir
        Write-Success "安装技能: $skill"
    } else {
        Write-Warning "未找到技能源文件: $skill"
    }
}

# 4. 安装Python依赖
Write-Info "步骤 4/5: 安装Python依赖..."
try {
    python -m pip install pyyaml -q 2>$null
    Write-Success "pyyaml安装完成"
} catch {
    Write-Warning "pyyaml安装失败，尝试使用pip3..."
    pip3 install pyyaml -q 2>$null
}

# 5. 安装技能和MCP
Write-Info "步骤 5/5: 安装技能和MCP..."
$traeManagerTool = "$traeSkillsDir\trae-manager\tools\trae_manager.py"

if (Test-Path $traeManagerTool) {
    if ($InstallCoreOnly) {
        Write-Info "安装核心技能..."
        python $traeManagerTool install-skills core
    } elseif ($ConfigFile -and (Test-Path $ConfigFile)) {
        Write-Info "从配置文件安装: $ConfigFile"
        python $traeManagerTool import $ConfigFile --auto-install
    } else {
        Write-Info "安装推荐技能集..."
        python $traeManagerTool install-skills skill-seeker,mcp-seeker,trae-manager
        python $traeManagerTool install-mcp filesystem,fetch
    }
} else {
    Write-Error "trae-manager工具未找到"
}

# 6. 验证安装
Write-Host ""
Write-Host "════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Info "验证安装..."

$verifyResults = @()
$skillsToCheck = @("trae-manager", "skill-seeker", "mcp-seeker")

foreach ($skill in $skillsToCheck) {
    $skillPath = Join-Path $traeSkillsDir "$skill\SKILL.md"
    if (Test-Path $skillPath) {
        $verifyResults += "✅ $skill"
    } else {
        $verifyResults += "❌ $skill"
    }
}

Write-Host ""
Write-Info "安装结果："
$verifyResults | ForEach-Object { Write-Host "  $_" }

# 7. 输出使用说明
Write-Host ""
Write-Host "════════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Success "Trae Skills Hub 安装完成！"
Write-Host ""
Write-Info "📝 快速开始："
Write-Host ""
Write-Host "  1. 检查环境:" -ForegroundColor White
Write-Host "     python $traeManagerTool check-env" -ForegroundColor Gray
Write-Host ""
Write-Host "  2. 搜索技能:" -ForegroundColor White
Write-Host "     python $traeSkillsDir\skill-seeker\tools\skill_search.py --local" -ForegroundColor Gray
Write-Host ""
Write-Host "  3. 搜索MCP:" -ForegroundColor White
Write-Host "     python $traeSkillsDir\mcp-seeker\tools\mcp_search.py --categories" -ForegroundColor Gray
Write-Host ""
Write-Host "  4. 导出配置:" -ForegroundColor White
Write-Host "     python $traeManagerTool export --full > my-config.json" -ForegroundColor Gray
Write-Host ""
Write-Host "  5. 查看文档:" -ForegroundColor White
Write-Host "     README.md - 项目说明" -ForegroundColor Gray
Write-Host "     DEPLOY.md - 部署指南" -ForegroundColor Gray
Write-Host ""

$skillCount = (Get-ChildItem $traeSkillsDir -Directory).Count
Write-Info "已安装技能数量: $skillCount"
Write-Host ""
Write-Host "🎉 现在可以开始使用Trae Skills Hub了！" -ForegroundColor Green
Write-Host ""
