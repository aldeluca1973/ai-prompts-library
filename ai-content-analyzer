#!/usr/bin/env python3
"""
AI Content Analyzer with Multi-Dimensional Scoring

What it does:
- Analyzes any text content (articles, emails, social posts, marketing copy)
- Provides multi-dimensional quality scoring
- Generates actionable improvement recommendations
- Compares against best-in-class examples
- Supports batch processing of multiple files

Why use this:
- Get objective quality metrics on your content
- Identify specific areas for improvement
- Ensure consistency across content library
- Perfect for content audits and optimization

Usage:
    python ai_content_analyzer.py --file article.txt --type blog-post
    python ai_content_analyzer.py --text "Your content here" --type email
    python ai_content_analyzer.py --batch content_folder/ --type social-post --export report.csv

Requirements:
    pip install openai pandas rich
    export OPENAI_API_KEY="sk-..."
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

try:
    from openai import OpenAI
    import pandas as pd
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Install with: pip install openai pandas rich")
    sys.exit(1)


@dataclass
class ContentScore:
    """Content analysis result"""
    overall_score: float
    clarity_score: float
    engagement_score: float
    persuasiveness_score: float
    readability_score: float
    seo_score: float
    tone_alignment: str
    word_count: int
    reading_time_minutes: float
    key_strengths: List[str]
    areas_for_improvement: List[str]
    recommendations: List[str]
    competitor_comparison: str


class ContentAnalyzer:
    """AI-powered content quality analyzer"""
    
    CONTENT_TYPES = {
        "blog-post": "Blog article or thought leadership piece",
        "email": "Marketing or sales email",
        "social-post": "Social media post (LinkedIn, Twitter, etc.)",
        "landing-page": "Landing page or sales page copy",
        "ad-copy": "Advertisement or promotional copy",
        "product-description": "E-commerce product description",
    }
    
    def __init__(self, api_key: Optional[str] = None):
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.console = Console()
    
    def analyze_content(
        self,
        text: str,
        content_type: str = "blog-post",
        target_audience: str = "general professional",
        industry: str = "technology",
    ) -> ContentScore:
        """Analyze content and return comprehensive scoring"""
        
        prompt = self._build_analysis_prompt(text, content_type, target_audience, industry)
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert content strategist and copywriter with 20 years of experience analyzing and optimizing content for maximum impact."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            
            # Calculate reading time (avg 200 words/min)
            word_count = len(text.split())
            reading_time = word_count / 200
            
            return ContentScore(
                overall_score=result.get("overall_score", 0),
                clarity_score=result.get("clarity_score", 0),
                engagement_score=result.get("engagement_score", 0),
                persuasiveness_score=result.get("persuasiveness_score", 0),
                readability_score=result.get("readability_score", 0),
                seo_score=result.get("seo_score", 0),
                tone_alignment=result.get("tone_alignment", "Unknown"),
                word_count=word_count,
                reading_time_minutes=round(reading_time, 1),
                key_strengths=result.get("key_strengths", []),
                areas_for_improvement=result.get("areas_for_improvement", []),
                recommendations=result.get("recommendations", []),
                competitor_comparison=result.get("competitor_comparison", "")
            )
            
        except Exception as e:
            self.console.print(f"[red]Error analyzing content: {e}[/red]")
            raise
    
    def _build_analysis_prompt(
        self,
        text: str,
        content_type: str,
        target_audience: str,
        industry: str
    ) -> str:
        """Build comprehensive analysis prompt"""
        
        return f"""Analyze the following {content_type} content and provide a comprehensive quality assessment.

CONTENT TYPE: {self.CONTENT_TYPES.get(content_type, content_type)}
TARGET AUDIENCE: {target_audience}
INDUSTRY: {industry}

CONTENT TO ANALYZE:
---
{text}
---

Provide your analysis as a JSON object with the following structure:

{{
  "overall_score": <float 0-100>,
  "clarity_score": <float 0-100>,
  "engagement_score": <float 0-100>,
  "persuasiveness_score": <float 0-100>,
  "readability_score": <float 0-100>,
  "seo_score": <float 0-100>,
  "tone_alignment": "<professional/casual/technical/conversational>",
  "key_strengths": [
    "Specific strength 1",
    "Specific strength 2",
    "Specific strength 3"
  ],
  "areas_for_improvement": [
    "Specific weakness 1 with context",
    "Specific weakness 2 with context",
    "Specific weakness 3 with context"
  ],
  "recommendations": [
    "Actionable recommendation 1",
    "Actionable recommendation 2",
    "Actionable recommendation 3",
    "Actionable recommendation 4",
    "Actionable recommendation 5"
  ],
  "competitor_comparison": "1-2 sentences comparing this to best-in-class content in this category"
}}

SCORING CRITERIA:

**Clarity Score (0-100):**
- Message is immediately understandable
- No jargon without explanation
- Logical flow and structure
- Clear value proposition

**Engagement Score (0-100):**
- Hooks attention in first 10 seconds
- Maintains interest throughout
- Emotional resonance
- Storytelling elements

**Persuasiveness Score (0-100):**
- Clear call-to-action
- Addresses objections
- Social proof/credibility
- Benefits vs features

**Readability Score (0-100):**
- Sentence length variation
- Paragraph structure
- Use of subheadings
- Scannable format

**SEO Score (0-100):**
- Keyword presence and density
- Meta-worthy content
- Internal linking opportunities
- Search intent alignment

**Overall Score:**
Weighted average emphasizing the most important dimensions for this content type.

Be specific and actionable in your feedback. Reference exact phrases from the content when possible."""

    def display_results(self, score: ContentScore, content_preview: str):
        """Display results with rich formatting"""
        
        # Header
        self.console.print(Panel.fit(
            "[bold cyan]Content Analysis Report[/bold cyan]",
            border_style="cyan"
        ))
        
        # Overall Score
        score_color = "green" if score.overall_score >= 80 else "yellow" if score.overall_score >= 60 else "red"
        self.console.print(f"\n[bold]Overall Score:[/bold] [{score_color}]{score.overall_score:.1f}/100[/{score_color}]")
        
        # Detailed Scores Table
        table = Table(title="Detailed Scores", show_header=True, header_style="bold magenta")
        table.add_column("Dimension", style="cyan", width=20)
        table.add_column("Score", justify="right", style="green")
        table.add_column("Rating", justify="center")
        
        scores = [
            ("Clarity", score.clarity_score),
            ("Engagement", score.engagement_score),
            ("Persuasiveness", score.persuasiveness_score),
            ("Readability", score.readability_score),
            ("SEO", score.seo_score),
        ]
        
        for dimension, value in scores:
            rating = "⭐⭐⭐⭐⭐" if value >= 90 else "⭐⭐⭐⭐" if value >= 75 else "⭐⭐⭐" if value >= 60 else "⭐⭐"
            table.add_row(dimension, f"{value:.1f}", rating)
        
        self.console.print("\n", table)
        
        # Content Stats
        self.console.print(f"\n[bold]Word Count:[/bold] {score.word_count}")
        self.console.print(f"[bold]Reading Time:[/bold] {score.reading_time_minutes} minutes")
        self.console.print(f"[bold]Tone:[/bold] {score.tone_alignment}")
        
        # Strengths
        self.console.print("\n[bold green]✓ Key Strengths:[/bold green]")
        for strength in score.key_strengths:
            self.console.print(f"  • {strength}")
        
        # Areas for Improvement
        self.console.print("\n[bold yellow]⚠ Areas for Improvement:[/bold yellow]")
        for area in score.areas_for_improvement:
            self.console.print(f"  • {area}")
        
        # Recommendations
        self.console.print("\n[bold cyan]💡 Recommendations:[/bold cyan]")
        for i, rec in enumerate(score.recommendations, 1):
            self.console.print(f"  {i}. {rec}")
        
        # Competitor Comparison
        if score.competitor_comparison:
            self.console.print(f"\n[bold]Competitive Analysis:[/bold]\n{score.competitor_comparison}")
    
    def batch_analyze(
        self,
        input_path: Path,
        content_type: str,
        output_csv: Optional[Path] = None
    ) -> List[Dict]:
        """Analyze all text files in a directory"""
        
        results = []
        files = list(input_path.glob("*.txt")) + list(input_path.glob("*.md"))
        
        self.console.print(f"\n[cyan]Processing {len(files)} files...[/cyan]\n")
        
        for file_path in files:
            self.console.print(f"Analyzing: {file_path.name}")
            
            try:
                text = file_path.read_text(encoding="utf-8")
                score = self.analyze_content(text, content_type)
                
                result = asdict(score)
                result["filename"] = file_path.name
                results.append(result)
                
                self.console.print(f"  Score: {score.overall_score:.1f}/100 ✓\n")
                
            except Exception as e:
                self.console.print(f"  [red]Error: {e}[/red]\n")
        
        # Export to CSV if requested
        if output_csv:
            df = pd.DataFrame(results)
            # Flatten lists for CSV
            df['key_strengths'] = df['key_strengths'].apply(lambda x: '; '.join(x) if isinstance(x, list) else x)
            df['areas_for_improvement'] = df['areas_for_improvement'].apply(lambda x: '; '.join(x) if isinstance(x, list) else x)
            df['recommendations'] = df['recommendations'].apply(lambda x: '; '.join(x) if isinstance(x, list) else x)
            df.to_csv(output_csv, index=False)
            self.console.print(f"\n[green]Exported results to: {output_csv}[/green]")
        
        return results


def main():
    parser = argparse.ArgumentParser(
        description="AI-powered content quality analyzer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python ai_content_analyzer.py --file article.txt --type blog-post
  python ai_content_analyzer.py --text "Your content" --type email --audience "B2B decision makers"
  python ai_content_analyzer.py --batch ./content --type social-post --export results.csv
        """
    )
    
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--file", type=Path, help="Single file to analyze")
    input_group.add_argument("--text", type=str, help="Direct text to analyze")
    input_group.add_argument("--batch", type=Path, help="Directory of files to analyze")
    
    parser.add_argument(
        "--type",
        choices=list(ContentAnalyzer.CONTENT_TYPES.keys()),
        default="blog-post",
        help="Content type for context-aware analysis"
    )
    parser.add_argument("--audience", default="general professional", help="Target audience")
    parser.add_argument("--industry", default="technology", help="Industry context")
    parser.add_argument("--export", type=Path, help="Export batch results to CSV")
    
    args = parser.parse_args()
    
    analyzer = ContentAnalyzer()
    
    try:
        if args.batch:
            # Batch processing
            if not args.batch.is_dir():
                print(f"Error: {args.batch} is not a directory")
                sys.exit(1)
            
            analyzer.batch_analyze(args.batch, args.type, args.export)
            
        else:
            # Single analysis
            if args.file:
                text = args.file.read_text(encoding="utf-8")
                content_preview = args.file.name
            else:
                text = args.text
                content_preview = text[:100] + "..."
            
            score = analyzer.analyze_content(
                text,
                content_type=args.type,
                target_audience=args.audience,
                industry=args.industry
            )
            
            analyzer.display_results(score, content_preview)
    
    except KeyboardInterrupt:
        print("\n\nAnalysis cancelled.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
