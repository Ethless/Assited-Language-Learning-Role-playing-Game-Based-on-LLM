<template>
  <div class="guessword-overlay">
    <!-- 上半遮罩 -->
    <div class="overlay-top"></div>

    <!-- 底部黑色遮罩 -->
    <div class="overlay-bottom"></div>

    <!-- 提示文字 -->
    <div class="guessword-text">{{ displayedText }}</div>

    <!-- 一组选项按钮 -->
    <div class="options">
      <button
        v-for="option in options"
        :key="option"
        @click="handleClick(option)"
      >
        {{ option }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'

const props = defineProps({
  options: {
    type: Array,
    default: () => []
  },
  jpName: {
    type: String,
    default: ''
  }
})


const emit = defineEmits(['guess'])

const displayedText = ref('')
let timer = null

function startTyping(text) {
  if (timer) clearInterval(timer)
  displayedText.value = ''
  let index = 0
  timer = setInterval(() => {
    if (index < text.length) {
      displayedText.value += text[index]
      index++
    } else {
      clearInterval(timer)
      timer = null
    }
  }, 60)
}

function handleClick(option) {
  emit('guess', option)
}

onMounted(() => {
  startTyping(`你想对【${props.jpName}】做什么？`)
})

watch(() => props.jpName, (newVal, oldVal) => {
  if (newVal !== oldVal) {
    startTyping(`【${props.jpName}】你要对这个物品做什么？`)
  }
})
</script>

<style scoped>
.guessword-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: 9999;
}

/* 上白遮罩 */
.overlay-top {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: calc(100% - 200px);
  background-color: rgba(255, 255, 255, 0.2);
  pointer-events: none;
  z-index: 10;
}

/* 下黑遮罩 */
.overlay-bottom {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 200px;
  background-color: rgba(0, 0, 0, 0.5);
  pointer-events: none;
  z-index: 5;
}

/* 打字提示文字 */
.guessword-text {
  position: absolute;
  bottom: 120px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 15;
  font-family: 'Source Han Sans SC', '思源黑体', sans-serif;
  font-size: 24px;
  line-height: 1.6;
  letter-spacing: 1px;
  color: #ffffff;
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

/* 按钮区域 */
.options {
  position: absolute;
  bottom: 300px;
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 20px;
  align-items: center;
  pointer-events: auto;
  z-index: 20;
}

button {
  width: 400px;
  padding: 15px;
  font-size: 20px;
  border: none;
  background-color: rgba(0, 0, 0, 0.6);
  color: white;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: rgba(0, 0, 0, 0.8);
}
</style>
