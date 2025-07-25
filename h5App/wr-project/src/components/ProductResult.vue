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
          <van-cell :title="t.resultProductIdLabel" :label="productInfo?.qrcode_id" />
          
          <!-- Name -->
          <van-cell :title="t.resultNameLabel" :label="productInfo?.name" />
          
          <!-- Email -->
          <van-cell :title="t.resultEmailLabel" :label="productInfo?.email" />
          
          <!-- Phone -->
          <van-cell :title="t.resultPhoneLabel" :label="productInfo?.phone || '-'" />
          
          <!-- Installer -->
          <van-cell :title="t.resultInstallerLabel" :label="productInfo?.installer || '-'" />
          
          <!-- Activation Date -->
          <van-cell 
            :title="t.resultActivationLabel" 
            :label="productInfo?.activation_date ? new Date(productInfo.activation_date).toISOString().split('T')[0] : '-'"
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

/* 修改van-cell的label样式 */
:deep(.van-cell__label) {
  margin-top: 8px;
  color: #323233;
  font-size: 14px;
  line-height: 1.4;
  word-break: break-all;
  text-align: left;
}

/* 增加标题和内容的间距 */
:deep(.van-cell__title) {
  margin-bottom: 4px;
}

/* 确保单元格有足够的高度 */
:deep(.van-cell) {
  padding-top: 12px;
  padding-bottom: 12px;
}
</style>