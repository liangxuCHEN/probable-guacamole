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

function handleFileUpload(event) {
  emit('fileUpload', event);
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
  <div class="bg-white rounded-xl p-8 shadow-custom mb-10">
    <div class="text-center mb-8">
      <div class="inline-flex items-center justify-center w-16 h-16 rounded-full bg-primary/10 text-primary mb-4">
        <img src="https://qiniu.yayaxueqin.cn/icon/erweima-blue-3.svg" alt="qrcode icon" class="w-6 h-6">
      </div>
      <h3 class="text-xl font-semibold text-neutral-600 mb-2">
        {{ t.uploadTitle }}
      </h3>
      <p class="text-neutral-400 max-w-md mx-auto">
        {{ t.uploadDesc }}
      </p>
    </div>

    <!-- QR Code Upload Button -->
    <div class="flex justify-center">
      <label for="qr-code-upload" class="cursor-pointer">
        <div class="bg-primary hover:bg-primary/90 text-white font-medium py-3 px-8 rounded-full shadow-md flex items-center transition-custom hover:shadow-lg">
          <img src="https://qiniu.yayaxueqin.cn/icon/xiangji.svg" alt="camera icon" class="w-5 h-5 mr-2">
          <span>{{ t.uploadBtnText }}</span>
        </div>
      </label>
      <input id="qr-code-upload" type="file" accept="image/*" class="hidden" @change="handleFileUpload">
    </div>

    <!-- Processing Animation -->
    <div v-if="showProcessingAnimation" class="mt-8 text-center">
      <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary mb-4"></div>
      <p class="text-neutral-500">{{ t.processingText }}</p>
    </div>

    <!-- Upload Preview -->
    <div v-if="showUploadPreview" class="mt-8 text-center">
      <div class="mb-4">
        <img :src="previewImageSrc" alt="Uploaded QR code" class="max-w-full h-auto rounded-lg shadow-md mx-auto">
      </div>
      <div class="flex justify-center space-x-4">
        <button @click="retakePhoto" class="bg-neutral-200 hover:bg-neutral-300 text-neutral-600 font-medium py-2 px-6 rounded-full flex items-center transition-custom">
          <img src="https://qiniu.yayaxueqin.cn/icon/redo-alt-solid.svg" alt="redo-alt icon" class="w-4 h-4 mr-1">
          <span>{{ t.retakeBtnText }}</span>
        </button>
        <button @click="confirmUpload" class="bg-primary hover:bg-primary/90 text-white font-medium py-2 px-6 rounded-full flex items-center shadow-md transition-custom hover:shadow-lg">
          <img src="https://qiniu.yayaxueqin.cn/icon/check-circle.svg" alt="check-circle icon" class="w-5 h-5 mr-1">
          <span>{{ t.confirmBtnText }}</span>
        </button>
      </div>
    </div>

    <!-- Image Cropper Section -->
    <div v-if="showCropperSection" class="mt-8">
      <div class="text-center mb-4">
        <h4 class="text-lg font-medium text-neutral-600 mb-2">
          {{ t.cropperTitle }}
        </h4>
        <p class="text-neutral-400 max-w-md mx-auto mb-4">
          {{ t.cropperDesc }}
        </p>
      </div>
      <div class="mb-4 relative">
        <div class="max-h-[70vh] overflow-hidden">
          <img id="cropper-image" src="" alt="Image to crop" class="max-w-full mx-auto">
        </div>
      </div>
      <div class="flex justify-center space-x-4">
        <button @click="cancelCrop" class="bg-neutral-200 hover:bg-neutral-300 text-neutral-600 font-medium py-2 px-6 rounded-full flex items-center transition-custom">
          <img src="https://qiniu.yayaxueqin.cn/icon/redo-alt-solid.svg" alt="cancel icon" class="w-4 h-4 mr-1">
          <span>{{ t.cancelCropText }}</span>
        </button>
        <button @click="cropAndScan" class="bg-primary hover:bg-primary/90 text-white font-medium py-2 px-6 rounded-full flex items-center shadow-md transition-custom hover:shadow-lg">
          <img src="https://qiniu.yayaxueqin.cn/icon/check-circle.svg" alt="crop icon" class="w-5 h-5 mr-1">
          <span>{{ t.cropBtnText }}</span>
        </button>
      </div>
    </div>
  </div>
</template>