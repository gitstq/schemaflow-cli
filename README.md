# 📊 SchemaFlow

<p align="center">
  <strong>Lightweight JSON Schema Terminal Visualizer & Validator</strong><br>
  Zero dependencies • Beautiful tree view • Validation & Analysis
</p>

<p align="center">
  <a href="#english">English</a> •
  <a href="#简体中文">简体中文</a> •
  <a href="#繁體中文">繁體中文</a>
</p>

---

<a name="english"></a>
## 🎉 Introduction

**SchemaFlow** is a lightweight, zero-dependency Python CLI tool that brings JSON Schema visualization, validation, and analysis directly to your terminal. No browser required, no heavy dependencies - just pure Python magic! ✨

### Why SchemaFlow?

- 🚀 **Terminal-Native**: View JSON Schema structures as beautiful tree diagrams right in your terminal
- 🎯 **Zero Dependencies**: Uses only Python standard library (3.8+)
- ✅ **Full Validation**: Validate JSON data against schemas with detailed error reporting
- 📊 **Smart Analysis**: Get insights into schema complexity and structure
- 🎨 **Syntax Highlighting**: Colorized output for better readability
- 🔧 **Developer-Friendly**: Simple CLI interface with intuitive commands

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🌳 **Visualize** | Display JSON Schema as beautiful tree structure with type annotations |
| ✅ **Validate** | Validate JSON data against schemas with detailed error messages |
| 📊 **Analyze** | Get schema statistics: property counts, nesting levels, constraints |
| 🎨 **Format** | Pretty-print JSON files with syntax highlighting |
| 🚫 **Zero Dependencies** | Only Python 3.8+ required |
| 🌈 **Colorized Output** | Terminal colors for better readability (optional) |
| 📦 **Lightweight** | Single Python file, easy to install and use |

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/gitstq/schemaflow-cli.git
cd schemaflow-cli

# Run directly
python3 schemaflow.py --help

# Or install as a package
pip install -e .
schemaflow --help
```

### Requirements

- Python 3.8 or higher
- No external dependencies required!

---

## 📖 Usage Guide

### 1. Visualize JSON Schema

```bash
# Basic visualization
python3 schemaflow.py visualize examples/user-schema.json

# Without colors
python3 schemaflow.py --no-color visualize examples/user-schema.json

# Compact mode (less verbose)
python3 schemaflow.py --compact visualize examples/user-schema.json
```

**Example Output:**
```
root: object [required=3] # Schema for user profile data
├── id*: integer [minimum=1] # Unique user identifier
├── username*: string [minLength=3, maxLength=50, pattern]
├── email*: string [format=email]
├── profile: object
│   ├── firstName: string [maxLength=100]
│   ├── lastName: string [maxLength=100]
│   └── age: integer [minimum=0, maximum=150]
└── roles: array [minItems=1, uniqueItems=True]
    └── [items]: string [enum=4]
```

### 2. Validate JSON Data

```bash
# Validate a JSON file against a schema
python3 schemaflow.py validate data.json schema.json

# Example with validation errors
python3 schemaflow.py validate examples/user-data-invalid.json examples/user-schema.json
```

**Example Output:**
```
❌ Validation failed with 7 error(s):
  • root.id: value -1 < minimum 1
  • root.username: string length 2 < minLength 3
  • root.email: string does not match format 'email'
  • root.profile.age: value 200 > maximum 150
```

### 3. Analyze Schema Structure

```bash
# Get schema statistics
python3 schemaflow.py analyze examples/user-schema.json
```

**Example Output:**
```
📊 Schema Analysis: examples/user-schema.json

  Total Properties:     16
  Required Properties:  3
  Max Nesting Level:    2
  Types Used:           object, integer, array, boolean, string, null
  Constraints Used:     minItems, maxLength, minimum, pattern, format
  Has References:       No
```

### 4. Format JSON Files

```bash
# Pretty-print JSON with syntax highlighting
python3 schemaflow.py format data.json

# Save formatted output
python3 schemaflow.py format data.json -o formatted.json

# Custom indentation
python3 schemaflow.py format data.json --indent 4
```

---

## 💡 Design Philosophy

SchemaFlow was designed with these principles:

1. **Simplicity**: No complex setup or configuration
2. **Portability**: Single-file Python script that works anywhere
3. **Performance**: Fast execution with minimal resource usage
4. **Clarity**: Beautiful, readable output that makes schemas understandable
5. **Completeness**: Full support for JSON Schema Draft 7 features

### Supported JSON Schema Features

- ✅ All primitive types (string, number, integer, boolean, null, array, object)
- ✅ Type unions (e.g., `["string", "null"]`)
- ✅ Nested objects and arrays
- ✅ Validation constraints (min/max, patterns, enums, formats)
- ✅ Required properties
- ✅ `oneOf`, `anyOf`, `allOf` combinators
- ✅ `additionalProperties` control
- ✅ `$ref` references (displayed)

---

## 📦 Project Structure

```
schemaflow-cli/
├── schemaflow.py          # Main CLI application
├── setup.py               # Package setup
├── requirements.txt       # Dependencies (empty - zero deps!)
├── examples/              # Example schemas and data
│   ├── user-schema.json
│   ├── user-data-valid.json
│   ├── user-data-invalid.json
│   ├── product-schema.json
│   └── api-response-schema.json
└── README.md
```

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Report Bugs**: Open an issue with detailed reproduction steps
2. **Suggest Features**: Share your ideas for new functionality
3. **Submit PRs**: Fork the repo and submit pull requests

### Development Setup

```bash
git clone https://github.com/gitstq/schemaflow-cli.git
cd schemaflow-cli
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e .
```

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

<a name="简体中文"></a>
## 🎉 项目介绍

**SchemaFlow** 是一款轻量级、零依赖的 Python CLI 工具，可在终端中直接实现 JSON Schema 的可视化、验证和分析。无需浏览器，无需繁重依赖——纯粹的 Python 魔法！✨

### 为什么选择 SchemaFlow？

- 🚀 **终端原生**：在终端中以美观的树形图查看 JSON Schema 结构
- 🎯 **零依赖**：仅使用 Python 标准库（3.8+）
- ✅ **完整验证**：使用详细的错误报告验证 JSON 数据
- 📊 **智能分析**：获取 Schema 复杂度和结构的洞察
- 🎨 **语法高亮**：彩色输出，提升可读性
- 🔧 **开发者友好**：简洁的 CLI 界面，直观的命令

---

## ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 🌳 **可视化** | 将 JSON Schema 显示为带有类型注释的美观树形结构 |
| ✅ **验证** | 使用详细的错误消息验证 JSON 数据 |
| 📊 **分析** | 获取 Schema 统计信息：属性数量、嵌套层级、约束条件 |
| 🎨 **格式化** | 使用语法高亮美化打印 JSON 文件 |
| 🚫 **零依赖** | 仅需 Python 3.8+ |
| 🌈 **彩色输出** | 终端颜色提升可读性（可选） |
| 📦 **轻量级** | 单文件 Python，易于安装和使用 |

---

## 🚀 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/gitstq/schemaflow-cli.git
cd schemaflow-cli

# 直接运行
python3 schemaflow.py --help

# 或作为包安装
pip install -e .
schemaflow --help
```

### 环境要求

- Python 3.8 或更高版本
- 无需外部依赖！

---

## 📖 使用指南

### 1. 可视化 JSON Schema

```bash
# 基础可视化
python3 schemaflow.py visualize examples/user-schema.json

# 无颜色输出
python3 schemaflow.py --no-color visualize examples/user-schema.json

# 紧凑模式（更简洁）
python3 schemaflow.py --compact visualize examples/user-schema.json
```

### 2. 验证 JSON 数据

```bash
# 验证 JSON 文件
python3 schemaflow.py validate data.json schema.json
```

### 3. 分析 Schema 结构

```bash
# 获取 Schema 统计信息
python3 schemaflow.py analyze examples/user-schema.json
```

### 4. 格式化 JSON 文件

```bash
# 美化打印 JSON
python3 schemaflow.py format data.json

# 保存格式化输出
python3 schemaflow.py format data.json -o formatted.json
```

---

## 💡 设计理念

SchemaFlow 遵循以下设计原则：

1. **简洁性**：无需复杂设置或配置
2. **可移植性**：单文件 Python 脚本，随处可用
3. **性能**：快速执行，资源占用最小
4. **清晰性**：美观、可读的输出，让 Schema 易于理解
5. **完整性**：完整支持 JSON Schema Draft 7 特性

---

## 📄 开源协议

本项目采用 **MIT 协议** 开源 - 详见 [LICENSE](LICENSE) 文件。

---

<a name="繁體中文"></a>
## 🎉 專案介紹

**SchemaFlow** 是一款輕量級、零依賴的 Python CLI 工具，可在終端機中直接實現 JSON Schema 的可視化、驗證和分析。無需瀏覽器，無需繁重依賴——純粹的 Python 魔法！✨

### 為什麼選擇 SchemaFlow？

- 🚀 **終端原生**：在終端機中以美觀的樹狀圖查看 JSON Schema 結構
- 🎯 **零依賴**：僅使用 Python 標準函式庫（3.8+）
- ✅ **完整驗證**：使用詳細的錯誤報告驗證 JSON 資料
- 📊 **智能分析**：獲取 Schema 複雜度和結構的洞察
- 🎨 **語法高亮**：彩色輸出，提升可讀性
- 🔧 **開發者友好**：簡潔的 CLI 介面，直觀的命令

---

## ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 🌳 **可視化** | 將 JSON Schema 顯示為帶有類型註釋的美觀樹狀結構 |
| ✅ **驗證** | 使用詳細的錯誤訊息驗證 JSON 資料 |
| 📊 **分析** | 獲取 Schema 統計資訊：屬性數量、嵌套層級、約束條件 |
| 🎨 **格式化** | 使用語法高亮美化列印 JSON 檔案 |
| 🚫 **零依賴** | 僅需 Python 3.8+ |
| 🌈 **彩色輸出** | 終端機顏色提升可讀性（可選） |
| 📦 **輕量級** | 單檔案 Python，易於安裝和使用 |

---

## 🚀 快速開始

### 安裝

```bash
# 克隆倉庫
git clone https://github.com/gitstq/schemaflow-cli.git
cd schemaflow-cli

# 直接執行
python3 schemaflow.py --help

# 或作為套件安裝
pip install -e .
schemaflow --help
```

### 環境需求

- Python 3.8 或更高版本
- 無需外部依賴！

---

## 📖 使用指南

### 1. 可視化 JSON Schema

```bash
# 基礎可視化
python3 schemaflow.py visualize examples/user-schema.json

# 無顏色輸出
python3 schemaflow.py --no-color visualize examples/user-schema.json

# 緊湊模式（更簡潔）
python3 schemaflow.py --compact visualize examples/user-schema.json
```

### 2. 驗證 JSON 資料

```bash
# 驗證 JSON 檔案
python3 schemaflow.py validate data.json schema.json
```

### 3. 分析 Schema 結構

```bash
# 獲取 Schema 統計資訊
python3 schemaflow.py analyze examples/user-schema.json
```

### 4. 格式化 JSON 檔案

```bash
# 美化列印 JSON
python3 schemaflow.py format data.json

# 儲存格式化輸出
python3 schemaflow.py format data.json -o formatted.json
```

---

## 💡 設計理念

SchemaFlow 遵循以下設計原則：

1. **簡潔性**：無需複雜設定或配置
2. **可攜性**：單檔案 Python 腳本，隨處可用
3. **效能**：快速執行，資源佔用最小
4. **清晰性**：美觀、可讀的輸出，讓 Schema 易於理解
5. **完整性**：完整支援 JSON Schema Draft 7 特性

---

## 📄 開源協議

本專案採用 **MIT 協議** 開源 - 詳見 [LICENSE](LICENSE) 檔案。

---

<p align="center">
  Made with ❤️ by SchemaFlow Team<br>
  ⭐ Star us on GitHub if you find this useful!
</p>
