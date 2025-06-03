<template>
  <div class="items">
    <img
      v-for="(img, index) in selectedImages"
      :key="index"
      :src="img"
      :style="getImageStyle(index)"
      class="item-image"
      alt="道具贴图"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

// 使用 Vite 的 import.meta.glob 自动导入文件夹下所有图片
const allImages = import.meta.glob('@/assets/Items/*.{png,jpg,jpeg,gif,JPG}', {
  eager: true,
  import: 'default'
})

const imageUrls = Object.values(allImages)
const selectedImages = ref([])

onMounted(() => {
  const shuffled = [...imageUrls].sort(() => 0.5 - Math.random())
  selectedImages.value = shuffled.slice(0, 2)
})

function getImageStyle(index) {
  const positions = [
    { top: '150px', left: '200px' },
    { top: '300px', left: '600px' }
  ]
  return {
    position: 'absolute',
    width: '100px',
    height: 'auto',
    ...positions[index % positions.length]
  }
}
</script>

<style scoped>
.items {
  position: relative;
  width: 100%;
  height: 100%;
}

.item-image {
  pointer-events: none;
}
</style>
