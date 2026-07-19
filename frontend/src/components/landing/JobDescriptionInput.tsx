import { useState } from 'react'
import { AlignLeft } from 'lucide-react'
import { JOB_DESCRIPTION_MAX_CHARS, validateJobDescriptionText } from '@/utils/fileValidation'
import { cn } from '@/utils/cn'

interface JobDescriptionInputProps { text: string; disabled?: boolean; onTextChange: (text: string) => void }

export function JobDescriptionInput({ text, disabled = false, onTextChange }: JobDescriptionInputProps) {
  const [textTouched, setTextTouched] = useState(false)
  const error = textTouched ? validateJobDescriptionText(text) : null
  return (
    <div className="flex flex-col gap-2">
      <span className="text-sm font-medium text-foreground">Job Description</span>
      <div className="inline-flex items-center gap-2 rounded-lg border border-border bg-card px-3 py-2 text-sm font-medium"><AlignLeft className="size-4 text-primary" aria-hidden />Paste text</div>
      <label htmlFor="job-description-text" className="sr-only">Job description text</label>
      <textarea id="job-description-text" value={text} disabled={disabled} rows={6} placeholder="Paste the full job description here — responsibilities, requirements, qualifications…" onChange={(event) => onTextChange(event.target.value)} onBlur={() => setTextTouched(true)} aria-describedby={error ? 'job-description-error' : 'job-description-text-hint'} aria-invalid={!!error} className={cn('min-h-[140px] w-full resize-y rounded-xl border bg-card px-4 py-3 text-sm leading-relaxed text-foreground transition-colors', 'placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2', disabled && 'cursor-not-allowed opacity-60', error ? 'border-red-300' : 'border-border hover:border-primary/30')} />
      <p id="job-description-text-hint" className="text-xs text-muted">Plain text only · {text.trim().length.toLocaleString()} / {JOB_DESCRIPTION_MAX_CHARS.toLocaleString()} characters</p>
      <p className="text-xs text-muted">Job description file upload will be supported in a future update. Paste the text for now.</p>
      {error && <p id="job-description-error" role="alert" className="text-xs font-medium text-red-600">{error}</p>}
    </div>
  )
}
