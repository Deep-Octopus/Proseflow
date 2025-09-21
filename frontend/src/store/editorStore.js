import { defineStore } from 'pinia';

export const useEditorStore = defineStore('editor', {
  state: () => ({
    content: `# 欢迎使用 Proseflow

这是一个智能化的 Markdown 编辑器。

1.  在上方输入您的 **API Key** 并点击 **校验**。
2.  选择一个 **文章模板**，比如“技术教程”。
3.  输入您想写的 **文章主题**，例如“如何学习 Vue 3”。
4.  点击 **生成文章**，然后见证奇迹！

您将看到 AI 生成的内容以打字机的方式出现在这里。

---

### 智能块示例

AI 可能会生成类似下面的特殊占位符，您可以与它们交互：

**图片占位符：**
[IMAGE type="概念图" describe="一个展示 Vue 3 核心概念（响应式、组件、指令）的思维导图"/]

**代码块：**
[CODE language=javascript, title="Vue 3 简单组件" describe="一个展示如何用组合式 API 创建响应式计数器的 Vue 组件"]
import { ref } from 'vue';

export default {
  setup() {
    const count = ref(0);

    function increment() {
      count.value++;
    }

    return {
      count,
      increment
    };
  }
}
[/CODE]

**图表示例：**
[PLANTUML type="时序图" describe="用户点击按钮后，Vue 3 的响应式系统如何更新 DOM 的过程"]
@startuml
actor User
participant Component
participant "Reactivity System"
participant "Virtual DOM"
participant DOM

User -> Component: Clicks button
Component -> "Reactivity System": Updates state (e.g., count.value++)
"Reactivity System" -> Component: Triggers re-render
Component -> "Virtual DOM": Generates new VNode tree
"Virtual DOM" -> "Virtual DOM": Diffs old and new trees
"Virtual DOM" -> DOM: Patches the actual DOM
@enduml
[/PLANTUML]

**公式示例 (LATEX):**
[LATEX describe="二次方程求根公式"]
x = \\frac{-b \\pm \\sqrt{b^2-4ac}}{2a}
[/LATEX]

**链接示例：**
[LINK title="Vue 3 官方文档" describe="指向 Vue 3 官方文档的链接，是学习 Vue 最权威的资源"]https://vuejs.org/[/LINK]
`,
  }),
  actions: {
    setContent(newContent) {
      this.content = newContent;
    },
    appendContent(chunk) {
      this.content += chunk;
    },
    /**
     * 更新一个智能块的内容
     * @param {{ oldBlock: string, newBlock: string }} payload
     */
    updateBlockContent({ oldBlock, newBlock }) {
      console.log("old",oldBlock)
      console.log("new",newBlock)
      if (this.content.includes(oldBlock)) {
        this.content = this.content.replace(oldBlock, newBlock);
      } else {
        // 添加一个警告，以防找不到要替换的内容
        console.warn(
          "updateBlockContent failed: could not find old block.",
          { oldBlock, newBlock }
        );
      }
    },
  },
});

