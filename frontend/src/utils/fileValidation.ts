export const MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024
export const RESUME_ACCEPT = '.pdf,.doc,.docx,.txt,.png,.jpg,.jpeg'
export const RESUME_MIME_TYPES = [
  'application/pdf',
  'application/msword',
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
  'text/plain',
  'image/png',
  'image/jpeg',
] as const
const RESUME_EXTENSIONS = new Set(['pdf', 'doc', 'docx', 'txt', 'png', 'jpg', 'jpeg'])
export const JOB_DESCRIPTION_MIN_CHARS = 50
export const JOB_DESCRIPTION_MAX_CHARS = 15000

const EXTENSION_MIME: Record<string, string> = {
  pdf: 'application/pdf', doc: 'application/msword',
  docx: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
  txt: 'text/plain', png: 'image/png', jpg: 'image/jpeg', jpeg: 'image/jpeg',
}

function getExtension(name: string): string {
  const parts = name.split('.')
  return parts.length > 1 ? (parts.pop()?.toLowerCase() ?? '') : ''
}

export function resolveMimeType(file: File): string {
  if (file.type) return file.type
  return EXTENSION_MIME[getExtension(file.name)] ?? ''
}

export function validateResumeFile(file: File): string | null {
  if (file.size > MAX_FILE_SIZE_BYTES) return 'Resume must be 5 MB or smaller.'
  if (!RESUME_EXTENSIONS.has(getExtension(file.name))) {
    return 'Resume must be PDF, DOC, DOCX, TXT, PNG, JPG, or JPEG.'
  }
  return null
}

export function validateJobDescriptionText(text: string): string | null {
  const trimmed = text.trim()
  if (!trimmed) return 'Please paste the job description.'
  if (trimmed.length < JOB_DESCRIPTION_MIN_CHARS) return `Job description must be at least ${JOB_DESCRIPTION_MIN_CHARS} characters.`
  if (trimmed.length > JOB_DESCRIPTION_MAX_CHARS) return `Job description must be ${JOB_DESCRIPTION_MAX_CHARS.toLocaleString()} characters or fewer.`
  return null
}
