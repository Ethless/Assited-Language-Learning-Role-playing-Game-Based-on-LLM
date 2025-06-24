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


      <!-- ✅ 正确率，只对 vocabulary 有效 -->
      <div class="correct-rate" v-if="currentCategory.value === 'vocabulary'">
        正确率: {{ correctRate }}%
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

        <!-- 正确率放在分页条右侧 -->
        <div class="correct-rate">正确率: {{ correctRate }}%</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import notebookIcon from '@/assets/notebook-icon.svg'
import bubbleImg from '@/assets/notebook/bubble.png'

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

// ✅ 正确率（只针对 vocabulary）
const correctRate = computed(() => {
  const data = notes.vocabulary || []
  if (data.length === 0) return 0
  const correctCount = data.filter(item => item.correct_judge === 1).length
  return ((correctCount / data.length) * 100).toFixed(2)
})

const notebookOpenMap = {
  vocabulary: new URL('@/assets/notebook/notebook-open-vocabulary.svg', import.meta.url).href,
  events: new URL('@/assets/notebook/notebook-open-events.svg', import.meta.url).href,
  characters: new URL('@/assets/notebook/notebook-open-characters.svg', import.meta.url).href
}

const notebookOpen = computed(() => notebookOpenMap[currentCategory.value])

const totalPages = computed(() => {
  const data = notes[currentCategory.value] || []
  return Math.ceil(data.length / pageSize) || 1
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

function printAllNames() {
  const data = notes[currentCategory.value] || []
  data.forEach(item => {
    console.log('name:', item.name)
  })
}

async function loadCategory(category, forceReload = false) {
  if (!forceReload && notes[category]?.length > 0) return

  try {
    const res = await fetch(`/public/note/${category}.json?_=${Date.now()}`)
    const json = await res.json()
    notes[category] = json
  } catch (err) {
    console.error(`加载 ${category} 失败：`, err)
    notes[category] = []
  }

  if (category === currentCategory.value) {
    updateDisplayedData()
    printAllNames()
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
  const encodedFileName = encodeURIComponent(name + ".png")
  return new URL(`../assets/Items/${encodedFileName}`, import.meta.url).href
}

onMounted(async () => {
  // 先请求后端清空
  await fetch('/clear_vocabulary', { method: 'POST' })
  await loadCategory('vocabulary', true)
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
  gap: 10px;
  align-items: center;
  font-family: 'Source Han Serif SC', serif;
}

.correct-rate {
  margin-left: 30px;
  padding: 8px 16px;
  font-family: 'Source Han Serif SC', serif; /* 与整体一致 */
  font-size: 16px;
  font-weight: bold;
  color: #3e3e3e;
  background: linear-gradient(145deg, #fdf6e3, #f5deb3);
  border: 2px solid #8b6f47;
  border-radius: 12px;
  box-shadow: 2px 2px 6px rgba(0,0,0,0.2);
  transform: rotate(-2deg);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.correct-rate:hover {
  transform: rotate(0deg) scale(1.03);
  box-shadow: 4px 4px 12px rgba(0,0,0,0.3);
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
