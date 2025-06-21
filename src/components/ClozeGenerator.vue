<template>
  <div class="cloze-generator">
    <h2>📖 完形填空生成器</h2>

    <div class="cloze-content">
      <!-- 左侧：输入区 -->
      <div class="input-area">
        <label>背景故事：</label>
        <textarea v-model="background" rows="8" class="input-box"></textarea>

        <label>词表（可修改）：</label>
        <div class="word-list">
          <div
            v-for="(word, index) in wordList"
            :key="index"
            class="word-item"
          >
            <input v-model="word.jp" placeholder="日语词" />
            <input v-model="word.zh" placeholder="中文意思" />
          </div>
          <button @click="addWord" class="add-word-btn">➕ 新增词语</button>
        </div>

        <button @click="generateCloze" class="generate-btn">
          🎯 生成完形填空
        </button>
      </div>

      <!-- 右侧：结果区 -->
      <div class="result-area" v-if="result">
        <h3>{{ result.title }}</h3>
        <p class="content">{{ result.content }}</p>
        <h4>选项：</h4>
        <ul>
          <li v-for="option in result.options" :key="option.id">
            {{ option.id }} : {{ option.jp }} ({{ option.zh }})
          </li>
        </ul>
      </div>
    </div>d
  </div>
</template>

<script>
import api from "@/api";

export default {
  name: "ClozeGenerator",
  data() {
    return {
      background:
        "在江户时代的日本，武士阶层统治着社会。普通百姓生活简朴，商人阶层开始崛起。",
      wordList: [
        { jp: "シューズクリーナー", zh: "鞋子清洁器" },
        { jp: "小銭入れ", zh: "小钱包" },
        { jp: "着物", zh: "和服" },
      ],
      result: null,
    };
  },
  methods: {
    async generateCloze() {
      try {
        const response = await api.post("/cloze/generate", {
          background_story: this.background,
          word_list: this.wordList,
          count: 1,
        });
        this.result = response.data;
      } catch (error) {
        alert("生成失败，请检查后端是否正常运行！");
        console.error(error);
      }
    },
    addWord() {
      this.wordList.push({ jp: "", zh: "" });
    },
  },
};
</script>

<style scoped>
.cloze-generator {
  padding: 20px;
  background: #fff;
  border-radius: 10px;
  color: #333;
  max-width: 1200px;
  margin: auto;
}

h2 {
  text-align: center;
  margin-bottom: 20px;
}

.cloze-content {
  display: flex;
  gap: 30px; /* 左右栏间距 */
}

.input-area,
.result-area {
  flex: 1;
  min-width: 0; /* 防止溢出 */
}

.input-box {
  width: 100%;
  margin-bottom: 1em;
  padding: 8px;
}

.word-list {
  margin-bottom: 1em;
}

.word-item {
  display: flex;
  gap: 10px;
  margin-bottom: 0.5em;
}

.add-word-btn {
  margin-top: 5px;
  padding: 5px 10px;
}

.generate-btn {
  display: block;
  width: 100%;
  padding: 10px;
  font-weight: bold;
  background: #4caf50;
  color: white;
  border: none;
  border-radius: 5px;
}

.result-area {
  background: #f9f9f9;
  padding: 1em;
  border-radius: 8px;
  overflow: auto;
}

.result-area .content {
  white-space: pre-wrap;
  margin: 1em 0;
  line-height: 1.6;
}
</style>
