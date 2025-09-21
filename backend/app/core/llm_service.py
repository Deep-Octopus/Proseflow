import requests
import json
import asyncio
from openai import OpenAI
from typing import AsyncGenerator

from .config import SILICON_FLOW_BASE_URL

SYSTEM_RULE = """
在普通文本无法解释清楚，需要结合代码、图表、图片、公式、链接等内容才能讲解清楚时必须使用占位符标记，你必须按照下面的格式表示：
1. 代码表示(...表示生成的初始的代码)：[CODE language=python, title="快速排序代码" describe="python实现的快速排序代码"]...[/CODE]。注意：关键代码必须提供，并附带清晰的注释。避免大段代码粘贴，优先使用简洁、核心的示例。
2. 图表表示(...表示生成的初始的plantuml代码)：[PLANTUML type="流程图" describe="展示从收到请求到返回响应的完整步骤，突出缓存的作用"]...[/PLANTUML]
   [PLANTUML type="柱状图" describe="对比优化前后的性能数据，包括加载时间和内存占用"]...[/PLANTUML]
3. 图片表示(占位方便用户后面自己插入)：[IMAGE type="场景图" describe="一个小女孩拿着一支笔在写字"/]
   [IMAGE type="表情包" describe="一个“我全都要”的表情包，用于比喻同时需要高性能和低成本的场景"/]
4. 公式表示(...表示公式的latex表示)：[LATEX describe="a和b的乘积开三次方根最后除以4"]...[/LATEX]
5. 链接表示(...表示链接具体的URL链接)：[LINK title="气候变化对生物多样性影响论文" describe="指向权威学术数据库中关于 “气候变化对生物多样性影响” 的最新研究论文"]...[/LINK]

请你根据下面的要求，生成一篇{TYPE}，主题是《{TOPIC}》, 请直接开始生成文章正文，不要有任何额外的前言。
"""

class SiliconFlowService:
    def _get_headers(self, api_key: str):
        return {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "text/event-stream" # 关键：用于流式响应
        }

    async def validate_key(self, api_key: str) -> (bool, str):
        """
        通过发送一个简单的请求来验证 API Key。
        """
        try:
            client = OpenAI(api_key=api_key, base_url="https://api.siliconflow.cn/v1")
            response = client.chat.completions.create(  
                model="Qwen/Qwen2.5-Coder-32B-Instruct",  
                messages=[{  
                    "role": "user",  
                    "content": "你好"  
                }],  
                temperature=0.7,  
                max_tokens=5  
            )  
            print(response)
            if isinstance(response, dict) and response.get('object') == 'chat.completion':
            # 兼容可能的字典形式响应
                return True, "认证成功"
            elif hasattr(response, 'object') and response.object == 'chat.completion':
                # 对于OpenAI客户端返回的ChatCompletion对象
                return True, "认证成功"
            else:
                return False, "认证失败"
        except requests.RequestException as e:
            return False, f"An error occurred: {e}"

    def construct_prompt(self, template_content: str, article_type: str, topic: str) -> str:
        """
        构建最终发送给大模型的完整提示词。
        """
        rule_filled = SYSTEM_RULE.format(TYPE=article_type, TOPIC=topic)
        return f"{template_content}\n\n{rule_filled}"
        
    def construct_block_regeneration_prompt(self, block_type: str, description: str, language: str | None = None) -> str:
        """为智能块重新生成内容构建提示词"""
        if block_type == "CODE" and language:
            return f"请根据以下描述，生成一段 {language} 代码：\n{description}\n请只返回代码本身，不要包含其他解释或标记。"
        if block_type == "PLANTUML":
            return f"请根据以下描述，生成一段 PlantUML 代码来创建一个图表：\n{description}\n请只返回 PlantUML 代码本身，不要包含其他解释或标记。"
        if block_type == "LATEX":
            return f"请根据以下描述，生成一个 LaTeX 公式：\n{description}\n请只返回 LaTeX 代码本身，不要包含其他解释或标记。"
        return f"请根据以下描述生成内容：{description}"


    async def stream_generation(self, api_key: str, prompt: str) -> AsyncGenerator[str, None]:
        """
        以流式方式请求大模型并返回内容。
        """
        url = f"{SILICON_FLOW_BASE_URL}/chat/completions"
        payload = {
            "model": "zai-org/GLM-4.5",
            "messages": [{"role": "user", "content": prompt}],
            "stream": True,
            "response_format": {"type": "text"}
        }

        try:
            with requests.post(url, headers=self._get_headers(api_key), json=payload, stream=True) as response:
                response.raise_for_status()
                for line in response.iter_lines():
                    if line:
                        line_str = line.decode('utf-8')
                        if line_str.startswith('data: '):
                            json_str = line_str[len('data: '):]
                            if json_str.strip() == '[DONE]':
                                break
                            try:
                                data = json.loads(json_str)
                                content = data.get("choices", [{}])[0].get("delta", {}).get("content", "")
                                if content:
                                    yield f"data: {json.dumps({'content': content})}\n\n"
                                    await asyncio.sleep(0.01) # 控制流速
                            except json.JSONDecodeError:
                                continue # 忽略无法解析的行
        except requests.RequestException as e:
            error_message = f"Error communicating with LLM service: {e}"
            yield f"data: {json.dumps({'error': error_message})}\n\n"

# FastAPI 依赖注入
def get_llm_service():
    return SiliconFlowService()
