<template>
  <div class="plantuml-block-wrapper">
    <div class="header">
      <span class="title">{{ type }} - {{ describe }}</span>
      <div class="actions">
        <el-button size="small" @click="editPuml">编辑</el-button>
        <el-button size="small" type="primary" @click="regeneratePuml">AI 重新生成</el-button>
      </div>
    </div>
    <div class="puml-content">
      <img :src="pumlUrl" alt="PlantUML Diagram" />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { encode } from 'plantuml-encoder';

const props = defineProps({
  type: String,
  describe: String,
  code: String,
  matchCode: String
});

const pumlUrl = computed(() => {
  if (!props.code) return '';
  // 使用官方的 PlantUML 服务器来渲染
  const encoded = encode(props.code);
  return `http://www.plantuml.com/plantuml/svg/${encoded}`;
});

function editPuml() {
  console.log('Editing PlantUML:', props.code);
}

function regeneratePuml() {
  console.log('Regenerating PlantUML for:', props.describe);
}
</script>

<style scoped>
.plantuml-block-wrapper {
  border: 1px solid #444;
  border-radius: 5px;
  margin: 1em 0;
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5em 1em;
  background-color: #333;
  border-bottom: 1px solid #444;
  font-size: 0.9em;
  color: #ccc;
}
.puml-content {
  padding: 1em;
  background-color: #f5f5f5; /* 浅色背景以突出图表 */
  display: flex;
  justify-content: center;
  align-items: center;
}
.puml-content img {
  max-width: 100%;
}
</style>
