import { TestimonialCard } from '@/components/common/TestimonialCard'
import { SectionHeader } from '@/components/common/SectionHeader'
import { testimonials } from '@/data/testimonials'

export function TestimonialsSection() {
  return (
    <section
      id="testimonials"
      className="py-24 sm:py-32"
      aria-labelledby="testimonials-heading"
    >
      <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
        <SectionHeader
          badge="Testimonials"
          title="Trusted by ambitious professionals"
          description="Join thousands of candidates who've improved their resumes and accelerated their job search with HireMatch AI."
        />

        <div className="mt-16 grid gap-5 sm:grid-cols-2">
          {testimonials.map((testimonial, index) => (
            <TestimonialCard
              key={testimonial.id}
              testimonial={testimonial}
              index={index}
            />
          ))}
        </div>
      </div>
    </section>
  )
}
