import { FeatureCard } from '@/components/common/FeatureCard'
import { SectionHeader } from '@/components/common/SectionHeader'
import { features } from '@/data/features'

export function FeaturesSection() {
  return (
    <section
      id="features"
      className="border-t border-border/60 bg-surface/30 py-24 sm:py-32"
      aria-labelledby="features-heading"
    >
      <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
        <SectionHeader
          badge="Features"
          title="Everything you need to land the interview"
          description="From ATS compatibility to AI rewrites — HireMatch AI gives you a complete toolkit to tailor every application."
        />

        <div className="mt-16 grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {features.map((feature, index) => (
            <FeatureCard key={feature.id} feature={feature} index={index} />
          ))}
        </div>
      </div>
    </section>
  )
}
