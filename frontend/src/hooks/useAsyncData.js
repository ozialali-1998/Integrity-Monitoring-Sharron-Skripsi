import { useCallback, useEffect, useState } from 'react';

export function useAsyncData(fetcher, fallbackFetcher, dependencies = []) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await fetcher();
      setData(result);
    } catch (apiError) {
      setError(apiError);
      if (fallbackFetcher) {
        const fallback = await fallbackFetcher();
        setData(fallback);
      }
    } finally {
      setLoading(false);
    }
  }, dependencies);

  useEffect(() => {
    load();
  }, [load]);

  return { data, loading, error, refetch: load };
}
