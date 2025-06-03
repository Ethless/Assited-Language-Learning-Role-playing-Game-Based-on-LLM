<template>
  <div>
    <!-- 传递当前视图状态作为场景名 -->
    <Background :scene="currentView" />

    <StartScreen v-if="currentView === 'start'" @start="startGame" />
    
    <div v-else>
      <Notebook />
      <Items />
      <NPC />
      <SaveExitButton @exit="exitToStart" />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Background from './components/Background.vue'
import StartScreen from './components/StartScreen.vue'
import Notebook from './components/Notebook.vue'
import Items from './components/Items.vue'
import NPC from './components/NPC.vue'
import SaveExitButton from './components/SaveExitButton.vue'
import DialogBox from './components/DialogBox.vue'
import GuessWordGameVue from './components/GuessWordGame.vue'
const currentView = ref('start')

const startGame = () => {
  currentView.value = 'game'
}

const exitToStart = () => {
  currentView.value = 'start'
}
</script>
