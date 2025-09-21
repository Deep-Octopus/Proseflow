<template>
  <el-container class="app-container">
    <el-header>
      <TheHeader />
    </el-header>
    <el-main>
      <HomeView />
    </el-main>
  </el-container>
</template>

<script setup>
import TheHeader from './components/layout/TheHeader.vue';
import HomeView from './views/HomeView.vue';
</script>

<style>
.app-container {
  height: 100vh;
}
.el-header {
  border-bottom: 1px solid var(--el-border-color);
  display: flex;
  align-items: center;
}
.el-main {
  padding: 0;
  overflow: hidden; /* 防止编辑器溢出 */
}
</style>
