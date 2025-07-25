<script setup>
import { ref, defineProps, defineEmits } from 'vue';

// 添加本地响应式变量，用于控制预览状态
const localPreviewImageSrc = ref('');
const localShowUploadPreview = ref(false);

const props = defineProps({
  t: {
    type: Object,
    required: true
  },
  showProcessingAnimation: Boolean,
  showUploadPreview: Boolean,
  previewImageSrc: String
});

// 监听props变化，同步到本地变量
function updateLocalState() {
  localPreviewImageSrc.value = props.previewImageSrc || '';
  localShowUploadPreview.value = props.showUploadPreview || false;
}

// 初始化本地状态
updateLocalState();

const emit = defineEmits([
  'fileUpload', 
  'retakePhoto', 
  'confirmUpload'
]);

function handleFileUpload(file) {
  // 处理文件上传并更新本地预览状态
  const reader = new FileReader();
  reader.onload = (e) => {
    localPreviewImageSrc.value = e.target.result;
    localShowUploadPreview.value = true;
  };
  reader.readAsDataURL(file.file);
  
  // Vant的Uploader组件传递的是文件对象，而不是事件对象
  // 创建一个模拟的事件对象，包含files属性
  const mockEvent = {
    target: {
      files: [file.file]
    }
  };
  emit('fileUpload', mockEvent);
}

function retakePhoto() {
  // 直接在组件内部处理重拍逻辑
  localPreviewImageSrc.value = '';
  localShowUploadPreview.value = false;
  emit('retakePhoto');
}

function confirmUpload() {
  emit('confirmUpload');
}

// 移除裁剪相关的函数
</script>

<template>
  <div class="qr-uploader-container">
    <van-icon name="qr" size="36" color="#1989fa" />
    <h3 class="uploader-title">{{ t.uploadTitle }}</h3>
    <p class="uploader-desc">{{ t.uploadDesc }}</p>
    
    <!-- QR Code Upload Button -->
    <div class="button-container">
      <van-uploader class="custom-uploader" :after-read="handleFileUpload" accept="image/*">
        <van-button type="primary" icon="photograph" block round>
          {{ t.uploadBtnText }}
        </van-button>
      </van-uploader>
    </div>

    <!-- Processing Animation -->
    <div v-if="showProcessingAnimation" class="processing-container">
      <van-loading type="spinner" color="#1989fa" size="24px" />
      <p class="processing-text">{{ t.processingText }}</p>
    </div>

    <!-- Upload Preview -->
    <div v-if="showUploadPreview || localShowUploadPreview" class="preview-container">
      <div class="preview-image-container">
        <van-image :src="localPreviewImageSrc" alt="Uploaded QR code" fit="contain" />
      </div>
      <div class="button-container">
        <van-button plain @click="retakePhoto" icon="replay">
          {{ t.retakeBtnText }}
        </van-button>
        <van-button type="primary" @click="confirmUpload" icon="success">
          {{ t.confirmBtnText }}
        </van-button>
      </div>
    </div>

    <!-- 移除裁剪相关的模板 -->
  </div>
</template>

<style scoped>
.qr-uploader-container {
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

.uploader-title {
  font-size: 18px;
  font-weight: 600;
  color: #323233;
  margin: 12px 0 0;
}

.uploader-desc {
  color: #969799;
  text-align: center;
  max-width: 300px;
  margin: 0 auto;
}

.button-container {
  width: 100%;
  margin-top: 16px;
  display: flex;
  justify-content: center;
  gap: 12px;
  padding: 0 16px;
}

.custom-uploader {
  width: 100%;
  display: block;
}

.button-container :deep(.van-uploader) {
  width: 100%;
  display: block;
}

.button-container :deep(.van-uploader__wrapper) {
  width: 100%;
  display: block;
}

.button-container :deep(.van-button) {
  width: 100% !important;
  display: block;
}

.processing-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}

.processing-text {
  margin-top: 12px;
  color: #969799;
}

.preview-container {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.preview-image-container {
  width: 100%;
  margin-bottom: 16px;
  border-radius: 8px;
  overflow: hidden;
}

/* 移除裁剪相关的样式 */
</style>