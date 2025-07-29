import axios from 'axios';

// 创建axios实例
const request = axios.create({
  baseURL: '/api', // 使用相对路径，通过Vite代理转发请求
  timeout: 10000, // 请求超时时间
  headers: {
    'Content-Type': 'application/json',
    'Origin': 'https://k.innrgpower.com' // 明确指定请求来源
  },
  withCredentials: true // 允许跨域请求携带凭证
});

// 请求拦截器
request.interceptors.request.use(
  config => {
    // 在发送请求之前可以做一些处理
    return config;
  },
  error => {
    // 处理请求错误
    console.error('请求错误:', error);
    return Promise.reject(error);
  }
);

// 响应拦截器
request.interceptors.response.use(
  response => {
    // 对响应数据做一些处理
    return response;
  },
  error => {
    // 处理响应错误
    console.error('响应错误:', error);
    return Promise.reject(error);
  }
);

export default request;