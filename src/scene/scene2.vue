<template>
  <div class="scene2">
    <!-- 只负责发出事件通知，不直接操作 currentView -->
    <SceneSwitcher @changeScene="onChangeScene":buttons="sceneButtons" />
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

    <!-- 对话框 -->
    <DialogBox
      :character="dialog.character"
      :text="dialog.text"
    />

        <Item 
      :positions="itemPositions" 
      @click="startGame" 
    />

    <GuessWordGame 
      v-if="showGame"
      @game-ended="handleGameEnded"
    />

    <!-- 可点击区域：覆盖整个中间画面 -->
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

const emit = defineEmits(['changeScene'])

const sceneButtons = [
  { name: 'scene1', label: '画室' },
  { name: 'scene3', label: '外婆的和服店' },
  // 这里可以只列出这几个，或者更少，灵活配置
]

const dialog = ref({ character: '', text: '' })
const dialogs = ref([])
const currentIndex = ref(0)

// 定义道具位置，由父组件控制
const itemPositions = ref([
  { top: '60%', left: '500px' },
])



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
.scene2 {
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