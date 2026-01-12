from crewai import Crew, Process
from agents import JobApplicationAgents
from tasks import JobApplicationTasks
from dotenv import load_dotenv
import os
import sys

# Load environment variables
load_dotenv()

def main():
    try:
        # Check for API keys
        groq_key = os.getenv("GROQ_API_KEY")
        serper_key = os.getenv("SERPER_API_KEY")
        
        if not groq_key:
            print("❌ ERROR: GROQ_API_KEY not found in .env file")
            sys.exit(1)
        
        if not serper_key:
            print("❌ ERROR: SERPER_API_KEY not found in .env file")
            sys.exit(1)
        
        print("✅ API keys loaded successfully")
        print("=" * 60)
        print("🚀 Job Application Assistant")
        print("=" * 60)
        
        # Get user input
        print("\n📋 Let's gather your job search criteria...\n")
        
        job_criteria = {
            'role': input("What role are you looking for? (e.g., Software Developer): ").strip() or "Software Developer",
            'location': input("Preferred location? (e.g., Remote, New York): ").strip() or "Remote",
            'experience': input("Experience level? (e.g., Entry, Mid, Senior): ").strip() or "Mid-level",
            'keywords': input("Key skills/keywords? (e.g., Python, AI, React): ").strip() or "Python, AI"
        }
        
        print("\n" + "=" * 60)
        print("🤖 Initializing AI Agents...")
        print("=" * 60 + "\n")
        
        # Initialize agents and tasks
        agents = JobApplicationAgents()
        tasks = JobApplicationTasks()
        
        # Create agents
        print("Creating Job Researcher Agent...")
        job_researcher = agents.job_researcher_agent()
        
        print("Creating Resume Strategist Agent...")
        resume_strategist = agents.resume_strategist_agent()
        
        # Create tasks
        print("Creating research task...")
        research_task = tasks.research_jobs_task(job_researcher, job_criteria)
        
        # For demo purposes, we'll use placeholder data
        demo_job_description = "Looking for a Python developer with AI/ML experience"
        demo_resume = "Software developer with 3 years of Python experience"
        
        print("Creating resume tailoring task...")
        tailor_resume_task = tasks.tailor_resume_task(
            resume_strategist,
            demo_job_description,
            demo_resume
        )
        
        # Create the crew
        print("Assembling crew...")
        crew = Crew(
            agents=[job_researcher, resume_strategist],
            tasks=[research_task, tailor_resume_task],
            process=Process.sequential,
            verbose=True
        )
        
        # Run the crew
        print("\n🎯 Starting job search process...\n")
        result = crew.kickoff()
        
        # Display results
        print("\n" + "=" * 60)
        print("✅ RESULTS")
        print("=" * 60)
        print(result)
        
        # Save results to file
        with open("job_search_results.txt", "w", encoding="utf-8") as f:
            f.write(str(result))
        
        print("\n💾 Results saved to 'job_search_results.txt'")
        print("\n" + "=" * 60)
        print("🎉 Job Application Assistant Complete!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ ERROR occurred: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        import traceback
        print("\nFull traceback:")
        traceback.print_exc()

if __name__ == "__main__":
    main()
