from crewai import Task

class JobApplicationTasks:
    
    def research_jobs_task(self, agent, job_criteria):
        return Task(
            description=f"""
            Search for job opportunities based on these criteria:
            - Role: {job_criteria.get('role')}
            - Location: {job_criteria.get('location')}
            - Experience: {job_criteria.get('experience')}
            - Keywords: {job_criteria.get('keywords')}
            
            Find at least 3-5 relevant job postings.
            """,
            agent=agent,
            expected_output="A list of 3-5 job opportunities with requirements and links."
        )

    def tailor_resume_task(self, agent, current_resume):
        return Task(
            description=f"""
            Analyze the job postings provided by the Job Research Specialist (previous task). 
            Select the single best matching job from that list.
            
            Then, tailor this resume for that specific job:
            Resume Summary: {current_resume}
            """,
            agent=agent,
            expected_output="A tailored resume strategy and keywords."
        )
    
    def write_cover_letter_task(self, agent, candidate_info):
        return Task(
            description=f"""
            Using the job description found by the Researcher and the resume strategy from the Strategist,
            write a compelling cover letter.
            
            Candidate Info: {candidate_info}
            """,
            agent=agent,
            expected_output="A professional 3-4 paragraph cover letter."
        )
    
    def prepare_interview_task(self, agent, company_name, job_description):
        return Task(
            description=f"""
            Look at the "Resume Strategy" from the previous task to identify the target company and job.
            
            Prepare comprehensive interview materials for:
            Target: {company_name}
            Context: {job_description}
            
            Provide:
            1. Company background and recent news (use Search Tools)
            2. 10 likely interview questions specific to this role
            3. Suggested answers with the STAR method
            4. Questions to ask the interviewer
            """,
            agent=agent,
            expected_output="Complete interview preparation guide with company research, questions, answers, and strategy"
        )
