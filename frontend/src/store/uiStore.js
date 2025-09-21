import { defineStore } from 'pinia';

export const useUiStore = defineStore('ui', {
  state: () => ({
    apiKey: '',
    apiKeyValid: false,
    isLoading: false,
    promptRefreshTrigger: 0, // Add a trigger state for reactivity
  }),
  actions: {
    setApiKey(key) {
      this.apiKey = key;
    },
    setApiKeyValid(isValid) {
      this.apiKeyValid = isValid;
    },
    setLoading(loading) {
      this.isLoading = loading;
    },
    // Action to increment the trigger, which other components can watch
    triggerPromptRefresh(promptRefreshTrigger) {
      this.promptRefreshTrigger = promptRefreshTrigger;
    },
  },
});