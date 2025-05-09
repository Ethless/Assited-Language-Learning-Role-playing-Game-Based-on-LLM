<template>
  <!-- 开始界面 -->
  <div v-if="!gameStarted" class="start-screen">
    <h1>视觉冒险游戏</h1>
    <button @click="startGame">开始游戏</button>
  </div>

  <!-- 游戏界面 -->
  <div v-else class="game-container">
    <button class="back-button" @click="returnToStart">返回主页</button>
    <GameCanvas @tool-selected="showToolFeedback" />
    
    <div v-if="currentFeedback" class="feedback-box">
      {{ currentFeedback }}
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import GameCanvas from './components/GameCanvas.vue'

const gameStarted = ref(false)
const currentFeedback = ref('')

const startGame = () => {
  gameStarted.value = true
  currentFeedback.value = ''
}

const returnToStart = () => {
  gameStarted.value = false
}

const showToolFeedback = (toolName) => {
  const feedbackMap = {
    'sword': '⚔️ 你选择了剑：攻击力+10',
    'potion': '🧪 喝下药水：生命值恢复50点',
    'key': '🔑 获得钥匙：可以打开宝箱'
  }
  currentFeedback.value = feedbackMap[toolName] || '❓ 未知工具'
}
</script>

<style>
body {
  margin: 0;
  background: #0a192f;
  min-height: 100vh;
  font-family: 'Arial', sans-serif;
}
</style>

<style scoped>
.start-screen {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
  color: #ccd6f6;
}

.start-screen h1 {
  font-size: 3rem;
  margin-bottom: 2rem;
  text-shadow: 0 0 10px rgba(100, 255, 218, 0.5);
}

.start-screen button {
  padding: 12px 24px;
  font-size: 1.2rem;
  background: transparent;
  color: #64ffda;
  border: 1px solid #64ffda;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.start-screen button:hover {
  background: rgba(100, 255, 218, 0.1);
  transform: translateY(-3px);
}

.game-container {
  position: relative;
  height: 100vh;
}

.back-button {
  position: fixed;
  top: 20px;
  right: 20px;
  padding: 8px 16px;
  background: rgba(255, 71, 87, 0.2);
  color: #ff4757;
  border: 1px solid #ff4757;
  border-radius: 4px;
  cursor: pointer;
  z-index: 100;
  transition: all 0.3s;
}

.back-button:hover {
  background: rgba(255, 71, 87, 0.4);
}

.feedback-box {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(10, 25, 47, 0.9);
  color: #64ffda;
  padding: 15px 30px;
  border-radius: 8px;
  border: 1px solid #64ffda;
  max-width: 80%;
  text-align: center;
  font-family: monospace;
  box-shadow: 0 0 15px rgba(100, 255, 218, 0.3);
}
</style>