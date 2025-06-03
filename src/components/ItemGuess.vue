<template>
    <div class="item-detail">
      <button class="back-button" @click="$emit('back')">← 返回道具列表</button>
      
      <div class="item-content">
        <img :src="item.image" :alt="item.chinese" class="detail-image">
        
        <div class="item-description">
          <p>{{ item.chinese }}</p>
        </div>
        
        <div class="guess-section">
          <h3>道具名称(日语): {{ item.japanese }}</h3>
          <p>请输入这个道具的中文释义:</p>
          
          <input 
            type="text" 
            v-model="userGuess" 
            @keyup.enter="checkAnswer"
            placeholder="输入你的答案..."
            class="guess-input"
            ref="guessInput"
          >
          
          <button @click="checkAnswer" class="submit-button">提交</button>
          
          <div v-if="feedback" class="feedback" :class="{ correct: isCorrect, incorrect: !isCorrect }">
            {{ feedback }}
          </div>
        </div>
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
        isCorrect: false
      }
    },
    mounted() {
      this.$refs.guessInput.focus()
    },
    methods: {
      checkAnswer() {
        if (!this.userGuess.trim()) {
          this.feedback = '请输入你的答案'
          this.isCorrect = false
          return
        }
        
        if (this.userGuess.trim() === this.item.answer) {
          this.feedback = '回答正确！'
          this.isCorrect = true
        } else {
          this.feedback = `回答错误，正确答案是: ${this.item.answer}`
          this.isCorrect = false
        }
      }
    }
  }
  </script>
  
  <style scoped>
  .item-detail {
    margin-top: 20px;
  }
  
  .back-button {
    background: none;
    border: none;
    color: #666;
    font-size: 16px;
    cursor: pointer;
    margin-bottom: 20px;
  }
  
  .back-button:hover {
    color: #333;
  }
  
  .detail-image {
    max-width: 300px;
    max-height: 300px;
    display: block;
    margin: 0 auto 20px;
    border-radius: 8px;
  }
  
  .item-description {
    background: #f5f5f5;
    padding: 15px;
    border-radius: 8px;
    margin-bottom: 20px;
  }
  
  .guess-section {
    background: #f9f9f9;
    padding: 20px;
    border-radius: 8px;
  }
  
  .guess-input {
    width: 100%;
    padding: 10px;
    font-size: 16px;
    border: 1px solid #ddd;
    border-radius: 4px;
    margin: 10px 0;
  }
  
  .submit-button {
    background-color: #4CAF50;
    color: white;
    border: none;
    padding: 10px 20px;
    font-size: 16px;
    cursor: pointer;
    border-radius: 4px;
    transition: background-color 0.3s;
  }
  
  .submit-button:hover {
    background-color: #45a049;
  }
  
  .feedback {
    margin-top: 15px;
    padding: 10px;
    border-radius: 4px;
  }
  
  .correct {
    background-color: #dff0d8;
    color: #3c763d;
  }
  
  .incorrect {
    background-color: #f2dede;
    color: #a94442;
  }
  </style>