import subprocess
import uuid
import os
import asyncio
from fastapi.background import BackgroundTasks

class ConversionError(Exception):
    pass

class PandocService:
    def __init__(self, temp_dir: str = "/tmp/proseflow"):
        self.temp_dir = temp_dir
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)

    def _get_paths(self):
        unique_id = uuid.uuid4()
        input_path = os.path.join(self.temp_dir, f"{unique_id}.md")
        return input_path, unique_id

    def convert(self, markdown_content: str, export_format: str) -> (str, str):
        if export_format not in ['pdf', 'docx', 'md']:
            raise ConversionError(f"Unsupported export format: {export_format}")

        input_path, unique_id = self._get_paths()
        
        with open(input_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
            
        output_path = os.path.join(self.temp_dir, f"{unique_id}.{export_format}")
        
        if export_format == 'md':
            return input_path, "text/markdown"

        # 构建 Pandoc 命令
        # 对于 PDF，需要 LaTeX 环境 (如 MiKTeX, TeX Live, MacTeX)
        # 使用 xelatex 引擎可以更好地支持中文
        command = [
            "pandoc",
            input_path,
            "-o",
            output_path,
        ]
        
        if export_format == 'pdf':
            command.extend(["--pdf-engine=xelatex", "-V", "mainfont=SimSun"]) # 指定中文字体

        try:
            subprocess.run(command, check=True, capture_output=True, text=True, encoding='utf-8')
        except FileNotFoundError:
            raise ConversionError("Pandoc not found. Please ensure it is installed and in your system's PATH.")
        except subprocess.CalledProcessError as e:
            # 清理临时文件
            if os.path.exists(input_path):
                os.remove(input_path)
            raise ConversionError(f"Pandoc conversion failed: {e.stderr}")
            
        media_types = {
            'pdf': 'application/pdf',
            'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        }

        return output_path, media_types[export_format]
        
    def create_cleanup_task(self, *paths: str) -> BackgroundTasks:
        async def cleanup():
            await asyncio.sleep(5) # 等待文件发送完成
            for path in paths:
                if os.path.exists(path):
                    os.remove(path)
        return BackgroundTasks(cleanup)
