interface PasswordStrengthProps {
  password: string
}

export default function PasswordStrength({ password }: PasswordStrengthProps) {
  const calculateStrength = (pass: string): { score: number; label: string; color: string } => {
    if (!pass) return { score: 0, label: '', color: '' }

    let score = 0
    
    // Length
    if (pass.length >= 8) score++
    if (pass.length >= 12) score++
    
    // Contains lowercase
    if (/[a-z]/.test(pass)) score++
    
    // Contains uppercase
    if (/[A-Z]/.test(pass)) score++
    
    // Contains number
    if (/\d/.test(pass)) score++
    
    // Contains special character
    if (/[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(pass)) score++

    if (score <= 2) return { score: 1, label: 'Débil', color: 'bg-red-500' }
    if (score <= 4) return { score: 2, label: 'Media', color: 'bg-yellow-500' }
    if (score <= 5) return { score: 3, label: 'Buena', color: 'bg-blue-500' }
    return { score: 4, label: 'Fuerte', color: 'bg-green-500' }
  }

  const strength = calculateStrength(password)

  if (!password) return null

  return (
    <div className="mt-2">
      <div className="flex items-center gap-2 mb-1">
        <div className="flex-1 h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
          <div
            className={`h-full ${strength.color} transition-all duration-300`}
            style={{ width: `${(strength.score / 4) * 100}%` }}
          />
        </div>
        <span className={`text-xs font-medium ${
          strength.score === 1 ? 'text-red-600 dark:text-red-400' :
          strength.score === 2 ? 'text-yellow-600 dark:text-yellow-400' :
          strength.score === 3 ? 'text-blue-600 dark:text-blue-400' :
          'text-green-600 dark:text-green-400'
        }`}>
          {strength.label}
        </span>
      </div>
      <div className="text-xs text-gray-600 dark:text-gray-400 space-y-1">
        {password.length < 8 && (
          <p>• Mínimo 8 caracteres</p>
        )}
        {!/[A-Z]/.test(password) && (
          <p>• Incluye al menos una mayúscula</p>
        )}
        {!/[a-z]/.test(password) && (
          <p>• Incluye al menos una minúscula</p>
        )}
        {!/\d/.test(password) && (
          <p>• Incluye al menos un número</p>
        )}
        {!/[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password) && (
          <p>• Incluye al menos un carácter especial</p>
        )}
      </div>
    </div>
  )
}

