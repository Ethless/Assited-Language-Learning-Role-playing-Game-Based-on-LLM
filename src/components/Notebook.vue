<template>
  <div class="notebook-button-wrapper">
    <img
      :src="notebookIcon"
      class="notebook-icon"
      alt="查看笔记"
      @click="toggleNote"
    />

    <div v-if="showNote" class="notebook-overlay" @click.self="toggleNote">
      <img :src="notebookOpen" class="notebook-image" alt="打开的笔记本" />

      <!-- ✅ 分类按钮 -->
      <div class="notebook-tabs">
        <button @click="setCategory('vocabulary')">词汇</button>
        <button @click="setCategory('events')">事件</button>
        <button @click="setCategory('characters')">人物</button>
      </div>

      <!-- ✅ 显示当前分类文本 -->
      <div class="notebook-text">{{ noteText }}</div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import notebookIcon from '@/assets/notebook-icon.svg'
import notebookOpen from '@/assets/notebook-open.svg'

const showNote = ref(false)
const currentCategory = ref('vocabulary')
const noteText = ref('（加载中...）')

// 所有笔记内容，初始为空
const notes = {
  vocabulary: '',
  events: '',
  characters: ''
}

// 通用的 txt 加载函数
async function loadCategory(category) {
  try {
    const res = await fetch(`/note/${category}.txt`)
    if (!res.ok) throw new Error('加载失败')
    const text = await res.text()
    notes[category] = text
    if (currentCategory.value === category) {
      noteText.value = text
    }
  } catch (err) {
    notes[category] = `（${category} 笔记加载失败）`
    if (currentCategory.value === category) {
      noteText.value = notes[category]
    }
  }
}

// 切换分类按钮
function setCategory(category) {
  currentCategory.value = category
  if (notes[category]) {
    noteText.value = notes[category]
  } else {
    noteText.value = '（加载中...）'
    loadCategory(category)
  }
}

// 显示或隐藏笔记本
function toggleNote() {
  showNote.value = !showNote.value
  if (showNote.value) {
    setCategory(currentCategory.value)
  }
}

// 初始加载 vocabulary
onMounted(() => {
  loadCategory('vocabulary')
})
</script>

<style scoped>
.notebook-button-wrapper {
  position: fixed;
  top: 5px;
  right: 0px;
  z-index: 1000;
}

.notebook-icon {
  width: 150px;
  cursor: pointer;
  transition: transform 0.2s ease;
}
.notebook-icon:hover {
  transform: scale(1.05);
}

.notebook-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(138, 138, 138, 0.439);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}

.notebook-image {
  position: absolute;
  width: 100vw;
  height: 100vh;
  top: -40px;
  left: 0;
  object-fit: cover;
  pointer-events: none;
  z-index: 1;
}

.notebook-text {
  position: absolute;
  z-index: 2;
  top: 70px;
  left: 50%;
  transform: translateX(-50%);
  width: 60%;
  padding: 20px;
  font-size: 20px;
  color: #333;
  white-space: pre-line;
  font-family: 'Source Han Serif SC', serif;
  background-color: transparent;
  border-radius: 12px;
}

.notebook-tabs {
  position: absolute;
  bottom: 60px;
  left: 40px;
  z-index: 3;
  display: flex;
  gap: 12px;
}

.notebook-tabs button {
  padding: 8px 14px;
  font-size: 16px;
  font-family: 'Source Han Serif SC', serif;
  background-color: #f8f8f8;
  border: 1px solid #888;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}
.notebook-tabs button:hover {
  background-color: #e0e0e0;
}
</style>
