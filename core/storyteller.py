PERSPECTIVE_FIRST_PERSON = "first_person"
PERSPECTIVE_THIRD_PERSON = "third_person"

class storyteller:
    def __init__(self, client):
        self.client = client
        self.background = ""
        self.ending = ""
        self.scene = ""
        self.items = []
        self.summary_history = []

    def set_background(self, background):
        self.background = background

    def set_ending(self, ending):
        self.ending = ending

    def update_scene(self, scene):
        self.scene = scene

    def add_collected_items(self, items):
        self.items.extend(items)

    def add_plot_summary(self, summary):
        self.summary_history.append(summary)

    def generate_plot(self, perspective=PERSPECTIVE_FIRST_PERSON):
        prompt = self._compose_prompt(perspective)
        response = self.client.generate(messages=[{"role": "user", "content": prompt}])
        return {"plot": response}

    def generate_ending_transition(self, perspective=PERSPECTIVE_FIRST_PERSON):
        prompt = f"""
        你即将写出一个衔接故事结局的段落，请参考以下信息：

        - 背景：{self.background}
        - 当前场景：{self.scene}
        - 已收集物品：{", ".join(self.items)}
        - 剧情进展摘要：{"；".join(self.summary_history)}
        - 结局剧情：{self.ending}

        请用{self._perspective_text(perspective)}生成一个100~200 字的文学化剧情段落，将前面的剧情自然的连接到结局剧情。
        要求：
        1. 每次生成100-200字的一段剧情
        2. 剧情需从给出的剧情总结开始
        3. 自然的衔接前置剧情和结局剧情
        4. 保持场景一致性
        5. 以前置剧情开头
        6. 以结局剧情结尾
        """
        response = self.client.generate(messages=[{"role": "user", "content": prompt}])
        return {"plot": response}

    def _compose_prompt(self, perspective):
        return f"""
        你是一位科幻小说作家，请以{self._perspective_text(perspective)}讲述以下设定的故事片段：

        - 故事背景：{self.background}
        - 当前场景：{self.scene}
        - 已收集物品：{", ".join(self.items)}
        - 剧情进展摘要：{"；".join(self.summary_history) or "（暂无）"}

        请生成 100~200 字的文学化剧情段落，注意代入感和环境描写。
        """

    def _perspective_text(self, perspective):
        return {
            PERSPECTIVE_FIRST_PERSON: "第一人称（我）",
            PERSPECTIVE_THIRD_PERSON: "第三人称（他/她）"
        }.get(perspective, "第一人称")
