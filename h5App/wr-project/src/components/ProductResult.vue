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
  <van-card class="product-result-card">
    <template #title>
      <!-- Not Activated Section -->
      <div v-if="showNotActivated" class="not-activated-section">
        <van-icon name="warning-o" size="36" color="#ff976a" />
        <h3 class="result-title">{{ t.notActivatedTitle }}</h3>
        <p class="result-desc">{{ t.notActivatedDesc }}</p>
      </div>
      
      <!-- Activated Section -->
      <div v-if="showActivated" class="activated-section">
        <van-icon name="checked" size="36" color="#07c160" />
        <h3 class="result-title">{{ t.activatedTitle }}</h3>
      </div>
    </template>
    
    <template #price>
      <!-- Product Info -->
      <div v-if="showActivated" class="product-info-section">
        <van-cell-group inset>
          <!-- Product ID -->
          <van-cell :title="t.resultProductIdLabel" :value="productInfo?.qrcode_id" />
          
          <!-- Name -->
          <van-cell :title="t.resultNameLabel" :value="productInfo?.name" />
          
          <!-- Email -->
          <van-cell :title="t.resultEmailLabel" :value="productInfo?.email" />
          
          <!-- Phone -->
          <van-cell :title="t.resultPhoneLabel" :value="productInfo?.phone || '-'" />
          
          <!-- Installer -->
          <van-cell :title="t.resultInstallerLabel" :value="productInfo?.installer || '-'" />
          
          <!-- Activation Date -->
          <van-cell 
            :title="t.resultActivationLabel" 
            :value="productInfo?.activation_date ? new Date(productInfo.activation_date).toISOString().split('T')[0] : '-'" 
          />
        </van-cell-group>
        
        <!-- Warranty Status -->
        <div v-if="productInfo" class="warranty-status">
          <van-notice-bar
            v-if="productInfo.under_warranty"
            color="#07c160"
            background="#e8f5e9"
            :text="t.resultWarrantyActive"
            left-icon="checked"
          >
            <template #right-icon>
              <span class="days-remaining" v-if="productInfo.warranty_end">
                {{ Math.ceil((new Date(productInfo.warranty_end) - new Date()) / (1000 * 60 * 60 * 24)) }} {{ t.resultDaysRemaining }}
              </span>
            </template>
          </van-notice-bar>
          
          <van-notice-bar
            v-else
            color="#ee0a24"
            background="#ffebee"
            :text="t.resultWarrantyExpired"
            left-icon="warning-o"
          />
        </div>
        
        <!-- Restart Button -->
        <div class="restart-button">
          <van-button plain @click="restart">
            {{ t.restartBtnText }}
          </van-button>
        </div>
      </div>
    </template>
  </van-card>
</template>

<style scoped>
.product-result-card {
  background-color: #ffffff;
  border-radius: 12px;
  margin-bottom: 20px;
  padding: 16px;
  box-shadow: 0 8px 12px rgba(0, 0, 0, 0.05);
}

.not-activated-section,
.activated-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 16px;
}

.result-title {
  font-size: 18px;
  font-weight: 600;
  color: #323233;
  margin: 12px 0 8px;
}

.result-desc {
  color: #969799;
  text-align: center;
  max-width: 300px;
  margin: 0 auto;
}

.product-info-section {
  margin-top: 16px;
}

.warranty-status {
  margin: 16px 0;
}

.days-remaining {
  font-size: 14px;
  font-weight: 500;
}

.restart-button {
  margin-top: 16px;
  display: flex;
  justify-content: center;
}
</style>