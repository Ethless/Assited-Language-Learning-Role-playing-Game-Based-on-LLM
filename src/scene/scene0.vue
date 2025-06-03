<template>
  <div class="scene0">
    <!-- 场景切换按钮 -->
    <SceneSwitcher @changeScene="onChangeScene" :buttons="sceneButtons" />

    <!-- 背景图层 -->
    <Background scene="scene0" />

    <!-- 故事生成 -->
    <StoryProvider
      background="你是喜多川百音子，现在1964年，你刚出生没多久，当时日本经济发展很快，
      出生前父亲升职了，家里也在东京世田谷区(富人区)买了新房子"
      ending="画画太闷了，我想出门走走，该去哪里呢"
      scene="在家中房间，被父母叮嘱没有画完画就不许出门"
      @ready="onStoryReady"
    />

    <!-- 对话框 -->
    <DialogBox
      :character="dialog.character"
      :text="dialog.text"
    />

    <!-- 可点击区域：覆盖整个中间画面 -->
    <div class="click-layer" @click="nextDialog"></div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '@/api'
import Background from '/src/components/Background.vue'
import DialogBox from '/src/components/DialogBox.vue'
import SceneSwitcher from './SceneSwitcher.vue'
import StoryProvider from '/src/components/StoryProvider.vue'

const emit = defineEmits(['changeScene'])

const sceneButtons = [
  { name: 'scene1', label: '画室' },
  { name: 'scene2', label: '庭院' },
  { name: 'scene3', label: '外婆的和服店' }
]

const dialog = ref({ character: '', text: '' })
const dialogs = ref([])
const currentIndex = ref(0)

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
.scene0 {
  position: relative;
  width: 100%;
  height: 100vh;
  overflow: hidden;
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
