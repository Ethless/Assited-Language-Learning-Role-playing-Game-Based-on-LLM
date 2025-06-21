import re
import json
import random
from typing import List, Dict

class ClozeGenerator:
    """
    完形填空生成器
    功能：根据背景故事和词表生成完形填空题目
    """
    
    def __init__(self, client):
        """
        初始化完形填空生成器
        
        参数:
            client: DeepSeekClient 实例
        """
        self.client = client
        
    def generate_cloze(self, background_story: str, word_list: List[Dict]) -> Dict:
        """
        生成完形填空题目
        
        参数:
            background_story (str): 背景故事描述
            word_list (list): 词表列表
            
        返回:
            dict: 完形填空题目数据
        """
        # 准备提示词
        prompt = self._build_prompt(background_story, word_list)
        
        # 调用API生成内容
        response = self.client.generate(
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500
        )
        
        # 解析并格式化输出
        return self._format_output(response, word_list)
    
    def _build_prompt(self, background_story: str, word_list: List[Dict]) -> str:
        """
        构建生成提示词
        
        参数:
            background_story (str): 背景故事
            word_list (list): 词表
            
        返回:
            str: 完整的提示词
        """
        # 准备词表描述
        word_descriptions = []
        for word in word_list:
            word_descriptions.append(f"{word['jp']} ({word['zh']})")
        
        # 构建提示词
        prompt = f"""
## 任务说明
你需要创建一个完形填空练习，要求如下：
1. 背景故事：{background_story}
2. 使用以下词表中的所有词语（每个词语必须使用一次）：
   {", ".join(word_descriptions)}
3. 在文中用 [序号] 标记需要填空的位置,且不出现原词
4. 生成一个简短的标题
5. 内容长度：200-300字
6. 符合背景故事的时代背景但不干扰主要剧情

## 输出格式
请严格按照以下JSON格式输出：
{{
    "title": "生成的标题",
    "content": "生成的完形填空内容，其中填空位置用[0]、[1]等标记"
}}
"""
        return prompt
    
    def _format_output(self, response: str, word_list: List[Dict]) -> Dict:
        """
        格式化API响应
        
        参数:
            response (str): API返回的文本
            word_list (list): 词表
            
        返回:
            dict: 格式化后的完形填空数据
        """
        try:
            # 尝试解析JSON
            data = json.loads(response)
            title = data.get("title", "")
            content = data.get("content", "")
        except:
            # 后备方案：提取标题和内容
            title = self._extract_title(response)
            content = self._extract_content(response)
        
        # 验证占位符数量
        placeholder_count = self._count_placeholders(content)
        if placeholder_count != len(word_list):
            # 自动修正占位符数量
            content = self._adjust_placeholders(content, len(word_list))
        
        # 构建返回数据
        return {
            "title": title,
            "content": content,
            "blanks": self._build_blanks_list(len(word_list)),
            "options": self._build_options_list(word_list)
        }
    
    def _extract_title(self, text: str) -> str:
        """
        从文本中提取标题
        
        参数:
            text (str): 原始文本
            
        返回:
            str: 提取的标题
        """
        # 尝试匹配标题行
        match = re.search(r'"title":\s*"([^"]+)"', text)
        if match:
            return match.group(1)
        
        # 尝试匹配第一行作为标题
        first_line = text.split('\n')[0].strip()
        if first_line and len(first_line) < 50:  # 标题不宜过长
            return first_line.replace('"', '')
        
        return "完形填空练习"
    
    def _extract_content(self, text: str) -> str:
        """
        从文本中提取内容
        
        参数:
            text (str): 原始文本
            
        返回:
            str: 提取的内容
        """
        # 尝试匹配内容字段
        match = re.search(r'"content":\s*"([^"]+)"', text)
        if match:
            return match.group(1)
        
        # 尝试提取包含占位符的段落
        placeholder_pattern = r'(\[.*?\].*?\[.*?\])'
        matches = re.findall(placeholder_pattern, text)
        if matches:
            return max(matches, key=len)  # 返回最长的匹配段落
        
        # 后备方案：返回整个文本
        return text
    
    def _count_placeholders(self, content: str) -> int:
        """
        统计内容中的占位符数量
        
        参数:
            content (str): 内容文本
            
        返回:
            int: 占位符数量
        """
        return len(re.findall(r'\[\d+\]', content))
    
    def _adjust_placeholders(self, content: str, required_count: int) -> str:
        """
        调整占位符数量
        
        参数:
            content (str): 内容文本
            required_count (int): 需要的占位符数量
            
        返回:
            str: 调整后的内容
        """
        current_count = self._count_placeholders(content)
        
        if current_count < required_count:
            # 添加缺失的占位符
            for i in range(current_count, required_count):
                content += f" [占位符{i}]"
        elif current_count > required_count:
            # 移除多余的占位符
            pattern = r'\[\d+\]'
            matches = re.findall(pattern, content)
            if len(matches) > required_count:
                # 保留前required_count个占位符
                for i in range(required_count, len(matches)):
                    content = content.replace(matches[i], "", 1)
        
        # 标准化占位符编号
        for i in range(required_count):
            content = content.replace(f"[占位符{i}]", f"[{i}]", 1)
        
        return content
    
    def _build_blanks_list(self, count: int) -> List[Dict]:
        """
        构建空白列表
        
        参数:
            count (int): 空白数量
            
        返回:
            list: 空白列表
        """
        return [{"id": i, "correctOptionId": i} for i in range(count)]
    
    def _build_options_list(self, word_list: List[Dict]) -> List[Dict]:
        """
        构建选项列表
        
        参数:
            word_list (list): 词表
            
        返回:
            list: 选项列表
        """
        return [{
            "id": idx,
            "jp": word["jp"],
            "zh": word["zh"]
        } for idx, word in enumerate(word_list)]
    
    def generate_multiple_cloze(self, background_story: str, word_list: List[Dict], count: int = 3) -> List[Dict]:
        """
        生成多个完形填空题目
        
        参数:
            background_story (str): 背景故事
            word_list (list): 词表
            count (int): 题目数量
            
        返回:
            list: 多个完形填空题目列表
        """
        results = []
        for _ in range(count):
            results.append(self.generate_cloze(background_story, word_list))
        return results