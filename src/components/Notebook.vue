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

      <div class="notebook-tabs">
        <button @click="setCategory('vocabulary')">词汇</button>
        <button @click="setCategory('events')">事件</button>
        <button @click="setCategory('characters')">人物</button>
      </div>

      <div class="notebook-grid">
        <div
          v-for="(item, index) in displayedData"
          :key="item.id || index"
          class="notebook-cell"
          :class="{ incorrect: item.correct_judge === 0 }"
          @mouseover="hoveredIndex = index"
          @mouseleave="hoveredIndex = null"
        >
          {{ item.jp }}（{{ item.zh }}）

          <img
            v-if="hoveredIndex === index"
            :src="bubbleImg"
            class="hover-bubble"
            alt="提示"
          />

          <!-- 新增：对应 name 图片，显示在气泡上 -->
          <img
            v-if="hoveredIndex === index"
            :src="getItemImg(item.name)"
            class="hover-item-img"
            alt="道具图片"
          />
        </div>
      </div>

      <div class="notebook-pagination">
        <button @click="prevPage" :disabled="currentPage === 1"><</button>
        <span class="pagination-info">{{ currentPage }} / {{ totalPages }}</span>
        <button @click="nextPage" :disabled="currentPage === totalPages">></button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import notebookIcon from '@/assets/notebook-icon.svg'
import bubbleImg from '@/assets/notebook/bubble.svg'

const showNote = ref(false)
const currentCategory = ref('vocabulary')
const currentPage = ref(1)
const pageSize = 20

const hoveredIndex = ref(null)

const displayedData = ref([])

const notes = {
  vocabulary: [],
  events: [],
  characters: []
}

const notebookOpenMap = {
  vocabulary: new URL('@/assets/notebook/notebook-open-vocabulary.svg', import.meta.url).href,
  events: new URL('@/assets/notebook/notebook-open-events.svg', import.meta.url).href,
  characters: new URL('@/assets/notebook/notebook-open-characters.svg', import.meta.url).href
}

const notebookOpen = computed(() => notebookOpenMap[currentCategory.value])

const totalPages = computed(() => {
  const data = notes[currentCategory.value] || []
  return Math.ceil(data.length / pageSize)
})

function updateDisplayedData() {
  const data = notes[currentCategory.value] || []
  const start = (currentPage.value - 1) * pageSize
  displayedData.value = data.slice(start, start + pageSize)
}

function nextPage() {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
    updateDisplayedData()
  }
}

function prevPage() {
  if (currentPage.value > 1) {
    currentPage.value--
    updateDisplayedData()
  }
}

// 打印当前分类数据中所有 name 字段
function printAllNames() {
  const data = notes[currentCategory.value] || []
  data.forEach(item => {
    console.log('name:', item.name)
  })
}

async function loadCategory(category, forceReload = false) {
  if (!forceReload && notes[category]?.length > 0) return

  try {
    const res = await fetch(`/note/${category}.json?_=${Date.now()}`)
    const json = await res.json()
    notes[category] = json
  } catch (err) {
    console.error(`加载 ${category} 失败：`, err)
    notes[category] = []
  }

  if (category === currentCategory.value) {
    updateDisplayedData()
    printAllNames()  // <--- 这里加打印
  }
}

function setCategory(category) {
  currentCategory.value = category
  currentPage.value = 1
  loadCategory(category, true)
}

function toggleNote() {
  showNote.value = !showNote.value
  if (showNote.value) {
    currentPage.value = 1
    loadCategory(currentCategory.value, true)
  }
}

function getItemImg(name) {
  // 这里的name是原始name，例如 "lint roller"
  // 直接用 encodeURIComponent 编码整个文件名，空格转%20
  const encodedFileName = encodeURIComponent(name + ".png");
  // console.log(encodedFileName)
  return new URL(`../assets/Items/${encodedFileName}`, import.meta.url).href;
}

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
  transition: opacity 0.3s ease;
}

.notebook-tabs {
  position: absolute;
  bottom: 60px;
  left: 305px;
  z-index: 3;
  display: flex;
  gap: 32px;
}
.notebook-tabs button {
  padding: 25px 22px;
  font-size: 16px;
  font-family: 'Source Han Serif SC', serif;
  background-color: transparent;
  border: 1px solid transparent;
  border-radius: 6px;
  cursor: pointer;
  text-indent: -9999px;
}
.notebook-tabs button:hover {
  background-color: transparent;
}

.notebook-grid {
  position: absolute;
  z-index: 2;
  top: 90px;
  left: 52%;
  transform: translateX(-50%);
  width: 75%;
  max-width: 1000px;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-template-rows: repeat(5, auto);
  gap: 30px;
  padding: 20px;
  font-size: 16px;
  color: #333;
  text-align: left;
  font-family: 'Source Han Serif SC', serif;
  background-color: transparent;
  pointer-events: auto;
}

.notebook-cell {
  background-color: transparent;
  padding: 12px;
  border-radius: 8px;
  box-shadow: 0 2px 6px transparent;
  text-align: left;
  position: relative;
}

.notebook-cell.incorrect {
  text-decoration: underline wavy rgb(204, 0, 0);
  text-underline-offset: 4px;
}

.hover-bubble {
  position: absolute;
  top: -40%;
  right: 30px;
  transform: translateY(-50%);
  width: 150px;
  height: 150px;
  pointer-events: none;
  z-index: 5;
}

.notebook-pagination {
  position: absolute;
  bottom: 160px;
  left: 52%;
  transform: translateX(-50%);
  z-index: 3;
  display: flex;
  gap: 2px;
  align-items: center;
  font-family: 'Source Han Serif SC', serif;
}

.notebook-pagination button {
  padding: 10px 10px;
  font-size: 14px;
  border: 1px solid transparent;
  border-radius: 4px;
  background-color: transparent;
  cursor: pointer;
}
.notebook-pagination button:disabled {
  opacity: 0.5;
  cursor: default;
}
.pagination-info {
  color: #000000;
  font-weight: bold;
}

.hover-bubble {
  position: absolute;
  top: -40%;
  right: 30px;
  transform: translateY(-50%);
  width: 150px;
  height: 150px;
  pointer-events: none;
  z-index: 5;
}

/* 新增：道具图片显示在气泡中间，叠加位置可根据需要调整 */
.hover-item-img {
  position: absolute;
  top: -90%;
  right: 80px; /* 调整位置使其在气泡中心 */
  width: 45px;
  height: 45px;
  object-fit: contain;
  pointer-events: none;
  z-index: 6;
}
</style>
