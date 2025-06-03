<template>
    <div class="item-detail">
      <!-- 返回按钮（仅在猜词阶段显示） -->
      <button v-if="!showOptions" class="back-button" @click="$emit('back')">
        ← 返回道具列表
      </button>
  
      <!-- 猜词阶段 -->
      <div v-if="!showOptions" class="guess-section">
        <!-- 原有猜词界面内容... -->
        <img :src="item.image" class="detail-image">
        <div class="item-description">{{ item.chinese }}</div>
        
        <div class="guess-form">
          <h3>道具名称(日语): {{ item.japanese }}</h3>
          <input 
            v-model="userGuess" 
            @keyup.enter="checkAnswer"
            placeholder="输入中文释义..."
          >
          <button @click="checkAnswer">提交</button>
          <div v-if="feedback" :class="['feedback', isCorrect ? 'correct' : 'incorrect']">
            {{ feedback }}
          </div>
        </div>
      </div>
  
      <!-- 操作选项阶段 -->
      <div v-if="showOptions" class="options-section">
        <h2>请选择对「{{ item.chinese }}」的操作</h2>
        <div v-if="loadingOptions" class="loading">加载选项中...</div>
        <div v-else class="options-grid">
          <button 
            v-for="option in options" 
            :key="option.id"
            @click="handleOptionSelect(option)"
            class="option-btn"
          >
            {{ option.text }}
          </button>
        </div>
        <button @click="showOptions = false" class="back-option">返回重新猜词</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'ItemGuess',
    props: {
      item: {
        type: Object,
        required: true
      }
    },
    data() {
      return {
        userGuess: '',
        feedback: '',
        isCorrect: false,
        showOptions: false,  // 控制是否显示操作选项
        options: [],         // 存储从API获取的选项
        loadingOptions: false
      }
    },
    methods: {
      async checkAnswer() {
        if (this.userGuess.trim().toLowerCase() === this.item.answer.toLowerCase()) {
          this.feedback = '回答正确！'
          this.isCorrect = true
          await this.fetchOptions()  // 获取操作选项
          this.showOptions = true    // 显示选项界面
        } else {
          this.feedback = `回答错误，正确答案是: ${this.item.answer}`
          this.isCorrect = false
        }
      },
  
      // 从后端获取操作选项
      async fetchOptions() {
        this.loadingOptions = true
        try {
          // 这里替换为实际的API调用
          const response = await fetch(`/api/items/${this.item.id}/options`)
          this.options = await response.json()
          
          // 模拟数据（开发时使用）
          // this.options = [
          //   { id: 1, text: '使用道具' },
          //   { id: 2, text: '分解道具' },
          //   { id: 3, text: '赠送给NPC' },
          //   { id: 4, text: '存入仓库' }
          // ]
        } catch (error) {
          console.error('获取选项失败:', error)
          this.options = []
        } finally {
          this.loadingOptions = false
        }
      },
  
      // 处理用户选择
      async handleOptionSelect(option) {
        try {
          // 发送选择到后端
          const response = await fetch('/api/item-actions', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              itemId: this.item.id,
              actionId: option.id
            })
          })
          
          const result = await response.json()
          alert(`操作成功: ${result.message}`)
          this.$emit('action-completed', { item: this.item, action: option })
        } catch (error) {
          alert('操作失败，请重试')
          console.error('操作提交失败:', error)
        }
      }
    }
  }
  </script>
  
  <style scoped>
  /* 原有样式保持不变... */
  
  /* 新增操作选项样式 */
  .options-section {
    padding: 20px;
    text-align: center;
  }
  
  .loading {
    margin: 20px 0;
    color: #666;
  }
  
  .options-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 15px;
    margin: 20px 0;
  }
  
  .option-btn {
    padding: 15px;
    background: #f8f8f8;
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.2s;
  }
  
  .option-btn:hover {
    background: #e0e0e0;
    transform: translateY(-2px);
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  }
  
  .back-option {
    margin-top: 20px;
    background: none;
    border: none;
    color: #666;
    cursor: pointer;
    text-decoration: underline;
  }
  </style>