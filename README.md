# KaamSetu Frontend (React + TypeScript)

Dual-interface Progressive Web App scaffold for:

- Worker interface at `/worker` (mobile first, low-bandwidth friendly)
- Contractor interface at `/contractor` (dashboard and operations)

## Tech Stack

- React 19 + TypeScript + Vite
- React Router v6 (lazy route loading)
- TanStack Query + Zustand-ready architecture
- Tailwind CSS + PostCSS
- i18next (Hindi, Tamil, Telugu, Marathi seeds)
- IndexedDB queue (`idb-keyval`) for offline actions
- Manual service worker registration (`public/sw.js`)

## Quick Start

```bash
npm install
npm run dev
```

Open:

- `http://localhost:5173/worker`
- `http://localhost:5173/contractor`

## Build

```bash
npm run build
npm run preview
```

## Project Structure

```text
src/
  apps/
    worker/
    contractor/
  shared/
    api/
    components/
    constants/
    i18n/
    utils/
  service-worker/
public/
  sw.js
  manifest-worker.webmanifest
  manifest-contractor.webmanifest
```

## Notes

- Service worker currently provides static cache-first and jobs API network-first behavior.
- Offline application queue is wired in `src/shared/api/offlineQueue.ts`.
- This is a production-oriented scaffold; connect real backend APIs and auth flows next.
