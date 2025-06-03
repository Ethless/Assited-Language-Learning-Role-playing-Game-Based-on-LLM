from core.DSchat import DeepSeekClient,Conversation

class NPC_chat:
    def __init__(self):
        pass
    def generate(self):
        pass
        
class item_chat:
    """
    物品交互模拟器类
    """
    
    def __init__(self, client: DeepSeekClient):
        """
        初始化物品交互模拟器
        
        参数:
            client (DeepSeekClient): DeepSeek API 客户端
        """
        self.client = client
        self.current_item = None
        self.current_options = []
        
        # 创建对话实例（用于保持交互状态）
        self.conversation = Conversation(
            client,
            conversation_id="item_interaction",
            system_prompt="你是一个物品交互模拟器。根据物品描述生成三个交互选项，然后根据用户选择模拟物品的变化。",
            temperature=1.5,  # 适度创造性
            max_tokens=100,
            memory_limit=6
        )
    
    def set_item(self, item_name: str, item_description: str):
        """
        设置当前物品并重置状态
        
        参数:
            item_name (str): 物品名称
            item_description (str): 物品描述
        """
        # 重置对话状态
        self.conversation.clear_memory()
        self.current_item = item_name
        self.current_options = []
        
        # 设置系统提示（包含物品信息）
        system_prompt = f"""
        你是一个物品交互模拟器。当前物品：{item_name}。
        物品描述：{item_description}
        
        请遵守以下规则：
        1. 用户请求选项时，生成三个可行的交互选项
        2. 每个选项应简洁明了（不超过6个字）
        3. 当用户选择选项时，模拟物品的变化结果
        4. 变化结果应包含物品状态变化的描述
        """
        self.conversation.update_parameters(system_prompt=system_prompt)
    
    def generate_options(self) -> list:
        """
        生成三个交互选项
        
        返回:
            list: 三个交互选项的列表
        """
        # 请求生成选项
        response = self.conversation.generate_response(
            "请生成三个可行的交互选项，用JSON数组格式返回,遵循以下格式：[选项1，选项2，选项3]",
            json_mode=True
        )

        # 处理响应（确保是列表格式）
        if isinstance(response, list) and len(response) >= 3:
            self.current_options = response[:3]
            return self.current_options
        elif "options" in response and isinstance(response["options"], list):
            self.current_options = response["options"][:3]
            return self.current_options
        else:
            # 后备方案：如果JSON解析失败
            self.current_options = ["使用物品", "检查物品", "改变物品"]
            return self.current_options
    
    def interact(self, option: str) -> dict:
        """
        执行交互选项并返回结果
        
        参数:
            option (str): 用户选择的选项内容
            
        返回:
            dict: 包含交互结果的字典
        """
        patten = '{\'result\':<执行选项后，物品发生变化的描述>,\'new_state\':<物品变化后的状态>}'
        if not self.current_item:
            return {"error": "未设置物品", "suggestion": "请先调用set_item()设置物品"}
        
        # 验证选项是否在可用选项中
        if option not in self.current_options:
            return {
                "error": "无效选项",
                "valid_options": self.current_options,
                "suggestion": "请从可用选项中选择"
            }
        
        # 请求模拟交互结果（临时不记忆此次交互）
        response = self.conversation.generate_response(
            f"执行选项：{option}。请模拟物品变化结果，用JSON字典返回变化描述，输出需遵守以下格式:{patten}",
            json_mode=True,
            add_to_memory=False  # 关键修改：临时不记忆此次交互
        )

        # 标准化响应格式
        result = {
            "item": self.current_item,
            "action": option,
            "result": response.get("result", "未知变化"),
            "new_state": response.get("new_state", "状态未知"),
            "available_options": self.current_options.copy()  # 保留当前选项
        }
        
        # 添加原始响应用于调试
        result["raw_response"] = response
        
        return result
    
    def multi_step_interaction(self, item_name: str, item_description: str) -> dict:
        """
        完整交互流程：设置物品 → 生成选项 → 随机选择 → 返回结果（测试用）
        
        参数:
            item_name (str): 物品名称
            item_description (str): 物品描述
            
        返回:
            dict: 包含完整交互结果的字典
        """
        # 设置物品
        self.set_item(item_name, item_description)
        
        # 生成选项
        options = self.generate_options()
        
        # 随机选择一个选项（模拟用户选择）
        import random
        selected_option = random.choice(options)
        
        # 执行交互
        result = self.interact(selected_option)
        
        # 添加选项信息到结果
        result["all_options"] = options
        
        return result

    def get_all_memory(self):
        '''
        返回所有记忆，如需进行持久化保存，可以调用
        '''
        return self.conversation.get_full_conversation()

class story_NPC_chat:
    """
    NPC 对话系统
    """
    
    def __init__(self, client: DeepSeekClient):
        """
        初始化 NPC 对话系统
        
        参数:
            client (DeepSeekClient): DeepSeek API 客户端
        """
        self.client = client
        self.npc_name = None
        self.npc_setting = None
        
        # 创建对话实例
        self.conversation = Conversation(
            client,
            conversation_id="npc_conversation",
            system_prompt="你是一个角色扮演助手，请根据设定扮演NPC并进行自然对话。",
            temperature=1.5,  # 适度创造性
            max_tokens=150,
            memory_limit=20
        )
    
    def set_npc_setting(
        self,
        name: str,
        personality: str,
        background: str,
        environment: str = "未知地点"
    ):
        """
        设置 NPC 角色设定
        
        参数:
            name (str): NPC 名称
            personality (str): 角色性格描述
            background (str): 角色背景故事
            environment (str): 当前环境背景
        """
        self.npc_name = name
        self.npc_setting = {
            "personality": personality,
            "background": background,
            "environment": environment
        }
        
        # 构建系统提示
        system_prompt = f"""
        你正在扮演角色【{name}】，请严格遵循以下设定：
        1. 性格特点：{personality}
        2. 背景故事：{background}
        3. 当前环境：{environment}
        
        对话规则：
        - 保持角色一致性，使用符合角色身份的语言风格
        - 自然回应用户的对话
        - 当要求生成选项时，提供三个合理的对话选择
        """
        
        # 重置对话并更新设定
        self.conversation.clear_memory()
        self.conversation.update_parameters(system_prompt=system_prompt)
        
        # 添加初始问候
        self.conversation.add_message("assistant", f"（{name}看着你）你好，我是{name}。")
    
    def generate_dialogue(self, **kwargs) -> dict:
        """
        生成 NPC 的对话回应
        
        返回:
            str: NPC 的回应内容
        """
        if not self.npc_name:
            return "错误：请先设置NPC角色（调用set_npc_setting）"
        
        #返回值的格式
        patten = '{\'action\':[<动作1>,<动作2>],\'respond\':[<回应内容1>,<回应内容2>]}'

        # 基于对话历史生成回应
        response = self.conversation.generate_response(
            f"请根据角色设定生成自然的对话回应(此回应无需生成选项)，用JSON数组格式返回，包含两个数组，\'action\'：包含npc动作或表情列表(1-3个),\'respond\':包含对应动作或表情下npc的对话内容(与动作一一对应),遵循以下格式：{patten}",
            add_to_memory=False,  # 稍后手动添加
            json_mode= True
        )

        #标准化处理
        response = self.output_stand(response)

        # 将回应添加到记忆
        self.conversation.add_message("assistant", response['total'])
        return response
    
    def generate_options(self) -> list:
        """
        生成三个对话选项供用户选择
        
        返回:
            list: 三个选项的字符串列表
        """
        if not self.npc_name:
            return ["请先设置NPC角色"]
        
        # 请求生成选项
        prompt = f"请生成三个可能的用户回应选项，每个选项不超过15个字，用JSON数组格式返回"
        response = self.conversation.generate_response(
            prompt,
            json_mode=True,
            add_to_memory=False  # 不污染主对话
        )
        
        # 解析选项
        if isinstance(response, list) and len(response) >= 3:
            return response[:3]
        elif "options" in response and isinstance(response["options"], list):
            return response["options"][:3]
        else:
            # 后备选项
            return [
                f"询问{self.npc_name}的背景",
                f"讨论当前环境",
                f"请求建议"
            ]
    
    def add_user_response(self, user_input: str):
        """
        添加用户回应到对话记忆
        
        参数:
            user_input (str): 用户选择的对话选项或自由输入
        """
        if not self.npc_name:
            raise ValueError("NPC角色未设置")
        
        self.conversation.add_message("user", user_input)
    
    def generate_goodbye(self, reason: str = "有急事") -> dict:
        """
        生成结束对话的告别语
        
        参数:
            reason (str): 离开原因
            
        返回:
            str: 告别语
        """
        if not self.npc_name:
            return "再见！"
        
        #返回值的格式
        patten = '{\'action\':[<动作1>,<动作2>],\'respond\':[<回应内容1>,<回应内容2>]}'

        # 生成情境化的告别语
        prompt = f"请以{self.npc_name}的身份生成结束对话的告别语，离开原因：{reason},用JSON数组格式返回，包含两个数组，\'action\'：包含npc动作或表情列表(1-3个),\'respond\':包含对应动作或表情下npc的对话内容(与动作一一对应),遵循以下格式：{patten}"
        goodbye = self.conversation.generate_response(
            prompt,
            temperature=0.5,  # 低随机性
            add_to_memory=False,
            json_mode= True
        )

        #标准化处理
        goodbye = self.output_stand(goodbye)

        # 添加到记忆并返回
        self.conversation.add_message("assistant", goodbye['total'])
        return goodbye
    
    def summarize_conversation(self) -> dict:
        """
        总结对话内容
        
        返回:
            dict: 包含总结信息的字典
        """
        if not self.npc_name:
            return {"error": "对话尚未开始"}
        
        # 生成摘要
        summary = self.conversation.generate_summary(
            focus="key_points",
            include_in_conversation=False
        )
        
        # 提取关键信息
        return {
            "npc_name": self.npc_name,
            "conversation_summary": summary,
            "total_messages": len(self.conversation.memory) // 2,
            "last_interaction": self.conversation.memory[-1]["content"] if self.conversation.memory else ""
        }
    
    def get_full_conversation(self) -> str:
        """
        获取完整对话文本（不含系统提示）
        
        返回:
            str: 格式化后的对话历史
        """
        return self.conversation.get_conversation_text()
    
    def reset_conversation(self):
        """重置对话历史（保留角色设定）"""
        if self.npc_name and self.npc_setting:
            # 保留系统提示重置对话
            self.set_npc_setting(
                self.npc_name,
                self.npc_setting["personality"],
                self.npc_setting["background"],
                self.npc_setting["environment"]
            )

    def output_stand(self,response) -> dict:
        # 标准化响应
        if isinstance(response, dict):
            actions = response.get("action", [])
            responds = response.get("respond", [])
            
            # 确保两个列表长度一致
            min_length = min(len(actions), len(responds))
            actions = actions[:min_length]
            responds = responds[:min_length]
            
            # 构建完整描述
            total = " ".join(f"*{action}* {respond}" for action, respond in zip(actions, responds))
            
            response = {
                'action': actions,
                'respond': responds,
                'total': total
            }
        
        else:    
            # 后备方案：普通文本处理
            response = {
                'action': ["站立不动"],
                'respond': [response if isinstance(response, str) else str(response)],
                'total': response if isinstance(response, str) else str(response)
            }
        return response
    
    def get_all_memory(self):
        '''
        返回所有记忆，如需进行持久化保存，可以调用
        '''
        return self.conversation.get_full_conversation()