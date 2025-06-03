<template>
  <div class="scene-switcher">
    <img 
      src="@/assets/switch-icon.png" 
      alt="切换场景" 
      class="toggle-icon" 
      @click="showOptions = !showOptions" 
    />

    <div v-if="showOptions" class="options">
      <button 
        v-for="btn in buttons" 
        :key="btn.name" 
        @click="switchTo(btn.name)"
      >
        {{ btn.label }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, defineEmits, defineProps } from 'vue'

const emit = defineEmits(['changeScene'])
const showOptions = ref(false)

// 传入按钮数组 [{ name: 'start', label: '开始界面' }, ...]
const props = defineProps({
  buttons: {
    type: Array,
    default: () => [
      { name: 'start', label: '开始界面' },
      { name: 'scene0', label: '场景 0' },
      { name: 'scene1', label: '场景 1' },
      { name: 'scene2', label: '场景 2' },
    ]
  }
})

function switchTo(sceneName) {
  emit('changeScene', sceneName)
  showOptions.value = false
}
</script>


<style scoped>
.scene-switcher {
  position: fixed;
  top: 100px;
  right: 20px;
  z-index: 1000;
}

.toggle-icon {
  width: 100px;
  height: 100px;
  cursor: pointer;
}

/* 中央按钮组容器 */
.options {
  position: fixed;
  top: 40%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

/* 场景按钮样式 */
button {
  width: 400px;
  padding: 15px 0;
  font-size: 20px;
  border: none;
  background-color: rgba(0, 0, 0, 0.6); /* 半透明黑底 */
  color: white;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: rgba(0, 0, 0, 0.8); /* 悬停时更不透明 */
}

</style>
