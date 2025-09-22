# Proseflow ✨

<p align="center">
  <img src="logo.png" alt="Proseflow Logo" width="150"/>
</p>

<p align="center">
  <strong>一个为创作者而生的智能文档工作流引擎。</strong>
  <br />
  Proseflow 深度集成大语言模型（LLM），让你通过自然语言“对话”的方式，轻松完成博文、教程、推文等内容的生成、编辑与格式美化。
</p>

<p align="center">
    <a href="https://github.com/your-username/proseflow/stargazers">
        <img src="https://img.shields.io/github/stars/your-username/proseflow?style=flat-square" alt="GitHub stars">
    </a>
    <a href="https://github.com/your-username/proseflow/network/members">
        <img src="https://img.shields.io/github/forks/your-username/proseflow?style=flat-square" alt="GitHub forks">
    </a>
    <a href="https://github.com/your-username/proseflow/issues">
        <img src="https://img.shields.io/github/issues/your-username/proseflow?style=flat-square" alt="GitHub issues">
    </a>
    <a href="https://github.com/your-username/proseflow/blob/main/LICENSE">
        <img src="https://img.shields.io/github/license/your-username/proseflow?style=flat-square" alt="License">
    </a>
</p>

> **项目理念**：我们相信，未来的文档创作将是人与 AI 协同的艺术。Proseflow 致力于成为创作者手中最得心应手的那支“神笔”，将繁琐的格式调整与内容组织交给 AI，让创作者能 100% 专注于思想与灵感的流动。

---

## 🚀 核心功能

* 🔑 **API 密钥集成**: 支持用户配置自己的“硅基流动”大模型 API Key，确保私密与安全。
* ✍️ **流式生成**: 文章内容以打字机效果流式输出，即时响应，即时编辑，享受流畅的创作心流。
* 🧠 **智能提示词模板**: 内置多种文章类型的提示词模板，并支持用户贡献和分享，激发创作灵感。
* 🧱 **富文本智能块**:
    * `[CODE]`: 代码块，支持语法高亮、一键复制、AI 解释或重构。
    * `[PLANTUML]`: 通过 PlantUML 文本实时生成流程图、时序图等，支持 AI 辅助生成和编辑。
    * `[IMAGE]`: 图片占位符，支持本地上传或调用 AI 文生图模型即时生成。
    * `[LATEX]`: 优雅地编写 LaTeX 公式，支持实时预览和 AI 辅助编写。
    * `[LINK]`: 方便地插入和管理超链接。
* 🧰 **上下文工具栏**: 选中内容时自动浮现相关编辑工具，操作直观，界面极简。
* 📄 **多格式导出**: 支持将最终文章一键导出为 **Markdown**, **PDF** 和 **Word** 格式，满足不同分发渠道的需求。

## 🛠️ 技术栈

| 分类       | 技术                                                                  |
| ---------- | --------------------------------------------------------------------- |
| **前端** | `Vue 3` (Composition API), `Pinia`, `Element Plus`, `markdown-it`       |
| **后端** | `Python 3.10+`, `FastAPI`, `SQLAlchemy`, `Uvicorn`                        |
| **数据库** | `SQLite`                                                              |
| **文档转换** | `Pandoc`                                                              |
| **部署** | `Docker`, `Docker Compose`                                              |

## ⚡ 快速开始

只需两步，即可在你的本地机器上运行 Proseflow。

### 1. 环境准备

请确保你的系统已经安装了以下软件：

* **Docker & Docker Compose**: [获取 Docker](https://docs.docker.com/get-docker/)
* **Pandoc**: 用于支持多格式导出功能。

    ```bash
    # 在 macOS (使用 Homebrew)
    brew install pandoc

    # 在 Debian/Ubuntu
    sudo apt-get update && sudo apt-get install -y pandoc

    # 在 Windows (使用 Chocolatey)
    choco install pandoc
    ```
    *你也可以从 [Pandoc 官网](https://pandoc.org/installing.html) 下载安装包。*

### 2. 运行项目

**a. 克隆项目**

```bash
git clone [https://github.com/your-username/proseflow.git](https://github.com/your-username/proseflow.git)
cd proseflow
```

**b. 构建并启动服务**

在项目根目录下，执行以下命令：

```bash
docker-compose up --build
```

这个命令会为你完成所有事情：构建前端和后端的 Docker 镜像，并启动容器化服务。

**c. 访问应用**

服务启动成功后：

  * 🌐 **前端应用**: 打开浏览器访问 👉 **`http://localhost:5173`**
  * 📚 **后端 API 文档**: 访问 👉 **`http://localhost:8000/docs`** 查看由 FastAPI 自动生成的 Swagger UI。

## 📖 使用说明

1.  **输入 API Key**: 在页面顶部的输入框中，填入你的“硅基流动” API Key。
2.  **校验 Key**: 点击“校验”按钮，系统会验证 Key 的有效性。
3.  **选择模板**: 从下拉菜单中选择一个预设的文章模板。
4.  **输入主题**: 在输入框中填写你想创作的文章主题。
5.  **生成文章**: 点击“生成文章”按钮，坐和放宽，欣赏 AI 为你创作。
6.  **编辑与交互**:
      * 直接在编辑器中修改文本。
      * 点击代码、图表、公式等智能块，会弹出编辑或重新生成的选项。
      * 使用浮动工具栏或斜杠命令（规划中）手动插入智能块。
7.  **导出文件**: 创作完成后，点击右上角的“导出”按钮，选择你想要的格式。

## 📂 目录结构

```
proseflow/
├── backend/          # FastAPI 后端应用
│   ├── app/
│   └── Dockerfile
├── frontend/         # Vue 3 前端应用
│   ├── src/
│   └── Dockerfile
├── docker-compose.yml # Docker 编排文件
└── README.md          # 就是你正在看的这个文件
```

## ⚠️ 注意事项

本项目默认使用“硅基流动”大模型 API。如果你想替换为其他模型（如 OpenAI GPT, Anthropic Claude 等），你需要修改后端的核心服务文件： `backend/app/core/llm_service.py` 中的 API 调用逻辑。

## 🤝 贡献指南

我们热烈欢迎各种形式的贡献！无论是提交 Issue、修复 Bug、增加新功能还是完善文档，都对 Proseflow 意义重大。

请在提交 Pull Request 前，先创建一个 Issue 来讨论你的想法。

## 📄 许可证

本项目采用 [MIT License](https://www.google.com/url?sa=E&source=gmail&q=https://github.com/your-username/proseflow/blob/main/LICENSE) 开源。

导出样式: 导出为 PDF/Word 时，样式可能与在线预览有轻微差异。后端使用 Pandoc 进行转换，您可以修改 pandoc_service.py 来定制更复杂的导出样式。

数据库: 项目默认使用 SQLite，数据库文件 proseflow.db 会在 backend/ 目录下自动创建。对于生产环境，建议替换为 PostgreSQL 或其他更健壮的数据库。
