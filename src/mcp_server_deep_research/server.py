from enum import Enum
import logging
from typing import Any
import json

# Import MCP server
from mcp.server.models import InitializationOptions
from mcp.types import (
    TextContent,
    Tool,
    Resource,
    Prompt,
    PromptArgument,
    GetPromptResult,
    PromptMessage,
)
from mcp.server import NotificationOptions, Server
from pydantic import AnyUrl
import mcp.server.stdio

logger = logging.getLogger(__name__)
logger.info("Starting deep research server")


### Prompt templates
class DeepResearchPrompts(str, Enum):
    DEEP_RESEARCH = "deep-research"


class PromptArgs(str, Enum):
    RESEARCH_QUESTION = "research_question"


PROMPT_TEMPLATE = """
You are an expert research analyst tasked with conducting comprehensive, multi-dimensional research on a complex topic and producing a publication-quality research report. Your goal is to provide deep, critical analysis that goes beyond surface-level information to deliver genuine insights and evidence-based conclusions.

The research question is:

<research_question>
{research_question}
</research_question>

Follow this advanced research methodology systematically:

═══════════════════════════════════════════════════════════════════════════════
PHASE 1: PRELIMINARY ANALYSIS & RESEARCH DESIGN
═══════════════════════════════════════════════════════════════════════════════

1. <question_elaboration>
   Conduct a thorough elaboration of the research question:
   
   a) CONCEPTUAL CLARIFICATION
      - Define all key terms and concepts with precision
      - Identify ambiguous language that requires clarification
      - Establish clear boundaries for what is IN and OUT of scope
      - Specify any temporal, geographical, or contextual constraints
   
   b) DOMAIN MAPPING
      - Identify the primary knowledge domain(s) this question belongs to
      - Recognize intersecting disciplines and cross-domain considerations
      - Note relevant theoretical frameworks or established models
   
   c) STAKEHOLDER IDENTIFICATION
      - Who cares about this question and why?
      - What different perspectives exist on this topic?
      - Which groups or entities are affected by this issue?
   
   d) COMPLEXITY ASSESSMENT
      Evaluate the complexity level (Simple/Moderate/Complex/Highly Complex):
      - Simple: Single-domain, straightforward comparison or definition
      - Moderate: Multiple aspects, some interdependencies
      - Complex: Multi-domain, significant interdependencies, multiple perspectives
      - Highly Complex: Highly interdisciplinary, contentious, rapidly evolving
      
      This assessment will determine research depth and structure.
</question_elaboration>

2. <research_strategy>
   Based on your complexity assessment, design an appropriate research strategy:
   
   a) SELECT ANALYTICAL FRAMEWORKS
      Choose 1-3 frameworks most appropriate for this question:
      
      - SWOT Analysis: For strategic questions about opportunities, risks, capabilities
      - PEST/PESTEL: For macro-environmental factors (Political, Economic, Social, Technological, Environmental, Legal)
      - 5W2H Framework: For diagnostic questions (What, Why, When, Where, Who, How, How Much)
      - Comparative Analysis: For evaluating alternatives across dimensions
      - Trend Analysis: For understanding historical evolution and future trajectories
      - Case Study Method: For deep-dive into specific examples
      - Stakeholder Analysis: For understanding different perspectives and interests
      - Evidence Pyramid: For medical/scientific questions requiring evidence hierarchy
      - Systems Thinking: For complex interdependent phenomena
   
   b) DETERMINE RESEARCH DEPTH
      - Layer 1 (Overview): Always required - establish foundational understanding
      - Layer 2 (Deep Dive): For Moderate/Complex questions - focused investigation of key areas
      - Layer 3 (Expert Analysis): For Complex/Highly Complex - cutting-edge insights, specialized knowledge
</research_strategy>

═══════════════════════════════════════════════════════════════════════════════
PHASE 2: HIERARCHICAL QUESTION DECOMPOSITION
═══════════════════════════════════════════════════════════════════════════════

3. <subquestion_generation>
   Generate a hierarchical structure of research questions based on complexity:
   
   QUANTITY GUIDELINES:
   - Simple questions: 3-4 core subquestions
   - Moderate questions: 5-6 core subquestions + 2-3 secondary deep-dive questions
   - Complex questions: 6-7 core subquestions + 3-5 secondary questions (1-2 per relevant core question)
   - Highly Complex: 7-8 core subquestions + 5-8 secondary questions (distributed across core questions)
   
   STRUCTURE FORMAT:
   
   Core Subquestion 1: [Fundamental aspect]
      Priority: High/Medium/Low
      Dependencies: None / [Related subquestion numbers]
      │
      ├─ Deep-dive 1.1: [Specific investigation area] (if complexity warrants)
      └─ Deep-dive 1.2: [Another specific angle] (if needed)
   
   Core Subquestion 2: [Another fundamental aspect]
      Priority: High/Medium/Low
      Dependencies: [If this builds on subquestion 1, note it]
      │
      └─ Deep-dive 2.1: [Specific investigation] (if complexity warrants)
   
   [Continue for all subquestions...]
   
   QUALITY CRITERIA FOR EACH SUBQUESTION:
   - Specific and focused (answerable, not overly broad)
   - Collectively exhaustive (cover all major aspects)
   - Mutually exclusive where possible (minimize overlap)
   - Researchable through available sources
   - Aligned with selected analytical framework(s)
   
   INTERDISCIPLINARY PERSPECTIVES:
   Tag each core subquestion with relevant disciplinary lenses:
   - Technical/Engineering: Implementation, feasibility, mechanisms
   - Business/Economic: Market dynamics, financial implications, ROI
   - Social/Cultural: Human impact, behavioral aspects, equity
   - Legal/Regulatory: Compliance, governance, policy
   - Ethical: Moral considerations, values, responsibilities
   - Scientific: Evidence base, empirical findings, theories
   - Historical: Evolution, precedents, context
</subquestion_generation>

═══════════════════════════════════════════════════════════════════════════════
PHASE 3: LAYERED INFORMATION GATHERING
═══════════════════════════════════════════════════════════════════════════════

4. For EACH subquestion, conduct research in progressive layers:

   <layer_1_overview>
   LAYER 1: OVERVIEW & FOUNDATION (Required for all questions)
   
   Objective: Establish baseline understanding
   
   a) BROAD WEB SEARCH
      - Perform 2-3 broad searches to understand the landscape
      - Target: Academic sources, reputable news, industry reports, official documentation
      - Capture: Definitions, key facts, major schools of thought, consensus views
   
   b) SOURCE CREDIBILITY ASSESSMENT
      For each source, evaluate:
      - Author/Organization Authority: Credentials, reputation, expertise
      - Publication Venue: Peer-reviewed? Reputable outlet? Blog?
      - Recency: When published? Still relevant? Has field evolved since?
      - Bias Indicators: Funding sources, conflicts of interest, ideological slant
      - Corroboration: Do other credible sources agree?
      
      Assign credibility rating: High / Medium / Low
   
   c) EVIDENCE EXTRACTION & CLASSIFICATION
      For each piece of information, classify as:
      - STRONG EVIDENCE: Peer-reviewed research, official statistics, expert consensus
      - MODERATE EVIDENCE: Reputable journalism, industry reports, expert opinion (single source)
      - WEAK EVIDENCE: Anecdotal reports, non-expert opinion, limited studies
      - SPECULATIVE: Predictions, hypotheses, early-stage research
      
      Quote sparingly: <25 words per quote, max 1 quote per source, only for key definitions or striking insights
   </layer_1_overview>

   <layer_2_deep_dive>
   LAYER 2: TARGETED DEEP DIVE (For Moderate/Complex/Highly Complex questions)
   
   Objective: Investigate specific angles, compare perspectives, identify patterns
   
   a) FOCUSED SEARCHES
      - Based on Layer 1 findings, identify knowledge gaps or areas requiring deeper investigation
      - Perform 3-5 targeted searches on specific sub-aspects
      - Seek out: Specialized sources, case studies, empirical data, competing viewpoints
   
   b) COMPARATIVE ANALYSIS
      When multiple viewpoints exist:
      - Mainstream Position: What do most experts/sources agree on?
      - Alternative Views: What dissenting or minority perspectives exist?
      - Evidence Quality: Which position has stronger empirical support?
      - Reasoning Quality: Evaluate logical coherence of each position
   
   c) PATTERN IDENTIFICATION
      - Trends over time: Has thinking on this evolved? In what direction?
      - Geographic variation: Do different regions approach this differently?
      - Contextual factors: What conditions influence outcomes?
   </layer_2_deep_dive>

   <layer_3_expert_analysis>
   LAYER 3: EXPERT-LEVEL INSIGHTS (For Complex/Highly Complex questions only)
   
   Objective: Access cutting-edge knowledge, specialized expertise, frontier insights
   
   a) FRONTIER RESEARCH
      - Recent academic publications (last 1-2 years)
      - Emerging trends not yet mainstream
      - Ongoing debates in specialist communities
      - Innovative applications or novel approaches
   
   b) EXPERT DISCOURSE
      - Thought leaders' analyses
      - Conference proceedings or technical presentations
      - Specialized industry reports
      - Expert interviews or panel discussions (if accessible)
   
   c) FUTURE TRAJECTORIES
      - What are leading experts predicting?
      - What assumptions underlie these predictions?
      - What could disrupt current trends?
   </layer_3_expert_analysis>

═══════════════════════════════════════════════════════════════════════════════
PHASE 4: CRITICAL ANALYSIS & SYNTHESIS
═══════════════════════════════════════════════════════════════════════════════

5. <critical_analysis>
   For the body of research collected, conduct rigorous critical analysis:
   
   a) EVIDENCE MAPPING
      Create a logical map of your findings:
      - Central Claims: What are the key assertions related to each subquestion?
      - Supporting Evidence: What evidence supports each claim? (rate strength)
      - Contradicting Evidence: What evidence challenges each claim?
      - Evidence Gaps: What's missing? Where is evidence thin or absent?
   
   b) LOGICAL COHERENCE CHECK
      - Causation vs. Correlation: Are claimed causal relationships actually supported?
      - Internal Consistency: Do different pieces of evidence contradict each other?
      - Reasoning Validity: Are inferences logically sound?
      - Assumption Identification: What unstated assumptions underlie key arguments?
   
   c) BIAS & LIMITATIONS ASSESSMENT
      - Selection Bias: Are certain types of sources over/under-represented?
      - Confirmation Bias: Did you seek out contradicting information?
      - Temporal Bias: Is recent information over-weighted vs. historical context?
      - Publication Bias: Might negative results be underrepresented?
   
   d) HYPOTHESIS FORMULATION & TESTING (for appropriate question types)
      If the research question involves causal claims or predictions:
      1. Formulate testable hypotheses based on initial findings
      2. Identify what evidence would support vs. refute each hypothesis
      3. Evaluate available evidence against hypotheses
      4. Conclude: Supported / Partially Supported / Not Supported / Insufficient Evidence
   
   e) CONFIDENCE LEVEL ASSIGNMENT
      For each major conclusion, assign confidence level:
      - HIGH CONFIDENCE: Multiple high-quality sources, strong consensus, robust evidence
      - MODERATE CONFIDENCE: Good sources, reasonable agreement, some evidence gaps
      - LOW CONFIDENCE: Limited sources, significant disagreement, or weak evidence
      - SPECULATIVE: Insufficient evidence, extrapolation required
</critical_analysis>

6. <interdisciplinary_synthesis>
   Integrate insights across different disciplinary perspectives:
   
   a) CROSS-PERSPECTIVE PATTERNS
      - Where do technical, economic, social, and ethical analyses align?
      - Where do they diverge or create tension?
      - What trade-offs exist between different optimization criteria?
   
   b) EMERGENT INSIGHTS
      - What insights emerge only when combining multiple perspectives?
      - Are there unintended consequences visible from one lens but not others?
      - What holistic understanding emerges from the integrated view?
   
   c) SYSTEMS-LEVEL UNDERSTANDING
      - How do different components interact?
      - What feedback loops or cascading effects exist?
      - What leverage points could produce disproportionate impact?
</interdisciplinary_synthesis>

═══════════════════════════════════════════════════════════════════════════════
PHASE 5: COMPREHENSIVE REPORT GENERATION
═══════════════════════════════════════════════════════════════════════════════

7. <report_creation>
   Create a publication-quality research report as an artifact with this structure:
   
   ┌─────────────────────────────────────────────────────────────────────┐
   │ RESEARCH REPORT: [Compelling Title Based on Research Question]      │
   └─────────────────────────────────────────────────────────────────────┘
   
   ╔══════════════════════════════════════════════════════════════════════╗
   ║ EXECUTIVE SUMMARY (200-300 words)                                    ║
   ╚══════════════════════════════════════════════════════════════════════╝
   
   A concise, standalone summary containing:
   - The research question and its significance
   - Research methodology employed
   - 3-5 key findings (most important discoveries)
   - Primary conclusion with confidence level
   - Critical implications or recommendations (if applicable)
   
   ╔══════════════════════════════════════════════════════════════════════╗
   ║ TABLE OF CONTENTS                                                    ║
   ╚══════════════════════════════════════════════════════════════════════╝
   
   [Auto-generated based on section structure]
   
   ╔══════════════════════════════════════════════════════════════════════╗
   ║ 1. INTRODUCTION                                                      ║
   ╚══════════════════════════════════════════════════════════════════════╝
   
   - Context and background
   - Research question and its importance
   - Scope and boundaries
   - Key concepts and definitions
   - Research approach overview
   
   ╔══════════════════════════════════════════════════════════════════════╗
   ║ 2. METHODOLOGY                                                       ║
   ╚══════════════════════════════════════════════════════════════════════╝
   
   - Complexity assessment rationale
   - Analytical frameworks selected and why
   - Research layers employed
   - Source selection criteria
   - Limitations of methodology
   
   ╔══════════════════════════════════════════════════════════════════════╗
   ║ 3. FINDINGS                                                          ║
   ╚══════════════════════════════════════════════════════════════════════╝
   
   [For EACH core subquestion, create a subsection:]
   
   3.X [SUBQUESTION TITLE]
   
   - Overview of findings
   - Evidence summary (with credibility ratings)
   - Analysis of perspectives (if multiple exist)
   - Key data/statistics (use tables where appropriate)
   - Deep-dive insights (for secondary questions if applicable)
   - Confidence level for conclusions
   - Proper citations [Author/Organization, "Title," URL]
   
   [Apply selected analytical framework(s) where relevant - e.g., SWOT table, trend chart, comparison matrix]
   
   ╔══════════════════════════════════════════════════════════════════════╗
   ║ 4. CRITICAL ANALYSIS                                                 ║
   ╚══════════════════════════════════════════════════════════════════════╝
   
   - Evidence strength assessment across findings
   - Logical coherence evaluation
   - Identification of contradictions or gaps
   - Bias and limitation analysis
   - Hypothesis testing results (if applicable)
   
   ╔══════════════════════════════════════════════════════════════════════╗
   ║ 5. SYNTHESIS & DISCUSSION                                            ║
   ╚══════════════════════════════════════════════════════════════════════╝
   
   - Integration of findings across subquestions
   - Interdisciplinary insights
   - Emergent patterns and themes
   - Contextual factors influencing outcomes
   - Comparison with theoretical expectations (if applicable)
   
   ╔══════════════════════════════════════════════════════════════════════╗
   ║ 6. CONCLUSIONS                                                       ║
   ╚══════════════════════════════════════════════════════════════════════╝
   
   - Direct answer to the research question
   - Supporting rationale from evidence
   - Confidence level and reasoning
   - Broader implications
   - Areas of uncertainty
   
   ╔══════════════════════════════════════════════════════════════════════╗
   ║ 7. RECOMMENDATIONS (if applicable)                                   ║
   ╚══════════════════════════════════════════════════════════════════════╝
   
   Based on findings, provide actionable recommendations for:
   - Decision-makers
   - Practitioners
   - Researchers
   - Other relevant stakeholders
   
   ╔══════════════════════════════════════════════════════════════════════╗
   ║ 8. RESEARCH LIMITATIONS                                              ║
   ╚══════════════════════════════════════════════════════════════════════╝
   
   Transparently acknowledge:
   - Scope constraints
   - Data availability issues
   - Methodological limitations
   - Potential biases
   - Time sensitivity of findings
   
   ╔══════════════════════════════════════════════════════════════════════╗
   ║ 9. FURTHER RESEARCH DIRECTIONS                                       ║
   ╚══════════════════════════════════════════════════════════════════════╝
   
   - Identified knowledge gaps
   - Promising areas for deeper investigation
   - Emerging questions from this research
   
   ╔══════════════════════════════════════════════════════════════════════╗
   ║ REFERENCES                                                           ║
   ╚══════════════════════════════════════════════════════════════════════╝
   
   [Comprehensive list of all sources cited]
   Format: Author/Organization. "Title." Publication/Website. URL. (Date accessed if relevant)
   Organized alphabetically or by appearance
   
   ╔══════════════════════════════════════════════════════════════════════╗
   ║ APPENDIX: KEY TERMS GLOSSARY (if needed)                             ║
   ╚══════════════════════════════════════════════════════════════════════╝
   
   [Definitions of technical or specialized terms used in the report]
   
   ╔══════════════════════════════════════════════════════════════════════╗
   ║ APPENDIX: SUPPLEMENTARY DATA (if applicable)                         ║
   ╚══════════════════════════════════════════════════════════════════════╝
   
   [Additional tables, charts, or detailed data supporting the analysis]
   
</report_creation>

═══════════════════════════════════════════════════════════════════════════════
CRITICAL RESEARCH ETHICS & COPYRIGHT GUIDELINES
═══════════════════════════════════════════════════════════════════════════════

You MUST adhere to these ethical and legal guidelines:

✓ CITATION REQUIREMENTS:
  - Cite ALL sources with author/organization, title, and URL
  - Attribute all facts, data, and ideas to their sources
  - Never present others' work as your own

✓ QUOTATION LIMITS (to respect copyright):
  - Maximum 25 words per quotation
  - Maximum 1 quotation per source
  - Use quotations only for definitions, key insights, or particularly notable phrasing
  - Everything else must be paraphrased in your own words

✓ PROHIBITED CONTENT:
  - No reproduction of song lyrics, poems, or creative works
  - No extensive excerpts from copyrighted material
  - No proprietary information or confidential data
  - Keep any summary of copyrighted content to 2-3 sentences maximum

✓ INTELLECTUAL INTEGRITY:
  - Present multiple perspectives fairly
  - Acknowledge uncertainty and limitations
  - Don't cherry-pick evidence to support predetermined conclusions
  - Distinguish between facts, interpretations, and opinions

═══════════════════════════════════════════════════════════════════════════════

Now begin your comprehensive research process. Document each phase thoroughly, showing your analytical reasoning at each step. Produce a research report that represents the highest standard of depth, rigor, and insight.
"""


### Research Processor
class ResearchProcessor:
    def __init__(self):
        self.research_data = {
            "question": "",
            "elaboration": "",
            "subquestions": [],
            "search_results": {},
            "extracted_content": {},
            "final_report": "",
        }
        self.notes: list[str] = []

    def add_note(self, note: str):
        """Add a note to the research process."""
        self.notes.append(note)
        logger.debug(f"Note added: {note}")

    def update_research_data(self, key: str, value: Any):
        """Update a specific key in the research data dictionary."""
        self.research_data[key] = value
        self.add_note(f"Updated research data: {key}")

    def get_research_notes(self) -> str:
        """Return all research notes as a newline-separated string."""
        return "\n".join(self.notes)

    def get_research_data(self) -> dict:
        """Return the current research data dictionary."""
        return self.research_data


### MCP Server Definition
async def main():
    research_processor = ResearchProcessor()
    server = Server("deep-research-server")

    @server.list_resources()
    async def handle_list_resources() -> list[Resource]:
        logger.debug("Handling list_resources request")
        return [
            Resource(
                uri="research://notes",
                name="Research Process Notes",
                description="Notes generated during the research process",
                mimeType="text/plain",
            ),
            Resource(
                uri="research://data",
                name="Research Data",
                description="Structured data collected during the research process",
                mimeType="application/json",
            ),
        ]

    @server.read_resource()
    async def handle_read_resource(uri: AnyUrl) -> str:
        logger.debug(f"Handling read_resource request for URI: {uri}")
        if str(uri) == "research://notes":
            return research_processor.get_research_notes()
        elif str(uri) == "research://data":
            return json.dumps(research_processor.get_research_data(), indent=2)
        else:
            raise ValueError(f"Unknown resource: {uri}")

    @server.list_prompts()
    async def handle_list_prompts() -> list[Prompt]:
        logger.debug("Handling list_prompts request")
        return [
            Prompt(
                name=DeepResearchPrompts.DEEP_RESEARCH,
                description="A prompt to conduct deep research on a question",
                arguments=[
                    PromptArgument(
                        name=PromptArgs.RESEARCH_QUESTION,
                        description="The research question to investigate",
                        required=True,
                    ),
                ],
            )
        ]

    @server.get_prompt()
    async def handle_get_prompt(
        name: str, arguments: dict[str, str] | None
    ) -> GetPromptResult:
        logger.debug(f"Handling get_prompt request for {name} with args {arguments}")
        if name != DeepResearchPrompts.DEEP_RESEARCH:
            logger.error(f"Unknown prompt: {name}")
            raise ValueError(f"Unknown prompt: {name}")

        if not arguments or PromptArgs.RESEARCH_QUESTION not in arguments:
            logger.error("Missing required argument: research_question")
            raise ValueError("Missing required argument: research_question")

        research_question = arguments[PromptArgs.RESEARCH_QUESTION]
        prompt = PROMPT_TEMPLATE.format(research_question=research_question)

        # Store the research question
        research_processor.update_research_data("question", research_question)
        research_processor.add_note(
            f"Research initiated on question: {research_question}"
        )

        logger.debug(
            f"Generated prompt template for research_question: {research_question}"
        )
        return GetPromptResult(
            description=f"Deep research template for: {research_question}",
            messages=[
                PromptMessage(
                    role="user",
                    content=TextContent(type="text", text=prompt.strip()),
                )
            ],
        )

    @server.list_tools()
    async def handle_list_tools() -> list[Tool]:
        logger.debug("Handling list_tools request")
        return [
            Tool(
                name="start_deep_research",
                description="Start a comprehensive deep research process on a specific question. This tool initiates a structured research workflow that guides the AI through question elaboration, subquestion generation, web searching, content analysis, and report generation. Use this when you need to conduct thorough research on a complex topic.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "research_question": {
                            "type": "string",
                            "description": "The research question to investigate in depth",
                        }
                    },
                    "required": ["research_question"],
                },
            )
        ]

    @server.call_tool()
    async def handle_call_tool(name: str, arguments: dict | None) -> list[TextContent]:
        logger.debug(f"Handling call_tool request for {name} with args {arguments}")
        
        if name != "start_deep_research":
            logger.error(f"Unknown tool: {name}")
            raise ValueError(f"Unknown tool: {name}")
        
        if not arguments or "research_question" not in arguments:
            logger.error("Missing required argument: research_question")
            raise ValueError("Missing required argument: research_question")
        
        research_question = arguments["research_question"]
        
        # Update research processor state
        research_processor.update_research_data("question", research_question)
        research_processor.add_note(
            f"Research initiated via tool on question: {research_question}"
        )
        
        # Format the prompt template with the research question
        prompt = PROMPT_TEMPLATE.format(research_question=research_question)
        
        logger.debug(
            f"Generated research guidance for question: {research_question}"
        )
        
        return [
            TextContent(
                type="text",
                text=prompt.strip()
            )
        ]

    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        logger.debug("Server running with stdio transport")
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="deep-research-server",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )
