import { useEffect, useRef, useState } from 'react'
import { motion } from 'framer-motion'
import { Loader2, ScanSearch } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { FileDropZone } from '@/components/landing/FileDropZone'
import { JobDescriptionInput } from '@/components/landing/JobDescriptionInput'
import { api } from '@/services/api'
import { getApiErrorMessage } from '@/services/apiErrors'
import type { AnalyzeResponse } from '@/types'
import { RESUME_ACCEPT, validateJobDescriptionText, validateResumeFile } from '@/utils/fileValidation'

interface AnalyzerUploadSectionProps { onAnalysisComplete: (result: AnalyzeResponse) => void; onAnalysisReset: () => void }

export function AnalyzerUploadSection({ onAnalysisComplete, onAnalysisReset }: AnalyzerUploadSectionProps) {
  const [resumeFile, setResumeFile] = useState<File | null>(null)
  const [jobText, setJobText] = useState('')
  const [resumeError, setResumeError] = useState<string | null>(null)
  const [formError, setFormError] = useState<string | null>(null)
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const requestRef = useRef<AbortController | null>(null)
  useEffect(() => () => requestRef.current?.abort(), [])

  const cancelAndReset = () => {
    requestRef.current?.abort(); requestRef.current = null
    setIsAnalyzing(false); setFormError(null); onAnalysisReset()
  }
  const handleResumeSelect = (file: File | null) => {
    cancelAndReset(); setResumeFile(file); setResumeError(file ? validateResumeFile(file) : null)
  }
  const handleJobTextChange = (text: string) => { cancelAndReset(); setJobText(text) }

  const handleAnalyze = async () => {
    setFormError(null); onAnalysisReset()
    if (!resumeFile) { setFormError('Please upload your resume.'); return }
    const resumeValidation = validateResumeFile(resumeFile)
    const jobValidation = validateJobDescriptionText(jobText)
    setResumeError(resumeValidation)
    if (resumeValidation || jobValidation) { setFormError(jobValidation ?? resumeValidation); return }
    requestRef.current?.abort()
    const controller = new AbortController(); requestRef.current = controller; setIsAnalyzing(true)
    try {
      const result = await api.analyzeResume(resumeFile, jobText, controller.signal)
      if (requestRef.current === controller && !controller.signal.aborted) onAnalysisComplete(result)
    } catch (error) {
      if (!controller.signal.aborted && requestRef.current === controller) setFormError(getApiErrorMessage(error instanceof Error ? error : {}))
    } finally {
      if (requestRef.current === controller) { requestRef.current = null; setIsAnalyzing(false) }
    }
  }

  const canAnalyze = !isAnalyzing && !!resumeFile && !resumeError && validateJobDescriptionText(jobText) === null
  return (
    <section id="analyzer" className="relative pb-24 sm:pb-32" aria-labelledby="analyzer-heading">
      <div className="mx-auto max-w-3xl px-4 sm:px-6 lg:px-8"><motion.div initial={{ opacity: 0, y: 24 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true, margin: '-40px' }} transition={{ duration: 0.5 }}>
        <Card className="glass border-white/60 shadow-lg shadow-primary/5"><CardHeader className="text-center"><CardTitle id="analyzer-heading" className="text-xl sm:text-2xl">Analyze your match</CardTitle><CardDescription className="mx-auto max-w-md">Upload your resume and paste the job description to get ATS scores, skill gaps, and tailored suggestions.</CardDescription></CardHeader>
          <CardContent className="space-y-6"><div className="grid gap-6 sm:grid-cols-2">
            <FileDropZone id="resume-upload" label="Resume Upload" hint="PDF, DOC, DOCX, TXT, PNG, JPG, or JPEG · Max 5 MB" accept={RESUME_ACCEPT} file={resumeFile} error={resumeError} disabled={isAnalyzing} onFileSelect={handleResumeSelect} onValidate={validateResumeFile} />
            <JobDescriptionInput text={jobText} disabled={isAnalyzing} onTextChange={handleJobTextChange} />
          </div><div aria-live="polite" aria-atomic="true">{formError && <p role="alert" className="text-center text-sm font-medium text-red-600">{formError}</p>}{isAnalyzing && <p className="sr-only">Analysis is in progress.</p>}</div>
          <div className="flex justify-center pt-2"><Button size="lg" className="min-w-[220px]" disabled={!canAnalyze} onClick={handleAnalyze}>{isAnalyzing ? <><Loader2 className="size-4 animate-spin" aria-hidden />Analyzing…</> : <><ScanSearch className="size-4" aria-hidden />Analyze Resume</>}</Button></div></CardContent>
        </Card>
      </motion.div></div>
    </section>
  )
}
