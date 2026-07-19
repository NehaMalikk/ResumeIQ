import { useEffect, useRef, useState } from 'react'
import { AnalysisResultsSection } from '@/components/landing/AnalysisResultsSection'
import { AnalyzerUploadSection } from '@/components/landing/AnalyzerUploadSection'
import { HeroSection } from '@/components/landing/HeroSection'
import type { AnalyzeResponse } from '@/types'

export function LandingPage() {
  const [analysisResult, setAnalysisResult] = useState<AnalyzeResponse | null>(null)
  const resultsRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (analysisResult && resultsRef.current) {
      resultsRef.current.scrollIntoView({ behavior: 'smooth', block: 'start' })
    }
  }, [analysisResult])

  return (
    <>
      <HeroSection />
      <AnalyzerUploadSection
        onAnalysisComplete={setAnalysisResult}
        onAnalysisReset={() => setAnalysisResult(null)}
      />
      {analysisResult && (
        <div ref={resultsRef}>
          <AnalysisResultsSection result={analysisResult} />
        </div>
      )}
    </>
  )
}
