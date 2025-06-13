<template>
  <div class="dialog-container">
    <!-- 🆕 上半部分白色遮罩 -->
    <div class="dialog-overlay-top"></div>

    <!-- 原有底部黑色遮罩 -->
    <div class="dialog-overlay"></div>

    <!-- <img src="@/assets/player.png" alt="装饰贴图" class="dialog-image" /> -->

    <!-- 对话文本 -->
    <div class="dialog-text" ref="textRef">{{ displayedText }}</div>
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

const displayedText = ref('')
const textRef = ref(null)

let index = 0
let timer = null

function startTyping() {
  displayedText.value = ''
  index = 0
  clearInterval(timer)
  timer = setInterval(() => {
    if (index < props.text.length) {
      displayedText.value += props.text[index]
      index++
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
  height: 100vh; /* 改为全屏，支持上遮罩 */
  z-index: 1000;
  pointer-events: none;
}

/* 🆕 上半部分白色遮罩 */
.dialog-overlay-top {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: calc(100% - 200px); /* 除去下方对话框高度 */
  background-color: transparent; /* 白色半透明 */
  pointer-events: auto;
  z-index: 0;
}

/* .dialog-container {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100vw;
  height: 175px;
  z-index: 1000;
  display: flex;
  justify-content: flex-start;
  align-items: flex-start;
  pointer-events: none;
} */

.dialog-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 200px;
  background-color: rgba(0, 0, 0, 0.5);
  pointer-events: auto;
  z-index: 0;
}

.dialog-text {
  position: absolute;
  bottom: 100px; /* 距离底部一点距离，美观 */
  left: 20%;
  right: 20%;
  z-index: 1;

  font-family: 'Source Han Sans SC', '思源黑体', sans-serif;
  font-size: 24px;
  line-height: 1.5;
  letter-spacing: 5%;
  text-align: left;
  color: #FFFFFF;

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

/* 左下角贴图样式 */
.dialog-image {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 250px; /* 贴图宽度，可按实际调整 */
  height: auto;
  pointer-events: none;
}
</style>
