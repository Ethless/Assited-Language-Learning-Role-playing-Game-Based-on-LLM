<template>
  <div class="scene1">
    <!-- 只负责发出事件通知，不直接操作 currentView -->
    <SceneSwitcher @changeScene="onChangeScene":buttons="sceneButtons" />
    <Background scene="scene1" />

    <!-- 对话框组件，显示当前角色的台词 -->
    <DialogBox
      :character="dialog.character"
      :text="dialog.text"
      @next="nextDialog"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
// import api from "@/api";
import Background from '/src/components/Background.vue'
import DialogBox from '/src/components/DialogBox.vue'
import SceneSwitcher from './SceneSwitcher.vue'

// 对话数据，可以根据需要改成从 props 或 store 获取
const dialogs = [
  { character: '小明', text: '这里是我们的冒险开始的地方。' },
  { character: '小红', text: '准备好了吗？前面充满未知。' },
  { character: '小明', text: '走吧！' }
]

const sceneButtons = [
  { name: 'scene1', label: '暂时不离开' },
  { name: 'scene2', label: '庭院' },
  { name: 'scene3', label: '外婆的和服店' },
  // 这里可以只列出这几个，或者更少，灵活配置
]

const currentIndex = ref(0)
const dialog = ref(dialogs[currentIndex.value])

// 点击“下一句”按钮时调用
const nextDialog = () => {
  if (currentIndex.value < dialogs.length - 1) {
    currentIndex.value++
    dialog.value = dialogs[currentIndex.value]
  } else {
    // 对话结束后的操作，例如进入下一个场景
    console.log('对话结束，可以切换场景')
  }
}

// 触发父组件事件
function onChangeScene(newScene) {
  // 这里把事件发给父组件
  // script setup 默认提供了 emit 方法，要先导入
  emit('changeScene', newScene)
}

const emit = defineEmits(['changeScene'])
</script>

<style scoped>
.scene1 {
  position: relative;
  width: 100%;
  height: 100%;
}
</style>
