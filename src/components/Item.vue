<template>
  <div class="items">
    <!-- 每个道具的容器，包括点击提示和贴图 -->
    <div
      v-for="(img, index) in selectedImages"
      :key="index"
      :style="getImageStyle(positions[index])"
      class="item-wrapper"
    >
      <!-- 白色圆圈 + 外层透明边框 -->
      <div class="click-circle-wrapper" @click="handleClick(index)">
        <div class="click-circle"></div>
      </div>

      <!-- 道具贴图（不再可点击） -->
      <img
        :src="img"
        class="item-image"
        alt="道具贴图"
      />
    </div>

    <!-- 放大图 -->
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
import selectionData from '/src/assets/selection.json'

const clickedImage = ref(null)
const emit = defineEmits(['itemClicked', 'cleared'])

const nameMap = {}
selectionData.forEach(item => {
  const key = item.name.replace(/\s+/g, '').toLowerCase()
  nameMap[key] = {
    zh: item.zh,
    jp: item.jp,
    description: item.description,
  }
})


function clearClickedImage() {
  clickedImage.value = null
  emit('cleared')
  this.wasCleared = true
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
    top: position.top,
    left: position.left,
  }
}

function handleClick(index) {
  clickedImage.value = selectedImages.value[index]

  const decodedUrl = decodeURIComponent(selectedImages.value[index])
  const fileName = decodedUrl.split('/').pop() || ''
  const baseName = fileName.replace(/\.[^/.]+$/, '')
  const key = baseName.replace(/\s+/g, '').toLowerCase()

  // 从 selectionData 找对应 item
  const item = selectionData.find(i => {
    return i.name.replace(/\s+/g, '').toLowerCase() === key
  })

  const zhName = item?.zh || baseName
  const jpName = item?.jp || ''
  const desc = item?.description || '（暂无描述）'

  emit('itemClicked', {
    itemId: item?.id || null,  // 这里保证不会报错
    jpName: jpName,
    character: '系统',
    text: `【${jpName}（ ？？？）】\n※ ${desc}`
  })
}


</script>

<style scoped>
.items {
  position: relative;
  width: 100%;
  height: 100%;
}

.item-wrapper {
  position: absolute;
  width: 100px;
  height: auto;
}

/* 放大贴图 */
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

/* 道具贴图 */
.item-image {
  width: 80px;
  height: auto;
  pointer-events: auto;
  z-index: 10;
}

/* 外层半透明点击圈 */
.click-circle-wrapper {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, 75%);
  width: 28px;
  height: 28px;
  background-color: rgba(255, 255, 255, 0.4);
  border-radius: 50%;
  z-index: 15;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 0 6px rgba(0, 0, 0, 0.15);
}

/* 内部白色点击圈 */
.click-circle {
  width: 14px;
  height: 14px;
  background-color: white;
  border-radius: 50%;
  transition: transform 0.2s ease-in-out;
}

.click-circle-wrapper:hover .click-circle {
  transform: scale(1.5);
}
</style>
