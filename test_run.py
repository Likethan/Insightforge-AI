import os
from dotenv import load_dotenv # type: ignore
import google.generativeai as genai # type: ignore

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

topic = "The Future of Artificial Intelligence in Agriculture"
analysis = "AI is expected to increase crop yields by 30% globally. Startups in Tamil Nadu are adopting AI-driven soil analysis."
chart_mention = "The bar chart shows a 45% increase in AI adoption in farming from 2020 to 2025."

prompt = f"""
SYSTEM ROLE: You are a professional REPORT GENERATION ENGINE.

You MUST follow ALL instructions strictly. Do NOT skip sections. Do NOT shorten the response.

-----------------------------------
INPUT
-----------------------------------
Topic: "{topic}"

Research Analysis:
{analysis if analysis else "No additional analysis provided."}

Chart Insight:
{chart_mention if chart_mention else "No chart insight provided."}

-----------------------------------
MANDATORY RULES (STRICT)
-----------------------------------

- You MUST generate a FULL structured report.
- You MUST NOT give a short answer.
- You MUST follow the exact format below.
- You MUST expand even simple topics into detailed explanations.
- You MUST include ALL sections.
- If data is missing, intelligently generate relevant content.

-----------------------------------
OUTPUT FORMAT (DO NOT CHANGE)
-----------------------------------

# Title: 

## 1. Executive Summary
Write a detailed executive summary explaining the topic and its core strategic importance.

## 2. Strategic Analysis
Explain the topic deeply with clear concepts, drivers, and subtopics.

## 3. AI Insights
Provide advanced intelligence-driven analysis of the topic, identifying automation potential, patterns, and anomalies.

## 4. Global Trends
Discuss worldwide impact, macro trends, and global industry relevance.

## 5. Case Studies
Give at least two real-world examples (companies, projects, or scenarios).

## 6. Data Visualization Insights
Interpret data trends, patterns, and projections. Outline key metrics that can be visually graphed.

## 7. Conclusion
Provide a strong summary with strategic recommendations.

## 8. References
Mention general sources like research papers, industry reports, global data platforms.

-----------------------------------
WRITING STYLE
-----------------------------------

- Formal and professional tone
- Paragraph-based (NOT only bullet points)
- Clear, detailed, and well-structured
- No repetition
- No vague statements

-----------------------------------
FINAL INSTRUCTION
-----------------------------------

Generate the COMPLETE report now. Do not skip anything.
"""

try:
    response = model.generate_content(prompt)
    import sys
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    print("=== GENERATED REPORT ===")
    print(response.text)
except Exception as e:
    print(f"ERROR: {e}")
