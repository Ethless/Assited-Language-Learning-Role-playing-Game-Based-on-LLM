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
  const imgUrl = selectedImages.value[index]
  const decodedUrl = decodeURIComponent(imgUrl)
  const fileName = decodedUrl.split('/').pop() || ''
  const baseName = fileName.replace(/\.[^/.]+$/, '')

  // 判断名字是否含空格、-、_
  if (/[ \-_]/.test(baseName)) {
    // 从词表随机找一个没有空格、-、_的词条
    const candidates = selectionData.filter(item => !/[ \-_]/.test(item.name))
    if (candidates.length === 0) {
      console.warn('词表中没有符合条件的替代词条')
      return
    }
    const randomItem = candidates[Math.floor(Math.random() * candidates.length)]

    clickedImage.value = imgUrl // 放大图还是用当前点击的图片

    emit('itemClicked', {
      itemId: randomItem.id,
      jpName: randomItem.jp,
      character: '系统',
      text: `【${randomItem.jp}（ ？？？）】\n※ ${randomItem.description || '（暂无描述）'}`
    })
  } else {
    // 正常根据图片名匹配词条
    const key = baseName.replace(/\s+/g, '').toLowerCase()
    const item = selectionData.find(i => {
      return i.name.replace(/\s+/g, '').toLowerCase() === key
    })

    clickedImage.value = imgUrl

    emit('itemClicked', {
      itemId: item?.id || null,
      jpName: item?.jp || '',
      character: '系统',
      text: `【${item?.jp || baseName}（ ？？？）】\n※ ${item?.description || '（暂无描述）'}`
    })
  }
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
