<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import jsQR from 'jsqr';
import '../assets/cropper.css';
import Cropper from 'cropperjs';
import LanguageSwitcher from './LanguageSwitcher.vue';
import QrCodeUploader from './QrCodeUploader.vue';
import RegistrationForm from './RegistrationForm.vue';
import ProductResult from './ProductResult.vue';

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
const showCropperSection = ref(false);
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
const toastMessage = ref('');
const showToast = ref(false);
const toastType = ref('success');
const accessCode = ref('');
const accessCodeValid = ref(true); // Set to false if access code validation is required
let cropper = null;

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
  document.getElementById('qr-code-upload').value = '';
  showUploadPreview.value = false;
}

// Confirm upload and process image
function confirmUpload() {
  showUploadPreview.value = false;
  
  const img = new Image();
  img.onload = function() {
    const CROP_THRESHOLD = 3000;
    
    if (img.width > CROP_THRESHOLD || img.height > CROP_THRESHOLD) {
      showCropperSection.value = true;
      initCropper(img.src);
    } else {
      showProcessingAnimation.value = true;
      processImage(img);
    }
  };
  
  img.onerror = function() {
    showErrorToast(t.value.imageLoadError);
    showUploadPreview.value = true;
  };
  
  img.src = previewImageSrc.value;
}

// Initialize cropper
function initCropper(src) {
  setTimeout(() => {
    const image = document.getElementById('cropper-image');
    image.src = src;
    
    if (cropper) {
      cropper.destroy();
    }
    
    cropper = new Cropper(image, {
      aspectRatio: NaN,
      viewMode: 1,
      guides: true,
      highlight: true,
      autoCropArea: 0.5,
      dragMode: 'move',
      responsive: true,
      restore: false,
      minContainerWidth: 300,
      minContainerHeight: 300
    });
  }, 100);
}

// Cancel crop
function cancelCrop() {
  showCropperSection.value = false;
  if (cropper) {
    cropper.destroy();
    cropper = null;
  }
  showUploadPreview.value = true;
}

// Crop and scan
function cropAndScan() {
  if (!cropper) return;
  
  showCropperSection.value = false;
  showProcessingAnimation.value = true;
  
  const canvas = cropper.getCroppedCanvas({
    maxWidth: 1000,
    maxHeight: 1000,
    fillColor: '#fff'
  });
  
  if (!canvas) {
    showProcessingAnimation.value = false;
    showErrorToast(t.value.processingError);
    showUploadPreview.value = true;
    return;
  }
  
  const croppedImg = new Image();
  croppedImg.onload = function() {
    processImage(croppedImg);
    
    if (cropper) {
      cropper.destroy();
      cropper = null;
    }
  };
  
  croppedImg.onerror = function() {
    showProcessingAnimation.value = false;
    showErrorToast(t.value.processingError);
    showUploadPreview.value = true;
    
    if (cropper) {
      cropper.destroy();
      cropper = null;
    }
  };
  
  croppedImg.src = canvas.toDataURL('image/jpeg');
}

// Process image and detect QR code
function processImage(img) {
  try {
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    
    let width = img.width;
    let height = img.height;
    const RESIZE_THRESHOLD = 400;
    const MAX_SIZE = 300;
    
    if (width > RESIZE_THRESHOLD || height > RESIZE_THRESHOLD) {
      const ratio = Math.min(MAX_SIZE / width, MAX_SIZE / height);
      width = Math.floor(width * ratio);
      height = Math.floor(height * ratio);
    } else if (width > MAX_SIZE || height > MAX_SIZE) {
      const ratio = Math.min(MAX_SIZE / width, MAX_SIZE / height);
      width = Math.floor(width * ratio);
      height = Math.floor(height * ratio);
    }
    
    canvas.width = width;
    canvas.height = height;
    ctx.drawImage(img, 0, 0, width, height);
    
    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    const code = jsQR(imageData.data, imageData.width, imageData.height, {
      inversionAttempts: 'dontInvert',
    });
    
    if (code) {
      const qrcodeId = code.data;
      
      // Send request to backend API
      axios.post('/api/wr', { qrcode_id: qrcodeId })
        .then(response => {
          showProcessingAnimation.value = false;
          
          if (response.data.status === 'success') {
            if (response.data.data.is_activated) {
              showActivatedResultWithData(response.data.data.product);
            } else {
              showNotActivatedResultWithData(response.data.data.product);
            }
          } else {
            showErrorToast(response.data.message || t.value.processingError);
            showUploadPreview.value = true;
          }
        })
        .catch(error => {
          showProcessingAnimation.value = false;
          showErrorToast(t.value.processingError);
          console.error('Error:', error);
          showUploadPreview.value = true;
        });
    } else {
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
    // Prepare form data
    const submitData = {
      qrcode_id: productId.value,
      name: formData.value.name.trim(),
      email: formData.value.email.trim(),
      phone: formData.value.phone.trim(),
      city: formData.value.city.trim(),
      country: formData.value.country.trim(),
      installer: formData.value.installer.trim()
    };
    
    // Send activation request
    axios.post('/api/activate-product/', submitData)
      .then(response => {
        if (response.data.status === 'success') {
          showSuccessToast(t.value.toastMessage);
          showActivatedResultWithData(response.data.data);
        } else {
          showErrorToast(response.data.message || t.value.processingError);
        }
      })
      .catch(error => {
        showErrorToast(t.value.processingError);
        console.error('Error:', error);
      });
  }
}

// Show success toast
function showSuccessToast(message) {
  toastMessage.value = message;
  toastType.value = 'success';
  showToast.value = true;
  
  setTimeout(() => {
    showToast.value = false;
  }, 3000);
}

// Show error toast
function showErrorToast(message) {
  toastMessage.value = message;
  toastType.value = 'error';
  showToast.value = true;
  
  setTimeout(() => {
    showToast.value = false;
  }, 3000);
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

// Submit access code
function submitAccessCode() {
  if (accessCode.value.trim()) {
    // In a real app, you would validate the access code with the server
    // For now, we'll just simulate a successful validation
    accessCodeValid.value = true;
    showAccessCodeError.value = false;
  }
}

// Check for initial QR code ID in URL
onMounted(() => {
  const urlParams = new URLSearchParams(window.location.search);
  const qrcodeId = urlParams.get('qrcode_id');
  const urlAccessCode = urlParams.get('access_code');
  
  if (urlAccessCode) {
    accessCode.value = urlAccessCode;
    // In a real app, you would validate the access code with the server
    // For now, we'll just simulate a successful validation
    accessCodeValid.value = true;
  }
  
  if (!accessCodeValid.value) {
    showAccessCodeError.value = true;
  } else if (qrcodeId) {
    // If URL contains qrcode_id parameter, automatically query product info
    axios.post('/api/wr', { qrcode_id: qrcodeId })
      .then(response => {
        if (response.data.status === 'success') {
          if (response.data.data.is_activated) {
            showActivatedResultWithData(response.data.data.product);
          } else {
            showNotActivatedResultWithData(response.data.data.product);
          }
        } else {
          showErrorToast(response.data.message || t.value.processingError);
        }
      })
      .catch(error => {
        showErrorToast(t.value.processingError);
        console.error('Error:', error);
      });
  }
});
</script>

<template>
  <div>
    <!-- Language Switcher -->
    <LanguageSwitcher 
      :currentLang="currentLang" 
      @switchLanguage="switchLanguage" 
    />

    <!-- Main Content -->
    <main class="flex-grow container mx-auto px-4 py-8 max-w-4xl">
      <!-- Header -->
      <header class="text-center mb-10">
        <h1 class="text-[clamp(1.8rem,5vw,2.5rem)] font-bold text-neutral-600 mb-2">
          {{ t.title }}
        </h1>
        <p class="text-neutral-400 max-w-2xl mx-auto">
          {{ t.subtitle }}
        </p>
      </header>

      <!-- Car Image Section -->
      <div class="mb-10 relative overflow-hidden rounded-xl shadow-xl">
        <img src="https://qiniu.notebay.cn/web/car-L-1.png-c" alt="Car product image" class="w-full h-auto object-cover transition-transform duration-700 hover:scale-105">
        <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent flex items-end">
          <div class="p-6 text-white">
            <h2 class="text-2xl font-bold mb-1">{{ t.carTitle }}</h2>
            <p class="text-white/80">{{ t.carDesc }}</p>
          </div>
        </div>
      </div>

      <!-- QR Code Upload Section -->
      <QrCodeUploader 
        v-if="showUploadSection"
        :t="t"
        :showProcessingAnimation="showProcessingAnimation"
        :showUploadPreview="showUploadPreview"
        :showCropperSection="showCropperSection"
        :previewImageSrc="previewImageSrc"
        @fileUpload="handleFileUpload"
        @retakePhoto="retakePhoto"
        @confirmUpload="confirmUpload"
        @cancelCrop="cancelCrop"
        @cropAndScan="cropAndScan"
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
    </main>

    <!-- Footer -->
    <footer class="bg-white border-t border-neutral-200 py-6">
      <div class="container mx-auto px-4 text-center">
        <p class="text-neutral-400 text-sm">
          {{ t.footerText }}
        </p>
      </div>
    </footer>

    <!-- Success Toast -->
    <div 
      :class="[
        'fixed bottom-4 right-4 px-6 py-3 rounded-lg shadow-lg transform transition-all duration-300 flex items-center z-50',
        showToast ? 'translate-y-0 opacity-100' : 'translate-y-20 opacity-0',
        toastType === 'success' ? 'bg-green-500 text-white' : 'bg-red-500 text-white'
      ]"
    >
      <img src="https://qiniu.yayaxueqin.cn/icon/check-circle.svg" alt="check-circle icon" class="w-5 h-5 mr-1">
      <span>{{ toastMessage }}</span>
    </div>

    <!-- Access Code Error Message -->
    <div v-if="showAccessCodeError" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div class="bg-white rounded-xl p-8 shadow-lg max-w-md w-full mx-4">
        <div class="text-center mb-6">
          <div class="inline-flex items-center justify-center w-16 h-16 rounded-full bg-red-100 text-red-500 mb-4">
            <img src="https://qiniu.yayaxueqin.cn/icon/fasfa-exclamation-triangle.svg" alt="error" class="w-8 h-8">
          </div>
          <h3 class="text-xl font-semibold text-neutral-600 mb-2">
            {{ t.accessErrorTitle }}
          </h3>
          <p class="text-neutral-500">
            {{ t.accessErrorMessage }}
          </p>
        </div>
        <div class="space-y-4">
          <div class="flex flex-col">
            <label for="access-code-input" class="block text-sm font-medium text-neutral-500 mb-1">
              <span>{{ t.accessCodeLabel }}</span>
            </label>
            <input type="text" id="access-code-input" v-model="accessCode" class="w-full px-4 py-2 border border-neutral-200 rounded-lg focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none transition-custom" :placeholder="t.accessCodePlaceholder">
          </div>
          <div class="flex justify-center">
            <button @click="submitAccessCode" class="bg-primary hover:bg-primary/90 text-white font-medium py-2 px-6 rounded-full transition-custom">
              <span>{{ t.submitAccessCodeText }}</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>[plugin:vite:import-analysis] Missing "./dist/cropper.css" specifier in "cropperjs" package
