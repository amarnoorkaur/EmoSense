"""
Root Cause Reasoning Engine
Uses LLM to identify underlying causes behind customer frustrations and praises
"""
from typing import Dict, List, Any, Optional
import os
from openai import OpenAI
import json


class RootCauseEngine:
    """
    Analyzes pain point clusters to identify root causes using GPT-4o-mini
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize OpenAI client"""
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key required for root cause analysis")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = "gpt-4o-mini"
    
    def infer_root_causes(
        self,
        clusters: List[Dict[str, Any]],
        emotions: Dict[str, float],
        themes: List[str],
        macro_summary: str,
        raw_comments: List[str]
    ) -> Dict[str, Any]:
        """
        Infer root causes for each pain point cluster
        
        Args:
            clusters: List of pain point clusters
            emotions: Overall emotion distribution
            themes: Extracted themes/keywords
            macro_summary: Summary of all comments
            raw_comments: Raw customer comments
            
        Returns:
            Dictionary with root cause analysis
        """
        if not clusters:
            return {
                "root_causes": [],
                "error": "No clusters provided for analysis"
            }
        
        # Build comprehensive context
        context = self._build_analysis_context(
            clusters=clusters,
            emotions=emotions,
            themes=themes,
            macro_summary=macro_summary,
            raw_comments=raw_comments
        )
        
        # Build reasoning prompt
        prompt = self._build_reasoning_prompt(context)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": self._get_system_prompt()
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.5,  # Lower for more focused reasoning
                max_tokens=1500
            )
            
            analysis_text = response.choices[0].message.content
            
            # Parse root causes (structured output expected)
            root_causes = self._parse_root_causes(analysis_text, clusters)
            
            return {
                "root_causes": root_causes,
                "total_clusters_analyzed": len(clusters),
                "model": self.model,
                "tokens_used": response.usage.total_tokens if hasattr(response, 'usage') else None
            }
        
        except Exception as e:
            return {
                "root_causes": [],
                "error": f"Root cause analysis failed: {str(e)}"
            }
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for root cause reasoning"""
        return """You are a SENIOR ROOT CAUSE ANALYST with deep expertise in:
- Customer psychology and behavioral patterns
- Product-market fit analysis
- UX research and pain point identification
- Cause-and-effect reasoning
- Business problem diagnosis

Your ONLY job: Identify the TRUE UNDERLYING CAUSE behind customer feedback patterns.

CRITICAL RULES:
1. Every root cause MUST be grounded in actual customer comments
2. Identify WHY customers feel what they feel (not just WHAT they feel)
3. Use cause-and-effect logic
4. Quote specific customer comments as evidence
5. Distinguish between symptoms and root causes
6. Never make assumptions not supported by data
7. Be specific, not generic

Examples of GOOD root cause analysis:

❌ BAD (symptom): "Users are confused"
✅ GOOD (root cause): "Users are confused because the onboarding flow doesn't explain how pricing tiers work, leading to uncertainty about which plan to choose"

❌ BAD (vague): "Product has issues"
✅ GOOD (specific): "Export feature crashes in sessions longer than 30 minutes because users mention 'crashes when exporting large files', suggesting a memory management issue"

❌ BAD (generic): "Users want improvements"
✅ GOOD (actionable): "Users request dark mode because they use the app at night and find the bright interface straining, as evidenced by 'too bright at night' and 'hurts my eyes'"

Your output MUST identify:
- The underlying cause (WHY this pain exists)
- Evidence from actual comments
- The connection between cause and effect
"""
    
    def _build_analysis_context(
        self,
        clusters: List[Dict[str, Any]],
        emotions: Dict[str, float],
        themes: List[str],
        macro_summary: str,
        raw_comments: List[str]
    ) -> str:
        """Build comprehensive context for analysis"""
        
        # Format clusters
        clusters_text = ""
        for i, cluster in enumerate(clusters, 1):
            sentiment = cluster.get('sentiment_summary', {})
            clusters_text += f"""
CLUSTER {i}: {cluster.get('theme_name', 'Unknown Theme')}
- Size: {cluster.get('size', 0)} comments ({cluster.get('percentage', 0):.1f}% of total)
- Keywords: {', '.join(cluster.get('theme_keywords', []))}
- Sentiment: {sentiment.get('status', 'Unknown')} ({sentiment.get('negative', 0):.0%} negative, {sentiment.get('positive', 0):.0%} positive)
- Top Emotions: {', '.join([f"{e.capitalize()}: {p:.0%}" for e, p in cluster.get('emotion_distribution', {}).items()])}

Example Comments:
{chr(10).join([f'  - "{comment}"' for comment in cluster.get('comment_examples', [])[:3]])}
"""
        
        # Format overall emotions
        top_emotions = sorted(emotions.items(), key=lambda x: x[1], reverse=True)[:8]
        emotions_text = "\n".join([f"  - {e.capitalize()}: {p:.1%}" for e, p in top_emotions])
        
        # Format themes
        themes_text = ", ".join(themes[:15]) if themes else "No themes extracted"
        
        context = f"""
═══════════════════════════════════════════════════════════════
CUSTOMER FEEDBACK ANALYSIS CONTEXT
═══════════════════════════════════════════════════════════════

**MACRO SUMMARY:**
{macro_summary}

**OVERALL EMOTIONS:**
{emotions_text}

**KEY THEMES:**
{themes_text}

**PAIN POINT CLUSTERS:**
{clusters_text}

**TOTAL COMMENTS ANALYZED:** {len(raw_comments)}

═══════════════════════════════════════════════════════════════
"""
        return context
    
    def _build_reasoning_prompt(self, context: str) -> str:
        """Build the reasoning prompt"""
        return f"""
{context}

═══════════════════════════════════════════════════════════════
YOUR TASK: ROOT CAUSE ANALYSIS
═══════════════════════════════════════════════════════════════

For EACH cluster above, identify the ROOT CAUSE behind that pain point or praise pattern.

Use this exact format for EACH cluster:

---
## Cluster [ID]: [Theme Name]

**Root Cause:**
[Explain WHY customers experience this pain/praise - what's the underlying reason?]

**Cause-Effect Logic:**
[Explain the connection: Because [root cause], customers experience [symptom/feeling]]

**Evidence from Comments:**
- "[Quote supporting comment 1]"
- "[Quote supporting comment 2]"
- "[Quote supporting comment 3]"

**Actionable Insight:**
[What specific action would address this ROOT CAUSE (not just the symptom)?]
---

CRITICAL INSTRUCTIONS:
1. Identify the UNDERLYING cause, not surface-level symptoms
2. Use actual customer quotes as evidence
3. Explain cause-and-effect clearly
4. Be specific and actionable
5. Focus on WHY, not just WHAT
6. Never make up information not in the comments

Analyze ALL clusters now:
"""
    
    def _parse_root_causes(self, analysis_text: str, clusters: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Parse the root cause analysis from LLM response
        
        Args:
            analysis_text: Raw text from LLM
            clusters: Original clusters for matching
            
        Returns:
            Structured list of root causes
        """
        root_causes = []
        
        # Try to extract structured data
        # Split by cluster sections
        sections = analysis_text.split('## Cluster')
        
        for i, section in enumerate(sections[1:], 1):  # Skip first empty section
            try:
                # Extract components
                lines = section.strip().split('\n')
                
                # Find root cause
                root_cause = ""
                for line in lines:
                    if '**Root Cause:**' in line:
                        idx = lines.index(line)
                        root_cause = lines[idx + 1].strip() if idx + 1 < len(lines) else ""
                        break
                
                # Find evidence (quotes)
                evidence = []
                in_evidence_section = False
                for line in lines:
                    if '**Evidence from Comments:**' in line:
                        in_evidence_section = True
                        continue
                    if in_evidence_section:
                        if line.startswith('- "') or line.startswith('  - "'):
                            # Extract quote
                            quote = line.strip().lstrip('- "').rstrip('"')
                            if quote:
                                evidence.append(quote)
                        elif line.startswith('**'):
                            break
                
                # Find actionable insight
                actionable_insight = ""
                for line in lines:
                    if '**Actionable Insight:**' in line:
                        idx = lines.index(line)
                        actionable_insight = lines[idx + 1].strip() if idx + 1 < len(lines) else ""
                        break
                
                # Match to cluster
                cluster_match = clusters[i - 1] if i - 1 < len(clusters) else None
                
                if cluster_match and root_cause:
                    root_causes.append({
                        "cluster_id": cluster_match.get('cluster_id', i - 1),
                        "theme_name": cluster_match.get('theme_name', 'Unknown'),
                        "root_cause": root_cause,
                        "evidence": evidence[:5],  # Top 5 evidence quotes
                        "actionable_insight": actionable_insight,
                        "cluster_size": cluster_match.get('size', 0)
                    })
            
            except Exception as e:
                # Fallback: create basic entry
                cluster_match = clusters[i - 1] if i - 1 < len(clusters) else None
                if cluster_match:
                    root_causes.append({
                        "cluster_id": cluster_match.get('cluster_id', i - 1),
                        "theme_name": cluster_match.get('theme_name', 'Unknown'),
                        "root_cause": section[:200] + "..." if len(section) > 200 else section,
                        "evidence": [],
                        "actionable_insight": "",
                        "cluster_size": cluster_match.get('size', 0)
                    })
        
        return root_causes


def get_root_cause_engine() -> Optional[RootCauseEngine]:
    """
    Get cached root cause engine instance
    
    Returns:
        RootCauseEngine instance or None if API key not available
    """
    try:
        return RootCauseEngine()
    except ValueError:
        return None
