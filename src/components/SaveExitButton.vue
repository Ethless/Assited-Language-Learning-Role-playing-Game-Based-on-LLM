<template>
  <div class="save-exit">
    <button @click="saveGame">保存游戏</button>
    <button @click="$emit('exit')">退出到主菜单</button>
  </div>
</template>

<script setup>
const saveGame = () => {
  alert('保存功能尚未实现')
}
</script>
