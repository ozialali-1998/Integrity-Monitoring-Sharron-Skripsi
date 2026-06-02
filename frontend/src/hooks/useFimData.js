import { fallbackApi, fimApi } from '../services/fimApi.js';
import { useAsyncData } from './useAsyncData.js';

export const useDashboard = () => useAsyncData(() => fimApi.getDashboard(), () => fallbackApi.getDashboard(), []);
export const useDirectories = () => useAsyncData(() => fimApi.getDirectories(), () => fallbackApi.getDirectories(), []);
export const useVerificationResults = () => useAsyncData(() => fimApi.getVerificationResults(), () => fallbackApi.getVerificationResults(), []);
export const useBenchmarkResults = () => useAsyncData(() => fimApi.getBenchmarkResults(), () => fallbackApi.getBenchmarkResults(), []);
export const useLogs = () => useAsyncData(() => fimApi.getLogs(), () => fallbackApi.getLogs(), []);
export const useSettings = () => useAsyncData(() => fimApi.getSettings(), () => fallbackApi.getSettings(), []);
