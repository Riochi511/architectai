import { useState } from "react"

import { AuthProvider } from "./contexts/AuthContext.jsx"
import { useAuth } from "./contexts/useAuth"

import Login from "./pages/Login"
import Register from "./pages/Register"

import {
  runOrchestration,
  getOrchestrationStatus,
  getOrchestrationOutputs,
} from "./services/orchestration"

import "./App.css"

function AuthenticatedApp() {
  const { user, logout } = useAuth()

  const [projectId, setProjectId] =
    useState("")
  const [status, setStatus] =
    useState(null)
  const [outputs, setOutputs] =
    useState(null)
  const [loading, setLoading] =
    useState(false)
  const [error, setError] =
    useState("")

  function getProjectId() {
    const id = Number(projectId)

    if (
      !Number.isInteger(id) ||
      id <= 0
    ) {
      throw new Error(
        "Enter a valid project ID.",
      )
    }

    return id
  }

  async function handleRun() {
    setLoading(true)
    setError("")
    setStatus(null)
    setOutputs(null)

    try {
      const id = getProjectId()
      const result =
        await runOrchestration(id)

      setStatus(result)
      setOutputs(result.outputs)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  async function handleStatus() {
    setLoading(true)
    setError("")

    try {
      const id = getProjectId()
      const result =
        await getOrchestrationStatus(id)

      setStatus(result)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  async function handleOutputs() {
    setLoading(true)
    setError("")

    try {
      const id = getProjectId()
      const result =
        await getOrchestrationOutputs(id)

      setOutputs(result)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="app">
      <section className="container">
        <header className="header">
          <div className="topbar">
            <div>
              <p className="eyebrow">
                ARCHITECTAI
              </p>

              <h1>
                AI Solutions Architecture
              </h1>
            </div>

            <div className="user-menu">
              <span>{user?.full_name}</span>

              <button
                type="button"
                className="secondary"
                onClick={logout}
              >
                Sign out
              </button>
            </div>
          </div>

          <p className="subtitle">
            Turn product ideas into
            production-ready engineering
            blueprints.
          </p>
        </header>

        <section className="panel">
          <label htmlFor="project-id">
            Project ID
          </label>

          <input
            id="project-id"
            type="number"
            min="1"
            placeholder="Enter project ID"
            value={projectId}
            onChange={(event) =>
              setProjectId(
                event.target.value,
              )
            }
          />

          <div className="actions">
            <button
              type="button"
              onClick={handleRun}
              disabled={loading}
            >
              {loading
                ? "Working..."
                : "Run Orchestration"}
            </button>

            <button
              type="button"
              className="secondary"
              onClick={handleStatus}
              disabled={loading}
            >
              Check Status
            </button>

            <button
              type="button"
              className="secondary"
              onClick={handleOutputs}
              disabled={loading}
            >
              Get Outputs
            </button>
          </div>
        </section>

        {error && (
          <section className="error">
            <strong>Request failed</strong>
            <p>{error}</p>
          </section>
        )}

        {status && (
          <section className="panel">
            <h2>
              Orchestration Status
            </h2>

            <div className="status-grid">
              <div>
                <span>Status</span>
                <strong>
                  {status.status}
                </strong>
              </div>

              <div>
                <span>Run ID</span>
                <strong>
                  {status.run_id ?? "N/A"}
                </strong>
              </div>

              <div>
                <span>Current Stage</span>
                <strong>
                  {status.current_stage ??
                    "N/A"}
                </strong>
              </div>
            </div>

            <h3>
              Completed Stages
            </h3>

            <div className="stages">
              {(
                status.completed_stages || []
              ).map((stage) => (
                <span
                  className="stage"
                  key={stage}
                >
                  {stage}
                </span>
              ))}
            </div>
          </section>
        )}

        {outputs && (
          <section className="panel">
            <h2>
              Generated Outputs
            </h2>

            <pre>
              {JSON.stringify(
                outputs,
                null,
                2,
              )}
            </pre>
          </section>
        )}
      </section>
    </main>
  )
}

function AppContent() {
  const { user, loading } =
    useAuth()

  const [showRegister, setShowRegister] =
    useState(false)

  if (loading) {
    return (
      <main className="auth-page">
        <section className="auth-card">
          <p className="eyebrow">
            ARCHITECTAI
          </p>

          <h1>Loading...</h1>
        </section>
      </main>
    )
  }

  if (!user) {
    if (showRegister) {
      return (
        <Register
          onLogin={() =>
            setShowRegister(false)
          }
        />
      )
    }

    return (
      <Login
        onRegister={() =>
          setShowRegister(true)
        }
      />
    )
  }

  return <AuthenticatedApp />
}

function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  )
}

export default App


