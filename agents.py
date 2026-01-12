from crewai import Agent, LLM
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
import os

# Initialize the LLM (Groq)
llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

# Tools
search_tool = SerperDevTool(api_key=os.getenv("SERPER_API_KEY"))
scrape_tool = ScrapeWebsiteTool()


class JobApplicationAgents:
    
    def job_researcher_agent(self):
        return Agent(
            role='Job Research Specialist',
            goal='Find the most relevant job postings based on user preferences',
            backstory='You are an expert at finding job opportunities.',
            tools=[search_tool, scrape_tool],
            llm=llm,
            verbose=True
        )
    
    def resume_strategist_agent(self):
        return Agent(
            role='Resume Optimization Specialist',
            goal='Analyze job descriptions and suggest resume improvements',
            backstory='You are a professional resume writer.',
            llm=llm,
            verbose=True
        )
    
    def cover_letter_writer_agent(self):
        return Agent(
            role='Cover Letter Expert',
            goal='Write compelling cover letters',
            backstory='You are a master of persuasive writing.',
            llm=llm,
            verbose=True
        )
    
    def application_tracker_agent(self):
        return Agent(
            role='Application Organization Specialist',
            goal='Track job applications and deadlines',
            backstory='You are highly organized.',
            llm=llm,
            verbose=True
        )
    
    def interview_prep_agent(self):
        return Agent(
            role='Interview Preparation Coach',
            goal='Prepare interview questions and answers',
            backstory='You are an interview coach.',
            tools=[search_tool, scrape_tool],
            llm=llm,
            verbose=True
        )