interface FastApiValidationIssue {
  loc?: Array<string | number>
  msg?: string
  type?: string
}

export class ApiError extends Error {
  readonly status: number | null
  readonly detail?: string | FastApiValidationIssue[]

  constructor(
    status: number | null,
    message: string,
    detail?: string | FastApiValidationIssue[]
  ) {
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.detail = detail
  }
}

function statusMessage(status: number): string {
  switch (status) {
    case 400: return 'The resume or job description is invalid.'
    case 415: return 'This file type is not supported.'
    case 422: return 'Please provide both a resume and job description.'
    case 500: return 'The analysis could not be completed. Please try again.'
    default: return 'The analysis request failed. Please try again.'
  }
}

export async function createApiError(response: Response): Promise<ApiError> {
  let detail: string | FastApiValidationIssue[] | undefined
  if (response.headers.get('content-type')?.includes('application/json')) {
    try {
      const body: { detail?: string | FastApiValidationIssue[] } = await response.json()
      detail = body.detail
    } catch {
      // Invalid error JSON is deliberately replaced with a safe status message.
    }
  }
  const message = typeof detail === 'string' && response.status < 500
    ? detail
    : statusMessage(response.status)
  return new ApiError(response.status, message, detail)
}

export function getApiErrorMessage(error: object): string {
  if (error instanceof ApiError) return error.message
  if (error instanceof TypeError) {
    return 'Unable to reach the analysis service. Check your connection and try again.'
  }
  return 'The analysis could not be completed. Please try again.'
}
