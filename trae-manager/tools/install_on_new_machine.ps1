#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Trae环境新机器安装脚本
.DESCRIPTION
    在新机器上一键安装完整的Trae环境
.EXAMPLE
    .\install_on_new_machine.ps1 -ConfigFile "my-trae-setup.json"
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
    if ($args) {
        Write-Output $args
    }
    $host.UI.RawUI.ForegroundColor = $fc
}

function Write-Success($message) {
    Write-ColorOutput Green "✅ $message"
}

function Write-Info($message) {
    Write-ColorOutput Cyan "ℹ️  $message"
}

function Write-Warning($message) {
    Write-ColorOutput Yellow "⚠️  $message"
}

function Write-Error($message) {
    Write-ColorOutput Red "❌ $message"
}

Write-Info "开始安装Trae环境..."
Write-Info "================================"

# 1. 检查环境
if (-not $SkipEnvCheck) {
    Write-Info "步骤 1/5: 检查系统环境..."
    
    $checks = @{
        "Node.js" = @{ Command = "node"; Args = "--version"; MinVersion = "18.0.0" }
        "npm" = @{ Command = "npm"; Args = "--version"; MinVersion = "9.0.0" }
        "Python" = @{ Command = "python"; Args = "--version"; MinVersion = "3.9.0" }
        "Git" = @{ Command = "git"; Args = "--version"; MinVersion = "2.30.0" }
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
        Write-Info "下载地址："
        Write-Info "  - Node.js: https://nodejs.org/"
        Write-Info "  - Python: https://python.org/"
        Write-Info "  - Git: https://git-scm.com/"
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

# 3. 安装trae-manager
Write-Info "步骤 3/5: 安装trae-manager..."
$traeManagerDir = "$traeSkillsDir\trae-manager"

if (Test-Path $traeManagerDir) {
    Write-Warning "trae-manager已存在，备份现有版本..."
    $backupDir = "$traeManagerDir.backup.$(Get-Date -Format 'yyyyMMddHHmmss')"
    Move-Item $traeManagerDir $backupDir
    Write-Info "已备份到: $backupDir"
}

# 复制trae-manager（假设脚本在trae-manager/tools目录中）
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$sourceDir = Split-Path -Parent $scriptDir

if (Test-Path "$sourceDir\SKILL.md") {
    Copy-Item -Recurse -Force $sourceDir $traeManagerDir
    Write-Success "trae-manager安装完成"
} else {
    Write-Error "无法找到trae-manager源文件"
    Write-Info "请确保此脚本位于trae-manager/tools目录中"
    exit 1
}

# 4. 安装依赖
Write-Info "步骤 4/5: 安装Python依赖..."
try {
    python -m pip install pyyaml -q
    Write-Success "pyyaml安装完成"
} catch {
    Write-Warning "pyyaml安装失败，尝试使用pip3..."
    pip3 install pyyaml -q
}

# 5. 安装技能和MCP
Write-Info "步骤 5/5: 安装技能和MCP..."
$traeManagerTool = "$traeManagerDir\tools\trae_manager.py"

if ($InstallCoreOnly) {
    Write-Info "安装核心技能..."
    python $traeManagerTool install-skills core
} elseif ($ConfigFile -and (Test-Path $ConfigFile)) {
    Write-Info "从配置文件安装: $ConfigFile"
    python $traeManagerTool import $ConfigFile --auto-install
} else {
    Write-Info "安装推荐技能集..."
    # 安装核心技能
    python $traeManagerTool install-skills skill-seeker,mcp-seeker,trae-manager
    # 安装推荐MCP
    python $traeManagerTool install-mcp filesystem,fetch
}

# 6. 验证安装
Write-Info "================================"
Write-Info "验证安装..."

$verifyResults = @()

# 检查trae-manager
if (Test-Path "$traeSkillsDir\trae-manager\SKILL.md") {
    $verifyResults += "✅ trae-manager"
} else {
    $verifyResults += "❌ trae-manager"
}

# 检查skill-seeker
if (Test-Path "$traeSkillsDir\skill-seeker\SKILL.md") {
    $verifyResults += "✅ skill-seeker"
} else {
    $verifyResults += "❌ skill-seeker"
}

# 检查mcp-seeker
if (Test-Path "$traeSkillsDir\mcp-seeker\SKILL.md") {
    $verifyResults += "✅ mcp-seeker"
} else {
    $verifyResults += "❌ mcp-seeker"
}

Write-Info "安装结果："
$verifyResults | ForEach-Object { Write-Info "  $_" }

# 7. 输出使用说明
Write-Info "================================"
Write-Success "Trae环境安装完成！"
Write-Info ""
Write-Info "使用说明："
Write-Info "  1. 检查环境: python $traeManagerTool check-env"
Write-Info "  2. 导出配置: python $traeManagerTool export --full"
Write-Info "  3. 安装技能: python $traeManagerTool install-skills <skill-name>"
Write-Info "  4. 安装MCP: python $traeManagerTool install-mcp <mcp-name>"
Write-Info ""
Write-Info "已安装技能数量: $((Get-ChildItem $traeSkillsDir -Directory).Count)"
Write-Info ""
Write-Info "🎉 现在可以开始使用Trae了！"
