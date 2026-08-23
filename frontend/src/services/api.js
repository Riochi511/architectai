const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000"

export async function apiRequest(
  path,
  {
    method = "GET",
    body,
    token,
  } = {},
) {
  const headers = {
    Accept: "application/json",
  }

  if (body !== undefined) {
    headers["Content-Type"] = "application/json"
  }

  if (token) {
    headers.Authorization = `Bearer ${token}`
  }

  const response = await fetch(
    `${API_BASE_URL}${path}`,
    {
      method,
      headers,
      body:
        body !== undefined
          ? JSON.stringify(body)
          : undefined,
    },
  )

  if (!response.ok) {
    const contentType =
      response.headers.get("content-type") || ""

    let data

    if (contentType.includes("application/json")) {
      data = await response.json()
    } else {
      data = await response.text()
    }

    const message =
      typeof data === "object" &&
      data !== null &&
      "detail" in data
        ? data.detail
        : `API request failed with status ${response.status}`

    throw new Error(message)
  }

  const contentType =
    response.headers.get("content-type") || ""

  if (contentType.includes("application/json")) {
    return response.json()
  }

  return response.text()
}

export function getStoredToken() {
  return localStorage.getItem("access_token")
}
