<template>
  <div class="header-content">
    <div class="logo">
      <h1>Proseflow</h1>
    </div>
    <div class="controls">
      <el-input
        v-model="apiKey"
        placeholder="请输入硅基流动 API Key"
        class="api-key-input"
        clearable
      >
        <template #append>
          <el-button @click="validateKey" :loading="uiStore.isValidatingKey">校验</el-button>
        </template>
      </el-input>
      <!-- 新增的创建模板按钮 -->
      <el-button @click="showTemplateDialog = true" type="primary" plain class="new-template-btn">
        新建模板
      </el-button>

      <el-select v-model="selectedPrompt" placeholder="选择文章模板" class="control-item">
        <el-option
          v-for="item in promptOptions"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        />
      </el-select>

      <el-input
        v-model="topic"
        placeholder="输入文章主题"
        class="control-item topic-input"
        clearable
      />

      <el-button
        type="primary"
        @click="generateArticle"
        :loading="uiStore.isGenerating"
        :disabled="!isReadyToGenerate"
      >
        生成文章
      </el-button>
    </div>
    <div class="actions">
       <el-dropdown @command="handleExport">
        <el-button type="success">
          导出 <el-icon class="el-icon--right"><arrow-down /></el-icon>
        </el-button>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item command="md">Markdown (.md)</el-dropdown-item>
            <el-dropdown-item command="pdf">PDF (.pdf)</el-dropdown-item>
            <el-dropdown-item command="docx">Word (.docx)</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </div>
  <!-- 新增的创建模板对话框 -->
  <el-dialog v-model="showTemplateDialog" title="创建新的提示词模板" width="500px">
    <el-form :model="newTemplateForm" label-position="top">
      <el-form-item label="模板标题">
        <el-input v-model="newTemplateForm.title" placeholder="例如：技术博客、周报生成器"></el-input>
      </el-form-item>
      <el-form-item label="内容 (Content)">
        <el-input
            v-model="newTemplateForm.content"
            type="textarea"
            :rows="5"
            placeholder="定义 AI 在生成内容时扮演的角色和必须遵守的规则。例如：你是一位资深的前端开发工程师，你的写作风格必须严谨、专业，多使用代码示例。"></el-input>
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="showTemplateDialog = false">取消</el-button>
        <el-button type="primary" @click="handleSaveTemplate" :loading="isSaving">
          保存
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { ElMessage } from 'element-plus';
import { ArrowDown } from '@element-plus/icons-vue';
import { useUiStore } from '@/store/uiStore.js';
import { useEditorStore } from '@/store/editorStore.js';
import { streamGenerate, validateApiKey, getPrompts, createPromptTemplate } from '@/services/llmService.js';
import { exportDocument } from '@/services/apiClient.js';
import { saveAs } from 'file-saver';


const uiStore = useUiStore();
const editorStore = useEditorStore();

const apiKey = ref('');
const topic = ref('');
const selectedPrompt = ref('通用博文');
const promptOptions = ref([]);
// 创建模板对话框的状态
const showTemplateDialog = ref(false);
const isSaving = ref(false);
const newTemplateForm = ref({
  title: '',
  content: ''
});


const isReadyToGenerate = computed(() => {
  return apiKey.value && topic.value && selectedPrompt.value && !uiStore.isGenerating;
});

onMounted(()=>{initPrompt()});

async function initPrompt() {
  try {
    const prompts = await getPrompts();
    promptOptions.value = prompts.map(p => ({ label: p.title, value: p.title }));
  } catch (error) {
    ElMessage.error('获取提示词模板失败');
  }
}


async function validateKey() {
  if (!apiKey.value) {
    ElMessage.warning('请输入 API Key');
    return;
  }
  uiStore.isValidatingKey = true;
  try {
    const response = await validateApiKey(apiKey.value);
    ElMessage.success(response.message || 'API Key 校验成功！');
  } catch (error) {
    ElMessage.error(error.detail || 'API Key 无效');
  } finally {
    uiStore.isValidatingKey = false;
  }
}

async function generateArticle() {
  if (!isReadyToGenerate.value) return;

  uiStore.setLoading(true);
  editorStore.setContent('');

  const params = {
    api_key: apiKey.value,
    topic: topic.value,
    article_type: selectedPrompt.value, // 使用模板标题作为文章类型
    prompt_template: selectedPrompt.value
  };

  try {
    await streamGenerate(params, (chunk) => {
      editorStore.appendContent(chunk);
    });
  } catch (error) {
    ElMessage.error('生成文章时出错');
    console.error(error);
  } finally {
    uiStore.setLoading(false);
  }
}

async function handleExport(format) {
    if (!editorStore.content) {
        ElMessage.warning('没有内容可以导出');
        return;
    }
    try {
        const response = await exportDocument(editorStore.content, format);
        const blob = new Blob([response.data], { type: response.headers['content-type'] });
        saveAs(blob, `export.${format}`);
        ElMessage.success(`成功导出为 ${format.toUpperCase()}`);
    } catch (error) {
        ElMessage.error(`导出失败: ${error.detail || error.message}`);
    }
}

// 保存新模板的逻辑
async function handleSaveTemplate() {
  if (!newTemplateForm.value.title || !newTemplateForm.value.content) {
    ElMessage.warning('所有字段均为必填项。');
    return;
  }

  isSaving.value = true;
  try {
    const createdTemplate = await createPromptTemplate(newTemplateForm.value);
    ElMessage.success(`模板 "${createdTemplate.title}" 创建成功！`);
    uiStore.triggerPromptRefresh(uiStore.promptRefreshTrigger+1); // 触发刷新
    showTemplateDialog.value = false;
    // 清空表单
    newTemplateForm.value = { title: '', content: '' };
    await initPrompt()
  } catch (error) {
    console.error("Error creating template:", error);
    ElMessage.error('创建模板失败，请稍后重试。');
  } finally {
    isSaving.value = false;
  }
}
</script>

<style scoped>
.header-content {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.logo h1 {
  font-size: 1.5rem;
  margin: 0;
  color: var(--el-text-color-primary);
}
.controls {
  display: flex;
  align-items: center;
  gap: 15px;
}
.api-key-input {
  width: 350px;
}
.topic-input {
  width: 250px;
}
.control-item {
  min-width: 150px;
}
.actions {
  display: flex;
  align-items: center;
}
</style>
