<template>
    <div class="item-list">
      <h2>选择道具开始游戏</h2>
      <div class="items-container">
        <ItemCard
          v-for="item in items"
          :key="item.id"
          :item="item"
          @click="handleItemClick(item)"
        />
      </div>
    </div>
  </template>
  
  <script>
  import ItemCard from './ItemCard.vue'
  
  export default {
    name: 'ItemList',
    components: {
      ItemCard
    },
    props: {
      items: {
        type: Array,
        required: true
      }
    },
    methods: {
      handleItemClick(item) {
        this.$emit('select-item', item)
      }
    }
  }
  </script>
  
  <style scoped>
  .item-list {
    text-align: center;
  }
  
  .items-container {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 20px;
    margin-top: 20px;
  }
  </style>