import clsx from 'clsx'
import { NavLink } from 'react-router-dom'

const NAV_ITEMS = [
  { path: '/worker', icon: '🏠', label: 'Home' },
  { path: '/worker/jobs', icon: '🔍', label: 'Jobs' },
  { path: '/worker/my-jobs', icon: '📋', label: 'My Jobs' },
  { path: '/worker/profile', icon: '👤', label: 'Profile' },
]

export const BottomNav = () => {
  return (
    <nav className="fixed bottom-0 left-0 right-0 mx-auto flex max-w-md justify-around border-t border-slate-300 bg-white py-2">
      {NAV_ITEMS.map((item) => (
        <NavLink
          key={item.path}
          to={item.path}
          className={({ isActive }) =>
            clsx('touch-target-48 flex w-20 flex-col items-center justify-center rounded-md text-xs', isActive && 'bg-slate-100 font-bold text-worker-primary')
          }
        >
          <span aria-hidden="true">{item.icon}</span>
          <span>{item.label}</span>
        </NavLink>
      ))}
    </nav>
  )
}
