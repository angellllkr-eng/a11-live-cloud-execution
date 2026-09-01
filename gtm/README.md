# A11 GTM Artifacts & Landing Page Builder

This directory contains auto-generated marketing assets for the A11 platform launch.

## Structure

```
gtm/
├── artifact_generator.py    # LLM-powered asset generation
├── v0_templates/            # v0.app landing page templates
├── case_studies/            # Customer proof (auto-generated)
├── messaging_pack/          # Email, ad copy, social posts
├── sales_deck/              # Investor/customer presentation
└── README.md                # This file
```

## Quick Start: Generate GTM Assets

```bash
# 1. Install dependencies
pip install -r ../requirements.txt

# 2. Set API keys
export GEMINI_API_KEY="your-key"
export ANTHROPIC_API_KEY="your-key"

# 3. Run generator
python artifact_generator.py

# 4. Output: gtm_artifacts.json
# Contains all landing page config, case studies, messaging, deck outline
```

## v0.app Integration

The `artifact_generator.py` outputs a v0.app-ready landing page config.

**To deploy:**

1. Go to https://v0.app/templates/landing-pages
2. Select a template (Hero + Features + Pricing recommended)
3. Paste `landing_page_config` JSON into the template builder
4. Customize colors/fonts if needed
5. Export as React components or static HTML
6. Deploy to Vercel / your hosting

**Landing page structure:**
- Hero: Headline + CTA
- Value Props: 4 key differentiators
- Features: Halo, A11, Echo, Cloud Native
- Pricing: 3 tiers (Starter, Growth, Enterprise)
- Case Studies: 3 customer proof points (auto-generated)
- Final CTA: Beta signup

## Generated Assets

### Case Studies
Auto-generated from customer profiles using:
- **Gemini 3.7** (fast draft)
- **Claude 3.5 Sonnet** (polish + refinement)

Each case study includes:
- Problem statement
- Solution narrative
- Quantified results
- Customer testimonial (quote-ready)

### Messaging Pack
Generated using Claude (depth) for:
- Email subject lines (5 variants)
- Email body templates (2 long-form)
- Ad headlines + body copy
- LinkedIn posts (professional angle)
- Twitter/X posts (viral angles)
- Objection handlers (FAQ/rebuttals)

### Sales Deck Outline
8-slide structure for investor/customer pitches:
1. The Problem
2. The Solution (A11)
3. Architecture (Halo/A11/Echo)
4. Market Opportunity
5. Revenue Model
6. GTM Strategy
7. Competitive Advantages
8. Traction + Ask

## Brand Guidelines

**Colors:**
- Primary: `#0F172A` (Dark Blue)
- Accent: `#8B5CF6` (Purple)
- Success: `#10B981` (Green)
- Error: `#EF4444` (Red)

**Fonts:**
- Heading: Inter
- Body: Inter

**Tone:**
- Technical but accessible
- Emphasis: auditable, sovereign, zero-trust, enterprise-grade

## Deployment

Once assets are generated:

1. **Landing Page**: Deploy v0 template to Vercel
2. **Email**: Send messaging pack to email marketing platform
3. **Social**: Schedule Twitter/LinkedIn posts
4. **Sales**: Share deck with investors + warm leads
5. **Case Studies**: Feature on landing page + blog

## Automation

The generator runs on:
- Every new customer onboarding (auto-generate case study)
- Weekly (refresh messaging pack + social posts)
- Monthly (update metrics in case studies)

Integration hooks:
- Slack notification on new artifacts
- Auto-commit to GitHub (gtm/generated/)
- Upload to S3 for distribution

## Notes

- All artifacts are **generated fresh** on each run
- Timestamps included for tracking
- Ready for immediate use (copy-paste to platforms)
- Customizable prompts in `artifact_generator.py`

---

**Next:** Deploy landing page, run beta launch, measure CAC/LTV
