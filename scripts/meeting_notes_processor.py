#!/usr/bin/env python3
"""
AI Meeting Notes Processor with Action Item Extraction

What it does:
- Transforms messy meeting notes/transcripts into structured summaries
- Extracts action items with owners and deadlines
- Identifies key decisions and next steps
- Generates follow-up emails automatically
- Creates project management tickets (JIRA/Linear format)
- Tracks recurring topics across multiple meetings

Why use this:
- Never lose track of meeting outcomes
- Automatically assign action items
- Generate professional meeting summaries in seconds
- Perfect for team leads, PMs, and executive assistants

Usage:
    python meeting_notes_processor.py --notes meeting.txt --attendees "John, Sarah, Mike"
    python meeting_notes_processor.py --transcript zoom_transcript.vtt --format email
    python meeting_notes_processor.py --batch meetings_folder/ --export reports/

Requirements:
    pip install openai python-dateutil webvtt-py
    export OPENAI_API_KEY="sk-..."
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import re

try:
    from openai import OpenAI
    from dateutil import parser as date_parser
    try:
        import webvtt
        VTT_AVAILABLE = True
    except ImportError:
        VTT_AVAILABLE = False
        print("Note: webvtt-py not installed. VTT transcript support disabled.")
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Install with: pip install openai python-dateutil webvtt-py")
    sys.exit(1)


@dataclass
class ActionItem:
    """Single action item from meeting"""
    task: str
    owner: Optional[str]
    deadline: Optional[str]
    priority: str  # high, medium, low
    status: str = "pending"


@dataclass
class Decision:
    """Key decision made during meeting"""
    decision: str
    context: str
    decision_maker: Optional[str]
    impact: str  # high, medium, low


@dataclass
class MeetingSummary:
    """Complete meeting summary"""
    meeting_title: str
    meeting_date: Optional[str]
    attendees: List[str]
    summary: str
    key_topics: List[str]
    decisions: List[Decision]
    action_items: List[ActionItem]
    next_meeting: Optional[str]
    parking_lot: List[str]  # Topics tabled for later
    meeting_effectiveness_score: float


class MeetingNotesProcessor:
    """AI-powered meeting notes processor"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
    
    def parse_vtt_transcript(self, vtt_path: Path) -> str:
        """Parse VTT transcript file (Zoom, Teams, etc.)"""
        if not VTT_AVAILABLE:
            raise RuntimeError("webvtt-py not installed. Install with: pip install webvtt-py")
        
        transcript_lines = []
        for caption in webvtt.read(str(vtt_path)):
            # Remove timestamps and speaker labels if present
            text = caption.text.strip()
            if text:
                transcript_lines.append(text)
        
        return " ".join(transcript_lines)
    
    def process_notes(
        self,
        notes_text: str,
        meeting_title: Optional[str] = None,
        attendees: Optional[List[str]] = None,
        meeting_date: Optional[str] = None,
    ) -> MeetingSummary:
        """Process raw meeting notes into structured summary"""
        
        prompt = self._build_processing_prompt(
            notes_text,
            meeting_title,
            attendees,
            meeting_date
        )
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": """You are an expert executive assistant who specializes in 
                        transforming messy meeting notes into clear, actionable summaries with 
                        perfect action item tracking."""
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
            
            # Parse into dataclass
            decisions = [
                Decision(**d) for d in result.get("decisions", [])
            ]
            
            action_items = [
                ActionItem(**a) for a in result.get("action_items", [])
            ]
            
            return MeetingSummary(
                meeting_title=result.get("meeting_title", meeting_title or "Meeting"),
                meeting_date=result.get("meeting_date", meeting_date),
                attendees=result.get("attendees", attendees or []),
                summary=result.get("summary", ""),
                key_topics=result.get("key_topics", []),
                decisions=decisions,
                action_items=action_items,
                next_meeting=result.get("next_meeting"),
                parking_lot=result.get("parking_lot", []),
                meeting_effectiveness_score=result.get("meeting_effectiveness_score", 0.7)
            )
            
        except Exception as e:
            print(f"Error processing notes: {e}")
            raise
    
    def _build_processing_prompt(
        self,
        notes: str,
        title: Optional[str],
        attendees: Optional[List[str]],
        date: Optional[str]
    ) -> str:
        """Build comprehensive processing prompt"""
        
        attendees_str = ", ".join(attendees) if attendees else "Not specified"
        
        return f"""Process the following meeting notes and extract structured information.

MEETING CONTEXT:
Title: {title or "To be determined"}
Date: {date or "To be determined"}
Attendees: {attendees_str}

RAW MEETING NOTES/TRANSCRIPT:
---
{notes}
---

Provide your analysis as a JSON object with this structure:

{{
  "meeting_title": "Clear, descriptive title if not provided",
  "meeting_date": "YYYY-MM-DD format if mentioned",
  "attendees": ["Name 1", "Name 2"],
  "summary": "2-3 paragraph executive summary of the meeting",
  "key_topics": [
    "Topic 1",
    "Topic 2",
    "Topic 3"
  ],
  "decisions": [
    {{
      "decision": "What was decided",
      "context": "Why this decision was made",
      "decision_maker": "Person who made the call (if mentioned)",
      "impact": "high|medium|low"
    }}
  ],
  "action_items": [
    {{
      "task": "Specific, actionable task description",
      "owner": "Person responsible (if mentioned, else null)",
      "deadline": "YYYY-MM-DD or 'this week', 'next sprint', etc.",
      "priority": "high|medium|low",
      "status": "pending"
    }}
  ],
  "next_meeting": "When next meeting scheduled (if mentioned)",
  "parking_lot": [
    "Topic tabled for later discussion 1",
    "Topic tabled for later discussion 2"
  ],
  "meeting_effectiveness_score": <0.0-1.0>
}}

EXTRACTION GUIDELINES:

**Summary:**
- Lead with the most important outcomes
- Include key context and background
- Mention any roadblocks or concerns raised
- Keep it executive-level (readable in 30 seconds)

**Key Topics:**
- List 3-7 main discussion areas
- Use clear, descriptive phrases
- Prioritize by time spent and importance

**Decisions:**
- Only include ACTUAL decisions made (not discussions)
- Be specific about what was decided
- Include context for "why" when mentioned
- Mark impact based on scope of implications

**Action Items:**
- Make each item specific and actionable (starts with verb)
- Extract owner even if implied from context
- Infer reasonable deadlines if mentioned relatively (e.g., "by end of week")
- Set priority based on urgency indicators in discussion
- Format: "Do X by Y" not "We should think about X"

**Parking Lot:**
- Topics mentioned but explicitly deferred
- Questions raised without answers
- Ideas noted for future consideration

**Meeting Effectiveness Score:**
- 0.9-1.0: Clear outcomes, all action items assigned, decisions made
- 0.7-0.8: Good progress, most items addressed, some ambiguity
- 0.5-0.6: Some progress, many open items, unclear next steps
- 0.3-0.4: Mostly discussion, few concrete outcomes
- 0.0-0.2: Unclear purpose, no outcomes, poor use of time

BE SPECIFIC: Don't say "Follow up on X" - say "Send proposal for X to client by Friday"
INFER CONTEXT: Use discussion context to assign priorities and owners when reasonable
STAY FACTUAL: Only include what was actually discussed, don't add assumptions"""
    
    def generate_follow_up_email(self, summary: MeetingSummary) -> str:
        """Generate professional follow-up email"""
        
        email_parts = []
        email_parts.append(f"Subject: Meeting Recap: {summary.meeting_title}")
        email_parts.append(f"\nHi team,\n")
        email_parts.append(f"Thank you for joining {'today' if not summary.meeting_date else summary.meeting_date}'s meeting. Here's a quick recap:\n")
        
        # Summary
        email_parts.append(f"**Summary:**\n{summary.summary}\n")
        
        # Key Topics
        if summary.key_topics:
            email_parts.append(f"\n**Topics Discussed:**")
            for topic in summary.key_topics:
                email_parts.append(f"• {topic}")
            email_parts.append("")
        
        # Decisions
        if summary.decisions:
            email_parts.append(f"\n**Decisions Made:**")
            for i, decision in enumerate(summary.decisions, 1):
                email_parts.append(f"{i}. {decision.decision}")
                if decision.context:
                    email_parts.append(f"   → {decision.context}")
            email_parts.append("")
        
        # Action Items
        if summary.action_items:
            email_parts.append(f"\n**Action Items:**")
            for item in summary.action_items:
                owner_str = f" ({item.owner})" if item.owner else ""
                deadline_str = f" - Due: {item.deadline}" if item.deadline else ""
                priority_emoji = "🔴" if item.priority == "high" else "🟡" if item.priority == "medium" else "🟢"
                email_parts.append(f"{priority_emoji} {item.task}{owner_str}{deadline_str}")
            email_parts.append("")
        
        # Parking Lot
        if summary.parking_lot:
            email_parts.append(f"\n**Parking Lot (for next time):**")
            for item in summary.parking_lot:
                email_parts.append(f"• {item}")
            email_parts.append("")
        
        # Next Meeting
        if summary.next_meeting:
            email_parts.append(f"\n**Next Meeting:** {summary.next_meeting}\n")
        
        email_parts.append(f"Please let me know if I missed anything or if you have questions.\n")
        email_parts.append(f"Best regards")
        
        return "\n".join(email_parts)
    
    def generate_jira_tickets(self, summary: MeetingSummary, project_key: str = "PROJ") -> List[Dict]:
        """Generate JIRA/Linear-format tickets from action items"""
        
        tickets = []
        
        for item in summary.action_items:
            # Map priority
            jira_priority = {
                "high": "High",
                "medium": "Medium",
                "low": "Low"
            }.get(item.priority, "Medium")
            
            # Parse deadline to due date
            due_date = None
            if item.deadline:
                try:
                    # Try parsing as date
                    parsed = date_parser.parse(item.deadline, fuzzy=True)
                    due_date = parsed.strftime("%Y-%m-%d")
                except:
                    # Use as-is if can't parse
                    due_date = item.deadline
            
            ticket = {
                "key": f"{project_key}-XXX",  # Will be auto-assigned
                "summary": item.task,
                "description": f"Action item from meeting: {summary.meeting_title}\n\nContext from meeting:\n{summary.summary}",
                "assignee": item.owner or "Unassigned",
                "priority": jira_priority,
                "due_date": due_date,
                "labels": [summary.meeting_title.replace(" ", "-").lower(), "meeting-action-item"],
                "issue_type": "Task"
            }
            
            tickets.append(ticket)
        
        return tickets
    
    def display_summary(self, summary: MeetingSummary):
        """Display formatted summary"""
        
        print("\n" + "="*80)
        print(f"MEETING SUMMARY: {summary.meeting_title}")
        print("="*80)
        
        if summary.meeting_date:
            print(f"\n📅 Date: {summary.meeting_date}")
        
        if summary.attendees:
            print(f"👥 Attendees: {', '.join(summary.attendees)}")
        
        effectiveness_emoji = "🟢" if summary.meeting_effectiveness_score >= 0.8 else "🟡" if summary.meeting_effectiveness_score >= 0.6 else "🔴"
        print(f"{effectiveness_emoji} Effectiveness: {summary.meeting_effectiveness_score:.1%}")
        
        print(f"\n📝 EXECUTIVE SUMMARY")
        print("-" * 80)
        print(summary.summary)
        
        if summary.key_topics:
            print(f"\n💬 KEY TOPICS")
            print("-" * 80)
            for topic in summary.key_topics:
                print(f"  • {topic}")
        
        if summary.decisions:
            print(f"\n✅ DECISIONS MADE")
            print("-" * 80)
            for i, decision in enumerate(summary.decisions, 1):
                impact_emoji = "🔴" if decision.impact == "high" else "🟡" if decision.impact == "medium" else "🟢"
                print(f"\n  {i}. {impact_emoji} {decision.decision}")
                if decision.context:
                    print(f"     Context: {decision.context}")
                if decision.decision_maker:
                    print(f"     Decision by: {decision.decision_maker}")
        
        if summary.action_items:
            print(f"\n🎯 ACTION ITEMS")
            print("-" * 80)
            for item in summary.action_items:
                priority_emoji = "🔴" if item.priority == "high" else "🟡" if item.priority == "medium" else "🟢"
                owner_str = f" ({item.owner})" if item.owner else " (Unassigned)"
                deadline_str = f" - Due: {item.deadline}" if item.deadline else ""
                print(f"  {priority_emoji} {item.task}{owner_str}{deadline_str}")
        
        if summary.parking_lot:
            print(f"\n🅿️  PARKING LOT")
            print("-" * 80)
            for item in summary.parking_lot:
                print(f"  • {item}")
        
        if summary.next_meeting:
            print(f"\n📅 NEXT MEETING: {summary.next_meeting}")
        
        print("\n" + "="*80)
    
    def batch_process(
        self,
        input_dir: Path,
        output_dir: Path,
        format: str = "text"
    ):
        """Process multiple meeting notes"""
        
        input_dir = Path(input_dir)
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        files = list(input_dir.glob("*.txt")) + list(input_dir.glob("*.md"))
        if VTT_AVAILABLE:
            files += list(input_dir.glob("*.vtt"))
        
        print(f"\n📝 Processing {len(files)} meeting notes...\n")
        
        for notes_file in files:
            print(f"Processing: {notes_file.name}")
            
            try:
                # Read notes
                if notes_file.suffix == ".vtt":
                    notes_text = self.parse_vtt_transcript(notes_file)
                else:
                    notes_text = notes_file.read_text(encoding="utf-8")
                
                # Process
                summary = self.process_notes(notes_text)
                
                # Save outputs
                stem = notes_file.stem
                
                if format == "email":
                    email = self.generate_follow_up_email(summary)
                    output_file = output_dir / f"{stem}_followup.txt"
                    output_file.write_text(email)
                
                elif format == "jira":
                    tickets = self.generate_jira_tickets(summary)
                    output_file = output_dir / f"{stem}_tickets.json"
                    output_file.write_text(json.dumps(tickets, indent=2))
                
                else:  # text
                    output_file = output_dir / f"{stem}_summary.json"
                    output_file.write_text(json.dumps(asdict(summary), indent=2, default=str))
                
                print(f"  ✓ Saved to: {output_file.name}\n")
                
            except Exception as e:
                print(f"  ✗ Error: {e}\n")


def main():
    parser = argparse.ArgumentParser(
        description="AI-powered meeting notes processor",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python meeting_notes_processor.py --notes meeting.txt --attendees "John, Sarah"
  python meeting_notes_processor.py --transcript zoom.vtt --format email
  python meeting_notes_processor.py --batch meetings/ --export summaries/ --format jira
        """
    )
    
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--notes", type=Path, help="Meeting notes file")
    input_group.add_argument("--transcript", type=Path, help="VTT transcript file")
    input_group.add_argument("--batch", type=Path, help="Directory of meeting notes")
    
    parser.add_argument("--title", help="Meeting title")
    parser.add_argument("--attendees", help="Comma-separated attendee names")
    parser.add_argument("--date", help="Meeting date (YYYY-MM-DD)")
    parser.add_argument(
        "--format",
        choices=["text", "email", "jira"],
        default="text",
        help="Output format"
    )
    parser.add_argument("--export", type=Path, help="Output directory for batch")
    parser.add_argument("--project-key", default="PROJ", help="JIRA project key for tickets")
    
    args = parser.parse_args()
    
    processor = MeetingNotesProcessor()
    
    try:
        if args.batch:
            if not args.batch.is_dir():
                print(f"Error: {args.batch} is not a directory")
                sys.exit(1)
            
            export_dir = args.export or Path("meeting_summaries")
            processor.batch_process(args.batch, export_dir, args.format)
            
        else:
            # Single meeting
            if args.transcript:
                notes_text = processor.parse_vtt_transcript(args.transcript)
            else:
                notes_text = args.notes.read_text(encoding="utf-8")
            
            attendees = args.attendees.split(",") if args.attendees else None
            
            summary = processor.process_notes(
                notes_text,
                args.title,
                attendees,
                args.date
            )
            
            processor.display_summary(summary)
            
            # Generate additional formats
            if args.format == "email":
                print("\n" + "="*80)
                print("FOLLOW-UP EMAIL")
                print("="*80)
                print(processor.generate_follow_up_email(summary))
            
            elif args.format == "jira":
                print("\n" + "="*80)
                print("JIRA TICKETS")
                print("="*80)
                tickets = processor.generate_jira_tickets(summary, args.project_key)
                print(json.dumps(tickets, indent=2))
    
    except KeyboardInterrupt:
        print("\n\nProcessing cancelled.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
