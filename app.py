from flask import Flask, render_template, request, jsonify, send_file
from crewai import Crew, Process
from agents import JobApplicationAgents
from tasks import JobApplicationTasks
from dotenv import load_dotenv
import os
import time

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Set secret key for Flask
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'}), 200

@app.route('/search-jobs', methods=['POST'])
def search_jobs():
    try:
        # Get form data
        data = request.json
        role = data.get('role', 'Software Developer')
        location = data.get('location', 'Remote')
        experience = data.get('experience', 'Entry')
        keywords = data.get('keywords', 'Python, AI')
        
        job_criteria = {
            'role': role,
            'location': location,
            'experience': experience,
            'keywords': keywords
        }
        
        # Initialize agents and tasks
        agents = JobApplicationAgents()
        tasks = JobApplicationTasks()
        
        # Create agents
        job_researcher = agents.job_researcher_agent()
        resume_strategist = agents.resume_strategist_agent()
        
        # Create tasks
        research_task = tasks.research_jobs_task(job_researcher, job_criteria)
        
        demo_job_description = f"Looking for a {role} with skills in {keywords}"
        demo_resume = f"{experience} level professional with relevant experience"
        
        tailor_resume_task = tasks.tailor_resume_task(
            resume_strategist,
            demo_job_description,
            demo_resume
        )
        
        # Create and run crew
        crew = Crew(
            agents=[job_researcher, resume_strategist],
            tasks=[research_task, tailor_resume_task],
            process=Process.sequential,
            verbose=False
        )
        
        # Run with rate limit handling
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                result = crew.kickoff()
                break
            except Exception as e:
                if "rate_limit" in str(e).lower():
                    retry_count += 1
                    if retry_count < max_retries:
                        time.sleep(15)
                        continue
                    else:
                        return jsonify({
                            'success': False,
                            'error': 'Rate limit exceeded. Please try again in a minute.'
                        }), 429
                else:
                    raise
        
        # Save results to file in /tmp (Render's writable directory)
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f"results_{timestamp}.txt"
        filepath = os.path.join('/tmp', filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(str(result))
        
        return jsonify({
            'success': True,
            'result': str(result),
            'filename': filename
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/download/<filename>')
def download_file(filename):
    try:
        filepath = os.path.join('/tmp', filename)
        return send_file(filepath, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)