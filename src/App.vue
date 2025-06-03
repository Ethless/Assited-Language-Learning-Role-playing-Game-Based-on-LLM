<template>
  <div>
    <!-- 传递当前视图状态作为场景名 -->
    <Background :scene="currentView" />

    <StartScreen v-if="currentView === 'start'" @start="startGame" />
    
    <!-- 第一个场景（Scene0） -->
    <Scene0 
      v-else-if="currentView === 'scene0'" 
      @changeScene="changeScene" 
    />
    <Scene1 
      v-else-if="currentView === 'scene1'" 
      @changeScene="changeScene" 
    />
    <Scene2
      v-else-if="currentView === 'scene2'" 
      @changeScene="changeScene" 
    />
    <Scene3
      v-else-if="currentView === 'scene3'" 
      @changeScene="changeScene" 
    />
    <div v-else>
      <Notebook />
      <Items />
      <NPC />
      <SaveExitButton @exit="exitToStart" />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Background from './components/Background.vue'
import StartScreen from './components/StartScreen.vue'
import Notebook from './components/Notebook.vue'
import Items from './components/Items.vue'
import NPC from './components/NPC.vue'
import SaveExitButton from './components/SaveExitButton.vue'
import Scene0 from './scene/scene0.vue'
import Scene1 from './scene/scene1.vue'
import Scene2 from './scene/scene2.vue'
import Scene3 from './scene/scene3.vue'
import SceneSwitcher from './scene/SceneSwitcher.vue'
import GuessWordGameVue from './components/GuessWordGame.vue'
const currentView = ref('start')

const startGame = () => {
  currentView.value = 'scene0'
}

function changeScene(newScene) {
  currentView.value = newScene
}

const exitToStart = () => {
  currentView.value = 'start'
}
</script>

<style scoped>
.app-container {
  width: 1920px;
  height: 1080px;
  margin: 0 auto;         /* 水平居中 */
  overflow: auto;         /* 内容超出显示滚动条 */
  background-color: #000; /* 根据需要设置背景色 */
  position: relative;
  /* 禁止缩放和滚动可在外层html/body加相关CSS，这里保持简单 */
}
</style>
