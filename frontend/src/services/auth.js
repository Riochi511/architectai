import { apiRequest } from "./api"

export async function loginUser(email, password) {
  const result = await apiRequest("/users/login", {
    method: "POST",
    body: {
      email,
      password,
    },
  })

  localStorage.setItem(
    "access_token",
    result.access_token,
  )

  return result
}

export async function registerUser(
  fullName,
  email,
  password,
) {
  return apiRequest("/users/register", {
    method: "POST",
    body: {
      full_name: fullName,
      email,
      password,
    },
  })
}

export async function getCurrentUser() {
  const token = localStorage.getItem(
    "access_token",
  )

  if (!token) {
    return null
  }

  try {
    return await apiRequest("/users/me", {
      token,
    })
  } catch {
    localStorage.removeItem(
      "access_token",
    )

    return null
  }
}

export function logoutUser() {
  localStorage.removeItem(
    "access_token",
  )
}
