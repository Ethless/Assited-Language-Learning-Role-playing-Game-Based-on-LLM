<template>
  <div class="canvas-container">
    <canvas ref="gameCanvas" width="800" height="500"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'

// 模拟贴图导入（实际使用时替换为真实路径）
const loadImage = (color, text) => {
  const canvas = document.createElement('canvas')
  canvas.width = 50
  canvas.height = 50
  const ctx = canvas.getContext('2d')
  ctx.fillStyle = color
  ctx.fillRect(0, 0, 50, 50)
  ctx.fillStyle = 'white'
  ctx.font = '12px Arial'
  ctx.textAlign = 'center'
  ctx.fillText(text, 25, 30)
  return canvas.toDataURL()
}

// 生成模拟贴图
const backgroundImg = loadImage('#112240', 'BG')
const characterImg = loadImage('#64ffda', '角色')
const swordIcon = loadImage('#ff4757', '剑')
const potionIcon = loadImage('#7bed9f', '药水')
const keyIcon = loadImage('#ffa502', '钥匙')

const gameCanvas = ref(null)
const emit = defineEmits(['tool-selected'])

onMounted(() => {
  const ctx = gameCanvas.value.getContext('2d')
  const canvasWidth = gameCanvas.value.width
  const canvasHeight = gameCanvas.value.height

  // 工具配置
  const tools = [
    { x: canvasWidth/2 - 100, y: canvasHeight/2 - 25, type: 'sword', img: swordIcon },
    { x: canvasWidth/2 + 50, y: canvasHeight/2 - 25, type: 'potion', img: potionIcon },
    { x: canvasWidth/2 - 25, y: canvasHeight/2 - 100, type: 'key', img: keyIcon }
  ]

  // 加载图片
  const loadImageToCanvas = (src, x, y, width, height) => {
    return new Promise((resolve) => {
      const img = new Image()
      img.src = src
      img.onload = () => {
        ctx.drawImage(img, x, y, width, height)
        resolve()
      }
    })
  }

  // 绘制游戏
  const drawGame = async () => {
    // 清空画布
    ctx.clearRect(0, 0, canvasWidth, canvasHeight)
    
    // 绘制背景
    await loadImageToCanvas(backgroundImg, 0, 0, canvasWidth, canvasHeight)
    
    // 绘制角色（居中）
    await loadImageToCanvas(characterImg, canvasWidth/2 - 50, canvasHeight/2 - 75, 100, 150)
    
    // 绘制工具
    for (const tool of tools) {
      await loadImageToCanvas(tool.img, tool.x, tool.y, 50, 50)
    }
  }

  // 点击处理
  const handleClick = (e) => {
    const rect = gameCanvas.value.getBoundingClientRect()
    const x = e.clientX - rect.left
    const y = e.clientY - rect.top

    // 检测工具点击
    tools.forEach(tool => {
      if (x > tool.x && x < tool.x + 50 && y > tool.y && y < tool.y + 50) {
        emit('tool-selected', tool.type)
      }
    })
  }

  gameCanvas.value.addEventListener('click', handleClick)
  drawGame()

  onBeforeUnmount(() => {
    gameCanvas.value?.removeEventListener('click', handleClick)
  })
})
</script>

<style scoped>
.canvas-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: calc(100vh - 100px);
  padding: 20px;
}

canvas {
  border: 2px solid #64ffda;
  background-color: #112240;
  box-shadow: 0 0 20px rgba(100, 255, 218, 0.2);
}
</style>