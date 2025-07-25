<script setup>
import { ref, defineProps, defineEmits } from 'vue';

const props = defineProps({
  t: {
    type: Object,
    required: true
  },
  showProcessingAnimation: Boolean,
  showUploadPreview: Boolean,
  showCropperSection: Boolean,
  previewImageSrc: String
});

const emit = defineEmits([
  'fileUpload', 
  'retakePhoto', 
  'confirmUpload', 
  'cancelCrop', 
  'cropAndScan'
]);

function handleFileUpload(file) {
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
  emit('retakePhoto');
}

function confirmUpload() {
  emit('confirmUpload');
}

function cancelCrop() {
  emit('cancelCrop');
}

function cropAndScan() {
  emit('cropAndScan');
}
</script>

<template>
  <van-card class="qr-uploader-card">
    <template #title>
      <div class="uploader-header">
        <van-icon name="qr" size="36" color="#1989fa" />
        <h3 class="uploader-title">{{ t.uploadTitle }}</h3>
        <p class="uploader-desc">{{ t.uploadDesc }}</p>
      </div>
    </template>
    
    <template #price>
      <!-- QR Code Upload Button -->
      <div class="upload-button-container">
        <van-uploader :after-read="handleFileUpload" accept="image/*">
          <van-button type="primary" icon="photograph" round>
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
      <div v-if="showUploadPreview" class="preview-container">
        <div class="preview-image-container">
          <van-image :src="previewImageSrc" alt="Uploaded QR code" fit="contain" />
        </div>
        <div class="preview-buttons">
          <van-button plain @click="retakePhoto" icon="replay">
            {{ t.retakeBtnText }}
          </van-button>
          <van-button type="primary" @click="confirmUpload" icon="success">
            {{ t.confirmBtnText }}
          </van-button>
        </div>
      </div>

      <!-- Image Cropper Section -->
      <div v-if="showCropperSection" class="cropper-container">
        <div class="cropper-header">
          <h4 class="cropper-title">{{ t.cropperTitle }}</h4>
          <p class="cropper-desc">{{ t.cropperDesc }}</p>
        </div>
        <div class="cropper-image-container">
          <img id="cropper-image" src="" alt="Image to crop">
        </div>
        <div class="cropper-buttons">
          <van-button plain @click="cancelCrop" icon="close">
            {{ t.cancelCropText }}
          </van-button>
          <van-button type="primary" @click="cropAndScan" icon="success">
            {{ t.cropBtnText }}
          </van-button>
        </div>
      </div>
    </template>
  </van-card>
</template>

<style scoped>
.qr-uploader-card {
  background-color: #ffffff;
  border-radius: 12px;
  margin-bottom: 20px;
  padding: 16px;
  box-shadow: 0 8px 12px rgba(0, 0, 0, 0.05);
}

.uploader-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 20px;
}

.uploader-title {
  font-size: 18px;
  font-weight: 600;
  color: #323233;
  margin: 12px 0 8px;
}

.uploader-desc {
  color: #969799;
  text-align: center;
  max-width: 300px;
  margin: 0 auto;
}

.upload-button-container {
  display: flex;
  justify-content: center;
  margin: 16px 0;
}

.processing-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 20px;
}

.processing-text {
  margin-top: 12px;
  color: #969799;
}

.preview-container {
  margin-top: 20px;
}

.preview-image-container {
  margin-bottom: 16px;
  border-radius: 8px;
  overflow: hidden;
}

.preview-buttons {
  display: flex;
  justify-content: center;
  gap: 12px;
}

.cropper-container {
  margin-top: 20px;
}

.cropper-header {
  text-align: center;
  margin-bottom: 16px;
}

.cropper-title {
  font-size: 16px;
  font-weight: 500;
  color: #323233;
  margin-bottom: 8px;
}

.cropper-desc {
  color: #969799;
  margin-bottom: 16px;
}

.cropper-image-container {
  max-height: 70vh;
  overflow: hidden;
  margin-bottom: 16px;
}

.cropper-buttons {
  display: flex;
  justify-content: center;
  gap: 12px;
}
</style>
