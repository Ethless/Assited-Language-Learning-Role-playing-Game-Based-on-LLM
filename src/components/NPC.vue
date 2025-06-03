<template> 
  <div class="npc" @click="showDialog">
    <h2>NPC 对话</h2>
    <p>点击 NPC 开始对话</p>

    <!-- 用 v-model:visible 绑定显示状态 -->
    <DialogBox v-model:visible="dialogVisible" :text="dialogText" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import DialogBox from './DialogBox.vue'

const dialogVisible = ref(false)
const dialogText = ref('芝士雪豹')

const showDialog = () => {
  dialogVisible.value = true
}
</script>

<style scoped>
.npc {
  border: 1px solid #ccc;
  padding: 20px;
  cursor: pointer;
  position: relative;
}
</style>
