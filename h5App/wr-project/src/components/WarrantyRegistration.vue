<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { showToast, showNotify } from 'vant';
import request from '../utils/request';
import jsQR from 'jsqr';
// 移除cropperjs导入
import LanguageSwitcher from './LanguageSwitcher.vue';
import QrCodeUploader from './QrCodeUploader.vue';
import RegistrationForm from './RegistrationForm.vue';
import ProductResult from './ProductResult.vue';
import AccessCodeInput from './AccessCodeInput.vue';

// Language data
const translations = {
  en: {
    title: "Product Warranty Registration",
    subtitle: "Register your product to activate warranty and receive support services",
    carTitle: "Batteries Series",
    carDesc: "Experience superior performance and reliability",
    uploadTitle: "Scan Product QR Code",
    uploadDesc: "Take a photo of your product's QR code to begin the warranty registration process",
    uploadBtnText: "Take Photo",
    processingText: "Processing QR code...",
    retakeBtnText: "Retake",
    confirmBtnText: "Confirm",
    formTitle: "Product Registration Form",
    productIdLabel: "Product ID",
    nameLabel: "Full Name",
    emailLabel: "Email Address",
    countryLabel: "Country",
    cityLabel: "City",
    phoneLabel: "Phone Number",
    installerLabel: "Installer",
    submitBtnText: "Submit Registration",
    nameErrorText: "Please enter your full name",
    emailErrorText: "Please enter a valid email address",
    phoneErrorText: "Please enter a valid phone number",
    installerErrorText: "Please enter installer information",
    notActivatedTitle: "Product Not Activated",
    notActivatedDesc: "This product has not been registered yet. Please fill out the form below to activate warranty.",
    activatedTitle: "Product Warranty Information",
    resultProductIdLabel: "Product ID",
    resultNameLabel: "Registered Name",
    resultEmailLabel: "Email Address",
    resultPhoneLabel: "Phone Number",
    resultActivationLabel: "Activation Date",
    resultInstallerLabel: "Installer",
    resultWarrantyStatusLabel: "Warranty Status",
    resultWarrantyExpired: "Your warranty has expired",
    resultWarrantyActive: "Your warranty is active",
    resultDaysRemaining: "days remaining",
    restartBtnText: "Scan Another QR Code",
    toastMessage: "Registration submitted successfully!",
    footerText: "© 2023 Premium Vehicle Batteries Warranty System. All rights reserved.",
    qrCodeNotDetected: "No QR code detected. Please try another image.",
    processingError: "Error processing image. Please try again.",
    imageLoadError: "Failed to load image. Please try again.",
    cropperTitle: "Select QR Code Area",
    cropperDesc: "Your image is large. Please select the area containing the QR code.",
    cropBtnText: "Crop & Scan",
    cancelCropText: "Cancel",
    accessErrorTitle: "Access Denied",
    accessErrorMessage: "You need a valid access code to view this page.",
    invalidAccessCode: "Invalid access code. Please try again.",
    backBtnText: "Back to Home",
    accessCodeLabel: "Access Code",
    accessCodePlaceholder: "Enter access code",
    submitAccessCodeText: "Submit"
  },
  zh: {
    title: "产品保修注册",
    subtitle: "注册您的产品以激活保修并获得支持服务",
    carTitle: "电池系列",
    carDesc: "体验卓越的性能和可靠性",
    uploadTitle: "扫描产品二维码",
    uploadDesc: "拍摄产品二维码照片以开始保修注册流程",
    uploadBtnText: "拍照上传",
    processingText: "正在处理二维码...",
    retakeBtnText: "重拍",
    confirmBtnText: "确认",
    formTitle: "产品注册表单",
    productIdLabel: "产品ID",
    nameLabel: "姓名",
    emailLabel: "电子邮箱",
    countryLabel: "省份",
    cityLabel: "地址",
    phoneLabel: "电话号码",
    installerLabel: "安装人员",
    resultInstallerLabel: "安装人员",
    submitBtnText: "提交注册",
    nameErrorText: "请输入您的姓名",
    emailErrorText: "请输入有效的电子邮箱地址",
    phoneErrorText: "请输入有效的电话号码",
    installerErrorText: "请输入安装人员信息",
    notActivatedTitle: "产品未激活",
    notActivatedDesc: "此产品尚未注册。请填写以下表单以激活保修。",
    activatedTitle: "产品保修信息",
    resultProductIdLabel: "产品ID",
    resultNameLabel: "注册姓名",
    resultEmailLabel: "电子邮箱",
    resultPhoneLabel: "电话号码",
    resultActivationLabel: "激活日期",
    resultWarrantyStatusLabel: "保修状态",
    resultWarrantyExpired: "您的保修已过期",
    resultWarrantyActive: "您的保修处于有效期",
    resultDaysRemaining: "天剩余",
    restartBtnText: "扫描另一个二维码",
    toastMessage: "注册提交成功！",
    footerText: "© 2023 高级汽车电池保修系统。保留所有权利。",
    qrCodeNotDetected: "未识别到二维码，请尝试其他图片。",
    processingError: "图像处理出错，请重试。",
    imageLoadError: "图像加载失败，请重试。",
    cropperTitle: "选择二维码区域",
    cropperDesc: "您的图片较大，请选择包含二维码的区域。",
    cropBtnText: "裁剪并扫描",
    cancelCropText: "取消",
    accessErrorTitle: "访问被拒绝",
    accessErrorMessage: "您需要有效的访问码才能查看此页面。",
    invalidAccessCode: "访问码无效，请重新输入。",
    backBtnText: "返回首页",
    accessCodeLabel: "访问码",
    accessCodePlaceholder: "请输入访问码",
    submitAccessCodeText: "提交"
  }
};

// Detect browser language and set initial language
function detectBrowserLanguage() {
  const browserLang = navigator.language || navigator.userLanguage;
  return browserLang && browserLang.toLowerCase().includes('zh') ? 'zh' : 'en';
}

// Current language - initialize based on browser language
const currentLang = ref(detectBrowserLanguage());

// Reactive states
const showUploadSection = ref(true);
const showFormSection = ref(false);
const showResultSection = ref(false);
const showNotActivated = ref(false);
const showActivated = ref(false);
const showProcessingAnimation = ref(false);
const showUploadPreview = ref(false);
// 移除裁剪相关的状态变量
const showAccessCodeError = ref(false);
const previewImageSrc = ref('');
const productId = ref('');
const formData = ref({
  name: '',
  email: '',
  phone: '',
  country: '',
  city: '',
  installer: ''
});
const errors = ref({
  name: false,
  email: false,
  phone: false,
  installer: false
});
const productInfo = ref(null);
const accessCode = ref('');
const accessCodeValid = ref(true); // Set to false if access code validation is required
// 移除裁剪器变量

// Computed properties
const t = computed(() => translations[currentLang.value]);

// Switch language
function switchLanguage(lang) {
  currentLang.value = lang;
}

// Handle file upload
function handleFileUpload(event) {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      previewImageSrc.value = e.target.result;
      showUploadPreview.value = true;
    };
    reader.readAsDataURL(file);
  }
}

// Retake photo
function retakePhoto() {
  // 不再直接操作DOM元素，因为可能不存在
  showUploadPreview.value = false;
  previewImageSrc.value = '';
}

// Confirm upload and process image
function confirmUpload() {
  showUploadPreview.value = false;
  showProcessingAnimation.value = true;
  
  const img = new Image();
  img.onload = function() {
    processImage(img);
  };
  
  img.onerror = function() {
    showErrorToast(t.value.imageLoadError);
    showUploadPreview.value = true;
    showProcessingAnimation.value = false;
  };
  
  img.src = previewImageSrc.value;
}

// 移除裁剪相关的函数

// Process image and detect QR code
function processImage(img) {
  try {
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    
    // 调整图像大小以提高处理效率
    let width = img.width;
    let height = img.height;
    const MAX_SIZE = 800; // 增加最大尺寸以提高识别率
    
    if (width > MAX_SIZE || height > MAX_SIZE) {
      const ratio = Math.min(MAX_SIZE / width, MAX_SIZE / height);
      width = Math.floor(width * ratio);
      height = Math.floor(height * ratio);
    }
    
    canvas.width = width;
    canvas.height = height;
    ctx.drawImage(img, 0, 0, width, height);
    
    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    const code = jsQR(imageData.data, imageData.width, imageData.height, {
      inversionAttempts: 'attemptBoth', // 尝试正常和反转颜色，提高识别率
    });
    
    if (code) {
      const qrcodeId = code.data;
      
      // 发送请求到后端API
      request.post('/api/wr_api', { 
        qrcode_id: qrcodeId,
        access_code: accessCode.value
      })
        .then(response => {
          showProcessingAnimation.value = false;
          
          if (response.data.status === 'success') {
            if (response.data.data.is_activated) {
              showActivatedResultWithData(response.data.data.product);
            } else {
              showNotActivatedResultWithData(response.data.data.product);
            }
          } else {
            showErrorToast(response.data || t.value.processingError);
            showUploadPreview.value = true;
          }
        })
        .catch(error => {
          showProcessingAnimation.value = false;
          // 检查错误响应是否包含数据
          if (error.response && error.response.data) {
            showErrorToast(error.response.data);
          } else {
            showErrorToast(t.value.processingError);
          }
          console.error('Error:', error);
          showUploadPreview.value = true;
        });
    } else {
      // 二维码识别失败，直接报错
      showProcessingAnimation.value = false;
      showErrorToast(t.value.qrCodeNotDetected);
      showUploadPreview.value = true;
    }
  } catch (error) {
    showProcessingAnimation.value = false;
    showErrorToast(t.value.processingError);
    console.error('Error processing image:', error);
    showUploadPreview.value = true;
  }
}

// Show not activated result with data
function showNotActivatedResultWithData(product) {
  productId.value = product.qrcode_id;
  showUploadSection.value = false;
  showResultSection.value = true;
  showNotActivated.value = true;
  showFormSection.value = true;
}

// Show activated result with data
function showActivatedResultWithData(product) {
  productInfo.value = product;
  showUploadSection.value = false;
  showResultSection.value = true;
  showActivated.value = true;
  showNotActivated.value = false;
  showFormSection.value = false;
}

// Submit registration form
function submitForm() {
  // Reset errors
  errors.value = {
    name: false,
    email: false,
    phone: false,
    installer: false
  };
  
  let isValid = true;
  
  // Validate name
  if (!formData.value.name.trim()) {
    errors.value.name = true;
    isValid = false;
  }
  
  // Validate email or phone based on language
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  
  if (currentLang.value === 'zh') {
    // Chinese: validate phone
    if (!formData.value.phone.trim()) {
      errors.value.phone = true;
      isValid = false;
    }
  } else {
    // English: validate email
    if (!emailRegex.test(formData.value.email.trim())) {
      errors.value.email = true;
      isValid = false;
    }
  }
  
  // Validate installer
  if (!formData.value.installer.trim()) {
    errors.value.installer = true;
    isValid = false;
  }
  
  if (isValid) {
// 首先验证访问码
request.post('/api/code_api', { 
  access_code: accessCode.value,
  lang: currentLang.value
})
.then(response => {
  if (response.data.status === 'success') {
    // 访问码有效，继续提交表单
    saveAccessCodeToLocalStorage(accessCode.value);
    submitFormData();
    } else {
      // 访问码无效
      accessCodeValid.value = false;
      clearAccessCodeFromLocalStorage();
      showErrorToast(t.value.invalidAccessCode);
    }
  })
  .catch(error => {
    // 检查错误响应是否包含数据
    if (error.response && error.response.data) {
      showErrorToast(error.response.data);
    } else {
      showErrorToast(t.value.processingError);
    }
    console.error('Error validating access code:', error);
  });
  }
}

// 提交表单数据
function submitFormData() {
  // 准备表单数据
  const submitData = {
    qrcode_id: productId.value,
    name: formData.value.name.trim(),
    email: formData.value.email.trim(),
    phone: formData.value.phone.trim(),
    city: formData.value.city.trim(),
    country: formData.value.country.trim(),
    installer: formData.value.installer.trim(),
    access_code: accessCode.value // 添加访问码
  };
  
  // Send activation request
  request.post('/api/activate-product/', submitData)
    .then(response => {
      if (response.data.status === 'success') {
        showSuccessToast(t.value.toastMessage);
        showActivatedResultWithData(response.data.data);
      } else {
        // 处理错误响应
        if (response.data.message === '无效的访问码' || 
            (response.data.message_en && response.data.message_en === 'Invalid access code')) {
          // 如果是访问码无效，重置状态
          accessCodeValid.value = false;
          showErrorToast(t.value.invalidAccessCode);
        } else {
          showErrorToast(response.data || t.value.processingError);
        }
      }
    })
    .catch(error => {
      // 检查错误响应是否包含数据
      if (error.response && error.response.data) {
        showErrorToast(error.response.data);
      } else {
        showErrorToast(t.value.processingError);
      }
      console.error('Error:', error);
    });
}

// Show success toast
function showSuccessToast(message) {
  showToast({
    message: message,
    type: 'success',
    position: 'bottom',
    duration: 3000
  });
}

// Show error toast
function showErrorToast(message) {
  // 检查响应是否包含多语言错误消息
  if (typeof message === 'object' && message !== null) {
    // 如果是对象，尝试根据当前语言获取对应的错误消息
    if (currentLang.value === 'en' && message.message_en) {
      showNotify({
        message: message.message_en,
        type: 'danger',
        duration: 3000
      });
    } else if (message.message) {
      showNotify({
        message: message.message,
        type: 'danger',
        duration: 3000
      });
    } else {
      // 如果没有找到适合的消息，使用默认错误消息
      showNotify({
        message: t.value.processingError,
        type: 'danger',
        duration: 3000
      });
    }
  } else {
    // 如果是字符串，直接显示
    showNotify({
      message: message,
      type: 'danger',
      duration: 3000
    });
  }
}

// Restart process
function restart() {
  showUploadSection.value = true;
  showResultSection.value = false;
  showNotActivated.value = false;
  showActivated.value = false;
  showFormSection.value = false;
  showUploadPreview.value = false;
  document.getElementById('qr-code-upload').value = '';
  
  // Clear form fields
  formData.value = {
    name: '',
    email: '',
    phone: '',
    country: '',
    city: '',
    installer: ''
  };
  
  // Clear errors
  errors.value = {
    name: false,
    email: false,
    phone: false,
    installer: false
  };
}

// 保存访问码到本地存储
function saveAccessCodeToLocalStorage(code) {
  localStorage.setItem('warranty_access_code', code);
}

// 从本地存储获取访问码
function getAccessCodeFromLocalStorage() {
  return localStorage.getItem('warranty_access_code');
}

// 清除本地存储中的访问码
function clearAccessCodeFromLocalStorage() {
  localStorage.removeItem('warranty_access_code');
}

// 处理访问码验证成功
function handleAccessCodeValidated(validAccessCode) {
  // 保存有效的访问码
  accessCode.value = validAccessCode;
  accessCodeValid.value = true;
  showAccessCodeError.value = false;
  
  // 保存访问码到本地存储
  saveAccessCodeToLocalStorage(validAccessCode);
  
  // 获取URL参数
  const urlParams = new URLSearchParams(window.location.search);
  const urlId = urlParams.get('id');
  const qrcodeId = urlParams.get('qrcode_id');
  
  // 如果有id参数，直接请求api/wr_api接口
  if (urlId) {
    showProcessingAnimation.value = true;
    
    request.post('/api/wr_api', {
      qrcode_id: urlId,
      access_code: accessCode.value
    })
    .then(response => {
      showProcessingAnimation.value = false;
      
      if (response.data.status === 'success') {
        if (response.data.data.is_activated) {
          showActivatedResultWithData(response.data.data.product);
        } else {
          showNotActivatedResultWithData(response.data.data.product);
        }
      } else {
        // 如果访问码无效，重置状态并清除本地存储
        if (response.data.message === '无效的访问码' || 
            (response.data.message_en && response.data.message_en === 'Invalid access code')) {
          accessCodeValid.value = false;
          clearAccessCodeFromLocalStorage();
        }
        showErrorToast(response.data || t.value.processingError);
      }
    })
    .catch(error => {
      showProcessingAnimation.value = false;
      // 检查错误响应是否包含数据
      if (error.response && error.response.data) {
        showErrorToast(error.response.data);
      } else {
        showErrorToast(t.value.processingError);
      }
      console.error('Error:', error);
    });
  } else if (qrcodeId) {
    // 如果有qrcode_id参数，也请求api/wr_api接口
    showProcessingAnimation.value = true;
    
    request.post('/api/wr_api', { 
      qrcode_id: qrcodeId,
      access_code: accessCode.value
    })
    .then(response => {
      showProcessingAnimation.value = false;
      
      if (response.data.status === 'success') {
        if (response.data.data.is_activated) {
          showActivatedResultWithData(response.data.data.product);
        } else {
          showNotActivatedResultWithData(response.data.data.product);
        }
      } else {
        // 如果访问码无效，重置状态并清除本地存储
        if (response.data.message === '无效的访问码') {
          accessCodeValid.value = false;
          clearAccessCodeFromLocalStorage();
        }
        showErrorToast(response.data.message || t.value.processingError);
      }
    })
    .catch(error => {
      showProcessingAnimation.value = false;
      showErrorToast(t.value.processingError);
      console.error('Error:', error);
    });
  }
}

// 检查URL中的参数并处理
onMounted(() => {
  const urlParams = new URLSearchParams(window.location.search);
  const qrcodeId = urlParams.get('qrcode_id');
  const urlAccessCode = urlParams.get('access_code');
  const urlId = urlParams.get('id');
  
  // 首先检查URL中是否有访问码
  if (urlAccessCode) {
    // 如果URL中有访问码，需要立即验证其有效性
    accessCode.value = urlAccessCode;
    
    // 验证访问码
    validateAccessCode(urlAccessCode, urlId, qrcodeId);
  } else {
    // 如果URL中没有访问码，检查本地存储中是否有保存的访问码
    const savedAccessCode = getAccessCodeFromLocalStorage();
    
    if (savedAccessCode) {
      // 如果本地存储中有访问码，使用它
      accessCode.value = savedAccessCode;
      
      // 验证保存的访问码
      validateAccessCode(savedAccessCode, urlId, qrcodeId);
    } else {
      // 如果没有访问码，显示访问码输入界面
      accessCodeValid.value = false;
    }
  }
});

// 验证访问码
function validateAccessCode(code, urlId, qrcodeId) {
  request.post('/api/code_api', { 
    access_code: code,
    lang: currentLang.value
  })
  .then(response => {
    if (response.data.status === 'success') {
      // 访问码有效
      accessCodeValid.value = true;
      
      // 保存到本地存储
      saveAccessCodeToLocalStorage(code);
      
      // 继续处理URL参数
      processUrlParameters(urlId, qrcodeId);
    } else {
      // 访问码无效
      accessCodeValid.value = false;
      clearAccessCodeFromLocalStorage();
      showErrorToast(t.value.invalidAccessCode);
    }
  })
  .catch(error => {
    accessCodeValid.value = false;
    // 检查错误响应是否包含数据
    if (error.response && error.response.data) {
      showErrorToast(error.response.data);
    } else {
      showErrorToast(t.value.processingError);
    }
    console.error('Error validating access code:', error);
  });
}

// 处理URL参数
function processUrlParameters(urlId, qrcodeId) {
  // 如果有id参数，直接请求api/wr_api接口
  if (urlId) {
    showProcessingAnimation.value = true;
    
    // 发送请求到api/wr_api接口，带上access_code和id参数
    request.post('/api/wr_api', { 
      qrcode_id: urlId,
      access_code: accessCode.value
    })
    .then(response => {
      showProcessingAnimation.value = false;
      
      if (response.data.status === 'success') {
        if (response.data.data.is_activated) {
          showActivatedResultWithData(response.data.data.product);
        } else {
          showNotActivatedResultWithData(response.data.data.product);
        }
      } else {
        // 如果访问码无效，重置状态
        if (response.data.message === '无效的访问码' || 
            (response.data.message_en && response.data.message_en === 'Invalid access code')) {
          accessCodeValid.value = false;
        }
        showErrorToast(response.data || t.value.processingError);
      }
    })
    .catch(error => {
      showProcessingAnimation.value = false;
      // 检查错误响应是否包含数据
      if (error.response && error.response.data) {
        showErrorToast(error.response.data);
      } else {
        showErrorToast(t.value.processingError);
      }
      console.error('Error:', error);
    });
  } else if (qrcodeId) {
    // 如果有qrcode_id参数，也请求api/wr_api接口
    showProcessingAnimation.value = true;
    
    request.post('/api/wr_api', { 
      qrcode_id: qrcodeId,
      access_code: accessCode.value
    })
    .then(response => {
      showProcessingAnimation.value = false;
      
      if (response.data.status === 'success') {
        if (response.data.data.is_activated) {
          showActivatedResultWithData(response.data.data.product);
        } else {
          showNotActivatedResultWithData(response.data.data.product);
        }
      } else {
        // 如果访问码无效，重置状态
        if (response.data.message === '无效的访问码') {
          accessCodeValid.value = false;
        }
        showErrorToast(response.data.message || t.value.processingError);
      }
    })
    .catch(error => {
      showProcessingAnimation.value = false;
      showErrorToast(t.value.processingError);
      console.error('Error:', error);
    });
  }
}
</script>

<template>
  <div>
    <!-- Language Switcher -->
    <LanguageSwitcher 
      :currentLang="currentLang" 
      @switchLanguage="switchLanguage" 
    />

    <!-- Main Content -->
    <div class="main-container">
      <!-- Header -->
      <div class="header-section">
        <h1 class="title">{{ t.title }}</h1>
        <p class="subtitle">{{ t.subtitle }}</p>
      </div>

      <!-- Car Image Section -->
      <div class="car-image-section">
        <van-image src="https://qiniu.notebay.cn/web/car-L-1.png-c" alt="Car product image" fit="cover" />
        <div class="car-image-overlay">
          <div class="car-image-text">
            <h2 class="car-title">{{ t.carTitle }}</h2>
            <p class="car-desc">{{ t.carDesc }}</p>
          </div>
        </div>
      </div>

      <!-- Access Code Input Section -->
      <AccessCodeInput
        v-if="!accessCodeValid"
        :t="t"
        :currentLang="currentLang"
        @accessCodeValidated="handleAccessCodeValidated"
      />

      <!-- QR Code Upload Section -->
      <QrCodeUploader 
        v-if="showUploadSection && accessCodeValid"
        :t="t"
        :showProcessingAnimation="showProcessingAnimation"
        :showUploadPreview="showUploadPreview"
        :previewImageSrc="previewImageSrc"
        @fileUpload="handleFileUpload"
        @retakePhoto="retakePhoto"
        @confirmUpload="confirmUpload"
      />

      <!-- Form Section -->
      <RegistrationForm 
        v-if="showFormSection"
        :t="t"
        :productId="productId"
        :formData="formData"
        :errors="errors"
        :currentLang="currentLang"
        @submitForm="submitForm"
      />

      <!-- Result Section -->
      <ProductResult 
        v-if="showResultSection"
        :t="t"
        :showNotActivated="showNotActivated"
        :showActivated="showActivated"
        :productInfo="productInfo"
        @restart="restart"
      />
    </div>

    <!-- Footer -->
    <van-divider />
    <footer class="footer">
      <p class="footer-text">{{ t.footerText }}</p>
    </footer>

    <!-- Toast 会由方法调用，不需要在模板中显示 -->

    <!-- 不再需要单独的访问码对话框，因为我们现在使用了AccessCodeInput组件 -->
  </div>
</template>

<style scoped>
.main-container {
  padding: 16px;
  max-width: 640px;
  margin: 0 auto;
}

.header-section {
  text-align: center;
  margin-bottom: 24px;
}

.title {
  font-size: clamp(1.8rem, 5vw, 2.5rem);
  font-weight: bold;
  color: #323233;
  margin-bottom: 8px;
}

.subtitle {
  color: #969799;
  max-width: 500px;
  margin: 0 auto;
}

.car-image-section {
  position: relative;
  margin-bottom: 24px;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 8px 12px rgba(0, 0, 0, 0.1);
}

.car-image-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.6), transparent);
  display: flex;
  align-items: flex-end;
}

.car-image-text {
  padding: 16px;
  color: white;
}

.car-title {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 4px;
}

.car-desc {
  opacity: 0.8;
}

.footer {
  padding: 16px;
  text-align: center;
}

.footer-text {
  color: #969799;
  font-size: 14px;
}

.access-error-content {
  padding: 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.access-error-title {
  font-size: 18px;
  font-weight: bold;
  color: #323233;
}

.access-error-message {
  color: #969799;
  text-align: center;
}
</style>
