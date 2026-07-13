export const MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024

export const RESUME_ACCEPT = '.pdf,.docx'
export const RESUME_MIME_TYPES = [
  'application/pdf',
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
] as const

export const JOB_DESCRIPTION_ACCEPT = '.pdf,.docx,.txt,.png,.jpg,.jpeg,.webp'
export const JOB_DESCRIPTION_MIME_TYPES = [
  ...RESUME_MIME_TYPES,
  'text/plain',
  'image/png',
  'image/jpeg',
  'image/webp',
] as const

export const JOB_DESCRIPTION_MIN_CHARS = 50
export const JOB_DESCRIPTION_MAX_CHARS = 15000

const EXTENSION_MIME: Record<string, string> = {
  pdf: 'application/pdf',
  docx:
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
  txt: 'text/plain',
  png: 'image/png',
  jpg: 'image/jpeg',
  jpeg: 'image/jpeg',
  webp: 'image/webp',
}

function getExtension(name: string): string {
  const parts = name.split('.')
  return parts.length > 1 ? (parts.pop()?.toLowerCase() ?? '') : ''
}

export function resolveMimeType(file: File): string {
  if (file.type) return file.type
  const ext = getExtension(file.name)
  return EXTENSION_MIME[ext] ?? ''
}

export function validateResumeFile(file: File): string | null {
  if (file.size > MAX_FILE_SIZE_BYTES) {
    return 'Resume must be 5 MB or smaller.'
  }
  const mime = resolveMimeType(file)
  if (!RESUME_MIME_TYPES.includes(mime as (typeof RESUME_MIME_TYPES)[number])) {
    return 'Resume must be a PDF or DOCX file.'
  }
  return null
}

export function validateJobDescriptionFile(file: File): string | null {
  if (file.size > MAX_FILE_SIZE_BYTES) {
    return 'Job description must be 5 MB or smaller.'
  }
  const mime = resolveMimeType(file)
  if (
    !JOB_DESCRIPTION_MIME_TYPES.includes(
      mime as (typeof JOB_DESCRIPTION_MIME_TYPES)[number]
    )
  ) {
    return 'Job description must be PDF, DOCX, TXT, or an image (PNG, JPG, WEBP).'
  }
  return null
}

export function validateJobDescriptionText(text: string): string | null {
  const trimmed = text.trim()
  if (!trimmed) {
    return 'Please paste the job description or switch to file upload.'
  }
  if (trimmed.length < JOB_DESCRIPTION_MIN_CHARS) {
    return `Job description must be at least ${JOB_DESCRIPTION_MIN_CHARS} characters.`
  }
  if (trimmed.length > JOB_DESCRIPTION_MAX_CHARS) {
    return `Job description must be ${JOB_DESCRIPTION_MAX_CHARS.toLocaleString()} characters or fewer.`
  }
  return null
}
