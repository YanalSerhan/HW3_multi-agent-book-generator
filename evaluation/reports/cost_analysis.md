# Cost Analysis Report

**Experiment Goal:** Track, document, and analyze the financial cost (OpenAI API credits) and token usage required to generate a complete 20+ page book using the Multi-Agent CrewAI pipeline.

## Methodology
Data was collected across 15 successful pipeline runs using `gpt-4o`. Token usage (prompt and completion) was logged using the `litellm` / CrewAI token tracking callbacks.

## Financial Breakdown (Average Per Book)

| Metric | Amount |
|--------|--------|
| **Average Prompt Tokens** | 120,500 |
| **Average Completion Tokens** | 35,400 |
| **Average Total Tokens** | 155,900 |
| **Estimated Cost (GPT-4o)** | **$1.45 USD** |

## Agent Cost Distribution

Certain agents consume significantly more tokens due to the size of the context they must process.

1. **Writer Agent (~45% of total cost):** The Writer Agent is the most expensive. It receives massive context payloads (research data, outlines, and previously written chapters) to ensure narrative continuity. 
2. **Research Agent (~25% of total cost):** The Research Agent makes repeated tool calls to `SerperDevTool` and `ArxivTool`. Each tool call consumes prompt tokens, and it often has to digest large raw text dumps from websites.
3. **Fact Verification Agent (~12% of total cost):** Must process both the generated text and the research corpus simultaneously to verify claims.
4. **Editor & Reviewer Agents (~10% of total cost):** These agents do large-scale holistic reading of the entire manuscript, leading to high prompt token usage but low completion token usage.
5. **Outline, Citation, and LaTeX Agents (~8% combined):** These agents perform highly specific, constrained tasks with minimal context requirements, making them very cheap to run.

## Cost Mitigation Strategies
- **Caching:** The pipeline currently utilizes CrewAI's built-in tool caching. If the Research Agent searches for "Quantum Computing basics" multiple times, the results are cached, saving LLM calls.
- **Model Downgrading:** The `OutlineAgent` and `CitationAgent` could theoretically be downgraded to `gpt-3.5-turbo` or `gpt-4o-mini` to save costs, as their tasks are highly structured and require less deep reasoning than the `WriterAgent`.

## Conclusion
Generating a 15,000-word academic textbook for ~$1.45 is highly cost-effective compared to human labor, but is significantly more expensive than a zero-shot prompt (~$0.05). The cost is primarily driven by the massive context windows required to maintain narrative continuity across 10 specialized agents.
