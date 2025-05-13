<template>
  <div class="start-screen">
    <button @click="$emit('start')">开始游戏</button>
    <button @click="importSave">导入存档</button>
    <button @click="exitGame">退出游戏</button>
  </div>
</template>

<script setup>
const importSave = () => {
  alert('导入存档功能尚未实现')
}

const exitGame = () => {
  window.close?.() || alert('退出游戏功能仅在桌面应用中可用')
}
</script>

<style scoped>
.start-screen button {
  margin: 10px;
  font-size: 18px;
}
</style>
