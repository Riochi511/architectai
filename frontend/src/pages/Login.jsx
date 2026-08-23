import { useState } from "react"
import { useAuth } from "../contexts/useAuth"

export default function Login({
  onRegister,
}) {
  const { login } = useAuth()

  const [email, setEmail] = useState("")
  const [password, setPassword] =
    useState("")
  const [loading, setLoading] =
    useState(false)
  const [error, setError] =
    useState("")

  async function handleSubmit(event) {
    event.preventDefault()

    setLoading(true)
    setError("")

    try {
      await login(email, password)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="auth-page">
      <section className="auth-card">
        <p className="eyebrow">
          ARCHITECTAI
        </p>

        <h1>Welcome back</h1>

        <p className="auth-subtitle">
          Sign in to continue building
          your engineering blueprint.
        </p>

        {error && (
          <div className="error">
            <strong>Login failed</strong>
            <p>{error}</p>
          </div>
        )}

        <form
          className="auth-form"
          onSubmit={handleSubmit}
        >
          <label htmlFor="email">
            Email
          </label>

          <input
            id="email"
            type="email"
            required
            autoComplete="email"
            value={email}
            onChange={(event) =>
              setEmail(
                event.target.value,
              )
            }
          />

          <label htmlFor="password">
            Password
          </label>

          <input
            id="password"
            type="password"
            required
            autoComplete="current-password"
            value={password}
            onChange={(event) =>
              setPassword(
                event.target.value,
              )
            }
          />

          <button
            type="submit"
            disabled={loading}
          >
            {loading
              ? "Signing in..."
              : "Sign in"}
          </button>
        </form>

        <button
          type="button"
          className="text-button"
          onClick={onRegister}
        >
          Create an account
        </button>
      </section>
    </main>
  )
}

