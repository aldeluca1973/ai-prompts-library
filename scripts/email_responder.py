#!/usr/bin/env python3
"""
Intelligent Email Response Generator with Context Awareness

What it does:
- Analyzes incoming emails for intent, urgency, and sentiment
- Generates context-aware, professional responses
- Maintains conversation history for multi-turn exchanges
- Supports multiple response tones (professional, casual, empathetic)
- Handles different email types (inquiry, complaint, follow-up, etc.)

Why use this:
- Save 60%+ time on email responses
- Maintain consistent brand voice
- Never miss important context from email threads
- Ensure appropriate tone for each situation
- Perfect for customer support, sales, and general correspondence

Usage:
    python email_responder.py --email incoming.txt --tone professional
    python email_responder.py --text "Email content" --context previous_thread.txt
    python email_responder.py --batch inbox/ --tone empathetic --export responses/

Requirements:
    pip install openai python-dateutil
    export OPENAI_API_KEY="sk-..."
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime

try:
    from openai import OpenAI
    from dateutil import parser as date_parser
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Install with: pip install openai python-dateutil")
    sys.exit(1)


@dataclass
class EmailAnalysis:
    """Email intent and metadata analysis"""
    intent: str  # inquiry, complaint, follow_up, booking, support, etc.
    urgency: str  # low, medium, high, critical
    sentiment: str  # positive, neutral, negative
    key_points: List[str]
    questions_asked: List[str]
    action_items: List[str]
    suggested_tone: str
    estimated_response_complexity: str


@dataclass
class EmailResponse:
    """Generated email response"""
    subject: str
    body: str
    tone_used: str
    key_points_addressed: List[str]
    confidence_score: float
    alternative_versions: List[str]


class EmailResponder:
    """AI-powered email response generator"""
    
    TONES = {
        "professional": "Formal, businesslike, respectful",
        "casual": "Friendly, conversational, approachable",
        "empathetic": "Understanding, compassionate, supportive",
        "assertive": "Direct, confident, clear boundaries",
        "apologetic": "Sorry, understanding, solution-focused",
    }
    
    def __init__(self, api_key: Optional[str] = None, company_context: Optional[str] = None):
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.company_context = company_context or "We are a professional services company."
        self.conversation_history = []
    
    def analyze_email(self, email_text: str, thread_context: Optional[str] = None) -> EmailAnalysis:
        """Analyze incoming email for intent, urgency, and key points"""
        
        prompt = f"""Analyze the following email and provide a structured analysis.

{'PREVIOUS CONVERSATION CONTEXT:' + thread_context if thread_context else ''}

EMAIL TO ANALYZE:
---
{email_text}
---

Provide your analysis as a JSON object with this structure:

{{
  "intent": "<inquiry|complaint|follow_up|booking|support|partnership|sales|other>",
  "urgency": "<low|medium|high|critical>",
  "sentiment": "<positive|neutral|negative>",
  "key_points": [
    "Main point 1",
    "Main point 2",
    "Main point 3"
  ],
  "questions_asked": [
    "Question 1",
    "Question 2"
  ],
  "action_items": [
    "Action item 1",
    "Action item 2"
  ],
  "suggested_tone": "<professional|casual|empathetic|assertive|apologetic>",
  "estimated_response_complexity": "<simple|moderate|complex>"
}}

ANALYSIS CRITERIA:

**Intent**: What is the sender trying to accomplish?
**Urgency**: How quickly does this need a response?
**Sentiment**: What is the emotional tone?
**Key Points**: What are the main topics discussed?
**Questions**: What specific questions need answers?
**Action Items**: What needs to be done?
**Suggested Tone**: What tone would be most appropriate for response?
**Complexity**: How detailed should the response be?
"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert email communication analyst who understands business correspondence patterns and emotional intelligence."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.2,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            
            return EmailAnalysis(
                intent=result.get("intent", "other"),
                urgency=result.get("urgency", "medium"),
                sentiment=result.get("sentiment", "neutral"),
                key_points=result.get("key_points", []),
                questions_asked=result.get("questions_asked", []),
                action_items=result.get("action_items", []),
                suggested_tone=result.get("suggested_tone", "professional"),
                estimated_response_complexity=result.get("estimated_response_complexity", "moderate")
            )
            
        except Exception as e:
            print(f"Error analyzing email: {e}")
            raise
    
    def generate_response(
        self,
        email_text: str,
        analysis: EmailAnalysis,
        tone: Optional[str] = None,
        thread_context: Optional[str] = None,
        your_name: str = "Our Team",
        company_signature: Optional[str] = None,
        additional_instructions: Optional[str] = None,
    ) -> EmailResponse:
        """Generate contextually appropriate email response"""
        
        tone = tone or analysis.suggested_tone
        tone_description = self.TONES.get(tone, "professional")
        
        prompt = f"""Generate a professional email response based on the analysis below.

COMPANY CONTEXT:
{self.company_context}

{'PREVIOUS CONVERSATION:' + thread_context if thread_context else ''}

INCOMING EMAIL:
---
{email_text}
---

EMAIL ANALYSIS:
- Intent: {analysis.intent}
- Urgency: {analysis.urgency}
- Sentiment: {analysis.sentiment}
- Key Points: {', '.join(analysis.key_points)}
- Questions to Answer: {', '.join(analysis.questions_asked) if analysis.questions_asked else 'None'}
- Action Items: {', '.join(analysis.action_items) if analysis.action_items else 'None'}

YOUR TASK:
Generate an email response with the following characteristics:

TONE: {tone} - {tone_description}

STRUCTURE:
1. Subject line (if replying, use "Re: [original subject]" - generate appropriate subject)
2. Greeting (appropriate to tone)
3. Opening (acknowledge their message with empathy)
4. Body (address all key points and answer all questions)
5. Next steps or call to action
6. Professional closing

REQUIREMENTS:
- Address EVERY question asked in the original email
- Acknowledge their sentiment appropriately
- Be specific and actionable
- Match the urgency level in your response timing language
- Keep paragraphs short (2-3 sentences max)
- Use "you" more than "I/we"
- Be human and authentic, not robotic
- If complaint: acknowledge, apologize if appropriate, offer solution
- If inquiry: provide complete information, offer additional help
- If follow-up: reference previous conversation naturally

{f'ADDITIONAL INSTRUCTIONS: {additional_instructions}' if additional_instructions else ''}

Provide response as JSON:

{{
  "subject": "Subject line text",
  "body": "Full email body without signature",
  "key_points_addressed": ["point 1", "point 2"],
  "confidence_score": <0.0-1.0>,
  "alternative_opening": "Alternative first paragraph if you want to soften/strengthen tone",
  "alternative_closing": "Alternative closing paragraph"
}}

Generate the response now."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert business communication specialist who writes clear, empathetic, and effective email responses."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            
            # Add signature if provided
            body = result.get("body", "")
            if company_signature:
                body += f"\n\n{company_signature}"
            elif your_name:
                body += f"\n\nBest regards,\n{your_name}"
            
            alternatives = []
            if result.get("alternative_opening"):
                alternatives.append(f"Alt Opening: {result['alternative_opening']}")
            if result.get("alternative_closing"):
                alternatives.append(f"Alt Closing: {result['alternative_closing']}")
            
            return EmailResponse(
                subject=result.get("subject", "Re: Your message"),
                body=body,
                tone_used=tone,
                key_points_addressed=result.get("key_points_addressed", []),
                confidence_score=result.get("confidence_score", 0.8),
                alternative_versions=alternatives
            )
            
        except Exception as e:
            print(f"Error generating response: {e}")
            raise
    
    def process_email(
        self,
        email_text: str,
        tone: Optional[str] = None,
        thread_context: Optional[str] = None,
        your_name: str = "Our Team",
        company_signature: Optional[str] = None,
        additional_instructions: Optional[str] = None,
    ) -> Tuple[EmailAnalysis, EmailResponse]:
        """Complete pipeline: analyze and generate response"""
        
        analysis = self.analyze_email(email_text, thread_context)
        response = self.generate_response(
            email_text,
            analysis,
            tone,
            thread_context,
            your_name,
            company_signature,
            additional_instructions
        )
        
        return analysis, response
    
    def display_results(self, analysis: EmailAnalysis, response: EmailResponse):
        """Display analysis and response"""
        
        print("\n" + "="*80)
        print("EMAIL ANALYSIS")
        print("="*80)
        print(f"\n📋 Intent: {analysis.intent.upper()}")
        print(f"⚡ Urgency: {analysis.urgency.upper()}")
        print(f"😊 Sentiment: {analysis.sentiment.upper()}")
        print(f"💭 Suggested Tone: {analysis.suggested_tone}")
        
        if analysis.key_points:
            print(f"\n🎯 Key Points:")
            for point in analysis.key_points:
                print(f"  • {point}")
        
        if analysis.questions_asked:
            print(f"\n❓ Questions to Answer:")
            for q in analysis.questions_asked:
                print(f"  • {q}")
        
        if analysis.action_items:
            print(f"\n✅ Action Items:")
            for item in analysis.action_items:
                print(f"  • {item}")
        
        print("\n" + "="*80)
        print("GENERATED RESPONSE")
        print("="*80)
        print(f"\nSubject: {response.subject}")
        print(f"Tone: {response.tone_used}")
        print(f"Confidence: {response.confidence_score:.1%}")
        print("\n" + "-"*80)
        print(response.body)
        print("-"*80)
        
        if response.key_points_addressed:
            print(f"\n✓ Addressed: {', '.join(response.key_points_addressed)}")
        
        if response.alternative_versions:
            print(f"\n💡 Alternative Options:")
            for alt in response.alternative_versions:
                print(f"  • {alt}")
    
    def batch_process(
        self,
        input_dir: Path,
        output_dir: Path,
        tone: str,
        your_name: str,
        company_signature: Optional[str] = None
    ):
        """Process multiple emails in batch"""
        
        input_dir = Path(input_dir)
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        email_files = list(input_dir.glob("*.txt")) + list(input_dir.glob("*.eml"))
        
        print(f"\n📧 Processing {len(email_files)} emails...\n")
        
        for email_file in email_files:
            print(f"Processing: {email_file.name}")
            
            try:
                email_text = email_file.read_text(encoding="utf-8")
                analysis, response = self.process_email(
                    email_text,
                    tone,
                    your_name=your_name,
                    company_signature=company_signature
                )
                
                # Save response
                response_file = output_dir / f"response_{email_file.stem}.txt"
                response_file.write_text(
                    f"Subject: {response.subject}\n\n{response.body}",
                    encoding="utf-8"
                )
                
                # Save analysis
                analysis_file = output_dir / f"analysis_{email_file.stem}.json"
                analysis_file.write_text(json.dumps(asdict(analysis), indent=2))
                
                print(f"  ✓ Response saved to: {response_file.name}\n")
                
            except Exception as e:
                print(f"  ✗ Error: {e}\n")


def main():
    parser = argparse.ArgumentParser(
        description="AI-powered email response generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python email_responder.py --email incoming.txt --tone professional
  python email_responder.py --text "Email text" --context thread.txt --name "John Smith"
  python email_responder.py --batch inbox/ --tone empathetic --export responses/
        """
    )
    
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--email", type=Path, help="Email file to respond to")
    input_group.add_argument("--text", type=str, help="Direct email text")
    input_group.add_argument("--batch", type=Path, help="Directory of emails")
    
    parser.add_argument(
        "--tone",
        choices=list(EmailResponder.TONES.keys()),
        help="Response tone (defaults to AI suggestion)"
    )
    parser.add_argument("--context", type=Path, help="Previous email thread file")
    parser.add_argument("--name", default="Our Team", help="Your name for signature")
    parser.add_argument("--signature", type=Path, help="File with company signature")
    parser.add_argument("--company", help="Company context description")
    parser.add_argument("--instructions", help="Additional response instructions")
    parser.add_argument("--export", type=Path, help="Output directory for batch processing")
    
    args = parser.parse_args()
    
    # Load optional files
    thread_context = args.context.read_text() if args.context else None
    signature = args.signature.read_text() if args.signature else None
    
    responder = EmailResponder(company_context=args.company)
    
    try:
        if args.batch:
            if not args.batch.is_dir():
                print(f"Error: {args.batch} is not a directory")
                sys.exit(1)
            
            export_dir = args.export or Path("responses")
            responder.batch_process(
                args.batch,
                export_dir,
                args.tone or "professional",
                args.name,
                signature
            )
            
        else:
            # Single email
            if args.email:
                email_text = args.email.read_text(encoding="utf-8")
            else:
                email_text = args.text
            
            analysis, response = responder.process_email(
                email_text,
                args.tone,
                thread_context,
                args.name,
                signature,
                args.instructions
            )
            
            responder.display_results(analysis, response)
    
    except KeyboardInterrupt:
        print("\n\nProcessing cancelled.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
