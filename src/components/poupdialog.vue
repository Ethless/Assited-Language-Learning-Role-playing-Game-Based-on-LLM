<template>
    <div v-if="isVisible" class="popup-overlay" @click.self="closeDialog">
      <div class="popup-dialog">
        <div class="popup-header">
          <span class="popup-title">{{ dialog.character }}</span>
          <span class="popup-close" @click="closeDialog">×</span>
        </div>
        <div class="popup-content">
          {{ dialog.text }}
        </div>
        <div class="popup-footer">
          <button @click="closeDialog">关闭</button>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  
  defineProps({
    dialog: {
      type: Object,
      required: true,
    },
    isVisible: {
      type: Boolean,
      default: false,
    },
  });
  
  const emit = defineEmits(['close']);
  
  const closeDialog = () => {
    emit('close');
  };
  </script>
  
  <style scoped>
  .popup-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }
  
  .popup-dialog {
    background-color: white;
    border-radius: 8px;
    width: 80%;
    max-width: 500px;
    max-height: 80%;
    overflow: auto;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  }
  
  .popup-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 16px;
    border-bottom: 1px solid #e0e0e0;
  }
  
  .popup-title {
    font-weight: bold;
    font-size: 18px;
  }
  
  .popup-close {
    cursor: pointer;
    font-size: 20px;
  }
  
  .popup-content {
    padding: 16px;
  }
  
  .popup-footer {
    padding: 12px 16px;
    border-top: 1px solid #e0e0e0;
    text-align: right;
  }
  
  button {
    background-color: #4CAF50;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    cursor: pointer;
  }
  </style>