<template>
  <div class="scene1">
    <!-- 只负责发出事件通知，不直接操作 currentView -->
    <SceneSwitcher @changeScene="onChangeScene" :buttons="sceneButtons" />
    <Background scene="scene1" />

    <!-- 故事生成 -->
    <StoryProvider
      background="你是喜多川百音子，现在在年幼的时候。1970年左右，日本经济发展很好，
      你每天上完课都要在校外的画室练习画画。你画的是水彩，坐在凳子上画，今天的画马上画完了"
      ending="我完成了今天的练习，在画室里面找找有没有好玩的物品"
      scene="在家外的老师开的画室，环境内并没有很显眼的物品"
      @ready="onStoryReady"
    />

    <!-- 对话框组件，显示当前角色的台词 -->
    <DialogBox
      :character="dialog.character"
      :text="dialog.text"
      @next="nextDialog"
    />

    <!-- 对话框组件，初始时隐藏 -->
    <DialogBox
      v-if="showDialogBox"
      :character="dialog.character"
      :text="dialog.text"
      @next="nextDialog"
    />
    <div class="click-layer" @click="nextDialog"></div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
// import api from "@/api";
import Background from '/src/components/Background.vue'
import DialogBox from '/src/components/DialogBox.vue'
import SceneSwitcher from './SceneSwitcher.vue'
import StoryProvider from '/src/components/StoryProvider.vue'
// import Item from '/src/components/Items.vue' // 引入道具组件

const emit = defineEmits(['changeScene'])

const sceneButtons = [
  { name: 'scene2', label: '庭院' },
  { name: 'scene3', label: '外婆的和服店' },
  // 这里可以只列出这几个，或者更少，灵活配置
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
.scene1 {
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
