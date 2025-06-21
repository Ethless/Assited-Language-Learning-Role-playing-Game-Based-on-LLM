<template>
  <div class="background" :style="backgroundStyle"></div>
</template>

<script setup>
import { computed } from 'vue'
import { defineProps } from 'vue'

// 接收场景名作为 prop
const props = defineProps({
  scene: {
    type: String,
    default: 'start',
  }
})

// 根据不同场景切换背景图
const backgroundStyle = computed(() => {
  let imagePath = ''
  if (props.scene === 'start') {
    imagePath = new URL('@/assets/background_start.png', import.meta.url).href
  } else if (props.scene === 'game') {
    imagePath = new URL('@/assets/background_game.png', import.meta.url).href
  } else if (props.scene === 'scene0') {
    imagePath = new URL('@/assets/background/bg1.jpg', import.meta.url).href
  } else if (props.scene === 'scene1') {
    imagePath = new URL('@/assets/background/bg2.jpg', import.meta.url).href
  } else if (props.scene === 'scene2') {
    imagePath = new URL('@/assets/background/bg3.jpg', import.meta.url).href
  } else if (props.scene === 'scene3') {
    imagePath = new URL('@/assets/background/bg4.jpg', import.meta.url).href
  }

  return {
    backgroundImage: `url(${imagePath})`,
    backgroundSize: 'cover',
    backgroundPosition: 'center',
    backgroundRepeat: 'no-repeat',
    position: 'fixed',
    top: 0,
    left: 0,
    width: '100vw',
    height: '100vh',
    zIndex: -1,
  }
})
</script>