import {
  apiRequest,
  getStoredToken,
} from "./api"

function authOptions() {
  return {
    token: getStoredToken(),
  }
}

export function runOrchestration(projectId) {
  return apiRequest(
    `/orchestration/run/${projectId}`,
    {
      method: "POST",
      ...authOptions(),
    },
  )
}

export function getOrchestrationStatus(projectId) {
  return apiRequest(
    `/orchestration/${projectId}/status`,
    authOptions(),
  )
}

export function getOrchestrationOutputs(projectId) {
  return apiRequest(
    `/orchestration/${projectId}/outputs`,
    authOptions(),
  )
}
