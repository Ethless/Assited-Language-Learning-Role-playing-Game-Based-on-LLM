<template>
  <div class="start-screen">
    <button @click="$emit('start')" class="btn japan-style">開始遊戲</button>
    <button @click="importSave" class="btn japan-style">導入存檔</button>
    <button @click="exitGame" class="btn japan-style">退出遊戲</button>
  </div>
</template>

<script setup>
const importSave = () => {
  alert('導入存檔功能尚未實現')
}

const exitGame = () => {
  window.close?.() || alert('退出遊戲功能僅在桌面應用中可用')
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+JP&display=swap');

.start-screen {
  position: absolute;
  top: 10vh;
  bottom: 10vh;
  left: 10vw;
  right: 10vw;

  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;

  background: #faf2e3; /* 和风柔色 */
  gap: 20px;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 0 10px rgba(0,0,0,0.2); /* 可选美化 */
}


.btn {
  min-width: 180px;
  padding: 12px 32px;
  font-size: 22px;
  font-weight: 700;
  font-family: 'Noto Serif JP', serif;
  border: 2.5px solid #b45f06; /* 深棕色边框 */
  border-radius: 12px;
  background: #fff8e1; /* 淡淡米黄色背景 */
  color: #5b3a00; /* 深棕色字体 */
  cursor: pointer;
  box-shadow:
    2px 2px 5px rgba(180, 95, 6, 0.3),
    inset 0 0 8px rgba(255, 255, 255, 0.6);
  transition: all 0.3s ease;
  user-select: none;
  text-shadow: 1px 1px 0 rgba(255, 255, 255, 0.7);
}

.btn:hover {
  background: #fff3c4;
  color: #783f04;
  box-shadow:
    3px 3px 8px rgba(183, 95, 6, 0.5),
    inset 0 0 12px rgba(255, 255, 255, 0.8);
  transform: translateY(-3px);
}

.btn:active {
  transform: translateY(1px);
  box-shadow:
    1px 1px 3px rgba(183, 95, 6, 0.4),
    inset 0 0 6px rgba(255, 255, 255, 0.5);
}

/* 取消按钮默认蓝色聚焦边框，改成棕色 */
.btn:focus-visible {
  outline: 3px solid #b45f06;
  outline-offset: 2px;
}
</style>
