<template>
  <div class="dialog-container">
    <div class="dialog-overlay-top"></div>
    <div class="dialog-overlay">
      <!-- 每行单独 div，文字宽度自适应且居中 -->
      <div
        v-for="(line, i) in displayedLines"
        :key="i"
        class="dialog-line"
      >
        {{ line }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'

const props = defineProps({
  text: {
    type: String,
    default: '默认对话内容'
  },
  speed: {
    type: Number,
    default: 50
  }
})

const displayedLines = ref(['']) // 初始化为一行空字符串
let currentLineIndex = 0
let timer = null
let charIndex = 0

function startTyping() {
  displayedLines.value = ['']
  currentLineIndex = 0
  charIndex = 0
  clearInterval(timer)

  timer = setInterval(() => {
    if (charIndex < props.text.length) {
      const char = props.text[charIndex]
      if (char === '\n') {
        // 换行，添加新行
        displayedLines.value.push('')
        currentLineIndex++
      } else {
        // 追加字符到当前行
        displayedLines.value[currentLineIndex] += char
      }
      charIndex++
    } else {
      clearInterval(timer)
    }
  }, props.speed)
}

watch(() => props.text, () => {
  startTyping()
})

onMounted(() => {
  startTyping()
})
</script>

<style scoped>
.dialog-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: 1000;
  pointer-events: none;
}

.dialog-overlay-top {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: calc(100% - 200px);
  background-color: rgba(255, 255, 255, 0.2);
  pointer-events: auto;
  z-index: 20;
}

.dialog-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 200px;
  background-color: rgba(0, 0, 0, 0.5);
  pointer-events: auto;
  z-index: 0;

  /* 允许竖直排列，顶部开始 */
  display: flex;
  flex-direction: column;
  align-items: center; /* 所有行水平居中 */
  padding: 20px 250px;
  box-sizing: border-box;
  overflow-y: auto;
}

/* 每行文字宽度自适应内容，水平居中 */
.dialog-line {
  display: inline-block; /* 宽度包裹内容 */
  margin: 0 auto;
  font-family: 'Source Han Sans SC', '思源黑体', sans-serif;
  font-size: 24px;
  line-height: 1.5;
  letter-spacing: 5%;
  color: #FFFFFF;
  text-align: center;

  text-shadow:
    -3px 0 #412E2E,
    3px 0 #412E2E,
    0 -3px #412E2E,
    0 3px #412E2E,
    -2px -2px #412E2E,
    2px -2px #412E2E,
    -2px 2px #412E2E,
    2px 2px #412E2E;
}

.dialog-image {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 250px;
  height: auto;
  pointer-events: none;
}
</style>
