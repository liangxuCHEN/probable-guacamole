<script setup>
import { defineProps, defineEmits } from 'vue';

const props = defineProps({
  currentLang: {
    type: String,
    required: true
  }
});

const emit = defineEmits(['switchLanguage']);

function switchLanguage(lang) {
  emit('switchLanguage', lang);
}
</script>

<template>
  <div class="fixed top-4 right-4 z-50">
    <div class="bg-white rounded-full shadow-lg p-1 flex">
      <button 
        :class="['px-3 py-1 rounded-full text-sm font-medium transition-custom', 
                currentLang === 'en' ? 'text-primary bg-primary/10' : 'text-neutral-500']"
        @click="switchLanguage('en')">
        EN
      </button>
      <button 
        :class="['px-3 py-1 rounded-full text-sm font-medium transition-custom', 
                currentLang === 'zh' ? 'text-primary bg-primary/10' : 'text-neutral-500']"
        @click="switchLanguage('zh')">
        中文
      </button>
    </div>
  </div>
</template>