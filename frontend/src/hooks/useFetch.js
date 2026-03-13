import { useState, useEffect, useCallback } from 'react'

/**
 * Generic fetch hook.
 * Usage: const { data, loading, error, refetch } = useFetch(apiFn, [deps])
 */
export function useFetch(apiFn, deps = []) {
  const [data,    setData]    = useState(null)
  const [loading, setLoading] = useState(true)
  const [error,   setError]   = useState(null)

  const fetch = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const res = await apiFn()
      setData(res.data)
    } catch (e) {
      setError(e?.response?.data?.detail || e.message || 'Something went wrong')
    } finally {
      setLoading(false)
    }
  }, deps) // eslint-disable-line

  useEffect(() => { fetch() }, [fetch])

  return { data, loading, error, refetch: fetch }
}
