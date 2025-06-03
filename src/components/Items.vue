<template>
  <div class="items">
    <img
      v-for="(img, index) in selectedImages"
      :key="index"
      :src="img"
      :style="getImageStyle(props.positions[index])"
      class="item-image"
      alt="道具贴图"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

// 定义 props，接收父组件传递的位置信息
const props = defineProps({
  positions: {
    type: Array,
    required: true
  }
})

// 使用 Vite 的 import.meta.glob 自动导入文件夹下所有图片
const allImages = import.meta.glob('@/assets/Items/*.{png,jpg,jpeg,gif,JPG}', {
  eager: true,
  import: 'default'
})

const imageUrls = Object.values(allImages)
const selectedImages = ref([])

onMounted(() => {
  const shuffled = [...imageUrls].sort(() => 0.5 - Math.random())
  const count = Math.min(props.positions.length, 4) // 这里取前 count 张图片
  selectedImages.value = shuffled.slice(0, count)
  
  console.log('All Images:', allImages); // 打印所有图片路径
  console.log('Selected Images:', selectedImages.value); // 打印选中的图片路径
})

function getImageStyle(position) {
  return {
    position: 'absolute',
    width: '100px',
    height: 'auto',
    top: position.top,
    left: position.left
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