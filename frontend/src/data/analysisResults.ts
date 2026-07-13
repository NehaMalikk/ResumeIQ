export interface AnalysisSuggestion {
  id: string
  title: string
  description: string
  priority: 'high' | 'medium' | 'low'
}

export interface AnalysisResults {
  atsMatchScore: number
  keywordMatch: {
    matched: number
    total: number
    percentage: number
  }
  missingKeywords: string[]
  suggestions: AnalysisSuggestion[]
  resumeStrength: {
    score: number
    label: string
    dimensions: { label: string; value: number }[]
  }
}

export const dummyAnalysisResults: AnalysisResults = {
  atsMatchScore: 78,
  keywordMatch: {
    matched: 24,
    total: 31,
    percentage: 77,
  },
  missingKeywords: [
    'Kubernetes',
    'CI/CD',
    'GraphQL',
    'system design',
    'cross-functional',
    'mentorship',
    'Agile',
  ],
  suggestions: [
    {
      id: '1',
      title: 'Add missing technical keywords',
      description:
        'Include Kubernetes, CI/CD, and GraphQL in your skills or project bullets where you have relevant experience.',
      priority: 'high',
    },
    {
      id: '2',
      title: 'Quantify impact in experience',
      description:
        'Replace generic duties with metrics — e.g. “reduced deployment time by 40%” or “led a team of 5 engineers.”',
      priority: 'high',
    },
    {
      id: '3',
      title: 'Mirror job title language',
      description:
        'The posting uses “Senior Software Engineer” — align your headline and summary to match that phrasing.',
      priority: 'medium',
    },
    {
      id: '4',
      title: 'Highlight leadership & collaboration',
      description:
        'Add a bullet about cross-functional work or mentorship to address soft-skill keywords in the JD.',
      priority: 'medium',
    },
    {
      id: '5',
      title: 'Shorten summary paragraph',
      description:
        'ATS parsers favor concise summaries. Trim to 3–4 lines focused on role fit and core stack.',
      priority: 'low',
    },
  ],
  resumeStrength: {
    score: 72,
    label: 'Good — room to improve',
    dimensions: [
      { label: 'Formatting', value: 88 },
      { label: 'Keywords', value: 77 },
      { label: 'Experience', value: 70 },
      { label: 'Skills', value: 65 },
      { label: 'Summary', value: 60 },
    ],
  },
}
