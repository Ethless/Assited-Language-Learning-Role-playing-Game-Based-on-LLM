<template>
  <div>
    <!-- 默认笔记本贴图（右上角） -->
    <img
      src="@/assets/notebook.png"
      alt="Notebook Closed"
      class="notebook-icon"
      @click="showOpenNotebook = true"
    />

    <!-- 翻开的笔记本弹窗 -->
    <div v-if="showOpenNotebook" class="popup">
      <div class="popup-content">
        <img src="@/assets/notebook_open.png" alt="Notebook Open" />
        <button @click="showOpenNotebook = false">关闭</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const showOpenNotebook = ref(false)
</script>

<style scoped>
/* 合上笔记本图标定位到右上角 */
.notebook-icon {
  position: fixed;
  top: 20px;
  right: 20px;
  width: 80px;
  height: auto;
  cursor: pointer;
  z-index: 1000;
  transition: transform 0.2s;
  box-shadow: 0px 13px 4px rgba(0, 0, 0, 0.25);
}
.notebook-icon:hover {
  transform: scale(1.1);
}

/* 覆盖全屏的弹窗 */
.popup {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.7);
  z-index: 2000;
  display: flex;
  justify-content: center;
  align-items: center;
}

/* 弹窗内容容器铺满区域 */
.popup-content {
  position: relative;
  width: 90vw;
  height: 90vh;
  overflow: hidden;
  border-radius: 12px;
}

/* 图片铺满整个内容区域 */
.open-notebook-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  border-radius: 12px;
}

/* 悬浮关闭按钮 */
.close-btn {
  position: absolute;
  top: 10px;
  right: 12px;
  font-size: 24px;
  color: #fff;
  background: rgba(0, 0, 0, 0.5);
  border: none;
  border-radius: 50%;
  width: 36px;
  height: 36px;
  cursor: pointer;
}
.close-btn:hover {
  background: rgba(0, 0, 0, 0.7);
}
</style>