import MarkdownIt from 'markdown-it';
import katex from 'markdown-it-katex';
import plantuml from 'markdown-it-plantuml';
// 这是一个简化的自定义组件渲染方式
// 在一个大型项目中，你可能会用更复杂的方式来挂载 Vue 组件
import CodeBlock from '../components/editor/CodeBlock.vue';
import PlantUMLBlock from '../components/editor/PlantUMLBlock.vue';
import ImagePlaceholder from '../components/editor/ImagePlaceholder.vue';
import LatexBlock from '../components/editor/LatexBlock.vue';
import LinkBlock from '../components/editor/LinkBlock.vue'
import { h, render as vueRender } from 'vue';

const useCustomParser = (md) => {
    const defaultRender = md.renderer.rules.fence;

    md.renderer.rules.fence = (tokens, idx, options, env, self) => {
        const token = tokens[idx];
        // 此处可以添加对 [CODE] 标签的特殊处理逻辑
        // 但为了简单，我们用正则表达式在渲染前替换
        return defaultRender(tokens, idx, options, env, self);
    };
};

export function useMarkdownParser() {
    const md = new MarkdownIt({
        html: true,
        linkify: true,
        typographer: true,
    }).use(katex).use(plantuml).use(useCustomParser);

    const render = (markdownText) => {
        let text = markdownText;

        const escapeAttr = (str) => {
            return str.replace(/'/g, '&#39;').replace(/"/g, '&quot;');
        }

        // 1. 替换 [CODE] 标签
        text = text.replace(/\[CODE\s+language=([^,]+),\s+title="([^"]+)"\s+describe="([^"]+)"\]([\s\S]*?)\[\/CODE\]/g, (match, lang, title, desc, code) => {
            const props = { language: lang.trim(), title, describe: desc, code: code.trim(), matchCode:match.trim() };
            const propsJson = JSON.stringify(props);
            return `<div class="vue-component" data-component="CodeBlock" data-props='${escapeAttr(propsJson)}'></div>`;
        });
        
        // 2. 替换 [PLANTUML] 标签
        text = text.replace(/\[PLANTUML\s+type="([^"]+)"\s+describe="([^"]+)"\]([\s\S]*?)\[\/PLANTUML\]/g, (match, type, desc, code) => {
             const props = { type, describe: desc, code: code.trim(), matchCode:match.trim() };
             const propsJson = JSON.stringify(props);
             return `<div class="vue-component" data-component="PlantUMLBlock" data-props='${escapeAttr(propsJson)}'></div>`;
        });
        
        // 3. 替换 [IMAGE] 标签
        text = text.replace(/\[IMAGE\s+type="([^"]+)"\s+describe="([^"]+)"\s*\/\]/g, (match, type, desc) => {
             const props = { type, describe: desc, matchCode:match.trim() };
             const propsJson = JSON.stringify(props);
             return `<div class="vue-component" data-component="ImagePlaceholder" data-props='${escapeAttr(propsJson)}'></div>`;
        });

        // 4. 替换 [LATEX] 标签
        text = text.replace(/\[LATEX\s+describe="([^"]+)"\]([\s\S]*?)\[\/LATEX\]/g, (match, desc, code) => {
            console.log("match tex:", match)
             const props = { describe: desc, latex: code.trim(), matchCode:match.trim() };
             const propsJson = JSON.stringify(props);
             return `<div class="vue-component latex-component" data-component="LatexBlock" data-props='${escapeAttr(propsJson)}'></div>`;
        });

        // 5. 替换 [LINK] 标签
        text = text.replace(/\[LINK\s+title="([^"]+)"\s+describe="([^"]+)"\]([\s\S]*?)\[\/LINK\]/g, (match, title, desc, url) => {
             const props = { title, describe: desc, url: url.trim(), matchCode:match.trim() };
             const propsJson = JSON.stringify(props);
             return `<div class="vue-component" data-component="LinkBlock" data-props='${escapeAttr(propsJson)}'></div>`;
        });
        
        // 6. 渲染剩余的 Markdown
        const renderedHtml = md.render(text);

        // 异步挂载 Vue 组件 (这是一个简化的实现)
        setTimeout(() => {
            const componentsMap = {
                CodeBlock,
                PlantUMLBlock,
                ImagePlaceholder,
                LatexBlock,
                LinkBlock
            };

            document.querySelectorAll('.vue-component').forEach(el => {
                if (el.dataset.component && !el.hasChildNodes()) {
                    const componentName = el.dataset.component;
                    const props = JSON.parse(el.dataset.props);
                    const vnode = h(componentsMap[componentName], props);
                    vueRender(vnode, el);
                }
            });
        }, 100);

        return renderedHtml;
    };

    return { render };
}