Proseflow 文章生成器
Proseflow 是一个专注于博文、推文、教程等文档类型生成和智能化编辑的网站。它深度集成了大语言模型（LLM）的能力，允许用户通过自然语言与编辑器交互，实现从内容生成到格式美化的全流程智能化。

核心功能
API 密钥集成: 用户可输入自己的“硅基流动”大模型 API Key。

智能提示词模板: 内置多种文章类型的提示词模板，并支持用户贡献和分享。

流式生成: 文章内容以打字机效果流式输出，即时响应，即时编辑。

富文本智能块:

[CODE]：代码块，支持编辑和 AI 重新生成。

[PLANTUML]：通过 PlantUML 语法生成图表，支持编辑和 AI 重新生成。

[IMAGE]：图片占位符，支持上传或 AI 生成图片。

[LATEX]：LaTeX 公式，支持编辑和 AI 重新生成。

[LINK]：超链接，支持修改和跳转。

上下文工具栏: 选中特定内容时浮现相关编辑工具，保持界面简洁。

多格式导出: 支持将最终文章导出为 Markdown、PDF 和 Word 格式。

技术栈
前端: Vue 3 (Composition API), Pinia, Element Plus, markdown-it

后端: Python 3.10+, FastAPI, SQLAlchemy, Uvicorn

数据库: SQLite

文档转换: Pandoc

部署: Docker, Docker Compose

快速开始
环境准备
Docker: 确保您已安装 Docker 和 Docker Compose。

Pandoc: 为了使用导出功能，您的系统中需要安装 Pandoc。

在 macOS 上: brew install pandoc

在 Debian/Ubuntu 上: sudo apt-get install pandoc

在 Windows 上: 使用 Chocolatey choco install pandoc 或从官网下载安装包。

运行项目
克隆或下载项目: 将 proseflow 文件夹下载到您的本地机器。

构建并启动服务:
在项目根目录（proseflow/）下，打开终端并运行以下命令：

docker-compose up --build

该命令会分别构建前端和后端的 Docker 镜像，并启动相应的服务。

访问应用:

前端应用: 打开浏览器并访问 http://localhost:5173。

后端 API 文档: 访问 http://localhost:8000/docs 查看由 FastAPI 自动生成的 API 文档。

使用说明
输入 API Key: 在页面顶部的输入框中，填入您的“硅基流动”API Key。

校验 Key: 点击“校验”按钮，系统会验证 Key 的有效性。

选择模板: 从下拉菜单中选择一个预设的文章模板。

输入主题: 在输入框中填写您想创作的文章主题。

生成文章: 点击“生成文章”按钮，等待内容流式输出。

编辑与交互:

直接在编辑器中修改文本。

点击代码、图表、公式等智能块，会弹出编辑或重新生成的选项。

使用工具栏或斜杠命令（规划中）手动插入智能块。

导出文件: 编辑完成后，点击右上角的“导出”按钮，选择您想要的格式（PDF, Word, Markdown）。

目录结构
proseflow/
├── backend/        # FastAPI 后端
├── frontend/       # Vue 3 前端
├── docker-compose.yml # Docker 编排文件
└── README.md       # 本文档

注意事项
硅基流动 API: 本项目中的大模型调用是为“硅基流动”设计的。如果您想替换为其他模型，需要修改后端 app/core/llm_service.py 中的 API 调用逻辑。

导出样式: 导出为 PDF/Word 时，样式可能与在线预览有轻微差异。后端使用 Pandoc 进行转换，您可以修改 pandoc_service.py 来定制更复杂的导出样式。

数据库: 项目默认使用 SQLite，数据库文件 proseflow.db 会在 backend/ 目录下自动创建。对于生产环境，建议替换为 PostgreSQL 或其他更健壮的数据库。