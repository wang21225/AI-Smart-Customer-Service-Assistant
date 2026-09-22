import axios from "axios";

export const http = axios.create({
  baseURL: "/api",
  timeout: 30000
});

export async function apiGet<T>(url: string): Promise<T> {
  const res = await http.get(url);
  return res.data.data as T;
}

export async function apiPost<T>(url: string, data?: unknown): Promise<T> {
  const res = await http.post(url, data);
  return res.data.data as T;
}

export async function apiPut<T>(url: string, data?: unknown): Promise<T> {
  const res = await http.put(url, data);
  return res.data.data as T;
}

export async function apiDelete<T>(url: string): Promise<T> {
  const res = await http.delete(url);
  return res.data.data as T;
}
