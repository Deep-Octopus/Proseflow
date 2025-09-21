<template>
  <div class="link-block-wrapper">
    <div class="header">
      <span class="title" :title="describe">{{ title }}</span>
      <div class="actions">
        <el-button size="small" @click="editLink">编辑</el-button>
        <el-button size="small" type="primary" @click="openLink">跳转</el-button>
      </div>
    </div>
    <div class="link-content">
      <a :href="url" target="_blank" rel="noopener noreferrer">{{ url }}</a>
    </div>
  </div>
</template>

<script setup>
import { ElMessageBox } from 'element-plus';
import { onMounted } from 'vue';

const props = defineProps({
  title: String,
  describe: String,
  url: String,
  matchCode: String
});
onMounted(()=>{
    console.log(props)
})
function openLink() {
  window.open(props.url, '_blank', 'noopener,noreferrer');
}

function editLink() {
  ElMessageBox.prompt('请输入新的 URL 链接', '修改链接', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    inputValue: props.url,
  })
    .then(({ value }) => {
      // 在实际应用中，这里应该发出一个事件来更新状态
      console.log('New URL (not updated in state yet):', value);
      ElMessage.success('链接已更新（仅为演示）');
    })
    .catch(() => {
      // 用户取消
    });
}
</script>

<style scoped>
.link-block-wrapper {
  border: 1px solid #444;
  border-radius: 5px;
  margin: 1em 0;
  background-color: #2c2c2c;
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
.link-content {
  padding: 1em;
  word-break: break-all;
}
.link-content a {
  color: #409eff;
  text-decoration: none;
}
.link-content a:hover {
  text-decoration: underline;
}
</style>