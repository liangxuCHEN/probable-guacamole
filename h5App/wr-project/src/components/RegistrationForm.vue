<script setup>
import { defineProps, defineEmits } from 'vue';

const props = defineProps({
  t: {
    type: Object,
    required: true
  },
  productId: String,
  formData: Object,
  errors: Object,
  currentLang: String
});

const emit = defineEmits(['submitForm']);

function submitForm() {
  emit('submitForm');
}
</script>

<template>
  <div class="bg-white rounded-xl p-8 shadow-custom mb-10">
    <h3 class="text-xl font-semibold text-neutral-600 mb-6">
      {{ t.formTitle }}
    </h3>
    
    <form @submit.prevent="submitForm" class="space-y-6">
      <!-- Product ID (Readonly) -->
      <div>
        <label for="product-id" class="block text-sm font-medium text-neutral-500 mb-1">
          <span>{{ t.productIdLabel }}</span>
          <span class="text-primary ml-1">*</span>
        </label>
        <input type="text" id="product-id" v-model="productId" class="w-full px-4 py-2 border border-neutral-200 rounded-lg focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none transition-custom" readonly>
      </div>
      
      <!-- Name -->
      <div>
        <label for="name" class="block text-sm font-medium text-neutral-500 mb-1">
          <span>{{ t.nameLabel }}</span>
          <span class="text-primary ml-1">*</span>
        </label>
        <input type="text" id="name" v-model="formData.name" class="w-full px-4 py-2 border" :class="[errors.name ? 'border-red-300' : 'border-neutral-200', 'rounded-lg focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none transition-custom']" required>
        <p v-if="errors.name" class="mt-1 text-sm text-red-500 flex items-center">
          <img src="https://qiniu.yayaxueqin.cn/icon/fasfa-exclamation-circle.svg" alt="check-circle icon" class="w-5 h-5 mr-1">
          <span>{{ t.nameErrorText }}</span>
        </p>
      </div>
      
      <!-- Email -->
      <div>
        <label for="email" class="block text-sm font-medium text-neutral-500 mb-1">
          <span>{{ t.emailLabel }}</span>
          <span v-if="currentLang !== 'zh'" class="text-primary ml-1">*</span>
        </label>
        <input type="email" id="email" v-model="formData.email" class="w-full px-4 py-2 border" :class="[errors.email ? 'border-red-300' : 'border-neutral-200', 'rounded-lg focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none transition-custom']" :required="currentLang !== 'zh'">
        <p v-if="errors.email" class="mt-1 text-sm text-red-500 flex items-center">
          <img src="https://qiniu.yayaxueqin.cn/icon/fasfa-exclamation-circle.svg" alt="exclamation-circle icon" class="w-5 h-5 mr-1">
          <span>{{ t.emailErrorText }}</span>
        </p>
      </div>
      
      <!-- Country -->
      <div>
        <label for="country" class="block text-sm font-medium text-neutral-500 mb-1">
          <span>{{ t.countryLabel }}</span>
        </label>
        <input type="text" id="country" v-model="formData.country" class="w-full px-4 py-2 border border-neutral-200 rounded-lg focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none transition-custom">
      </div>
      
      <!-- City -->
      <div>
        <label for="city" class="block text-sm font-medium text-neutral-500 mb-1">
          <span>{{ t.cityLabel }}</span>
        </label>
        <input type="text" id="city" v-model="formData.city" class="w-full px-4 py-2 border border-neutral-200 rounded-lg focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none transition-custom">
      </div>
      
      <!-- Phone -->
      <div>
        <label for="phone" class="block text-sm font-medium text-neutral-500 mb-1">
          <span>{{ t.phoneLabel }}</span>
          <span v-if="currentLang === 'zh'" class="text-primary ml-1">*</span>
        </label>
        <input type="tel" id="phone" v-model="formData.phone" class="w-full px-4 py-2 border" :class="[errors.phone ? 'border-red-300' : 'border-neutral-200', 'rounded-lg focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none transition-custom']" :required="currentLang === 'zh'">
        <p v-if="errors.phone" class="mt-1 text-sm text-red-500 flex items-center">
          <img src="https://qiniu.yayaxueqin.cn/icon/fasfa-exclamation-circle.svg" alt="exclamation-circle icon" class="w-5 h-5 mr-1">
          <span>{{ t.phoneErrorText }}</span>
        </p>
      </div>
      
      <!-- Installer -->
      <div>
        <label for="installer" class="block text-sm font-medium text-neutral-500 mb-1">
          <span>{{ t.installerLabel }}</span>
          <span class="text-primary ml-1">*</span>
        </label>
        <input type="text" id="installer" v-model="formData.installer" class="w-full px-4 py-2 border" :class="[errors.installer ? 'border-red-300' : 'border-neutral-200', 'rounded-lg focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none transition-custom']" required>
        <p v-if="errors.installer" class="mt-1 text-sm text-red-500 flex items-center">
          <img src="https://qiniu.yayaxueqin.cn/icon/fasfa-exclamation-circle.svg" alt="exclamation-circle icon" class="w-5 h-5 mr-1">
          <span>{{ t.installerErrorText }}</span>
        </p>
      </div>
      
      <!-- Submit Button -->
      <div class="pt-4">
        <button type="submit" class="w-full bg-primary hover:bg-primary/90 text-white font-medium py-3 px-6 rounded-lg shadow-md transition-custom hover:shadow-lg flex items-center justify-center">
          <span>{{ t.submitBtnText }}</span>
        </button>
      </div>
    </form>
  </div>
</template>