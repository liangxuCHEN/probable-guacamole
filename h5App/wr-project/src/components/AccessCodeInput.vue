<script setup>
import { ref, defineProps, defineEmits } from 'vue';
import request from '../utils/request';
import { showNotify } from 'vant';

const props = defineProps({
  t: {
    type: Object,
    required: true
  },
  currentLang: {
    type: String,
    required: true
  }
});

const emit = defineEmits(['accessCodeValidated']);

const accessCode = ref('');
const isLoading = ref(false);
const errorMessage = ref('');

// 验证访问码
function validateAccessCode() {
  if (!accessCode.value.trim()) {
    errorMessage.value = props.t.accessCodeRequired || '请输入访问码';
    return;
  }

  isLoading.value = true;
  errorMessage.value = '';

  // 请求后端验证访问码
  request.post('/api/code_api', { 
    access_code: accessCode.value,
    lang: props.currentLang // 带上当前语言变量
  })
    .then(response => {
      isLoading.value = false;
      
      if (response.data.status === 'success') {
        // 访问码有效，通知父组件
        emit('accessCodeValidated', accessCode.value);
      } else {
        // 访问码无效，显示错误信息
        errorMessage.value = props.t.invalidAccessCode || '访问码无效，请重新输入';
        showErrorToast(errorMessage.value);
      }
    })
    .catch(error => {
      isLoading.value = false;
      errorMessage.value = props.t.processingError || '处理请求时出错，请重试';
      showErrorToast(errorMessage.value);
      console.error('Error validating access code:', error);
    });
}

// 显示错误提示
function showErrorToast(message) {
  showNotify({
    message: message,
    type: 'danger',
    duration: 3000
  });
}
</script>

<template>
  <div class="access-code-container">
    <van-icon name="lock" size="36" color="#1989fa" />
    <h3 class="access-title">{{ t.accessErrorTitle }}</h3>
    <p class="access-desc">{{ t.accessErrorMessage }}</p>
    
    <van-field
      v-model="accessCode"
      :label="t.accessCodeLabel"
      :placeholder="t.accessCodePlaceholder"
      :error="!!errorMessage"
      :error-message="errorMessage"
      @keyup.enter="validateAccessCode"
    />
    
    <div class="button-container">
      <van-button 
        type="primary" 
        block 
        :loading="isLoading"
        :disabled="isLoading" 
        @click="validateAccessCode"
      >
        {{ t.submitAccessCodeText }}
      </van-button>
    </div>
  </div>
</template>

<style scoped>
.access-code-container {
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 8px 12px rgba(0, 0, 0, 0.05);
  margin-bottom: 20px;
}

.access-title {
  font-size: 18px;
  font-weight: 600;
  color: #323233;
  margin: 12px 0 0;
}

.access-desc {
  color: #969799;
  text-align: center;
  max-width: 300px;
  margin: 0 auto;
}

.button-container {
  width: 100%;
  margin-top: 16px;
}
</style>