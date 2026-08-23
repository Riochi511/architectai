import { useState } from "react"
import { useAuth } from "../contexts/useAuth"

export default function Register({
  onLogin,
}) {
  const { register } = useAuth()

  const [fullName, setFullName] =
    useState("")
  const [email, setEmail] =
    useState("")
  const [password, setPassword] =
    useState("")
  const [loading, setLoading] =
    useState(false)
  const [error, setError] =
    useState("")
  const [success, setSuccess] =
    useState("")

  async function handleSubmit(event) {
    event.preventDefault()

    setLoading(true)
    setError("")
    setSuccess("")

    try {
      await register(
        fullName,
        email,
        password,
      )

      setSuccess(
        "Account created. You can now sign in.",
      )

      setFullName("")
      setEmail("")
      setPassword("")
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

        <h1>Create your account</h1>

        <p className="auth-subtitle">
          Start turning ideas into
          production-ready architecture.
        </p>

        {error && (
          <div className="error">
            <strong>Registration failed</strong>
            <p>{error}</p>
          </div>
        )}

        {success && (
          <div className="success">
            {success}
          </div>
        )}

        <form
          className="auth-form"
          onSubmit={handleSubmit}
        >
          <label htmlFor="full-name">
            Full name
          </label>

          <input
            id="full-name"
            type="text"
            required
            autoComplete="name"
            value={fullName}
            onChange={(event) =>
              setFullName(
                event.target.value,
              )
            }
          />

          <label htmlFor="register-email">
            Email
          </label>

          <input
            id="register-email"
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

          <label htmlFor="register-password">
            Password
          </label>

          <input
            id="register-password"
            type="password"
            required
            minLength="6"
            autoComplete="new-password"
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
              ? "Creating account..."
              : "Create account"}
          </button>
        </form>

        <button
          type="button"
          className="text-button"
          onClick={onLogin}
        >
          Already have an account?
          Sign in
        </button>
      </section>
    </main>
  )
}

