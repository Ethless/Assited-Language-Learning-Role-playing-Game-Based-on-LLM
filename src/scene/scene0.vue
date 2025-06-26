<template>
  <div class="scene0">
    <!-- ✅ 白色遮罩 -->
    <div class="dialog-overlay-top"></div>

    <!-- 背景图层 -->
    <Background scene="scene0" />

    <!-- 故事生成 -->
    <StoryProvider
      background="你是喜多川百音子，时隔多年又来到家里的储物间，看着房间里的物品，回忆着时候妈妈教你画画的时候的情景。储物间里有一幅闪烁着微弱的蓝光的画，画上写着“1972年 老家庭院”，画面上是一处院子，澄澈的水面下是游动的鱼儿，其中一条金鱼的眼睛跳动着蓝光，似乎在与你对视。"
      ending="我手指不自觉地想要触摸画上的金鱼，在手指触碰到画的同时，胸前的勾玉竟慢慢地飘起来，紧接着一道闪亮的白光在我面前绽开，我一下子失去了意识。"
      scene="在家里的储物间，里面堆满杂物，灰尘很重"
      @ready="onStoryReady"
    />

    <!-- ✅ 对话框组件 -->
    <DialogBoxfull
      v-if="showDialogBox && useFullDialog"
      :character="dialog.character"
      :text="dialog.text"
      @click="handleDialogClick"
    />
    <DialogBox
      v-else-if="showDialogBox"
      :character="dialog.character"
      :text="dialog.text"
      @click="handleDialogClick"
    />

    <!-- ✅ 场景切换按钮 -->
    <SceneSwitcher @changeScene="onChangeScene" :buttons="sceneButtons" />

    <!-- ✅ 点击层 -->
    <div class="click-layer" @click="handleDialogClick"></div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

import Background from '/src/components/Background.vue'
import DialogBox from '/src/components/DialogBox.vue'
import DialogBoxfull from '/src/components/DialogBox_fullscreen.vue'
import SceneSwitcher from './SceneSwitcher.vue'
import StoryProvider from '/src/components/StoryProvider.vue'

const emit = defineEmits(['changeScene'])

const sceneButtons = [
  { name: 'scene1', label: '画室' },
  { name: 'scene2', label: '庭院' },
  { name: 'scene3', label: '外婆的和服店' },
  { name: 'scene4', label: '集市街头' },
  { name: 'scene5', label: '河边草地' }
  
]

// ✅ 对话控制逻辑
const dialog = ref({ character: '', text: '' })
const dialogs = ref([])
const currentIndex = ref(0)
const showDialogBox = ref(true)
const useFullDialog = ref(false)

function onStoryReady(generatedDialogs) {
  dialogs.value = generatedDialogs
  currentIndex.value = 0
  dialog.value = dialogs.value[0] || { character: '系统', text: '剧情为空' }
  showDialogBox.value = true
  useFullDialog.value = false
}

function handleDialogClick() {
  if (currentIndex.value < dialogs.value.length - 1) {
    currentIndex.value++
    dialog.value = dialogs.value[currentIndex.value]
  } else if (showDialogBox.value) {
    showDialogBox.value = false
  } else {
    console.log('剧情已结束且对话框隐藏')
  }
}

function onChangeScene(newScene) {
  emit('changeScene', newScene)
}
</script>

<style scoped>
.scene0 {
  position: relative;
  width: 100%;
  height: 100vh;
  overflow: hidden;
}

/* ✅ 白色遮罩 */
.dialog-overlay-top {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: calc(100vh - 175px);
  background-color: rgba(255, 255, 255, 0.2);
  pointer-events: none;
  z-index: 10;
}

/* ✅ 点击层 */
.click-layer {
  position: fixed;
  top: 75%;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 100;
  background: transparent;
  cursor: pointer;
}
</style>
