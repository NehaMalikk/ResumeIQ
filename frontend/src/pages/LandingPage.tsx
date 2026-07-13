import { useEffect, useRef, useState } from 'react'
import { AnalysisResultsSection } from '@/components/landing/AnalysisResultsSection'
import { AnalyzerUploadSection } from '@/components/landing/AnalyzerUploadSection'
import { HeroSection } from '@/components/landing/HeroSection'

export function LandingPage() {
  const [showResults, setShowResults] = useState(false)
  const resultsRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (showResults && resultsRef.current) {
      resultsRef.current.scrollIntoView({ behavior: 'smooth', block: 'start' })
    }
  }, [showResults])

  return (
    <>
      <HeroSection />
      <AnalyzerUploadSection
        onAnalysisComplete={() => setShowResults(true)}
        onAnalysisReset={() => setShowResults(false)}
      />
      {showResults && (
        <div ref={resultsRef}>
          <AnalysisResultsSection />
        </div>
      )}
    </>
  )
}
