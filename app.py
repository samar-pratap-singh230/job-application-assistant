from flask import Flask, render_template, request, jsonify, send_file
from crewai import Crew, Process
from agents import JobApplicationAgents
from tasks import JobApplicationTasks
from dotenv import load_dotenv
import os
import time

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'secret-key')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search-jobs', methods=['POST'])
def search_jobs():
    try:
        data = request.json
        
        job_criteria = {
            'role': data.get('role', 'Software Developer'),
            'location': data.get('location', 'Remote'),
            'experience': data.get('experience', 'Mid'),
            'keywords': data.get('keywords', 'Python')
        }
        
        agents_class = JobApplicationAgents()
        tasks_class = JobApplicationTasks()

        # Create Agents (Added Interview Agent)
        researcher = agents_class.job_researcher_agent()
        strategist = agents_class.resume_strategist_agent()
        writer = agents_class.cover_letter_writer_agent()
        interview_agent = agents_class.interview_prep_agent() # NEW

        # Create Tasks
        task_research = tasks_class.research_jobs_task(researcher, job_criteria)

        task_resume = tasks_class.tailor_resume_task(
            strategist, 
            f"Candidate with {job_criteria['experience']} experience"
        )
        task_resume.context = [task_research]

        task_letter = tasks_class.write_cover_letter_task(
            writer,
            f"Candidate with {job_criteria['experience']} experience"
        )
        task_letter.context = [task_research, task_resume]

        # NEW: Interview Task
        task_interview = tasks_class.prepare_interview_task(
            interview_agent,
            "The specific company selected in the Resume Strategy task",
            "The job description identified in the Research task"
        )
        task_interview.context = [task_resume, task_research]

        # Create Crew (Added new agent/task)
        crew = Crew(
            agents=[researcher, strategist, writer, interview_agent],
            tasks=[task_research, task_resume, task_letter, task_interview],
            process=Process.sequential,
            verbose=True
        )
        
        result = crew.kickoff()
        
        # Save to file (Updated Report Format)
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f"results_{timestamp}.txt"
        save_path = os.path.join('static', filename) if os.path.exists('static') else filename
        
        full_report = f"""
========================================
FINAL REPORT
========================================

--- (1) JOB RESEARCHER REPORT ---
{task_research.output}

--- (2) RESUME STRATEGY REPORT ---
{task_resume.output}

--- (3) COVER LETTER ---
{task_letter.output}

--- (4) INTERVIEW PREPARATION ---
{task_interview.output}
        """
        
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(full_report)
        
        # Return the full report to the web UI
        return jsonify({'success': True, 'result': full_report, 'filename': filename})
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/download/<filename>')
def download_file(filename):
    path = os.path.join('static', filename) if os.path.exists('static') else filename
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    app.run(port=5000, debug=True)


