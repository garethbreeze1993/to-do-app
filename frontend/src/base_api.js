import axios from "axios";
import { setupInterceptorsTo } from './setUpInteceptors.ts'

const api = setupInterceptorsTo(
  axios.create({
    // baseURL: process.env.NEXT_PUBLIC_ENDPOINT_AUTH,
    headers: {
      "Content-Type": "application/json",
    },
  })
);

export default api;
