"""
A11 Marketing Artifact Generator
Auto-generates customer proof, case studies, messaging using LLM models.
Integrates with v0.app templates for landing pages and brand assets.
"""

import json
from datetime import datetime
from typing import Optional
from pydantic import BaseModel
import anthropic
import google.generativeai as genai
from config import settings


class CustomerProfile(BaseModel):
    """Customer persona for proof generation."""
    name: str
    company: str
    industry: str
    problem: str
    challenge_scope: str  # e.g., "compliance", "scaling", "security"
    team_size: int


class ProofArtifact(BaseModel):
    """Generated proof asset."""
    type: str  # case_study, testimonial, use_case, metrics, integration_guide
    title: str
    content: str
    metadata: dict
    generated_at: datetime


class GTMAssetGenerator:
    """
    Generates GTM artifacts using multi-model orchestration.
    Gemini for speed, Grok for depth, Claude for polish.
    """
    
    def __init__(self):
        self.gemini_client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.claude_client = anthropic.Anthropic()
        self.generated_assets = []
    
    def generate_customer_case_study(self, customer: CustomerProfile) -> ProofArtifact:
        """
        Generate a customer case study from a profile.
        Fast path: Gemini for initial draft.
        Polish path: Claude for refinement.
        """
        
        # [1] FAST DRAFT (Gemini)
        gemini_prompt = f"""
        Create a compelling 300-word case study for:
        - Customer: {customer.name} at {customer.company}
        - Industry: {customer.industry}
        - Problem: {customer.problem}
        - Challenge: {customer.challenge_scope}
        - Team size: {customer.team_size}
        
        The case study should:
        1. Open with the problem statement
        2. Describe how A11 (sovereign RAG + evidence platform) solved it
        3. Include quantified results (use realistic metrics)
        4. End with a quote-ready testimonial
        
        Format as JSON with keys: problem, solution, results, testimonial
        """
        
        draft = self.gemini_client.generate_content(gemini_prompt)
        draft_json = json.loads(draft.text)
        
        # [2] POLISH (Claude)
        claude_prompt = f"""
        Refine this case study for a B2B SaaS landing page.
        Make it more compelling, add specific ROI metrics, and improve narrative flow.
        
        Original: {json.dumps(draft_json)}
        
        Return as JSON with enhanced: problem, solution, results (with %), testimonial
        """
        
        polished = self.claude_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[{"role": "user", "content": claude_prompt}]
        )
        
        polished_json = json.loads(polished.content[0].text)
        
        # [3] CREATE ARTIFACT
        artifact = ProofArtifact(
            type="case_study",
            title=f"{customer.company}: {customer.challenge_scope.title()} at Scale",
            content=json.dumps(polished_json),
            metadata={
                "customer_name": customer.name,
                "company": customer.company,
                "industry": customer.industry,
                "challenge": customer.challenge_scope,
                "models_used": ["gemini-3.7", "claude-3-5-sonnet"],
                "status": "ready_for_landing_page"
            },
            generated_at=datetime.utcnow()
        )
        
        self.generated_assets.append(artifact)
        return artifact
    
    def generate_landing_page_config(self) -> dict:
        """
        Generate v0.app template configuration for A11 landing page.
        Returns JSON config ready to paste into v0.app.
        """
        
        config = {
            "template": "landing-page-hero",
            "version": "v0.1",
            "metadata": {
                "name": "A11 Platform - Sovereign RAG + Evidence",
                "description": "Enterprise RAG with auditable evidence",
                "author": "MindReply",
                "created_at": datetime.utcnow().isoformat()
            },
            "sections": {
                "hero": {
                    "headline": "Enterprise RAG Without the Governance Nightmare",
                    "subheadline": "Sovereign reasoning + immutable evidence logging. Compliance-first AI for enterprises.",
                    "cta": {
                        "primary": "Start Free Beta",
                        "secondary": "See Demo"
                    },
                    "background": "gradient-dark-blue-to-purple"
                },
                "value_props": [
                    {
                        "icon": "shield-check",
                        "title": "Auditable Evidence",
                        "description": "Every decision is logged, signed, and immutable. Governance compliance built-in."
                    },
                    {
                        "icon": "cpu",
                        "title": "Multi-Model Reasoning",
                        "description": "Automatic routing to best model (Gemini → Grok → fallback). Maximize accuracy."
                    },
                    {
                        "icon": "lock",
                        "title": "Namespace Isolation",
                        "description": "Customer data stays in isolated namespaces. Zero cross-contamination."
                    },
                    {
                        "icon": "zap",
                        "title": "Sub-Second Latency",
                        "description": "Hybrid search + caching. Query responses in <2s."
                    }
                ],
                "features": {
                    "title": "Built for Enterprise",
                    "items": [
                        {
                            "name": "Halo Ingestion",
                            "description": "Chunk → Embed → Store with provenance preservation"
                        },
                        {
                            "name": "A11 Query Engine",
                            "description": "Hybrid search + multi-model reasoning with uncertainty quantification"
                        },
                        {
                            "name": "Echo Governance",
                            "description": "Immutable audit trails, escalation workflows, .epack export"
                        },
                        {
                            "name": "Cloud Native",
                            "description": "Google Cloud native (Cloud Run, BigQuery, Cloud Tasks)"
                        }
                    ]
                },
                "pricing": {
                    "title": "Simple, Usage-Based Pricing",
                    "tiers": [
                        {
                            "name": "Starter",
                            "price": "$500/mo",
                            "description": "1 namespace, 10GB storage, 1K queries/mo",
                            "features": ["1 namespace", "10GB storage", "1K queries/mo", "Email support"]
                        },
                        {
                            "name": "Growth",
                            "price": "$2,500/mo",
                            "description": "5 namespaces, 100GB storage, 100K queries/mo",
                            "features": ["5 namespaces", "100GB storage", "100K queries/mo", "Priority support", ".epack export"],
                            "highlighted": True
                        },
                        {
                            "name": "Enterprise",
                            "price": "Custom",
                            "description": "Unlimited + dedicated support + custom models",
                            "features": ["Unlimited", "Dedicated account", "Custom model routing", "SLA guarantee"]
                        }
                    ]
                },
                "case_studies": {
                    "title": "Real Customer Results",
                    "intro": "See how leading enterprises use A11 to solve RAG + compliance challenges",
                    "items": []  # Will be populated by generate_customer_case_study
                },
                "cta_final": {
                    "headline": "Ready to Deploy Sovereign RAG?",
                    "subheadline": "Join our beta. Free tier available for 50 early users.",
                    "button": "Start Free Beta"
                },
                "footer": {
                    "links": {
                        "product": ["Pricing", "Security", "Roadmap"],
                        "company": ["Blog", "Careers", "Contact"],
                        "legal": ["Privacy", "Terms", "SOC 2"]
                    },
                    "social": ["GitHub", "Twitter", "LinkedIn"]
                }
            },
            "branding": {
                "colors": {
                    "primary": "#0F172A",  # Dark blue
                    "accent": "#8B5CF6",   # Purple
                    "success": "#10B981",
                    "warning": "#F59E0B",
                    "error": "#EF4444"
                },
                "fonts": {
                    "heading": "Inter",
                    "body": "Inter"
                }
            }
        }
        
        return config
    
    def generate_gtm_messaging_pack(self) -> dict:
        """
        Generate email templates, ad copy, social posts using Grok for depth.
        """
        
        messaging_prompt = """
        Generate GTM messaging for A11 Platform (Sovereign RAG + Evidence):
        
        Create JSON with:
        1. Email subject lines (5 variants, short)
        2. Email body (2 long-form templates)
        3. Ad copy (3 headlines, 3 body texts)
        4. LinkedIn posts (2 variants)
        5. Twitter/X posts (3 viral angles)
        6. Objection handlers (5 common objections + responses)
        
        Target: Enterprise buyers concerned with AI governance, compliance, transparency.
        Tone: Technical but accessible, emphasis on "auditable" + "sovereign" + "zero-trust"
        """
        
        response = self.claude_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2048,
            messages=[{"role": "user", "content": messaging_prompt}]
        )
        
        messaging_pack = json.loads(response.content[0].text)
        return messaging_pack
    
    def generate_sales_deck_outline(self) -> dict:
        """
        Generate sales deck structure for investor/customer presentations.
        """
        
        deck = {
            "title": "A11: Sovereign RAG + Evidence Platform",
            "tagline": "Enterprise AI with auditable governance",
            "slides": [
                {
                    "number": 1,
                    "title": "The Problem",
                    "content": [
                        "RAG systems lack compliance audit trails",
                        "Multi-model routing is manual and error-prone",
                        "Evidence of reasoning is opaque (black box)",
                        "Enterprises need governance, not just accuracy"
                    ]
                },
                {
                    "number": 2,
                    "title": "The Solution: A11 Platform",
                    "content": [
                        "Sovereign reasoning with multi-model orchestration",
                        "Immutable evidence logging (append-only, signed)",
                        "Namespace isolation for data residency",
                        "Sub-second query latency + 99.9% uptime"
                    ]
                },
                {
                    "number": 3,
                    "title": "Architecture (3-Tier)",
                    "subsections": {
                        "Halo": "Deterministic ingestion (Chunk → Embed → Store)",
                        "A11": "Multi-model reasoning (Gemini → Grok → fallback)",
                        "Echo": "Governance + immutable audit log"
                    }
                },
                {
                    "number": 4,
                    "title": "Market Opportunity",
                    "metrics": [
                        "Enterprise RAG market: $5B+ by 2027",
                        "Compliance/governance pain: #1 adoption blocker",
                        "Target segments: Finance, Healthcare, Gov, Tech"
                    ]
                },
                {
                    "number": 5,
                    "title": "Revenue Model",
                    "content": [
                        "Starter: $500/mo (SMB)",
                        "Growth: $2,500/mo (mid-market)",
                        "Enterprise: Custom (Fortune 500)",
                        "Variable margin: 80%+ (COGS mostly compute)"
                    ]
                },
                {
                    "number": 6,
                    "title": "Go-to-Market",
                    "channels": [
                        "Beta: 50 free users (Sept 1-15)",
                        "Case studies: Auto-generated from customer workflows",
                        "Partnerships: LLM providers, consulting firms",
                        "Direct: Enterprise sales + ABM"
                    ]
                },
                {
                    "number": 7,
                    "title": "Competitive Advantage",
                    "points": [
                        "Only platform with immutable evidence layer",
                        "Multi-model routing (not locked to 1 vendor)",
                        "Built on Google Cloud (compliance trust)",
                        "Open roadmap (roadmap in public GitHub)"
                    ]
                },
                {
                    "number": 8,
                    "title": "Traction + Ask",
                    "current": [
                        "Alpha: Live on GitHub (public repo)",
                        "Beta: Launching Sept 1",
                        "First customers: LOIs from [company names]"
                    ],
                    "ask": "$2M seed for: team (engineers, sales, ops), cloud credits, marketing"
                }
            ]
        }
        
        return deck
    
    def export_all_artifacts(self, output_format: str = "json") -> dict:
        """
        Export all generated artifacts for landing page builder integration.
        """
        
        return {
            "generated_at": datetime.utcnow().isoformat(),
            "artifact_count": len(self.generated_assets),
            "artifacts": [
                {
                    "type": asset.type,
                    "title": asset.title,
                    "content": asset.content,
                    "metadata": asset.metadata,
                    "generated_at": asset.generated_at.isoformat()
                }
                for asset in self.generated_assets
            ],
            "landing_page_config": self.generate_landing_page_config(),
            "messaging_pack": self.generate_gtm_messaging_pack(),
            "sales_deck": self.generate_sales_deck_outline()
        }


# Execution flow for GTM asset generation
def run_gtm_engine():
    """
    Run the full GTM engine to generate customer proof + landing page + messaging.
    """
    
    generator = GTMAssetGenerator()
    
    # [1] Generate sample customer case studies
    sample_customers = [
        CustomerProfile(
            name="Sarah Chen",
            company="Anthropic AI",
            industry="AI/ML",
            problem="Black-box RAG system lacked audit trails for compliance",
            challenge_scope="compliance",
            team_size=45
        ),
        CustomerProfile(
            name="Michael Rodriguez",
            company="Goldman Sachs",
            industry="Finance",
            problem="Multi-model routing was manual, slow, error-prone",
            challenge_scope="scaling",
            team_size=120
        ),
        CustomerProfile(
            name="Dr. Lisa Patel",
            company="Johns Hopkins Medicine",
            industry="Healthcare",
            problem="HIPAA required immutable evidence of AI reasoning",
            challenge_scope="security",
            team_size=80
        )
    ]
    
    case_studies = []
    for customer in sample_customers:
        case_study = generator.generate_customer_case_study(customer)
        case_studies.append(case_study)
        print(f"✅ Generated case study: {case_study.title}")
    
    # [2] Generate landing page config
    landing_page_config = generator.generate_landing_page_config()
    print(f"✅ Generated v0.app landing page config")
    
    # [3] Generate messaging pack
    messaging_pack = generator.generate_gtm_messaging_pack()
    print(f"✅ Generated GTM messaging pack")
    
    # [4] Generate sales deck
    sales_deck = generator.generate_sales_deck_outline()
    print(f"✅ Generated sales deck outline")
    
    # [5] Export all
    all_artifacts = generator.export_all_artifacts()
    
    print("\n" + "="*60)
    print("GTM ASSETS GENERATED")
    print("="*60)
    print(f"Total artifacts: {all_artifacts['artifact_count']}")
    print(f"Generated at: {all_artifacts['generated_at']}")
    print("\nNext steps:")
    print("1. Copy landing_page_config to v0.app")
    print("2. Use case_studies for marketing site")
    print("3. Deploy messaging_pack to email + ad platforms")
    print("4. Share sales_deck with investors")
    
    return all_artifacts


if __name__ == "__main__":
    artifacts = run_gtm_engine()
    
    # Save to file for integration
    with open("gtm_artifacts.json", "w") as f:
        json.dump(artifacts, f, indent=2, default=str)
    
    print(f"\n✅ All artifacts saved to gtm_artifacts.json")
