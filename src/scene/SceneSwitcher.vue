<template>
  <div class="scene-switcher">
    <img 
      src="@/assets/switch-icon.png" 
      alt="切换场景" 
      class="toggle-icon" 
      @click="toggleOptions"
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

const emit = defineEmits(['changeScene', 'sceneSwitchIntent']) // ✅ 增加 sceneSwitchIntent
const showOptions = ref(false)

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

function toggleOptions() {
  showOptions.value = !showOptions.value
  if (showOptions.value) {
    emit('sceneSwitchIntent') // ✅ 在“展开切换面板”时就触发提示事件
  }
}

function switchTo(sceneName) {
  emit('changeScene', sceneName)
  showOptions.value = false
}

function hideOptions() {
  showOptions.value = false
}

defineExpose({ hideOptions })
</script>

<style scoped>
.scene-switcher {
  position: fixed;
  top: 100px;
  right: 20px;
  z-index: 1000;
  transition: transform 0.2s ease;
}

.toggle-icon:hover {
  transform: scale(1.05);
}

.toggle-icon {
  width: 100px;
  height: 100px;
  cursor: pointer;
}

.options {
  position: fixed;
  top: 40%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  z-index: 9999;
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
  transition: background-color 0.3s ease;
  z-index: 300;
}

button:hover {
  background-color: rgba(0, 0, 0, 0.8);
}
</style>