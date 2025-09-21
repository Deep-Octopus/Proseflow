<template>
  <div class="code-block-wrapper">
    <div class="header">
      <span class="title">{{ title }}</span>
      <div class="actions">
        <el-button size="small" @click="editCode">编辑</el-button>
        <el-button size="small" type="primary" @click="regenerateCode">AI 重新生成</el-button>
      </div>
    </div>
    <pre><code :class="`language-${language}`" v-html="highlightedCode"></code></pre>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
// 在实际项目中，你会使用一个高亮库，比如 highlight.js 或 prism.js
// 这里为了简化，我们只做基本展示
const props = defineProps({
  language: String,
  title: String,
  describe: String,
  code: String,
  matchCode: String
});

const highlightedCode = computed(() => {
  // 伪代码：实际应调用高亮库
  // return Prism.highlight(props.code, Prism.languages[props.language], props.language);
  return props.code.replace(/</g, "&lt;").replace(/>/g, "&gt;");
});

function editCode() {
  // 实现编辑逻辑，例如弹出一个模态框
  console.log('Editing code:', props.code);
}

function regenerateCode() {
  // 实现 AI 重新生成逻辑
  console.log('Regenerating code for:', props.describe);
}
</script>

<style scoped>
.code-block-wrapper {
  background-color: #1e1e1e;
  border-radius: 5px;
  margin: 1em 0;
  border: 1px solid #444;
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
pre {
  margin: 0;
}
</style>
