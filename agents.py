import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from tools import scrape_url, web_search

load_dotenv()


def _get_gemini_api_key() -> str:
    """Retrieve Gemini API key from environment variables or Streamlit secrets, with a safe fallback."""
    key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not key:
        try:
            import streamlit as st
            key = st.secrets.get("GEMINI_API_KEY") or st.secrets.get("GOOGLE_API_KEY")
        except Exception:
            pass
    # Return placeholder if no key found to prevent import-time ValidationError
    return key or "dummy_key_for_initialization"


def _get_gemini_model() -> str:
    """Allow model override via GEMINI_MODEL env var, defaulting to gemini-2.5-flash / gemini-1.5-flash."""
    return os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


# Global LLM instance (used by chains and agents)
llm = ChatGoogleGenerativeAI(
    model=_get_gemini_model(),
    temperature=0,
    google_api_key=_get_gemini_api_key(),
)


# 1st agent: Search Agent
def build_search_agent():
    return create_agent(
        model=llm,
        tools=[web_search],
    )


# 2nd agent: Reader Agent
def build_reader_agent():
    return create_agent(
        model=llm,
        tools=[scrape_url],
    )


# Writer chain
writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Write clear, structured and insightful reports."),
    ("human", """Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all URLs found in the research)

Be detailed, factual and professional."""),
])

writer_chain = writer_prompt | llm | StrOutputParser()

# Critic chain
critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
..."""),
])

critic_chain = critic_prompt | llm | StrOutputParser()
