export type JsonPrimitive = string | number | boolean | null
export type JsonValue = JsonPrimitive | JsonValue[] | { [key: string]: JsonValue }

export interface FeatureValue<T extends JsonValue> {
  value: T
  source: string
  confidence: number
  metadata: { [key: string]: JsonValue } | null
}

export interface ResumeFeaturesResponse {
  skills: FeatureValue<string[]>
  skill_count: FeatureValue<number>
  programming_languages: FeatureValue<string[]>
  frameworks: FeatureValue<string[]>
  databases: FeatureValue<string[]>
  cloud_tools: FeatureValue<string[]>
  devops_tools: FeatureValue<string[]>
  experience_years: FeatureValue<number | null>
  education_level: FeatureValue<string>
  project_count: FeatureValue<number>
  certification_count: FeatureValue<number>
  responsibility_count: FeatureValue<number>
  keyword_count: FeatureValue<number>
  section_completeness: FeatureValue<number>
  technical_strength: FeatureValue<number>
  resume_length_words: FeatureValue<number>
  estimated_pages: FeatureValue<number>
}

export interface JobFeaturesResponse {
  required_skills: FeatureValue<string[]>
  preferred_skills: FeatureValue<string[]>
  nice_to_have_skills: FeatureValue<string[]>
  required_skill_count: FeatureValue<number>
  preferred_skill_count: FeatureValue<number>
  minimum_experience: FeatureValue<number | null>
  education_level: FeatureValue<string>
  responsibility_count: FeatureValue<number>
  keyword_count: FeatureValue<number>
}

export interface ScoreBreakdownResponse {
  contributions: Record<string, number>
  maximums: Record<string, number>
  explanation: string
}

export interface ATSScoreResponse {
  overall_score: number
  skills_score: number
  experience_score: number
  education_score: number
  projects_score: number
  certifications_score: number
  keywords_score: number
  responsibilities_score: number
  semantic_score: number
  confidence: number
  score_breakdown: ScoreBreakdownResponse
  warnings: string[]
}

export interface ComparisonMetricResponse {
  name: string
  score: number
  matched_items: string[]
  missing_items: string[]
  extra_items: string[]
  details: string
  confidence: number
  metadata: { [key: string]: JsonValue }
}

export interface ComparisonResponse {
  overall_score: number
  metrics: ComparisonMetricResponse[]
  weights: Record<string, number>
}

export interface RecommendationResponse {
  id: string
  category: string
  priority: string
  title: string
  message: string
  impact: string
  evidence: string[]
  suggested_actions: string[]
}

export interface RecommendationReportResponse {
  summary: string
  overall_score: number
  confidence: number
  recommendations: RecommendationResponse[]
  strengths: RecommendationResponse[]
  missing_skills: string[]
  keyword_suggestions: string[]
  section_feedback: Record<string, string[]>
  warnings: string[]
}

export interface AnalysisMetadataResponse {
  parser_used?: string
  comparison_plugins_used?: string[]
  [key: string]: JsonValue | undefined
}

export interface AnalyzeResponse {
  metadata: AnalysisMetadataResponse
  ats_score: ATSScoreResponse | null
  comparison: ComparisonResponse | null
  recommendations: RecommendationReportResponse | null
  resume_features: ResumeFeaturesResponse
  job_features: JobFeaturesResponse
  warnings: string[]
  processing_time_ms: number
  pipeline_version: string
}
