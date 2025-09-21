<template>
  <div class="editor-wrapper">
    <div ref="editorContainer" class="editor-container" v-html="renderedHtml"></div>
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick } from 'vue';
import { useEditorStore } from '@/store/editorStore.js';
import { useMarkdownParser } from '@/utils/markdownParser.js';

const editorStore = useEditorStore();
const { render } = useMarkdownParser();

const editorContainer = ref(null);

// 使用 computed 属性来响应 editorStore 中 content 的变化
const renderedHtml = computed(() => {
  return render(editorStore.content);
});

// 监听内容变化，并滚动到底部，模拟打字机效果
watch(() => editorStore.content, async () => {
  await nextTick();
  const container = editorContainer.value;
  if (container) {
    container.scrollTop = container.scrollHeight;
  }
});

</script>

<style>
.editor-wrapper {
  width: 100%;
  max-width: 820px;
  height: calc(100vh - 61px); /* 减去 header 高度 */
  overflow-y: auto;
  padding: 2rem;
  box-sizing: border-box;
  background-color: #2f2f2f;
}

.editor-container {
  height: 100%;
  line-height: 1.7;
  color: #dcdcdc;
}

/* markdown-it 渲染样式 */
.editor-container h1, .editor-container h2, .editor-container h3 {
  border-bottom: 1px solid #444;
  padding-bottom: 0.3em;
}
.editor-container code {
  background-color: #1e1e1e;
  padding: 0.2em 0.4em;
  border-radius: 3px;
  font-family: 'Courier New', Courier, monospace;
}
.editor-container pre {
  background-color: #1e1e1e;
  padding: 1em;
  border-radius: 5px;
  overflow-x: auto;
}
.editor-container pre code {
  padding: 0;
  background-color: transparent;
}
.editor-container blockquote {
  border-left: 0.25em solid #555;
  color: #aaa;
  padding: 0 1em;
  margin-left: 0;
}
.editor-container a {
  color: #409eff;
  text-decoration: none;
}
.editor-container a:hover {
  text-decoration: underline;
}
</style>
