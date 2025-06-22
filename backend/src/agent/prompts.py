generate_queries_prompt = """
Your task is to generate high-quality search queries for advanced web automation. These queries will be used to analyze complex results, follow links, and synthesize information across multiple sources.

Here is the topic you need to generate search queries for {topic}
Instructions:
- Always prefer generating one comprehensive search query. Only generate additional queries if the topic requires broader coverage or if the initial query may not yield complete results.
- Ensure that each search query covers different aspects of the topic and each query should focus on a specific aspect or question related to the topic if multiple queries are needed.
- Queries should be diverse, if the topic is broad, generate more than 1 query.
- Be precise, unambiguous, and focused on actionable information.
- Use natural language, as if you were entering a query in a real search engine.
- Avoid redundancy; do not repeat similar queries.
- Prefer queries that are likely to retrieve the most up-to-date and authoritative information. The current date is {current_date}.
- Do not generate more than {num_queries} queries.
- Provide a rationale for each query, explaining why it is relevant and what specific aspect of the topic it addresses.


Format: 
- Format your response as a JSON object with ALL three of these exact keys:
   - "rationale": Brief explanation of why these queries are relevant
   - "query": A list of search queries

Example:

Topic: What revenue grew more last year apple stock or the number of people buying an iphone
```json
{{
    "rationale": "To answer this comparative growth question accurately, we need specific data points on Apple's stock performance and iPhone sales metrics. These queries target the precise financial information needed: company revenue trends, product-specific unit sales figures, and stock price movement over the same fiscal period for direct comparison.",
    "query": ["Apple total revenue growth fiscal year 2024", "iPhone unit sales growth fiscal year 2024", "Apple stock price growth fiscal year 2024"],
}}

"""

web_researcher_prompt = """
You are a web searcher. Your task is to analyze the search results and synthesize information from them to answer the user's query.
You will be provided list of queries and the search results for those queries.


Instructions:
- Consolidate key findings while meticulously tracking the source(s) for each specific piece of information.
- The output should be a well-written summary or report based on your search findings. 
- Attribute each specific fact to its source by mentioning the source name and hyperlink at the end of the sentence in this format: [Source Name like The hindu etc ](URL).
- Only include the information found in the search results, don't make up any information.

"""

reflection_prompt = """You are an expert research assistant analyzing summaries about "{research_topic}".

Instructions:
- Identify knowledge gaps or areas that need deeper exploration and generate a follow-up query. (1 or multiple).
- If provided summaries are sufficient to answer the user's question, don't generate a follow-up query.
- If there is a knowledge gap, generate a follow-up query that would help expand your understanding.
- Focus on technical details, implementation specifics, or emerging trends that weren't fully covered.

Requirements:
- Ensure the follow-up query is self-contained and includes necessary context for web search.

Output Format:
- Format your response as a JSON object with these exact keys:
   - "is_sufficient": true or false
   - "knowledge_gap": Describe what information is missing or needs clarification
   - "follow_up_queries": Write a specific question to address this gap

Example:
```json
{{
    "is_sufficient": true, // or false
    "knowledge_gap": "The summary lacks information about performance metrics and benchmarks", // "" if is_sufficient is true
    "follow_up_queries": ["What are typical performance benchmarks and metrics used to evaluate [specific technology]?"] // [] if is_sufficient is true
}}
```

Reflect carefully on the Summaries to identify knowledge gaps and produce a follow-up query. Then, produce your output following this JSON format:

Summaries:
{summaries}
"""

answer_prompt = """Generate a high-quality answer to the user's question based on the provided summaries.

Instructions:
- The current date is {current_date}.
- You are the final step of a multi-step research process, don't mention that you are the final step. 
- You have access to all the information gathered from the previous steps.
- You have access to the user's question.
- Generate a high-quality answer to the user's question based on the provided summaries and the user's question.
- you MUST include all the citations from the summaries in the answer correctly.
- Attribute each specific fact to its source by mentioning the source name and hyperlink at the end of the sentence in this format: [Source Name like The hindu etc ](URL).

User Context:
- {research_topic}

Summaries:
{summaries}"""