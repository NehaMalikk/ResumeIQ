import { useState } from 'react'
import { AlignLeft, Upload } from 'lucide-react'
import { FileDropZone } from '@/components/landing/FileDropZone'
import {
  JOB_DESCRIPTION_ACCEPT,
  JOB_DESCRIPTION_MAX_CHARS,
  validateJobDescriptionFile,
  validateJobDescriptionText,
} from '@/utils/fileValidation'
import { cn } from '@/utils/cn'

export type JobDescriptionMode = 'text' | 'file'

interface JobDescriptionInputProps {
  mode: JobDescriptionMode
  text: string
  file: File | null
  error: string | null
  disabled?: boolean
  onModeChange: (mode: JobDescriptionMode) => void
  onTextChange: (text: string) => void
  onFileSelect: (file: File | null) => void
}

export function JobDescriptionInput({
  mode,
  text,
  file,
  error,
  disabled = false,
  onModeChange,
  onTextChange,
  onFileSelect,
}: JobDescriptionInputProps) {
  const [textTouched, setTextTouched] = useState(false)

  const handleValidateFile = (f: File) => validateJobDescriptionFile(f)

  const textError =
    mode === 'text' && textTouched ? validateJobDescriptionText(text) : null
  const displayError = error ?? textError

  const switchMode = (next: JobDescriptionMode) => {
    if (disabled || next === mode) return
    onModeChange(next)
  }

  return (
    <div className="flex flex-col gap-2">
      <span className="text-sm font-medium text-foreground">Job Description</span>

      <div
        className="inline-flex w-full rounded-lg border border-border bg-surface/60 p-1"
        role="tablist"
        aria-label="Job description input method"
      >
        <button
          type="button"
          role="tab"
          aria-selected={mode === 'text'}
          disabled={disabled}
          onClick={() => switchMode('text')}
          className={cn(
            'flex flex-1 items-center justify-center gap-2 rounded-md px-3 py-2 text-xs font-medium transition-all sm:text-sm',
            mode === 'text'
              ? 'bg-card text-foreground shadow-sm'
              : 'text-muted hover:text-foreground',
            disabled && 'pointer-events-none opacity-60'
          )}
        >
          <AlignLeft className="size-4 shrink-0" aria-hidden />
          Paste text
        </button>
        <button
          type="button"
          role="tab"
          aria-selected={mode === 'file'}
          disabled={disabled}
          onClick={() => switchMode('file')}
          className={cn(
            'flex flex-1 items-center justify-center gap-2 rounded-md px-3 py-2 text-xs font-medium transition-all sm:text-sm',
            mode === 'file'
              ? 'bg-card text-foreground shadow-sm'
              : 'text-muted hover:text-foreground',
            disabled && 'pointer-events-none opacity-60'
          )}
        >
          <Upload className="size-4 shrink-0" aria-hidden />
          Upload file
        </button>
      </div>

      {mode === 'text' ? (
        <div className="flex flex-col gap-1.5">
          <label htmlFor="job-description-text" className="sr-only">
            Job description text
          </label>
          <textarea
            id="job-description-text"
            value={text}
            disabled={disabled}
            rows={6}
            placeholder="Paste the full job description here — responsibilities, requirements, qualifications…"
            onChange={(e) => onTextChange(e.target.value)}
            onBlur={() => setTextTouched(true)}
            aria-describedby={
              displayError ? 'job-description-error' : 'job-description-text-hint'
            }
            aria-invalid={!!displayError}
            className={cn(
              'min-h-[140px] w-full resize-y rounded-xl border bg-card px-4 py-3 text-sm leading-relaxed text-foreground transition-colors',
              'placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2',
              disabled && 'cursor-not-allowed opacity-60',
              displayError
                ? 'border-red-300'
                : 'border-border hover:border-primary/30'
            )}
          />
          <p
            id="job-description-text-hint"
            className="text-xs text-muted"
          >
            Plain text only · {text.trim().length.toLocaleString()} /{' '}
            {JOB_DESCRIPTION_MAX_CHARS.toLocaleString()} characters
          </p>
        </div>
      ) : (
        <FileDropZone
          id="job-upload"
          label=""
          hint="PDF, DOCX, TXT, PNG, JPG, or WEBP · Max 5 MB"
          accept={JOB_DESCRIPTION_ACCEPT}
          file={file}
          error={displayError}
          disabled={disabled}
          onFileSelect={onFileSelect}
          onValidate={handleValidateFile}
        />
      )}

      {mode === 'text' && displayError && (
        <p
          id="job-description-error"
          role="alert"
          className="text-xs font-medium text-red-600"
        >
          {displayError}
        </p>
      )}
    </div>
  )
}
