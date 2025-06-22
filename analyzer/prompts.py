import openai


def build_prompt(text: str, mode: str) -> str:
    if mode == "clarity":
        return f"""You're a SaaS marketing expert and homepage clarity strategist. Analyze the homepage below and return the following:

1. **Offer Clarity Score (1–10)** — Give a score and explain why you gave it, with a focus on how clearly the product and its benefit are conveyed above the fold.

2. **Target Audience Guess** — Based on the language, tone, and pitch, who is this homepage really speaking to?

3. **Emotional Resonance Check** — Does the copy appeal to a specific pain, desire, or frustration of that audience? If not, what’s missing emotionally?

4. **Summary of the Problem Being Solved and How** — Explain the core user problem and how this SaaS claims to solve it.

5. **Clarity Risks or Mismatches** — Are there parts of the copy that might confuse or alienate certain personas? Point out technical jargon, vague buzzwords, or unclear metaphors.

6. **Rewritten Hero Section** — Rewrite the top headline and subtext in a clear, compelling, and persona-focused way using the StoryBrand framework. Include a suggested CTA.

7. **Quick Fixes vs Deeper Rewrite Suggestions** — Give 3–5 actionable clarity improvements, but separate them into:
   - Small Tweaks (language simplification, rewording)
   - Strategic Fixes (structure, audience focus, message hierarchy)

8. **Missing Persuasion Hooks** — What psychological triggers could be added to increase clarity and conversion? (e.g., urgency, specificity, proof, authority)

Homepage:
{text}"""
    elif mode == "competitor":
        return f"""You're a SaaS go-to-market strategist and positioning expert. Analyze the homepage copy below and return:

1. Main headline or pitch (exact copy)
2. Key value proposition (summarized)
3. Top 2 primary use cases (ranked and justified)
4. Ideal customer persona (ICP)
5. Breakdown of GTM messaging:
   - CTAs
   - Key feature messaging
   - 5 Trust signals
   - Pricing strategy
6. SEO keywords being focused on (primary + secondary)
7. Rewritten offer in the storybrand framework
8. 3 Blind Spots or Missed Opportunities
9. Competitive Benchmarking: Compare with 1–2 similar SaaS competitors and highlight differences in clarity or appeal
10. Differentiation Clarity: Is this clearly unique? If not, suggest a better positioning angle
11. Emotional/Cognitive Hooks: What persuasion triggers are used? Suggest stronger ones if underused
12. Messaging Risks: Any strategic risks or misalignments in current copy?



Homepage:
{text}"""
    else:
        return "Invalid mode"


async def run_analysis(text: str, mode: str, api_key: str) -> str:
    client = openai.OpenAI(api_key=api_key)
    prompt = build_prompt(text, mode)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    return response.choices[0].message.content.strip()
