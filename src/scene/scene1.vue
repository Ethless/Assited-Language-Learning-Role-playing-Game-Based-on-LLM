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

    <!-- 道具组件，显示在对话框之外 -->
     <!-- 监听道具点击事件 -->
    <Item 
      :positions="itemPositions" 
    />
    <!-- 对话框组件，初始时隐藏 -->
    <DialogBox
      v-if="showDialogBox"
      :character="dialog.character"
      :text="dialog.text"
      @next="nextDialog"
    />
    <ItemInteraction
      v-for="(item, index) in items"
      :key="item.id"
      :item="item"
      :position="itemPositions[index]"
    />

    <GuessWordGame 
      v-if="showGame"
      @game-ended="handleGameEnded"
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
import Item from '/src/components/items.vue' // 引入道具组件
import ItemInteraction from '/src/components/ItemInteraction.vue'
//使用之前定义的道具数据
import { allItems } from '/src/assets/data/items.js'; // 假设你将道具数据存储在 /src/data/items.js 中
const emit = defineEmits(['changeScene'])

const sceneButtons = [
  { name: 'scene2', label: '庭院' },
  { name: 'scene3', label: '外婆的和服店' },
  // 这里可以只列出这几个，或者更少，灵活配置
]
const items = ref(allItems);

// 定义道具位置，由父组件控制
const itemPositions = ref([
  { top: '55%', left: '1100px' },
])

const dialog = ref({ character: '', text: '' })
const dialogs = ref([])
const currentIndex = ref(0)

function handleItemClicked(item) {
  console.log('道具被点击:', item)
  // 在这里可以添加其他逻辑，比如启动游戏
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
.scene1 {
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
