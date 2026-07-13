import {
  BarChart3,
  FileSearch,
  FileUp,
  Lightbulb,
  Sparkles,
  Target,
} from 'lucide-react'
import type { Feature } from '@/types'

export const features: Feature[] = [
  {
    id: 'ats-score',
    title: 'ATS Score Analysis',
    description:
      'Get an instant compatibility score against applicant tracking systems used by top employers.',
    icon: BarChart3,
  },
  {
    id: 'keyword-matching',
    title: 'Keyword Matching',
    description:
      'Align your resume with job descriptions through intelligent keyword gap detection.',
    icon: Target,
  },
  {
    id: 'resume-improvements',
    title: 'Resume Improvements',
    description:
      'Receive actionable, section-by-section recommendations to strengthen your profile.',
    icon: Sparkles,
  },
  {
    id: 'ai-suggestions',
    title: 'AI Suggestions',
    description:
      'Leverage AI to rewrite bullet points, improve tone, and highlight measurable impact.',
    icon: Lightbulb,
  },
  {
    id: 'jd-parsing',
    title: 'JD Parsing',
    description:
      'Paste any job description and we extract skills, requirements, and priorities automatically.',
    icon: FileSearch,
  },
  {
    id: 'multi-format',
    title: 'Multi-format Upload',
    description:
      'Upload PDF, DOCX, or plain text — we parse and analyze every format seamlessly.',
    icon: FileUp,
  },
]
