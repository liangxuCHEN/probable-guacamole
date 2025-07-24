<script setup>
import { defineProps, defineEmits } from 'vue';

const props = defineProps({
  t: {
    type: Object,
    required: true
  },
  showNotActivated: Boolean,
  showActivated: Boolean,
  productInfo: Object
});

const emit = defineEmits(['restart']);

function restart() {
  emit('restart');
}
</script>

<template>
  <div class="bg-white rounded-xl p-8 shadow-custom mb-10">
    <div v-if="showNotActivated" class="text-center mb-6">
      <div class="inline-flex items-center justify-center w-16 h-16 rounded-full bg-secondary/10 text-secondary mb-4">
        <img src="https://qiniu.yayaxueqin.cn/icon/fasfa-exclamation-triangle.svg" alt="exclamation" class="w-9 h-9">
      </div>
      <h3 class="text-xl font-semibold text-neutral-600 mb-2">
        {{ t.notActivatedTitle }}
      </h3>
      <p class="text-neutral-400 max-w-md mx-auto">
        {{ t.notActivatedDesc }}
      </p>
    </div>
    
    <div v-if="showActivated">
      <div class="text-center mb-6">
        <div class="inline-flex items-center justify-center w-16 h-16 rounded-full bg-green-100 text-green-500 mb-4">
          <img src="https://qiniu.yayaxueqin.cn/icon/circle-check-grenn.svg" alt="check-circle" class="text-2xl">
        </div>
        <h3 class="text-xl font-semibold text-neutral-600 mb-2">
          {{ t.activatedTitle }}
        </h3>
      </div>
      
      <div class="bg-neutral-50 rounded-lg p-6 mb-6">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- Product ID -->
          <div>
            <p class="text-sm text-neutral-400 mb-1">
              <span>{{ t.resultProductIdLabel }}</span>
            </p>
            <p class="font-medium text-neutral-600">{{ productInfo?.qrcode_id }}</p>
          </div>
          
          <!-- Name -->
          <div>
            <p class="text-sm text-neutral-400 mb-1">
              <span>{{ t.resultNameLabel }}</span>
            </p>
            <p class="font-medium text-neutral-600">{{ productInfo?.name }}</p>
          </div>
          
          <!-- Email -->
          <div>
            <p class="text-sm text-neutral-400 mb-1">
              <span>{{ t.resultEmailLabel }}</span>
            </p>
            <p class="font-medium text-neutral-600">{{ productInfo?.email }}</p>
          </div>
          
          <!-- Phone -->
          <div>
            <p class="text-sm text-neutral-400 mb-1">
              <span>{{ t.resultPhoneLabel }}</span>
            </p>
            <p class="font-medium text-neutral-600">{{ productInfo?.phone || '-' }}</p>
          </div>
          
          <!-- Installer -->
          <div>
            <p class="text-sm text-neutral-400 mb-1">
              <span>{{ t.resultInstallerLabel }}</span>
            </p>
            <p class="font-medium text-neutral-600">{{ productInfo?.installer || '-' }}</p>
          </div>

          <!-- Activation Date -->
          <div>
            <p class="text-sm text-neutral-400 mb-1">
              <span>{{ t.resultActivationLabel }}</span>
            </p>
            <p class="font-medium text-neutral-600">{{ productInfo?.activation_date ? new Date(productInfo.activation_date).toISOString().split('T')[0] : '-' }}</p>
          </div>
        </div>
      </div>
      
      <div v-if="productInfo" class="mb-6">
        <div v-if="productInfo.under_warranty" class="bg-green-50 border border-green-200 rounded-lg p-4 text-center">
          <div class="flex items-center justify-center text-green-600 mb-2">
            <img src="https://qiniu.yayaxueqin.cn/icon/check-circle.svg" alt="check-circle icon" class="w-5 h-5 mr-1">
            <span class="font-medium">{{ t.resultWarrantyActive }}</span>
          </div>
          <p class="text-neutral-600" v-if="productInfo.warranty_end">
            {{ Math.ceil((new Date(productInfo.warranty_end) - new Date()) / (1000 * 60 * 60 * 24)) }} {{ t.resultDaysRemaining }}
          </p>
        </div>
        <div v-else class="bg-red-50 border border-red-200 rounded-lg p-4 text-center">
          <div class="flex items-center justify-center text-red-600 mb-2">
            <img src="https://qiniu.yayaxueqin.cn/icon/fasfa-exclamation-circle.svg" alt="exclamation-circle icon" class="w-5 h-5 mr-1">
            <span class="font-medium">{{ t.resultWarrantyExpired }}</span>
          </div>
        </div>
      </div>
      
      <div class="flex justify-center">
        <button @click="restart" class="bg-neutral-200 hover:bg-neutral-300 text-neutral-600 font-medium py-2 px-6 rounded-full transition-custom">
          <span>{{ t.restartBtnText }}</span>
        </button>
      </div>
    </div>
  </div>
</template>