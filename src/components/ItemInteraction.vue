<template>
    <div class="item-interaction">
      <img
        :src="item.image"
        :style="getItemStyle()"
        class="item-image"
        alt="道具贴图"
        @click="handleItemClick"
        @mouseover="handleMouseOver"
        @mouseout="handleMouseOut"
      />
      <!-- 弹出式对话框组件 -->
      <PopupDialog
        :dialog="dialog"
        :is-visible="showDialogBox"
        @close="closeDialog"
      />
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import PopupDialog from '/src/components/poupdialog.vue';
  
  const props = defineProps({
    item: {
      type: Object,
      required: true,
    },
    position: {
      type: Object,
      required: true,
    },
  });
  
  const dialog = ref({
    character: '系统',
    text: '',
  });
  
  const showDialogBox = ref(false);
  
  function getItemStyle() {
    return {
      position: 'absolute',
      width: '100px',
      height: 'auto',
      top: props.position.top,
      left: props.position.left,
      cursor: 'pointer',
    };
  }
  
  function handleItemClick() {
    showDialogBox.value = true;
    dialog.value = {
      character: '系统',
      text: `你点击了道具: ${props.item.name}`,
    };
  }
  
  function handleMouseOver() {
    // 鼠标悬停效果
  }
  
  function handleMouseOut() {
    // 鼠标离开效果
  }
  
  function closeDialog() {
    showDialogBox.value = false;
  }
  </script>
  
  <style scoped>
  .item-interaction {
    position: relative;
    width: 100%;
    height: 100%;
  }
  
  .item-image {
    position: absolute;
    width: 100px;
    height: auto;
    pointer-events: auto;
  }
  </style>