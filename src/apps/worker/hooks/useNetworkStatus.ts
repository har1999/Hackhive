import { useEffect, useState } from 'react'

export type NetworkStatus = 'online' | 'offline' | 'slow'

export const useNetworkStatus = () => {
  const [status, setStatus] = useState<NetworkStatus>(navigator.onLine ? 'online' : 'offline')

  useEffect(() => {
    const onOnline = () => setStatus('online')
    const onOffline = () => setStatus('offline')

    window.addEventListener('online', onOnline)
    window.addEventListener('offline', onOffline)

    const connection = (navigator as Navigator & { connection?: { effectiveType?: string; addEventListener?: (event: string, cb: () => void) => void } }).connection
    const handleConnection = () => {
      if (!navigator.onLine) {
        setStatus('offline')
        return
      }
      setStatus(connection?.effectiveType === '2g' ? 'slow' : 'online')
    }

    connection?.addEventListener?.('change', handleConnection)
    handleConnection()

    return () => {
      window.removeEventListener('online', onOnline)
      window.removeEventListener('offline', onOffline)
    }
  }, [])

  return status
}
