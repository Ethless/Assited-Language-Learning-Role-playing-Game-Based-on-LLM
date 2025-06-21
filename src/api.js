import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000", // FastAPI 后端地址
});

export default api;
