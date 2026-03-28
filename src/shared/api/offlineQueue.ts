import { get, set } from 'idb-keyval'
import { api } from './client'

type SyncCapableRegistration = ServiceWorkerRegistration & {
  sync?: {
    register: (name: string) => Promise<void>
  }
}

type QueueItem = {
  idempotencyKey: string
  jobId: string
  createdAt: number
}

const QUEUE_KEY = 'queue_applications'

const readQueue = async (): Promise<QueueItem[]> => {
  return (await get<QueueItem[]>(QUEUE_KEY)) ?? []
}

export class OfflineQueue {
  async addJobApplication(jobId: string) {
    const queue = await readQueue()
    const nextItem = {
      idempotencyKey: `${jobId}:${Date.now()}`,
      jobId,
      createdAt: Date.now(),
    }

    await set(QUEUE_KEY, [...queue, nextItem])
    await this.registerSync()
  }

  async processQueue() {
    const queue = await readQueue()
    if (!queue.length) {
      return
    }

    const remaining: QueueItem[] = []

    for (const item of queue) {
      try {
        await api.applyForJob(item.jobId)
      } catch {
        remaining.push(item)
      }
    }

    await set(QUEUE_KEY, remaining)
  }

  private async registerSync() {
    if (!('serviceWorker' in navigator)) {
      return
    }

    const registration = (await navigator.serviceWorker.ready) as SyncCapableRegistration
    if (registration.sync) {
      await registration.sync.register('sync-applications')
    }
  }
}

export const offlineQueue = new OfflineQueue()
