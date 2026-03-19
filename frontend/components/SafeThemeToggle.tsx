'use client'

import { useContext } from 'react'
import { ThemeContext } from '@/contexts/ThemeContext'
import { SunIcon, MoonIcon } from '@heroicons/react/24/outline'

export default function SafeThemeToggle() {
  const context = useContext(ThemeContext)

  // If ThemeProvider is not available, use local state
  if (context === undefined) {
    const handleToggle = () => {
      const html = document.documentElement
      const isDark = html.classList.contains('dark')
      
      if (isDark) {
        html.classList.remove('dark')
        localStorage.setItem('theme', 'light')
      } else {
        html.classList.add('dark')
        localStorage.setItem('theme', 'dark')
      }
    }

    const isDark = typeof window !== 'undefined' && document.documentElement.classList.contains('dark')

    return (
      <button
        onClick={handleToggle}
        className="p-2 rounded-lg bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors"
        aria-label="Toggle theme"
      >
        {isDark ? (
          <SunIcon className="w-5 h-5 text-gray-800 dark:text-gray-200" />
        ) : (
          <MoonIcon className="w-5 h-5 text-gray-800 dark:text-gray-200" />
        )}
      </button>
    )
  }

  // If ThemeProvider is available, use it
  const { theme, toggleTheme } = context

  return (
    <button
      onClick={toggleTheme}
      className="p-2 rounded-lg bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors"
      aria-label="Toggle theme"
    >
      {theme === 'light' ? (
        <MoonIcon className="w-5 h-5 text-gray-800 dark:text-gray-200" />
      ) : (
        <SunIcon className="w-5 h-5 text-gray-800 dark:text-gray-200" />
      )}
    </button>
  )
}
