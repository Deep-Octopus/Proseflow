import axios from 'axios';

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

export async function exportDocument(markdown_content, export_format) {
    return apiClient.post('/export', {
        markdown_content,
        export_format
    }, {
        responseType: 'blob' // 关键：告诉 axios 期望接收二进制数据
    });
}


export default apiClient;
