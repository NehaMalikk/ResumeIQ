import { motion } from 'framer-motion'
import { AlertTriangle, CheckCircle2, Lightbulb, Sparkles, Target } from 'lucide-react'
import { Badge } from '@/components/ui/badge'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import type { AnalyzeResponse, RecommendationResponse } from '@/types'
import { cn } from '@/utils/cn'

const priorityStyles: Record<string, string> = {
  high: 'border-red-200/80 bg-red-50/60 text-red-700',
  medium: 'border-amber-200/80 bg-amber-50/60 text-amber-800',
  low: 'border-border bg-surface text-muted',
}
const clampPercentage = (value: number) => Number.isFinite(value) ? Math.min(100, Math.max(0, value)) : 0
const readable = (value: string) => value.replaceAll('_', ' ').replace(/\b\w/g, (letter) => letter.toUpperCase())

function ScoreRing({ score }: { score: number }) {
  const displayScore = clampPercentage(score)
  const circumference = 2 * Math.PI * 54
  return <div className="relative mx-auto size-36 sm:size-40" role="progressbar" aria-label="ATS match score" aria-valuenow={displayScore} aria-valuemin={0} aria-valuemax={100}>
    <svg className="size-full -rotate-90" viewBox="0 0 120 120" aria-hidden><circle cx="60" cy="60" r="54" fill="none" stroke="currentColor" strokeWidth="8" className="text-surface" /><circle cx="60" cy="60" r="54" fill="none" stroke="url(#scoreGradient)" strokeWidth="8" strokeLinecap="round" strokeDasharray={circumference} strokeDashoffset={circumference - (displayScore / 100) * circumference} /><defs><linearGradient id="scoreGradient"><stop offset="0%" stopColor="#5b5fc7" /><stop offset="100%" stopColor="#7c3aed" /></linearGradient></defs></svg>
    <div className="absolute inset-0 flex flex-col items-center justify-center"><span className="text-3xl font-semibold">{displayScore.toFixed(1)}</span><span className="text-xs text-muted">out of 100</span></div>
  </div>
}

function RecommendationCard({ item }: { item: RecommendationResponse }) {
  return <Card className="border-border/80 bg-card"><CardHeader className="pb-2"><div className="flex items-start justify-between gap-2"><CardTitle className="text-sm leading-snug">{item.title}</CardTitle><span className={cn('rounded-md border px-2 py-0.5 text-[10px] font-semibold uppercase', priorityStyles[item.priority.toLowerCase()] ?? priorityStyles.low)}>{item.priority}</span></div><CardDescription>{readable(item.category)} · {item.impact}</CardDescription></CardHeader><CardContent className="space-y-3"><p className="text-sm leading-relaxed text-muted">{item.message}</p>{item.evidence.length > 0 && <p className="text-xs text-muted"><span className="font-medium text-foreground">Evidence:</span> {item.evidence.join('; ')}</p>}{item.suggested_actions.length > 0 && <ul className="list-disc space-y-1 pl-4 text-xs text-muted">{item.suggested_actions.map((action) => <li key={`${item.id}-${action}`}>{action}</li>)}</ul>}</CardContent></Card>
}

export function AnalysisResultsSection({ result }: { result: AnalyzeResponse }) {
  const warnings = [...new Set([...result.warnings, ...(result.ats_score?.warnings ?? []), ...(result.recommendations?.warnings ?? [])])]
  const recommendations = result.recommendations?.recommendations ?? []
  const strengths = result.recommendations?.strengths ?? []
  const missingSkills = result.recommendations?.missing_skills ?? []
  return <section id="results" className="border-t border-border/60 bg-surface/20 pb-20 pt-4 sm:pb-28" aria-labelledby="results-heading">
    <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8"><motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6">
      <div className="text-center"><div className="inline-flex items-center gap-2 rounded-full border border-primary/20 bg-accent-soft/50 px-3 py-1 text-xs font-medium text-primary"><Sparkles className="size-3.5" aria-hidden />Analysis complete</div><h2 id="results-heading" className="mt-4 text-2xl font-semibold sm:text-3xl">Your ATS results</h2><p className="mx-auto mt-2 max-w-lg text-sm text-muted">{result.recommendations?.summary ?? 'Your resume was analyzed against the supplied job description.'}</p></div>

      <div className="grid gap-6 lg:grid-cols-3">
        <Card className="glass border-white/60 shadow-md"><CardHeader className="text-center"><CardTitle className="flex items-center justify-center gap-2 text-base"><Target className="size-4 text-primary" aria-hidden />ATS Match Score</CardTitle>{result.ats_score && <CardDescription>Confidence {clampPercentage(result.ats_score.confidence * 100).toFixed(0)}%</CardDescription>}</CardHeader><CardContent>{result.ats_score ? <ScoreRing score={result.ats_score.overall_score} /> : <p className="text-center text-sm text-muted">ATS scoring was not available for this run.</p>}</CardContent></Card>
        <Card className="glass border-white/60 shadow-md lg:col-span-2"><CardHeader><CardTitle className="flex items-center gap-2 text-base"><CheckCircle2 className="size-4 text-primary" aria-hidden />Comparison breakdown</CardTitle><CardDescription>{result.comparison ? `Overall comparison score: ${clampPercentage(result.comparison.overall_score).toFixed(1)}%` : 'Comparison was not available.'}</CardDescription></CardHeader><CardContent className="space-y-4">{result.comparison?.metrics.map((metric) => { const score = clampPercentage(metric.score); return <div key={metric.name}><div className="mb-1 flex justify-between text-sm"><span className="font-medium">{readable(metric.name)}</span><span className="text-muted">{score.toFixed(1)}%</span></div><div className="h-2 overflow-hidden rounded-full bg-surface" role="progressbar" aria-label={`${readable(metric.name)} score`} aria-valuenow={score} aria-valuemin={0} aria-valuemax={100}><div className="h-full rounded-full bg-primary/75" style={{ width: `${score}%` }} /></div>{metric.details && <p className="mt-1 text-xs text-muted">{metric.details}</p>}</div> })}{result.comparison && result.comparison.metrics.length === 0 && <p className="text-sm text-muted">No comparison metrics were returned.</p>}</CardContent></Card>
      </div>

      {result.ats_score && <Card><CardHeader><CardTitle className="text-base">Score breakdown</CardTitle><CardDescription>{result.ats_score.score_breakdown.explanation.split('\n')[0]}</CardDescription></CardHeader><CardContent className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">{Object.entries(result.ats_score.score_breakdown.contributions).map(([name, contribution]) => <div key={name} className="rounded-lg border border-border p-3"><p className="text-xs text-muted">{readable(name)}</p><p className="text-lg font-semibold">{contribution.toFixed(2)} <span className="text-xs font-normal text-muted">/ {(result.ats_score?.score_breakdown.maximums[name] ?? 0).toFixed(2)}</span></p></div>)}</CardContent></Card>}

      <Card><CardHeader><CardTitle className="text-base">Skill and keyword gaps</CardTitle><CardDescription>Items identified by the backend comparison and recommendation stages.</CardDescription></CardHeader><CardContent className="space-y-4">{missingSkills.length > 0 ? <div><p className="mb-2 text-sm font-medium">Missing skills</p><div className="flex flex-wrap gap-2">{missingSkills.map((skill) => <Badge key={skill} variant="secondary">{skill}</Badge>)}</div></div> : <p className="text-sm text-muted">No required skill gaps were identified.</p>}{result.recommendations && result.recommendations.keyword_suggestions.length > 0 && <div><p className="mb-2 text-sm font-medium">Keyword suggestions</p><div className="flex flex-wrap gap-2">{result.recommendations.keyword_suggestions.map((keyword) => <Badge key={keyword} variant="outline">{keyword}</Badge>)}</div></div>}{result.comparison?.metrics.filter((metric) => metric.matched_items.length > 0).map((metric) => <div key={`matched-${metric.name}`}><p className="mb-2 text-sm font-medium">Matched {readable(metric.name)}</p><div className="flex flex-wrap gap-2">{metric.matched_items.map((item) => <Badge key={`${metric.name}-${item}`}>{item}</Badge>)}</div></div>)}</CardContent></Card>

      <div><div className="mb-4 flex items-center gap-2"><Lightbulb className="size-5 text-primary" aria-hidden /><h3 className="text-lg font-semibold">Recommendations</h3></div>{recommendations.length > 0 ? <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">{recommendations.map((item) => <RecommendationCard key={item.id} item={item} />)}</div> : <Card><CardContent className="pt-6 text-sm text-muted">No recommendations were returned for this analysis.</CardContent></Card>}</div>
      {strengths.length > 0 && <div><h3 className="mb-4 text-lg font-semibold">Strengths</h3><div className="grid gap-4 sm:grid-cols-2">{strengths.map((item) => <RecommendationCard key={item.id} item={item} />)}</div></div>}
      {warnings.length > 0 && <Card className="border-amber-200 bg-amber-50/50"><CardHeader><CardTitle className="flex items-center gap-2 text-base"><AlertTriangle className="size-4 text-amber-700" aria-hidden />Analysis warnings</CardTitle></CardHeader><CardContent><ul className="list-disc space-y-1 pl-5 text-sm text-amber-900">{warnings.map((warning) => <li key={warning}>{warning}</li>)}</ul></CardContent></Card>}
      <Card><CardHeader><CardTitle className="text-base">Processing details</CardTitle></CardHeader><CardContent className="grid gap-3 text-sm sm:grid-cols-3"><div><span className="text-muted">Processing time</span><p className="font-medium">{Math.max(0, result.processing_time_ms).toFixed(1)} ms</p></div><div><span className="text-muted">Pipeline version</span><p className="font-medium">{result.pipeline_version}</p></div>{result.metadata.parser_used && <div><span className="text-muted">Resume parser</span><p className="font-medium">{result.metadata.parser_used}</p></div>}</CardContent></Card>
    </motion.div></div>
  </section>
}
