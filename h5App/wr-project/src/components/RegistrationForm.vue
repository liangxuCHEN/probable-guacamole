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
  <van-card class="registration-form-card">
    <template #title>
      <h3 class="form-title">{{ t.formTitle }}</h3>
    </template>
    
    <template #price>
      <van-form @submit="submitForm">
        <!-- Product ID (Readonly) -->
        <van-field
          :model-value="productId"
          :label="t.productIdLabel"
          readonly
          required
        />
        
        <!-- Name -->
        <van-field
          v-model="formData.name"
          :label="t.nameLabel"
          :placeholder="t.nameLabel"
          :error="errors.name"
          :error-message="errors.name ? t.nameErrorText : ''"
          required
        />
        
        <!-- Email -->
        <van-field
          v-model="formData.email"
          :label="t.emailLabel"
          :placeholder="t.emailLabel"
          :error="errors.email"
          :error-message="errors.email ? t.emailErrorText : ''"
          :required="currentLang !== 'zh'"
        />
        
        <!-- Country -->
        <van-field
          v-model="formData.country"
          :label="t.countryLabel"
          :placeholder="t.countryLabel"
        />
        
        <!-- City -->
        <van-field
          v-model="formData.city"
          :label="t.cityLabel"
          :placeholder="t.cityLabel"
        />
        
        <!-- Phone -->
        <van-field
          v-model="formData.phone"
          :label="t.phoneLabel"
          :placeholder="t.phoneLabel"
          :error="errors.phone"
          :error-message="errors.phone ? t.phoneErrorText : ''"
          :required="currentLang === 'zh'"
          type="tel"
        />
        
        <!-- Installer -->
        <van-field
          v-model="formData.installer"
          :label="t.installerLabel"
          :placeholder="t.installerLabel"
          :error="errors.installer"
          :error-message="errors.installer ? t.installerErrorText : ''"
          required
        />
        
        <!-- Submit Button -->
        <div class="submit-button-container">
          <van-button type="primary" block round native-type="submit">
            {{ t.submitBtnText }}
          </van-button>
        </div>
      </van-form>
    </template>
  </van-card>
</template>

<style scoped>
.registration-form-card {
  background-color: #ffffff;
  border-radius: 12px;
  margin-bottom: 20px;
  padding: 16px;
  box-shadow: 0 8px 12px rgba(0, 0, 0, 0.05);
}

.form-title {
  font-size: 18px;
  font-weight: 600;
  color: #323233;
  margin-bottom: 16px;
}

.submit-button-container {
  margin-top: 24px;
  padding: 0 16px;
}
</style>
