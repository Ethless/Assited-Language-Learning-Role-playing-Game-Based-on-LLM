<template>
    <div class="guess-word-game">
      <ItemList 
        v-if="!currentItem"
        :items="items"
        @select-item="selectItem"
      />
      <ItemGuess
        v-else
        :item="currentItem"
        @back="backToList"
      />
    </div>
  </template>
  
  <script>
  import ItemList from './ItemList.vue'
  import ItemGuess from './ItemGuess.vue'
  
  export default {
    name: 'GuessWordGame',
    components: {
      ItemList,
      ItemGuess
    },
    data() {
  return {
    items: [
      {
        id: 1,
        image: require('@/assets/blue_fish.png'), // 使用require语法
        chinese: '一种动物',
        japanese: '青い目の金魚',
        answer: '蓝眼金鱼'
      },
    ],
    currentItem: null
  }
},
    methods: {
      selectItem(item) {
        this.currentItem = item
      },
      backToList() {
        this.currentItem = null
      }
    }
  }
  </script>
  
  <style scoped>
  .guess-word-game {
    font-family: 'Arial', sans-serif;
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
  }
  </style>