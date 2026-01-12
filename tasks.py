from crewai import Task

class JobApplicationTasks:
    
    def research_jobs_task(self, agent, job_criteria):
        return Task(
            description=f"""
            Search for job opportunities based on these criteria:
            - Role/Position: {job_criteria.get('role', 'Software Developer')}
            - Location: {job_criteria.get('location', 'Remote')}
            - Experience Level: {job_criteria.get('experience', 'Mid-level')}
            - Keywords: {job_criteria.get('keywords', 'Python, AI')}
            
            Find at least 3-5 relevant job postings with:
            - Company name
            - Job title
            - Key requirements
            - Application link or contact info
            - Salary range (if available)
            """,
            agent=agent,
            expected_output="A detailed list of 3-5 job opportunities with complete information for each posting"
        )
    
    def tailor_resume_task(self, agent, job_description, current_resume):
        return Task(
            description=f"""
            Analyze this job description and provide specific suggestions for tailoring the resume:
            
            Job Description:
            {job_description}
            
            Current Resume Summary:
            {current_resume}
            
            Provide:
            1. Key skills from the job description to emphasize
            2. Specific achievements or experiences to highlight
            3. Keywords to include for ATS systems
            4. Suggested resume summary/objective
            5. Any certifications or skills to add prominence to
            """,
            agent=agent,
            expected_output="Detailed resume tailoring recommendations with specific sections and keywords to emphasize"
        )
    
    def write_cover_letter_task(self, agent, job_info, candidate_info):
        return Task(
            description=f"""
            Write a compelling cover letter for this position:
            
            Job Information:
            {job_info}
            
            Candidate Background:
            {candidate_info}
            
            The cover letter should:
            - Be 3-4 paragraphs
            - Show genuine interest in the company and role
            - Highlight relevant experience and skills
            - Demonstrate cultural fit
            - Include a strong call to action
            - Be professional yet personable
            """,
            agent=agent,
            expected_output="A complete, professional cover letter ready to be customized with specific names and details"
        )
    
    def track_applications_task(self, agent, applications_data):
        return Task(
            description=f"""
            Organize all job application information:
            
            Applications:
            {applications_data}
            
            Create a tracking system that includes:
            1. Company name and position
            2. Application date
            3. Application status
            4. Follow-up dates
            5. Interview dates (if scheduled)
            6. Notes and next steps
            
            Present this in a clear, structured format.
            """,
            agent=agent,
            expected_output="An organized table or structured format tracking all applications with dates and status"
        )
    
    def prepare_interview_task(self, agent, company_name, job_description):
        return Task(
            description=f"""
            Prepare comprehensive interview materials for:
            
            Company: {company_name}
            Job Description: {job_description}
            
            Provide:
            1. Company background and recent news
            2. 10 likely interview questions specific to this role
            3. Suggested answers with the STAR method
            4. Questions to ask the interviewer
            5. Key points to emphasize about your background
            """,
            agent=agent,
            expected_output="Complete interview preparation guide with company research, questions, answers, and strategy"
        )
