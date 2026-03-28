const CACHE_NAME = 'kaamsetu-static-v1'
const API_CACHE = 'kaamsetu-api-v1'

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) =>
      cache.addAll(['/', '/worker', '/contractor'])
    )
  )
  self.skipWaiting()
})

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys
          .filter((key) => key !== CACHE_NAME && key !== API_CACHE)
          .map((key) => caches.delete(key))
      )
    )
  )
  self.clients.claim()
})

self.addEventListener('fetch', (event) => {
  const { request } = event
  const requestUrl = new URL(request.url)

  if (requestUrl.pathname.startsWith('/api/jobs')) {
    event.respondWith(networkFirst(request, API_CACHE))
    return
  }

  if (request.destination === 'script' || request.destination === 'style' || request.destination === 'image') {
    event.respondWith(cacheFirst(request, CACHE_NAME))
    return
  }

  event.respondWith(fetch(request).catch(() => caches.match('/')))
})

async function cacheFirst(request, cacheName) {
  const cache = await caches.open(cacheName)
  const cached = await cache.match(request)
  if (cached) {
    return cached
  }

  const networkResponse = await fetch(request)
  cache.put(request, networkResponse.clone())
  return networkResponse
}

async function networkFirst(request, cacheName) {
  const cache = await caches.open(cacheName)
  try {
    const networkResponse = await fetch(request)
    cache.put(request, networkResponse.clone())
    return networkResponse
  } catch (error) {
    const cached = await cache.match(request)
    if (cached) {
      return cached
    }

    return new Response(JSON.stringify({ jobs: [] }), {
      headers: { 'Content-Type': 'application/json' },
      status: 200,
    })
  }
}
