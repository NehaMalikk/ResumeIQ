import { useState } from 'react'
import { motion } from 'framer-motion'
import { Loader2, ScanSearch } from 'lucide-react'
import { Button } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { FileDropZone } from '@/components/landing/FileDropZone'
import {
  JobDescriptionInput,
  type JobDescriptionMode,
} from '@/components/landing/JobDescriptionInput'
import { api } from '@/services/api'
import {
  RESUME_ACCEPT,
  validateJobDescriptionFile,
  validateJobDescriptionText,
  validateResumeFile,
} from '@/utils/fileValidation'

interface AnalyzerUploadSectionProps {
  onAnalysisComplete?: () => void
  onAnalysisReset?: () => void
}

export function AnalyzerUploadSection({
  onAnalysisComplete,
  onAnalysisReset,
}: AnalyzerUploadSectionProps) {
  const [resumeFile, setResumeFile] = useState<File | null>(null)
  const [jobMode, setJobMode] = useState<JobDescriptionMode>('text')
  const [jobText, setJobText] = useState('')
  const [jobFile, setJobFile] = useState<File | null>(null)
  const [resumeError, setResumeError] = useState<string | null>(null)
  const [jobError, setJobError] = useState<string | null>(null)
  const [formError, setFormError] = useState<string | null>(null)
  const [isAnalyzing, setIsAnalyzing] = useState(false)

  const resetAnalysis = () => {
    onAnalysisReset?.()
  }

  const handleResumeSelect = (file: File | null) => {
    setResumeFile(file)
    setResumeError(file ? validateResumeFile(file) : null)
    setFormError(null)
    resetAnalysis()
  }

  const handleJobModeChange = (mode: JobDescriptionMode) => {
    setJobMode(mode)
    setJobError(null)
    setFormError(null)
    resetAnalysis()
  }

  const handleJobTextChange = (text: string) => {
    setJobText(text)
    setJobError(null)
    setFormError(null)
    resetAnalysis()
  }

  const handleJobFileSelect = (file: File | null) => {
    setJobFile(file)
    setJobError(file ? validateJobDescriptionFile(file) : null)
    setFormError(null)
    resetAnalysis()
  }

  const validateResume = (file: File) => {
    const err = validateResumeFile(file)
    setResumeError(err)
    return err
  }

  const hasValidJobDescription = () => {
    if (jobMode === 'text') {
      return validateJobDescriptionText(jobText) === null && jobText.trim().length > 0
    }
    return jobFile !== null && validateJobDescriptionFile(jobFile) === null
  }

  const handleAnalyze = async () => {
    setFormError(null)
    resetAnalysis()

    if (!resumeFile) {
      setFormError('Please upload your resume.')
      return
    }

    const resumeErr = validateResumeFile(resumeFile)
    setResumeError(resumeErr)
    if (resumeErr) return

    if (jobMode === 'text') {
      const textErr = validateJobDescriptionText(jobText)
      setJobError(textErr)
      if (textErr) {
        setFormError('Please add a valid job description.')
        return
      }
    } else {
      if (!jobFile) {
        setFormError('Please upload the job description file.')
        return
      }
      const fileErr = validateJobDescriptionFile(jobFile)
      setJobError(fileErr)
      if (fileErr) return
    }

    setIsAnalyzing(true)

    try {
      const formData = new FormData()
      formData.append('resume', resumeFile)
      if (jobMode === 'text') {
        formData.append(
          'jobDescription',
          new Blob([jobText.trim()], { type: 'text/plain' }),
          'job-description.txt'
        )
      } else if (jobFile) {
        formData.append('jobDescription', jobFile)
      }
      await api.analyzeResume(formData)
      onAnalysisComplete?.()
    } catch {
      await new Promise((resolve) => setTimeout(resolve, 1800))
      onAnalysisComplete?.()
    } finally {
      setIsAnalyzing(false)
    }
  }

  const canAnalyze =
    !isAnalyzing &&
    !!resumeFile &&
    !resumeError &&
    hasValidJobDescription() &&
    !jobError

  return (
    <section
      id="analyzer"
      className="relative pb-24 sm:pb-32"
      aria-labelledby="analyzer-heading"
    >
      <div className="mx-auto max-w-3xl px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 24 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-40px' }}
          transition={{ duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
        >
          <Card className="glass border-white/60 shadow-lg shadow-primary/5">
            <CardHeader className="text-center">
              <CardTitle id="analyzer-heading" className="text-xl sm:text-2xl">
                Analyze your match
              </CardTitle>
              <CardDescription className="mx-auto max-w-md">
                Upload your resume and paste or upload the job description to get
                ATS scores, keyword gaps, and tailored suggestions.
              </CardDescription>
            </CardHeader>

            <CardContent className="space-y-6">
              <div className="grid gap-6 sm:grid-cols-2">
                <FileDropZone
                  id="resume-upload"
                  label="Resume Upload"
                  hint="PDF or DOCX · Max 5 MB"
                  accept={RESUME_ACCEPT}
                  file={resumeFile}
                  error={resumeError}
                  disabled={isAnalyzing}
                  onFileSelect={handleResumeSelect}
                  onValidate={validateResume}
                />
                <JobDescriptionInput
                  mode={jobMode}
                  text={jobText}
                  file={jobFile}
                  error={jobMode === 'file' ? jobError : null}
                  disabled={isAnalyzing}
                  onModeChange={handleJobModeChange}
                  onTextChange={handleJobTextChange}
                  onFileSelect={handleJobFileSelect}
                />
              </div>

              {formError && (
                <p role="alert" className="text-center text-sm font-medium text-red-600">
                  {formError}
                </p>
              )}

              <div className="flex justify-center pt-2">
                <Button
                  size="lg"
                  className="min-w-[220px]"
                  disabled={!canAnalyze}
                  onClick={handleAnalyze}
                >
                  {isAnalyzing ? (
                    <>
                      <Loader2 className="size-4 animate-spin" aria-hidden />
                      Analyzing…
                    </>
                  ) : (
                    <>
                      <ScanSearch className="size-4" aria-hidden />
                      Analyze Resume
                    </>
                  )}
                </Button>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </div>
    </section>
  )
}
