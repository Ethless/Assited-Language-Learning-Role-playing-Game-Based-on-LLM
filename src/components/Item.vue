<!-- Item.vue -->
<template>
  <div class="items">
    <!-- 道具贴图 -->
    <img
      v-for="(img, index) in selectedImages"
      :key="index"
      :src="img"
      :style="getImageStyle(positions[index])"
      class="item-image"
      alt="道具贴图"
      @click="handleClick(index)"
    />

    <!-- 居中放大的贴图 -->
    <img
      v-if="clickedImage"
      :src="clickedImage"
      class="enlarged-image"
      alt="放大贴图"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const clickedImage = ref(null)
const emit = defineEmits(['itemClicked', 'cleared'])

function clearClickedImage() {
  clickedImage.value = null
  emit('cleared')
  this.wasCleared = true  // 添加标记
}

defineExpose({ clearClickedImage })

const props = defineProps({
  positions: {
    type: Array,
    required: true,
  }
})

const allImages = import.meta.glob('@/assets/Items/*.{png,jpg,jpeg,gif,JPG}', {
  eager: true,
  import: 'default',
})
const imageUrls = Object.values(allImages)
const selectedImages = ref([])

onMounted(() => {
  const shuffled = [...imageUrls].sort(() => 0.5 - Math.random())
  const count = Math.min(props.positions.length, imageUrls.length)
  selectedImages.value = shuffled.slice(0, count)
})

function getImageStyle(position) {
  return {
    position: 'absolute',
    width: '100px',
    height: 'auto',
    top: position.top,
    left: position.left,
    cursor: 'pointer'
  }
}

function handleClick(index) {
  clickedImage.value = selectedImages.value[index] // ✅ 设置放大图
  emit('itemClicked', {
    character: '系统',
    text: `你点击了道具 ${index + 1}`
  })
}
</script>

<style scoped>
.items {
  position: relative;
  width: 100%;
  height: 100%;
}

.item-image {
  position: absolute;
  pointer-events: auto;
  z-index: 10;
}

.enlarged-image {
  position: fixed;
  top: 40%;
  left: 50%;
  width: 250px;
  height: auto;
  transform: translate(-50%, -50%);
  z-index: 9999;
  pointer-events: none;
}
</style>
