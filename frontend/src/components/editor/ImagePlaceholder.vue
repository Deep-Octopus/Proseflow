<template>
  <div class="image-placeholder" @click="handleClick">
    <div class="icon">+</div>
    <div class="description">{{ type }}: {{ describe }}</div>
    <div class="actions">
      点击上传或 AI 生成图片
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  type: String,
  describe: String,
  matchCode: String
});

function handleClick() {
  // 实现上传或 AI 生成的逻辑
  console.log('Triggering image upload/generation for:', props.describe);
}
</script>

<style scoped>
.image-placeholder {
  border: 2px dashed #555;
  border-radius: 5px;
  padding: 2em;
  margin: 1em 0;
  text-align: center;
  cursor: pointer;
  background-color: #3a3a3a;
  transition: background-color 0.3s;
}
.image-placeholder:hover {
  background-color: #4a4a4a;
}
.icon {
  font-size: 2.5em;
  color: #888;
}
.description {
  color: #ccc;
  margin-top: 0.5em;
}
.actions {
  font-size: 0.9em;
  color: #888;
  margin-top: 0.5em;
}
</style>
