<template> 
  <div class="guessword-overlay">
    <!-- 白色遮罩（上半部分） -->
    <div class="overlay-top"></div>

    <!-- 黑色遮罩（底部） -->
    <div class="overlay-bottom"></div>

    <!-- 🆕 打字提示文字 -->
    <div class="guessword-text">{{ displayedText }}</div>

    <!-- 猜词按钮 -->
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
    default: () => ['猫', '狗', '鸟']
  },
  jpName: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['guess'])

function handleClick(option) {
  emit('guess', option)
}

const displayedText = ref('')
let index = 0
let timer = null

function startTyping() {
  if (timer) clearInterval(timer)

  const fullText = `请你对【${props.jpName}（ ？？？）】的意思进行推测。`
  displayedText.value = ''
  index = 0
  timer = setInterval(() => {
    if (index < fullText.length) {
      displayedText.value += fullText[index]
      index++
    } else {
      clearInterval(timer)
      timer = null
    }
  }, 60)
}

onMounted(() => {
  startTyping()
  console.log('传入的选项是：', props.options)
})

// 监听jpName变化，重新触发打字效果
watch(() => props.jpName, (newVal, oldVal) => {
  if (newVal !== oldVal) {
    startTyping()
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
  /* pointer-events: none;  去掉这一行 */
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

/* 猜词按钮区域 */
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
