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
  <div class="language-switcher">
    <van-button-group class="lang-button-group">
      <van-button 
        :type="currentLang === 'en' ? 'primary' : 'default'" 
        size="small"
        @click="switchLanguage('en')">
        EN
      </van-button>
      <van-button 
        :type="currentLang === 'zh' ? 'primary' : 'default'" 
        size="small"
        @click="switchLanguage('zh')">
        中文
      </van-button>
    </van-button-group>
  </div>
</template>

<style scoped>
.language-switcher {
  position: fixed;
  top: 16px;
  right: 16px;
  z-index: 100;
}

.lang-button-group {
  background-color: #fff;
  border-radius: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}
</style>
