import {
  useEffect,
  useState,
} from "react"

import {
  getCurrentUser,
  loginUser,
  logoutUser,
  registerUser,
} from "../services/auth"

import { AuthContext } from "./authContext"

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let mounted = true

    async function loadUser() {
      const currentUser =
        await getCurrentUser()

      if (mounted) {
        setUser(currentUser)
        setLoading(false)
      }
    }

    loadUser()

    return () => {
      mounted = false
    }
  }, [])

  async function login(email, password) {
    await loginUser(email, password)

    const currentUser =
      await getCurrentUser()

    setUser(currentUser)

    return currentUser
  }

  async function register(
    fullName,
    email,
    password,
  ) {
    return registerUser(
      fullName,
      email,
      password,
    )
  }

  function logout() {
    logoutUser()
    setUser(null)
  }

  const value = {
    user,
    loading,
    isAuthenticated: Boolean(user),
    login,
    register,
    logout,
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}
