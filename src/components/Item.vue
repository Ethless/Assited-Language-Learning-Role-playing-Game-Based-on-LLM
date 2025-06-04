<!-- Item.vue -->
<template>
  <div class="items">
    <img
      v-for="(img, index) in selectedImages"
      :key="index"
      :src="img"
      :style="getImageStyle(positions[index])"
      class="item-image"
      alt="道具贴图"
      @click="handleClick(index)"
    />

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

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

const emit = defineEmits(['itemClicked'])

function handleClick(index) {
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
</style>
