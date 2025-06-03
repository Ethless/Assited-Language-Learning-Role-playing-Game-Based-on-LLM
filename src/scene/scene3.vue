<template>
  <div class="scene3">
    <!-- 只负责发出事件通知，不直接操作 currentView -->
    <SceneSwitcher @changeScene="onChangeScene":buttons="sceneButtons" />
    <Background scene="scene3" />

    <!-- 故事生成 -->
    <StoryProvider
      background="你是喜多川百音子，现在在年幼的时候。日本经济发展很好，
      外婆开了一家和服店，店面不大，但是有很多客人。你今天在外婆开的和服店帮忙看店，
      外婆的和服有很多款式，你非常喜欢"
      ending="你觉得看店有点无聊，想去找点好玩的"
      scene="在外婆在集市里开的和服店，里面挂了很多和服，外婆也在缝新的和服"
      @ready="onStoryReady"
    />

    <!-- 对话框组件，显示当前角色的台词 -->
    <DialogBox
      :character="dialog.character"
      :text="dialog.text"
      @next="nextDialog"
    />

    <!-- 道具组件，显示在对话框之外 -->
    <Item 
      :positions="itemPositions" 
      @click="startGame" 
    />

    <GuessWordGame 
      v-if="showGame"
      @game-ended="handleGameEnded"
    />

    <div class="click-layer" @click="nextDialog"></div>
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
// import api from "@/api";
import Background from '/src/components/Background.vue'
import DialogBox from '/src/components/DialogBox.vue'
import SceneSwitcher from './SceneSwitcher.vue'
import StoryProvider from '/src/components/StoryProvider.vue'
import Item from '/src/components/items.vue' // 引入道具组件
import GuessWordGame from '/src/game/GuessWordGame.vue' // 引入猜词游戏组件

const emit = defineEmits(['changeScene'])

const sceneButtons = [
  { name: 'scene1', label: '画室' },
  { name: 'scene2', label: '庭院' },
  // 这里可以只列出这几个，或者更少，灵活配置
]

// 定义道具位置，由父组件控制
const itemPositions = ref([
  { top: '60%', left: '500px' },
])

const dialog = ref({ character: '', text: '' })
const dialogs = ref([])
const currentIndex = ref(0)

// 控制猜词游戏的显示状态
const showGame = ref(false)

// 开始游戏的函数
const startGame = () => {
  showGame.value = true
  // 可以在这里添加其他游戏初始化逻辑
}

// 处理游戏结束的函数
const handleGameEnded = () => {
  showGame.value = false
  // 可以在这里添加游戏结束后的逻辑
}

function onStoryReady(generatedDialogs) {
  dialogs.value = generatedDialogs
  currentIndex.value = 0
  dialog.value = dialogs.value[0] || { character: '系统', text: '剧情为空' }
}

function nextDialog() {
  if (currentIndex.value < dialogs.value.length - 1) {
    currentIndex.value++
    dialog.value = dialogs.value[currentIndex.value]
  } else {
    console.log('对话结束，可以切换场景')
  }
}

function onChangeScene(newScene) {
  emit('changeScene', newScene)
}
</script>

<style scoped>
.scene3 {
  position: relative;
  width: 100%;
  height: 100vh;
  overflow: hidden;
}

/* 确保道具组件在场景中正确显示 */
:deep(.items) {
  position: absolute;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

:deep(.item-image) {
  position: absolute;
  width: 100px;
  height: 500;
}

/* 点击区域：默认覆盖整个中间区域 */
.click-layer {
  position: fixed;
  top: 75%;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 9999;
  background: transparent;
  cursor: pointer;
  pointer-events: auto;
}
</style>
