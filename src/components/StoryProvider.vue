<template>
  <div v-if="false"></div> <!-- 这是一个逻辑组件，不渲染任何内容 -->
</template>

<script setup>
import { onMounted } from 'vue'
import api from '@/api'

const props = defineProps({
  background: String,
  ending: String,
  scene: String
})

const emit = defineEmits(['ready']) // 输出剧情数据

async function generateStory() {
  try {
    await api.post('/story/setup', {
      background: props.background,
      ending: props.ending,
      scene: props.scene
    })

    const res = await api.get('/story/plot/first')
    const plotText = res.data.plot || ''

    const lines = plotText
      .split(/[\n。！？]/)
      .map(line => line.trim())
      .filter(line => line.length > 0)

    const dialogs = lines.map((line, idx) => ({
      character: idx % 2 === 0 ? '小明' : '小红',
      text: line
    }))

    emit('ready', dialogs)
  } catch (err) {
    console.error('剧情生成失败', err)
    emit('ready', [
      { character: '系统', text: '剧情生成失败，请稍后再试。' }
    ])
  }
}

onMounted(() => {
  generateStory()
})
</script>
