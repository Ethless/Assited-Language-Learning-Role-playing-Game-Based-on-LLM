<template>
  <div class="scene5">
    <!-- 只负责发出事件通知，不直接操作 currentView -->
    <SceneSwitcher @changeScene="onChangeScene":buttons="sceneButtons" />
    <Background scene="scene5" />

    <!-- 故事生成 -->
    <StoryProvider
      background="喜多川百音子，年幼时的你，日本经济蓬勃发展，你正坐在河边的草地上。
      河边长满了绿油油的水草，偶尔有几只蜻蜓飞舞。河水在阳光下闪闪发光，河边还有一些小朋友在玩耍，
      有的在捉小鱼，有的在扔石头打水漂"
      ending="玩累了，你感觉有些无聊，想找些有趣的事做"
      scene="河边草地"
      @ready="onStoryReady"
    />

    <!-- ✅ 对话框，根据是否全屏切换显示不同组件 -->
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

    <!-- 场景切换按钮 -->
    <SceneSwitcher
      ref="sceneSwitcherRef"
      @sceneSwitchIntent="onSceneSwitchIntent"
      @changeScene="onChangeScene"
      :buttons="sceneButtons"
    />

    <GuesswordExtended
      v-if="isGuesswordExtendedVisible"
      :options="currentActionJpOptions"
      :jpName="currentJpName"
      @guess="onExtendedGuess"
    />

    <Guessword
      v-if="isGuesswordVisible"
      :options="currentOptionsZh"
      :correctIndex="correctIndex"
      :jpName="currentJpName"
      :itemId="currentItemId"
      @close="onGuessClose" 
      @guess="onGuess"
    />

    <!-- ✅ 道具组件，监听点击事件 -->
    <Item
      ref="itemRef"
      :positions="itemPositions"
      @itemClicked="onItemClicked"
      @cleared="onCleared"
    />

    <!-- ✅ 添加笔记本按钮组件 -->
    <Notebook :guessedCorrect="guessedCorrect" />

    <!-- ✅ 添加完形填空按钮组件 -->
    <ClozeGenerator /> 

    <!-- 点击区域 -->
    <div
    class="click-layer" 
    @click="handleDialogClick">
  </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

import Background from '/src/components/Background.vue'
import DialogBox from '/src/components/DialogBox.vue'
import DialogBoxfull from '/src/components/DialogBox_fullscreen.vue'
import SceneSwitcher from './SceneSwitcher.vue'
import StoryProvider from '/src/components/StoryProvider.vue'
import Item from '/src/components/Item.vue'
import Notebook from '/src/components/Notebook.vue' // ✅ 引入笔记本组件
import ClozeGenerator from '/src/components/ClozeGenerator.vue'
import Guessword from '/src/game/Guessword.vue'
import GuesswordExtended from '/src/game/GuesswordExtended.vue'
import itemsData from '/src/assets/selection.json'

const sceneButtons = [
  { name: 'scene1', label: '画室' },
  { name: 'scene3', label: '外婆的和服店' },
  { name: 'scene4', label: '集市街头' },
  { name: 'scene2', label: '庭院' } // ✅ 添加当前场景按钮
]

// 对话控制逻辑
const emit = defineEmits(['changeScene'])
const dialog = ref({ character: '', text: '' })
const dialogs = ref([])
const currentIndex = ref(0)
const showDialogBox = ref(true)
const useFullDialog = ref(false) // ✅ 是否使用全屏对话框
const isGuesswordVisible = ref(false)
const triggeredFromItem = ref(false) // 只有点击了放大图物品才设为 true
const itemRef = ref(null)
const sceneSwitcherRef = ref(null)
const isGuesswordExtendedVisible = ref(false)
const currentItemId = ref(null)
const currentJpName = ref('')
const guessedOption = ref(null)
const guessedCorrect = ref(null)

const currentOptionsZh = computed(() => {
  console.log('传入的名字是：', currentItemId.value)
  const item = itemsData.find(i => i.id === Number(currentItemId.value))  // ✅ 类型匹配
  console.log('传入的道具是：', item)
  
  if (!item || !item.options) return []
  return item.options.map(opt => opt.zh)
})

const currentActionJpOptions = computed(() => {
  const item = itemsData.find(i => i.id === Number(currentItemId.value))
  if (!item || !item.actions) return []
  return item.actions.map(action => action.jp)
})

const correctIndex = computed(() => {
  const item = itemsData.find(i => i.id === Number(currentItemId.value))
  return item?.correct_num ?? -1
})

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

function handleDialogClick() {
  itemRef.value?.clearClickedImage()
  sceneSwitcherRef.value?.hideOptions?.()

  if (currentIndex.value < dialogs.value.length - 1) {
    currentIndex.value++
    dialog.value = dialogs.value[currentIndex.value]
    useFullDialog.value = false
  } else if (showDialogBox.value) {
    showDialogBox.value = false

    // ✅ 仅在来自物品放大图点击、并且被清除后触发猜词
    if (itemRef.value?.wasCleared && triggeredFromItem.value) {
      console.log('对话框关闭，触发猜词')
      isGuesswordVisible.value = true
      itemRef.value.wasCleared = false
      triggeredFromItem.value = false // ✅ 重置标志
    }
  } else {
    console.log('剧情已结束且对话框隐藏')
  }
}

function onGuess(payload) {
  // payload 现在是 { option: '狗', isCorrect: 1 }
  console.log('猜测选项：', payload.option)
  console.log('是否正确（1是0否）：', payload.isCorrect)

  guessedOption.value = payload.option
  guessedCorrect.value = payload.isCorrect  // 你需要定义 guessedCorrect 响应式变量

  // 这里可以做进一步逻辑，比如控制 UI 或记录答题情况
}

function onGuessClose() {
  isGuesswordVisible.value = false
  isGuesswordExtendedVisible.value = true
  // 可以这里判断 guessedOption.value 是否正确，做额外逻辑
}

function onItemClicked(payload) {
  dialog.value = payload
  useFullDialog.value = true
  showDialogBox.value = true
  triggeredFromItem.value = true

  currentItemId.value = payload.itemId
  currentJpName.value = payload.jpName
}


function onExtendedGuess(option) {
  console.log('第二组选项结果：', option)
  isGuesswordExtendedVisible.value = false
  // 如果你还想触发对话或剧情，可以在这里添加逻辑
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
  z-index: 100;
  background: transparent;
  cursor: pointer;
}
</style>