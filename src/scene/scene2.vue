<template>
  <div class="scene2">
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
      :jpName="currentJpName"
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
    <Notebook />

    <!-- 点击区域 -->
    <div
    class="click-layer" 
    @click="handleDialogClick">
  </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { computed } from 'vue'

import Background from '/src/components/Background.vue'
import DialogBox from '/src/components/DialogBox.vue'
import DialogBoxfull from '/src/components/DialogBox_fullscreen.vue'
import SceneSwitcher from './SceneSwitcher.vue'
import StoryProvider from '/src/components/StoryProvider.vue'
import Item from '/src/components/Item.vue'
import Notebook from '/src/components/Notebook.vue' // ✅ 引入笔记本组件
import Guessword from '/src/game/Guessword.vue'
import GuesswordExtended from '/src/game/GuesswordExtended.vue'
import itemsData from '/src/assets/selection.json'

const sceneButtons = [
  { name: 'scene1', label: '画室' },
  { name: 'scene3', label: '外婆的和服店' },
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

function onGuess(option) {
  console.log('猜测结果：', option)
  isGuesswordVisible.value = false         // 关闭第一组按钮
  isGuesswordExtendedVisible.value = true  // 显示第二组按钮组件
}

function onItemClicked(payload) {
  dialog.value = payload
  useFullDialog.value = true
  showDialogBox.value = true
  triggeredFromItem.value = true

  currentItemId.value = payload.itemId
  currentJpName.value = payload.jpName  // 这里保存 jpName
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