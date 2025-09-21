import apiClient from './apiClient';

export async function validateApiKey(apiKey) {
  try {
    const response = await apiClient.post('/llm/validate', { api_key: apiKey });
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
}

export async function getPrompts() {
  try {
    const response = await apiClient.get('/prompts/');
    return response.data;
  } catch (error) {
     console.error('Failed to get prompts:', error);
     throw error.response ? error.response.data : error;
  }
}

export async function createPromptTemplate(templateData) {
  try {
    const response = await apiClient.post('/prompts/', templateData);
    return response.data;
  } catch (error) {
    console.error("Failed to create prompt template:", error);
    throw error; // 抛出错误以便 UI 层捕获
  }
}

export async function streamGenerate(params, onChunk) {
  const response = await fetch('/api/v1/llm/generate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'text/event-stream'
    },
    body: JSON.stringify(params),
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();

  while (true) {
    const { done, value } = await reader.read();
    if (done) {
      break;
    }
    
    const chunkStr = decoder.decode(value);
    const lines = chunkStr.split('\n');

    for (const line of lines) {
      if (line.startsWith('data: ')) {
        try {
          const jsonStr = line.substring(6);
          const data = JSON.parse(jsonStr);
          if (data.error) {
            throw new Error(data.error);
          }
          if (data.content) {
            onChunk(data.content);
          }
        } catch (e) {
          console.error("Failed to parse stream chunk:", line, e);
        }
      }
    }
  }
}
