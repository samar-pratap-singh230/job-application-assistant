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
        if not os.getenv("GROQ_API_KEY") or not os.getenv("SERPER_API_KEY"):
            print("❌ ERROR: API keys not found in .env file")
            sys.exit(1)
            
        print("✅ API keys loaded successfully")
        print("=" * 60)
        print("🚀 Job Application Assistant (CLI Mode)")
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
        
        # 1. Initialize Classes
        agents_class = JobApplicationAgents()
        tasks_class = JobApplicationTasks()
        
        # 2. Create Agents
        print("Creating Job Researcher Agent...")
        job_researcher = agents_class.job_researcher_agent()
        
        print("Creating Resume Strategist Agent...")
        resume_strategist = agents_class.resume_strategist_agent()

        print("Creating Cover Letter Agent...")
        cover_letter_agent = agents_class.cover_letter_writer_agent()
        
        print("Creating Interview Coach Agent...") # <--- NEW
        interview_agent = agents_class.interview_prep_agent()
        
        # 3. Create Tasks
        print("Creating research task...")
        research_task = tasks_class.research_jobs_task(job_researcher, job_criteria)
        
        demo_resume = f"A {job_criteria['experience']} level professional with skills in {job_criteria['keywords']}"
        
        print("Creating resume tailoring task...")
        tailor_resume_task = tasks_class.tailor_resume_task(
            resume_strategist,
            demo_resume
        )
        tailor_resume_task.context = [research_task]

        print("Creating cover letter task...")
        cover_letter_task = tasks_class.write_cover_letter_task(
            cover_letter_agent,
            f"Candidate with {job_criteria['experience']} experience"
        )
        cover_letter_task.context = [research_task, tailor_resume_task]
        
        # --- NEW INTERVIEW TASK ---
        print("Creating interview prep task...")
        interview_task = tasks_class.prepare_interview_task(
            interview_agent,
            "The specific company selected in the Resume Strategy task",
            "The job description identified in the Research task"
        )
        # We link it to the resume task so it knows which job was picked
        interview_task.context = [tailor_resume_task, research_task]
        
        # 4. Create the Crew (Add the new agent and task!)
        print("Assembling crew...")
        crew = Crew(
            agents=[job_researcher, resume_strategist, cover_letter_agent, interview_agent],
            tasks=[research_task, tailor_resume_task, cover_letter_task, interview_task],
            process=Process.sequential,
            verbose=True
        )
        
        # 5. Run the crew
        print("\n🎯 Starting job search process...\n")
        
        result = crew.kickoff()
        
        # Display results in terminal
        print("\n" + "=" * 60)
        print("✅ RESULTS")
        print("=" * 60)
        print(result)
        
        # --- SAVING LOGIC (Updated to include Interview Output) ---
        full_report = f"""
========================================
🚀 FINAL REPORT
========================================

--- 🕵️ JOB RESEARCHER REPORT ---
{research_task.output}

--- 📝 RESUME STRATEGY REPORT ---
{tailor_resume_task.output}

--- ✉️ COVER LETTER ---
{cover_letter_task.output}

--- 🎤 INTERVIEW PREPARATION ---
{interview_task.output}
        """

        # Save to file
        with open("job_search_results.txt", "w", encoding="utf-8") as f:
            f.write(full_report)
            
        print("\n💾 Full Report saved to 'job_search_results.txt'")
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
