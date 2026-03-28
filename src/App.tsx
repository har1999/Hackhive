import { Suspense, lazy } from 'react'
import { Navigate, Route, Routes } from 'react-router-dom'

const WorkerApp = lazy(() => import('./apps/worker/App'))
const ContractorApp = lazy(() => import('./apps/contractor/App'))

function App() {
  return (
    <Suspense fallback={<div className="page-loader">Loading KaamSetu...</div>}>
      <Routes>
        <Route path="/" element={<Navigate to="/worker" replace />} />
        <Route path="/worker/*" element={<WorkerApp />} />
        <Route path="/contractor/*" element={<ContractorApp />} />
      </Routes>
    </Suspense>
  )
}

export default App
