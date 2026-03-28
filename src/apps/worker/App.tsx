import { Suspense, lazy } from 'react'
import { Navigate, Route, Routes } from 'react-router-dom'
import { BottomNav } from './components/BottomNav'
import { VoiceFab } from './components/VoiceFab'

const HomeScreen = lazy(() => import('./routes/HomeScreen'))
const JobSearchScreen = lazy(() => import('./routes/JobSearchScreen'))
const MyJobsScreen = lazy(() => import('./routes/MyJobsScreen'))
const ProfileScreen = lazy(() => import('./routes/ProfileScreen'))
const VoiceAssistantScreen = lazy(() => import('./routes/VoiceAssistantScreen'))

export default function WorkerApp() {
  return (
    <div className="worker-shell">
      <Suspense fallback={<div className="page-loader">Loading worker app...</div>}>
        <Routes>
          <Route path="/" element={<HomeScreen />} />
          <Route path="/jobs" element={<JobSearchScreen />} />
          <Route path="/my-jobs" element={<MyJobsScreen />} />
          <Route path="/profile" element={<ProfileScreen />} />
          <Route path="/assistant" element={<VoiceAssistantScreen />} />
          <Route path="*" element={<Navigate to="/worker" replace />} />
        </Routes>
      </Suspense>
      <VoiceFab />
      <BottomNav />
    </div>
  )
}
