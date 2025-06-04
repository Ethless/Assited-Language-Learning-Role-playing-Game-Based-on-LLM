<template>
  <div class="scene2">
    <!-- 场景切换按钮 -->
    <SceneSwitcher
      @sceneSwitchIntent="onSceneSwitchIntent"
      @changeScene="onChangeScene"
      :buttons="sceneButtons"
    />
    <Background scene="scene2" />

    <!-- 故事生成 -->
    <StoryProvider
      background="你是喜多川百音子，现在在年幼刚出生没多久的时候。当时日本经济发展很快，
      你在家中的庭院中玩耍，记不清池塘里隐隐约约是不是有一只蓝眼金鱼，你当时还不会画画，
      但是想把它画下来"
      ending="你凑近去看那只金鱼，看了一会就去找别的东西玩了"
      scene="在乡下家中庭院，庭院里有池塘，池塘水很清澈"
      @ready="onStoryReady"
    />

    <!-- ✅ 对话框，根据是否全屏切换显示不同组件 -->
    <DialogBoxfull
      v-if="showDialogBox && useFullDialog"
      :character="dialog.character"
      :text="dialog.text"
    />
    <DialogBox
      v-else-if="showDialogBox"
      :character="dialog.character"
      :text="dialog.text"
    />

    <!-- ✅ 道具组件，监听点击事件 -->
    <Item :positions="itemPositions" @itemClicked="onItemClicked" />

    <!-- 猜词游戏 -->
    <GuessWordGame v-if="showGame" @game-ended="handleGameEnded" />

    <!-- 点击区域 -->
    <div class="click-layer" @click="nextDialog"></div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

import Background from '/src/components/Background.vue'
import DialogBox from '/src/components/DialogBox.vue'
import DialogBoxfull from '/src/components/DialogBox_fullscreen.vue'
import SceneSwitcher from './SceneSwitcher.vue'
import StoryProvider from '/src/components/StoryProvider.vue'
import Item from '/src/components/Item.vue'
// import GuessWordGame from '/src/components/GuessWordGame.vue'

const emit = defineEmits(['changeScene'])

const sceneButtons = [
  { name: 'scene1', label: '画室' },
  { name: 'scene3', label: '外婆的和服店' },
]

// 对话控制逻辑
const dialog = ref({ character: '', text: '' })
const dialogs = ref([])
const currentIndex = ref(0)
const showDialogBox = ref(true)
const useFullDialog = ref(false) // ✅ 是否使用全屏对话框

// ✅ 道具位置数组
const itemPositions = ref([
  { top: '65%', left: '500px' },
  { top: '80%', left: '300px' },
  { top: '70%', left: '100px' },
  { top: '80%', left: '700px' },
])

// ✅ StoryProvider 回调
function onStoryReady(generatedDialogs) {
  dialogs.value = generatedDialogs
  currentIndex.value = 0
  dialog.value = dialogs.value[0] || { character: '系统', text: '剧情为空' }
  showDialogBox.value = true
  useFullDialog.value = false // 剧情使用普通对话框
}

// ✅ 点击继续剧情或关闭对话框
function nextDialog() {
  if (currentIndex.value < dialogs.value.length - 1) {
    currentIndex.value++
    dialog.value = dialogs.value[currentIndex.value]
    useFullDialog.value = false // 剧情使用普通对话框
  } else if (showDialogBox.value) {
    showDialogBox.value = false
  } else {
    console.log('剧情已结束且对话框隐藏')
  }
}

// ✅ 道具点击使用全屏对话框
function onItemClicked(payload) {
  dialog.value = payload
  useFullDialog.value = true
  showDialogBox.value = true
}

// ✅ 场景切换 intent 显示系统提示对话框（全屏）
function onSceneSwitchIntent() {
  dialog.value = {
    character: '系统',
    text: '你想去哪个场景？'
  }
  useFullDialog.value = true
  showDialogBox.value = true
}

// 场景切换
function onChangeScene(newScene) {
  emit('changeScene', newScene)
}
</script>

<style scoped>
.scene2 {
  position: relative;
  width: 100%;
  height: 100vh;
  overflow: hidden;
}

/* ✅ 确保道具组件显示正常 */
:deep(.items) {
  position: absolute;
  width: 100%;
  height: 100%;
  pointer-events: auto;
}

:deep(.item-image) {
  position: absolute;
  width: 100px;
  height: auto;
  z-index: 10;
}

/* 点击层样式 */
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
