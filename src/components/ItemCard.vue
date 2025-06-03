<template>
    <div class="item-card" @click="$emit('click')">
      <img :src="item.image" :alt="item.chinese" class="item-image">
      <div class="item-preview">{{ item.chinese }}</div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'ItemCard',
    props: {
      item: {
        type: Object,
        required: true
      }
    }
  }
  </script>
  
  <style scoped>
  .item-card {
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 10px;
    cursor: pointer;
    transition: transform 0.2s;
  }
  
  .item-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
  }
  
  .item-image {
    width: 100%;
    height: 150px;
    object-fit: cover;
    border-radius: 5px;
  }
  
  .item-preview {
    margin-top: 10px;
    font-size: 14px;
    color: #333;
    text-align: left;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }
  </style>