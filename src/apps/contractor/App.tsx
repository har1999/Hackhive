import { NavLink, Navigate, Route, Routes } from 'react-router-dom'
import Dashboard from './routes/Dashboard'
import PostJob from './routes/PostJob'
import Applicants from './routes/Applicants'
import Broadcast from './routes/Broadcast'
import Favorites from './routes/Favorites'

const links = [
  { to: '/contractor', label: 'Dashboard' },
  { to: '/contractor/post-job', label: 'Post Job' },
  { to: '/contractor/applicants', label: 'Applicants' },
  { to: '/contractor/broadcast', label: 'Broadcast' },
  { to: '/contractor/favorites', label: 'Favorites' },
]

export default function ContractorApp() {
  return (
    <div className="min-h-screen">
      <nav className="sticky top-0 z-10 flex flex-wrap gap-2 border-b border-slate-200 bg-white px-4 py-3">
        {links.map((link) => (
          <NavLink
            key={link.to}
            to={link.to}
            end={link.to === '/contractor'}
            className={({ isActive }) =>
              `rounded-md px-3 py-2 text-sm font-semibold ${isActive ? 'bg-blue-100 text-contractor-primary' : 'text-slate-700'}`
            }
          >
            {link.label}
          </NavLink>
        ))}
      </nav>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/post-job" element={<PostJob />} />
        <Route path="/applicants" element={<Applicants />} />
        <Route path="/broadcast" element={<Broadcast />} />
        <Route path="/favorites" element={<Favorites />} />
        <Route path="*" element={<Navigate to="/contractor" replace />} />
      </Routes>
    </div>
  )
}
