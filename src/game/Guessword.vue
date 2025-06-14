<template> 
  <div class="guessword-overlay" @click.self="handleOverlayClick">
    <!-- 白色遮罩（上半部分） -->
    <div class="overlay-top"></div>

    <!-- 黑色遮罩（底部） -->
    <div class="overlay-bottom"></div>

    <!-- 打字提示文字 -->
    <div class="guessword-text">{{ displayedText }}</div>

    <!-- 猜词按钮 -->
    <div class="options">
      <button
        v-for="(option, index) in options"
        :key="option"
        @click="handleClick(option)"
        :class="{
          'correct': hasClicked && index === props.correctIndex,
          'incorrect': hasClicked && selectedOption === option && index !== props.correctIndex
        }"
        :disabled="hasClicked"
      >
        {{ option }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import axios from 'axios'

const selectedOption = ref(null)
const hasClicked = ref(false)

const props = defineProps({
  options: {
    type: Array,
    default: () => ['猫', '狗', '鸟']
  },
  jpName: {
    type: String,
    default: ''
  },
  correctIndex: {
    type: Number,
    default: -1
  },
  itemId: {
    type: [String, Number],
    required: false
  }
})

// 这里声明 emit 事件，父组件要监听 'guess'，参数改为数字 0 或 1
const emit = defineEmits(['guess', 'close'])

function handleClick(option) {
  if (!hasClicked.value) {
    selectedOption.value = option
    hasClicked.value = true

    const correctOption = props.options[Number(props.correctIndex)]

    // 判断是否正确，0 表示错误，1 表示正确
    let correct_judge = option === correctOption ? 1 : 0
    emit('guess', { option, isCorrect: correct_judge })

    if (correct_judge === 1) {
      fullText.value = '完全没错！你可以去笔记本中查看该词的更多意思。'
      console.log('答对了')
    } else {
      fullText.value = '不是这个意思，去笔记本巩固吧。'
    }
    startTyping()

    // 发送保存请求，带上 correct_judge
    axios.post('http://localhost:8000/api/save-vocab', {
        id: props.itemId,
        correct_judge: correct_judge,
    }).then(res => {
      console.log('保存成功', res.data)
    }).catch(err => {
      console.error('保存失败', err)
    })
  }
}

function handleOverlayClick() {
  if (hasClicked.value) {
    emit('close')
    hasClicked.value = false
    selectedOption.value = null
  }
}

const displayedText = ref('')
const fullText = ref('')
let index = 0
let timer = null

function startTyping() {
  if (timer) clearInterval(timer)

  displayedText.value = ''
  index = 0
  timer = setInterval(() => {
    if (index < fullText.value.length) {
      displayedText.value += fullText.value[index]
      index++
    } else {
      clearInterval(timer)
      timer = null
    }
  }, 60)
}

onMounted(() => {
  fullText.value = `请你对【${props.jpName}（ ？？？）】的意思进行推测。`
  startTyping()
  console.log('传入的选项是：', props.options)
})

watch(() => props.jpName, (newVal, oldVal) => {
  if (newVal !== oldVal) {
    fullText.value = `请你对【${props.jpName}（ ？？？）】的意思进行推测。`
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
}

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
  transition: background-color 0.3s ease, border 0.3s ease;
}

button:hover:not(:disabled) {
  background-color: rgba(0, 0, 0, 0.8);
  /* 只有未禁用按钮才有hover效果 */
}

.correct {
  border: 6px solid #4DC361; /* 绿色边框 */
}

.incorrect {
  border: 6px solid #D34343; /* 红色边框 */
  opacity: 1;
}
</style>
