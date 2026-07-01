import { useCallback, useId, useRef, useState } from 'react'
import { FileText, Upload, X } from 'lucide-react'
import { cn } from '@/utils/cn'

interface FileDropZoneProps {
  id?: string
  label?: string
  hint: string
  accept: string
  file: File | null
  error: string | null
  disabled?: boolean
  onFileSelect: (file: File | null) => void
  onValidate: (file: File) => string | null
}

export function FileDropZone({
  id: idProp,
  label,
  hint,
  accept,
  file,
  error,
  disabled = false,
  onFileSelect,
  onValidate,
}: FileDropZoneProps) {
  const autoId = useId()
  const inputId = idProp ?? autoId
  const inputRef = useRef<HTMLInputElement>(null)
  const [isDragging, setIsDragging] = useState(false)

  const handleFile = useCallback(
    (next: File | null) => {
      if (!next) {
        onFileSelect(null)
        return
      }
      const validationError = onValidate(next)
      if (validationError) {
        onFileSelect(null)
        return
      }
      onFileSelect(next)
    },
    [onFileSelect, onValidate]
  )

  const onDragOver = (e: React.DragEvent) => {
    e.preventDefault()
    if (!disabled) setIsDragging(true)
  }

  const onDragLeave = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
  }

  const onDrop = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
    if (disabled) return
    const dropped = e.dataTransfer.files[0]
    if (dropped) handleFile(dropped)
  }

  const onInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selected = e.target.files?.[0] ?? null
    handleFile(selected)
    e.target.value = ''
  }

  const formatSize = (bytes: number) => {
    if (bytes < 1024) return `${bytes} B`
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
  }

  return (
    <div className="flex flex-col gap-2">
      {label ? (
        <label htmlFor={inputId} className="text-sm font-medium text-foreground">
          {label}
        </label>
      ) : null}

      <div
        role="button"
        tabIndex={disabled ? -1 : 0}
        onKeyDown={(e) => {
          if (disabled) return
          if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault()
            inputRef.current?.click()
          }
        }}
        onClick={() => !disabled && inputRef.current?.click()}
        onDragOver={onDragOver}
        onDragLeave={onDragLeave}
        onDrop={onDrop}
        aria-describedby={error ? `${inputId}-error` : `${inputId}-hint`}
        aria-invalid={!!error}
        className={cn(
          'group relative flex min-h-[140px] cursor-pointer flex-col items-center justify-center rounded-xl border-2 border-dashed px-4 py-6 text-center transition-all duration-200',
          'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2',
          disabled && 'pointer-events-none cursor-not-allowed opacity-60',
          error
            ? 'border-red-300 bg-red-50/50'
            : isDragging
              ? 'border-primary bg-accent-soft/40'
              : file
                ? 'border-primary/40 bg-accent-soft/20'
                : 'border-border bg-card hover:border-primary/40 hover:bg-surface/50'
        )}
      >
        <input
          ref={inputRef}
          id={inputId}
          type="file"
          accept={accept}
          className="sr-only"
          disabled={disabled}
          onChange={onInputChange}
        />

        {file ? (
          <div className="flex w-full max-w-sm items-center gap-3 rounded-lg border border-border/80 bg-white/90 px-3 py-2.5 shadow-sm">
            <div className="flex size-10 shrink-0 items-center justify-center rounded-lg bg-primary/10 text-primary">
              <FileText className="size-5" aria-hidden />
            </div>
            <div className="min-w-0 flex-1 text-left">
              <p className="truncate text-sm font-medium text-foreground">
                {file.name}
              </p>
              <p className="text-xs text-muted">{formatSize(file.size)}</p>
            </div>
            <button
              type="button"
              disabled={disabled}
              onClick={(e) => {
                e.stopPropagation()
                onFileSelect(null)
              }}
              className="flex size-8 shrink-0 items-center justify-center rounded-md text-muted transition-colors hover:bg-surface hover:text-foreground"
              aria-label={`Remove ${file.name}`}
            >
              <X className="size-4" />
            </button>
          </div>
        ) : (
          <>
            <div
              className={cn(
                'mb-3 flex size-11 items-center justify-center rounded-xl transition-colors',
                isDragging
                  ? 'bg-primary text-primary-foreground'
                  : 'bg-surface text-primary group-hover:bg-primary/10'
              )}
            >
              <Upload className="size-5" aria-hidden />
            </div>
            <p className="text-sm font-medium text-foreground">
              Drag and drop or{' '}
              <span className="text-primary">browse files</span>
            </p>
            <p id={`${inputId}-hint`} className="mt-1 text-xs text-muted">
              {hint}
            </p>
          </>
        )}
      </div>

      {error && (
        <p
          id={`${inputId}-error`}
          role="alert"
          className="text-xs font-medium text-red-600"
        >
          {error}
        </p>
      )}
    </div>
  )
}
