<template>
  <div class="button-group">
    <button @click="$emit('start')" class="btn japan-style">开始游戏</button>
    <button @click="loadGame" class="btn japan-style btn-secondary">读档</button>
    <button @click="showHelp" class="btn japan-style btn-secondary">帮助</button>
  </div>
</template>

<script setup>
const loadGame = () => {
  alert('讀檔功能尚未實現')
}

const showHelp = () => {
  alert('這是幫助訊息，目前尚未實作具體內容')
}
</script>

<style scoped>
@font-face {
  font-family: 'Unifont';
  src: url('@/assets/fonts/unifont-15.1.04.otf') format('opentype');
  font-weight: normal;
  font-style: normal;
}

.button-group {
  position: absolute;
  top: 660px;
  left: 590px;
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: center;
  gap: 10px;
  z-index: 20;
}

.btn {
  background: transparent;
  border: none;
  box-shadow: none;

  font-family: 'Unifont', 'Noto Serif JP', serif;
  font-size: 50px;
  font-weight: 2000;
  color: #fff; /* 白色填充 */
  cursor: pointer;
  user-select: none;

  /* 文字黑色描边 */
  /* -webkit-text-stroke: 1px black; */

  /* 取消阴影 */
  text-shadow: 10px 10px 2px rgba(0, 0, 0, 0.3);

  transition: all 0.3s ease;
  padding: 12px 32px;
  border-radius: 12px;
}

.btn-secondary {
  font-size: 36px;
  font-weight: 2000;
  /* 同样描边 */
  /* -webkit-text-stroke: 1px black; */
}

.btn:hover {
  color: #fff;
  transform: translateY(-2px);
  /* 可选加轻微阴影，突出文字 */
  text-shadow: 15px 15px 2px rgba(0, 0, 0, 0.762);
}

.btn:active {
  transform: translateY(1px);
  text-shadow: none;
}

.btn:focus-visible {
  outline: none;
}
</style>
