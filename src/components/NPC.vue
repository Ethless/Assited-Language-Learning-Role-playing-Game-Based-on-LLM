<template>
  <div class="npc" @click="showDialog">
    <h2>NPC 对话</h2>
    <p>点击 NPC 开始对话</p>

    <!-- 固定底部的对话框 -->
    <div v-if="dialogVisible" class="dialog-box">
      <p>{{ dialogText }}</p>
      <button @click.stop="closeDialog">关闭</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const dialogVisible = ref(false)
const dialogText = ref('你好，冒险者。我有一些事情想告诉你……')

const showDialog = () => {
  dialogVisible.value = true
}

const closeDialog = () => {
  dialogVisible.value = false
}
</script>

<style scoped>
.npc {
  border: 1px solid #ccc;
  padding: 20px;
  cursor: pointer;
  position: relative;
}

/* 对话框固定到底部 */
.dialog-box {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  background-color: rgba(20, 20, 20, 0.9);
  color: #fff;
  padding: 20px;
  box-sizing: border-box;
  border-top: 3px solid #888;
  z-index: 1000;
}

.dialog-box p {
  margin: 0 0 10px 0;
  font-size: 18px;
}

.dialog-box button {
  background: #555;
  color: white;
  border: none;
  padding: 6px 12px;
  font-size: 14px;
  cursor: pointer;
  border-radius: 4px;
}

.dialog-box button:hover {
  background: #777;
}
</style>
