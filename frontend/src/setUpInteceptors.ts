import axios, {
  AxiosError,
  AxiosInstance,
  AxiosRequestConfig,
  AxiosResponse,
} from "axios";

import createAuthRefreshInterceptor from 'axios-auth-refresh';

// Function that will be called to refresh authorization
const refreshAuthLogic = async (failedRequest) => {
    const refreshToken = localStorage.getItem("userRefreshToken");

      try {
        const rs = await axios.post(`/api/v1/refresh`, {
          refresh_token:  refreshToken,
        });

        const { access_token } = rs.data;

        localStorage.setItem("userToken", access_token);
        failedRequest.response.config.headers['Authorization'] = 'Bearer ' + access_token;
        return Promise.resolve();

}
  finally {

      }
}

function getAccessToken() {
    return localStorage.getItem('userToken');
}


const onRequest = (config: AxiosRequestConfig): AxiosRequestConfig => {
  config.headers["Authorization"] = `Bearer ${getAccessToken()}`;

  return config;
};

const onRequestError = (error: AxiosError): Promise<AxiosError> => {
  return Promise.reject(error);
};

const onResponse = (response: AxiosResponse): AxiosResponse => {
  return response;
};

const onResponseError = async (error: AxiosError): Promise<AxiosResponse<any>> => {
  return Promise.reject(error);
};

export const setupInterceptorsTo = (
  axiosInstance: AxiosInstance
): AxiosInstance => {
  createAuthRefreshInterceptor(axiosInstance, refreshAuthLogic);
  axiosInstance.interceptors.request.use(onRequest, onRequestError);
  axiosInstance.interceptors.response.use(onResponse, onResponseError);
  return axiosInstance;
};