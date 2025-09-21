<template>
  <div class="latex-block-wrapper">
    <div class="header">
      <span class="title" :title="describe">公式</span>
      <div class="actions">
        <el-button size="small" @click="editLatex">编辑</el-button>
        <el-button size="small" type="primary" @click="regenerateLatex">AI 重新生成</el-button>
      </div>
    </div>
    <div class="latex-content" ref="latexContainer"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import katex from 'katex';
import { ElMessageBox, ElMessage } from 'element-plus';
import { streamGenerate } from '@/services/llmService';
import { useUiStore } from '@/store/uiStore';
import { useEditorStore } from '@/store/editorStore';

const props = defineProps({
  describe: String,
  latex: String,
  matchCode: String
});

const latexContainer = ref(null);
const uiStore = useUiStore();
const editorStore = useEditorStore();

const renderFormula = () => {
  if (latexContainer.value && props.latex) {
    try {
      katex.render(props.latex, latexContainer.value, {
        throwOnError: false,
        displayMode: true,
      });
    } catch (e) {
      latexContainer.value.textContent = `Error rendering LaTeX: ${e.message}`;
      console.error(e);
    }
  }
};

onMounted(renderFormula);
watch(() => props.latex, renderFormula, { immediate: true });

function editLatex() {
  ElMessageBox.prompt('请编辑 LaTeX 代码', '编辑公式', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    inputValue: props.latex,
    inputType: 'textarea',
    rows: 5,
  })
    .then(({ value }) => {
      const oldBlock = props.matchCode
      // 构造旧的和新的内容块字符串
      const newBlock = `[LATEX describe="${props.describe}"]${value}[/LATEX]`;

      // 调用 store action 来更新全局内容，而不是直接修改 prop
      editorStore.updateBlockContent({ oldBlock, newBlock });

      ElMessage.success('公式已更新');
    })
    .catch(() => { /* User cancelled */ });
}

async function regenerateLatex() {
  if (!uiStore.apiKeyValid) {
    ElMessage.error('请先设置并校验有效的 API Key。');
    return;
  }

  uiStore.setLoading(true);
  ElMessage.info('正在请求 AI 重新生成公式...');

  const prompt = `你是一个数学家，请根据下面的描述生成一个 LaTeX 公式。
描述: "${props.describe}"
请只返回 LaTeX 代码，不要包含任何额外的解释或代码块标记。`;

  try {
    let newLatex = '';
    await streamGenerate(
      {
        prompt: prompt,
        api_key: uiStore.apiKey,
        template: {
          title: "Generate LaTeX",
          rules: "Return only the LaTeX code.",
          role: "mathematician"
        }
      },
      (chunk) => {
        newLatex += chunk;
      }
    );

    const finalLatex = newLatex.trim();
    if (finalLatex) {
      const oldBlock = `[LATEX describe="${props.describe}"]${props.latex}[/LATEX]`;
      const newBlock = `[LATEX describe="${props.describe}"]${finalLatex}[/LATEX]`;
      editorStore.updateBlockContent({ oldBlock, newBlock });
      ElMessage.success('AI 已重新生成公式');
    } else {
      ElMessage.warning('AI未能生成有效内容。');
    }

  } catch (error) {
    console.error('Error regenerating LaTeX:', error);
    ElMessage.error(`AI 生成失败: ${error.message}`);
  } finally {
    uiStore.setLoading(false);
  }
}
</script>

<style scoped>
.latex-block-wrapper {
  border: 1px solid #444;
  border-radius: 5px;
  margin: 1em 0;
  background-color: #2c2c2c;
  overflow: hidden;
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
.title {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 70%;
}
.latex-content {
  padding: 1.5em;
  background-color: #f9f9f9;
  color: #000;
  font-size: 1.1em;
  overflow-x: auto;
  text-align: center;
}
</style>

