<template>
  <div class="viewport-wrapper">
    <div class="app-container">
      <!-- 你的内容 -->
      <Background :scene="currentView" />
      <StartScreen v-if="currentView === 'start'" @start="startGame" />
      <Scene0 v-else-if="currentView === 'scene0'" @changeScene="changeScene" />
      <Scene1 v-else-if="currentView === 'scene1'" @changeScene="changeScene" />
      <Scene2 v-else-if="currentView === 'scene2'" @changeScene="changeScene" />
      <Scene3 v-else-if="currentView === 'scene3'" @changeScene="changeScene" />
      <div v-else>
        <Notebook />
        <Items />
        <NPC />
        <SaveExitButton @exit="exitToStart" />
      </div>

      <!-- 黑幕过渡层 -->
      <div class="fade-screen" :class="{ 'fade-in': isFading }"></div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Background from './components/Background.vue'
import StartScreen from './components/StartScreen.vue'
import Notebook from './components/Notebook.vue'
import Items from './components/Item.vue'
import NPC from './components/NPC.vue'
import SaveExitButton from './components/SaveExitButton.vue'
import Scene0 from './scene/scene0.vue'
import Scene1 from './scene/scene1.vue'
import Scene2 from './scene/scene2.vue'
import Scene3 from './scene/scene3.vue'

const currentView = ref('start')
const isFading = ref(false) // 控制黑幕状态

const startGame = () => {
  fadeToScene('scene0')
}

function changeScene(newScene) {
  fadeToScene(newScene)
}

const exitToStart = () => {
  fadeToScene('start')
}

// 封装一个切换场景带黑幕渐入渐出函数
function fadeToScene(targetScene) {
  isFading.value = true  // 先显示黑幕
  setTimeout(() => {
    currentView.value = targetScene // 切换背景或场景
    setTimeout(() => {
      isFading.value = false // 关闭黑幕，显示场景
    }, 500) // 500ms 渐出动画时间，与CSS动画保持一致
  }, 500) // 500ms 渐入动画时间
}
</script>

<style scoped>
.viewport-wrapper {
  width: 100vw;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
}

.app-container {
  width: 1920px;
  height: 1080px;
  position: relative;
  overflow: hidden;
}

/* 黑幕遮罩层 */
.fade-screen {
  position: fixed; /* 固定全屏 */
  top: 0; left: 0;
  width: 100vw;
  height: 100vh;
  background-color: black;
  opacity: 0;
  pointer-events: none; /* 不阻挡点击 */
  transition: opacity 0.5s ease;
  z-index: 9999; /* 确保在最上层 */
}

/* 触发渐入时 */
.fade-in {
  opacity: 1;
  pointer-events: auto; /* 阻止点击事件穿透 */
}
</style>
