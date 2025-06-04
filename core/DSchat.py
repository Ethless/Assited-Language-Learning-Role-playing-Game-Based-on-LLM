from dotenv import load_dotenv
load_dotenv()
import os
import re
import json
import requests
from typing import Dict, List, Optional, Union, Callable


class DeepSeekClient:
    """
    DeepSeek API 核心通信客户端
    负责处理与 DeepSeek API 的直接通信
    """
    
    def __init__(self, api_key: str = None):
        """
        初始化 API 客户端
        
        参数:
            api_key (str, optional): DeepSeek API 密钥。如果未提供，将从环境变量 DEEPSEEK_API_KEY 中读取
        """
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        if not self.api_key:
            raise ValueError("未提供 API 密钥且环境变量中未找到 DEEPSEEK_API_KEY")
            
        # API 配置
        self.api_url = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.session = requests.Session()
    
    def generate(
        self,
        messages: List[Dict[str, str]],
        model: str = "ep-20250530190548-bbm6q",
        temperature: float = 0.7,
        max_tokens: int = 300,
        **kwargs
    ) -> str:
        """
        发送生成请求到 DeepSeek API
        
        参数:
            messages (List[Dict]): 对话消息列表，格式为 [{"role": "user", "content": "消息内容"}, ...]
            model (str): 使用的模型名称，默认为 "deepseek-v3"
            temperature (float): 生成温度（0-2），控制随机性，默认0.7
            max_tokens (int): 最大生成 token 数，默认300
            **kwargs: 其他 API 参数（如 top_p, frequency_penalty 等）
        
        返回:
            str: 生成的文本内容
        
        异常:
            ConnectionError: API 请求失败（网络问题）
            RuntimeError: API 响应解析失败
        """
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            **kwargs
        }
        
        try:
            response = self.session.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=15
            )
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"API 请求失败: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"API 响应解析失败: {str(e)}")


class Conversation:
    """
    单个对话会话管理
    包含对话历史维护、AI 交互和手动摘要生成功能
    """
    
    def __init__(
        self,
        client: DeepSeekClient,
        conversation_id: str,
        system_prompt: str = "",
        model: str = "ep-20250530190548-bbm6q",
        temperature: float = 0.7,
        max_tokens: int = 300,
        memory_limit: int = 10
    ):
        """
        初始化对话会话
        
        参数:
            client (DeepSeekClient): DeepSeekClient 实例
            conversation_id (str): 对话唯一标识符
            system_prompt (str): 系统提示词，用于设定 AI 角色和行为
            model (str): 使用的模型名称，默认为 "deepseek-v3"
            temperature (float): 默认生成温度，默认0.7
            max_tokens (int): 默认最大生成长度（token 数），默认300
            memory_limit (int): 记忆容量（对话轮数），默认10
        """
        self.client = client
        self.conversation_id = conversation_id
        self.system_prompt = system_prompt
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.memory_limit = memory_limit
        
        # 对话历史
        self.memory: List[Dict[str, str]] = []
        
        if system_prompt:
            self.memory.append({"role": "system", "content": system_prompt})
    
    def add_message(self, role: str, content: str) -> None:
        """
        添加单条消息到对话历史
        
        参数:
            role (str): 消息角色（"user", "assistant", "system"）
            content (str): 消息内容
        
        说明:
            添加后会自动修剪记忆以保持容量限制
        """
        self.memory.append({"role": role, "content": content})
        self._trim_memory()
    
    def generate_response(
        self,
        user_input: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        json_mode: bool = False,
        add_to_memory: bool = True,
        **kwargs
    ) -> Union[str, dict]:
        """
        生成 AI 回复
        
        参数:
            user_input (str): 用户输入内容
            temperature (float, optional): 临时覆盖默认温度
            max_tokens (int, optional): 临时覆盖默认最大 token 数
            json_mode (bool): 是否要求返回 JSON 格式，默认False
            add_to_memory (bool): 是否将本次交互加入记忆，默认True
            **kwargs: 其他 API 参数
        
        返回:
            Union[str, dict]: 
                当 json_mode=False 时返回文本回复
                当 json_mode=True 时返回解析后的 JSON 对象或错误字典
        
        说明:
            当 json_mode=True 但响应不是有效 JSON 时，返回包含错误信息的字典
        """
        # 添加用户消息到请求
        request_messages = self.memory.copy()
        request_messages.append({"role": "user", "content": user_input})
        
        # 准备 API 参数
        api_params = {
            "messages": request_messages,
            "model": self.model,
            "temperature": temperature or self.temperature,
            "max_tokens": max_tokens or self.max_tokens,
        }
        
        if json_mode:
            api_params["response_format"] = {"type": "json_object"}
        
        api_params.update(kwargs)
        
        # 调用 API 生成回复
        ai_response = self.client.generate(**api_params)
        
        # 处理记忆
        if add_to_memory:
            self.memory.append({"role": "user", "content": user_input})
            self.memory.append({"role": "assistant", "content": ai_response})
            self._trim_memory()
        
        # 返回结果
        if json_mode:
            # 使用增强的 JSON 解析方法
            return self._parse_json_response(ai_response)
        return ai_response
    
    def generate_summary(
        self, 
        length: int = 150, 
        focus: str = "key_points",
        include_in_conversation: bool = False
    ) -> str:
        """
        手动生成对话摘要
        
        参数:
            length (int): 摘要长度（字数），默认150
            focus (str): 摘要重点类型，可选值: 
                "key_points" - 关键点和主要结论 (默认)
                "decisions" - 达成的决定和共识
                "action_items" - 待办事项和行动计划
                "full" - 全面总结
            include_in_conversation (bool): 是否将摘要添加为系统消息，默认False
        
        返回:
            str: 生成的摘要文本
        
        说明:
            此方法会单独调用API生成摘要，不影响主对话历史
        """
        # 确定摘要焦点
        focus_map = {
            "key_points": "关键点和主要结论",
            "decisions": "达成的决定和共识",
            "action_items": "待办事项和行动计划",
            "full": "全面总结"
        }
        focus_text = focus_map.get(focus, "关键点和主要结论")
        
        # 构造摘要提示
        prompt = f"""
        请根据以下对话历史生成一个简洁的摘要，长度不超过{length}字。
        摘要应聚焦于: {focus_text}。
        对话历史:
        {self.get_conversation_text()}
        """
        
        # 使用低温度确保摘要准确
        summary = self.client.generate(
            messages=[{"role": "user", "content": prompt}],
            model=self.model,
            temperature=0.3,
            max_tokens=length + 50  # 提供额外token空间
        )
        
        # 可选：将摘要添加为系统消息
        if include_in_conversation:
            # 保留原始系统提示（如果存在）
            original_system = None
            if self.memory and self.memory[0]["role"] == "system":
                original_system = self.memory[0]
                self.memory = self.memory[1:]
            
            # 添加摘要系统消息
            self.memory.insert(0, {"role": "system", "content": f"对话摘要: {summary}"})
            
            # 恢复原始系统提示
            if original_system:
                self.memory.insert(0, original_system)
        
        return summary
    
    def get_conversation_text(self, include_system: bool = False) -> str:
        """
        获取对话的文本表示
        
        参数:
            include_system (bool): 是否包含系统提示，默认False
        
        返回:
            str: 对话的文本格式（每行格式为"角色: 内容"）
        """
        text = []
        for msg in self.memory:
            if not include_system and msg["role"] == "system":
                continue
            text.append(f"{msg['role']}: {msg['content']}")
        return "\n".join(text)
    
    def import_memory(
        self,
        external_memory: List[Dict[str, str]],
        role_filter: Optional[List[str]] = None,
        max_messages: Optional[int] = None,
        prepend: bool = False
    ) -> None:
        """
        批量导入外部记忆到当前对话
        
        参数:
            external_memory (List[Dict]): 要导入的记忆列表
            role_filter (List[str], optional): 角色过滤列表（只导入指定角色的消息）
            max_messages (int, optional): 最多导入的消息数量
            prepend (bool): 是否添加到记忆开头（False时为追加到末尾），默认False
        
        说明:
            导入后会自动修剪记忆以保持容量限制
        """
        filtered_memory = external_memory.copy()
        
        if role_filter:
            filtered_memory = [msg for msg in filtered_memory if msg["role"] in role_filter]
        
        if max_messages:
            filtered_memory = filtered_memory[-max_messages:]
        
        if prepend:
            if self.memory and self.memory[0]["role"] == "system":
                system_msg = self.memory[0]
                self.memory = [system_msg] + filtered_memory + self.memory[1:]
            else:
                self.memory = filtered_memory + self.memory
        else:
            self.memory.extend(filtered_memory)
        
        self._trim_memory()
    
    def export_memory(
        self,
        include_system: bool = True,
        role_filter: Optional[List[str]] = None,
        max_messages: Optional[int] = None,
        transform: Optional[Callable[[Dict], Dict]] = None
    ) -> List[Dict[str, str]]:
        """
        导出对话记忆
        
        参数:
            include_system (bool): 是否包含系统提示，默认True
            role_filter (List[str], optional): 角色过滤列表
            max_messages (int, optional): 最多导出的消息数量
            transform (Callable, optional): 自定义转换函数，用于修改每条消息
        
        返回:
            List[Dict]: 导出的记忆列表
        """
        memory_copy = self.memory.copy()
        
        if not include_system and memory_copy and memory_copy[0]["role"] == "system":
            memory_copy = memory_copy[1:]
        
        if role_filter:
            memory_copy = [msg for msg in memory_copy if msg["role"] in role_filter]
        
        if max_messages:
            memory_copy = memory_copy[-max_messages:]
        
        if transform:
            memory_copy = [transform(msg) for msg in memory_copy]
        
        return memory_copy
    
    def get_full_conversation(self) -> List[Dict[str, str]]:
        """
        获取完整对话历史（包含系统提示）
        
        返回:
            List[Dict]: 完整的对话历史副本
        """
        return self.memory.copy()
    
    def clear_memory(self, keep_system: bool = True) -> None:
        """
        清空对话记忆
        
        参数:
            keep_system (bool): 是否保留系统提示，默认True
        """
        if keep_system and self.memory and self.memory[0]["role"] == "system":
            self.memory = [self.memory[0]]
        else:
            self.memory = []
    
    def update_parameters(
        self,
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        memory_limit: Optional[int] = None
    ) -> None:
        """
        动态更新对话参数
        
        参数:
            system_prompt (str, optional): 新的系统提示
            model (str, optional): 新的模型名称
            temperature (float, optional): 新的生成温度
            max_tokens (int, optional): 新的最大 token 数
            memory_limit (int, optional): 新的记忆容量
        
        说明:
            更新记忆容量后会立即应用新的限制
        """
        if system_prompt is not None:
            self.system_prompt = system_prompt
            if self.memory and self.memory[0]["role"] == "system":
                self.memory[0]["content"] = system_prompt
            elif system_prompt:
                self.memory.insert(0, {"role": "system", "content": system_prompt})
        
        if model is not None:
            self.model = model
        if temperature is not None:
            self.temperature = temperature
        if max_tokens is not None:
            self.max_tokens = max_tokens
        if memory_limit is not None:
            self.memory_limit = memory_limit
            self._trim_memory()
    
    def _trim_memory(self) -> None:
        """
        内部方法：修剪记忆以保持容量限制
        
        说明:
            确保记忆不超过 memory_limit 指定的容量
            系统提示会始终保留在开头
        """
        max_messages = self.memory_limit * 2
        if len(self.memory) > max_messages:
            system_msg = None
            if self.memory and self.memory[0]["role"] == "system":
                system_msg = self.memory[0]
                self.memory = self.memory[1:]
            
            self.memory = self.memory[-max_messages:]
            
            if system_msg:
                self.memory.insert(0, system_msg)

    def _parse_json_response(self, raw_response: str) -> dict:
        """
        增强的 JSON 解析方法，处理多种格式：
        1. 纯 JSON
        2. Markdown 代码块包裹的 JSON
        3. 不完整 JSON 修复
        """
        # 尝试直接解析
        try:
            return json.loads(raw_response)
        except json.JSONDecodeError:
            pass
        
        # 尝试提取 Markdown 代码块中的 JSON
        markdown_match = re.search(r'```(?:json)?\n(.*?)\n```', raw_response, re.DOTALL)
        if markdown_match:
            try:
                return json.loads(markdown_match.group(1))
            except json.JSONDecodeError:
                pass
        
        # 尝试提取 JSON 对象部分
        json_match = re.search(r'\{.*\}', raw_response, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(0))
            except json.JSONDecodeError:
                pass

        json_match = json.load(raw_response)
        if json_match:
            try:
                return json_match
            except json.JSONDecodeError:
                pass

        # 尝试修复常见格式问题
        try:
            # 处理多余引号
            fixed = re.sub(r'\\"', '"', raw_response)
            # 处理换行符
            fixed = fixed.replace('\n', ' ')
            # 处理尾部逗号
            fixed = re.sub(r',\s*}', '}', fixed)
            fixed = re.sub(r',\s*]', ']', fixed)
            return json.loads(fixed)
        except:
            return {
                "error": "JSON 解析失败",
                "raw_response": raw_response
            }