"""
Extract data from LinkedIn PDF export.
Handles parsing and cleaning of LinkedIn profile data.
"""

import pdfplumber
import re
from typing import Dict, List, Optional
from dateutil import parser as date_parser


class LinkedInPDFParser:
    """Parser for LinkedIn PDF exports."""
    
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.raw_text = ""
        self.parsed_data = {}
        
    def extract_text(self) -> str:
        """Extract all text from PDF."""
        text_parts = []
        with pdfplumber.open(self.pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    text_parts.append(text)
        self.raw_text = "\n".join(text_parts)
        return self.raw_text
    
    def parse(self) -> Dict:
        """Parse LinkedIn PDF and extract structured data."""
        if not self.raw_text:
            self.extract_text()
        
        self.parsed_data = {
            'personal_info': self._extract_personal_info(),
            'summary': self._extract_summary(),
            'experience': self._extract_experience(),
            'education': self._extract_education(),
            'skills': self._extract_skills(),
            'certifications': self._extract_certifications(),
            'languages': self._extract_languages(),
            'projects': self._extract_projects()
        }
        
        return self.parsed_data
    
    def _extract_personal_info(self) -> Dict:
        """Extract personal information (name, contact, location)."""
        lines = self.raw_text.split('\n')
        personal_info = {
            'name': '',
            'headline': '',
            'location': '',
            'email': '',
            'phone': '',
            'linkedin': ''
        }
        
        # Name is typically in the first few lines
        if lines:
            personal_info['name'] = lines[0].strip()
        
        # Extract email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_match = re.search(email_pattern, self.raw_text)
        if email_match:
            personal_info['email'] = email_match.group()
        
        # Extract phone
        phone_patterns = [
            r'\+?\d{1,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}',
            r'\+?\d{10,15}'
        ]
        for pattern in phone_patterns:
            phone_match = re.search(pattern, self.raw_text)
            if phone_match:
                personal_info['phone'] = phone_match.group()
                break
        
        # Extract LinkedIn URL
        linkedin_pattern = r'linkedin\.com/in/[\w-]+'
        linkedin_match = re.search(linkedin_pattern, self.raw_text, re.IGNORECASE)
        if linkedin_match:
            personal_info['linkedin'] = 'https://' + linkedin_match.group()
        
        # Extract location (common patterns)
        location_patterns = [
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*),\s*([A-Z]{2}|[A-Z][a-z]+)',
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*),\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)'
        ]
        for pattern in location_patterns:
            location_match = re.search(pattern, self.raw_text)
            if location_match:
                personal_info['location'] = location_match.group()
                break
        
        # Headline is usually near the name
        for i, line in enumerate(lines[:10]):
            if line.strip() and line != personal_info['name']:
                if not personal_info['headline']:
                    personal_info['headline'] = line.strip()
                break
        
        return personal_info
    
    def _extract_summary(self) -> str:
        """Extract professional summary/about section."""
        summary_patterns = [
            r'(?:Summary|About|Profile)[\s:]*\n(.*?)(?=\n(?:Experience|Education|Skills|Work|Employment))',
            r'(?:About|Summary)[\s:]*\n(.*?)(?=\n[A-Z][a-z]+\s+Experience)'
        ]
        
        for pattern in summary_patterns:
            match = re.search(pattern, self.raw_text, re.IGNORECASE | re.DOTALL)
            if match:
                summary = match.group(1).strip()
                # Clean up summary
                summary = re.sub(r'\s+', ' ', summary)
                return summary
        
        return ""
    
    def _extract_experience(self) -> List[Dict]:
        """Extract work experience entries."""
        experience = []
        
        # Look for experience section
        exp_patterns = [
            r'(?:Work\s+)?Experience[\s:]*\n(.*?)(?=\n(?:Education|Skills|Certifications|Languages|Projects|$))',
            r'Employment[\s:]*\n(.*?)(?=\n(?:Education|Skills|Certifications|Languages|Projects|$))'
        ]
        
        exp_text = ""
        for pattern in exp_patterns:
            match = re.search(pattern, self.raw_text, re.IGNORECASE | re.DOTALL)
            if match:
                exp_text = match.group(1)
                break
        
        if not exp_text:
            return experience
        
        # Split by job entries (typically separated by dates or company names)
        # Pattern: Company Name, Title, Date Range, Description
        job_pattern = r'([A-Z][^•\n]+?)\s+([A-Z][^•\n]+?)\s+((?:\d{1,2}[/-])?\d{4}\s*[-–—]\s*(?:Present|Current|(?:\d{1,2}[/-])?\d{4})|(?:\d{1,2}[/-])?\d{4})'
        
        jobs = re.split(r'\n(?=[A-Z][^•\n]{10,})', exp_text)
        
        for job_text in jobs:
            if len(job_text.strip()) < 20:
                continue
            
            # Try to extract company, title, dates
            lines = [l.strip() for l in job_text.split('\n') if l.strip()]
            if len(lines) < 2:
                continue
            
            job_entry = {
                'company': '',
                'title': '',
                'start_date': '',
                'end_date': '',
                'description': []
            }
            
            # First line is usually company or title
            job_entry['company'] = lines[0] if lines else ''
            
            # Look for dates
            date_pattern = r'((?:\d{1,2}[/-])?\d{4})\s*[-–—]\s*(Present|Current|(?:\d{1,2}[/-])?\d{4})'
            date_match = re.search(date_pattern, job_text)
            if date_match:
                job_entry['start_date'] = date_match.group(1)
                job_entry['end_date'] = date_match.group(2)
            
            # Title might be on second line or before dates
            if len(lines) > 1:
                potential_title = lines[1]
                if not re.search(date_pattern, potential_title):
                    job_entry['title'] = potential_title
            
            # Description is everything else
            description_start = 2
            if date_match:
                # Find where description starts
                for i, line in enumerate(lines):
                    if date_match.group() in line:
                        description_start = i + 1
                        break
            
            job_entry['description'] = [l for l in lines[description_start:] if l and not re.match(r'^[\d\s\-•]+$', l)]
            
            if job_entry['company'] or job_entry['title']:
                experience.append(job_entry)
        
        return experience
    
    def _extract_education(self) -> List[Dict]:
        """Extract education entries."""
        education = []
        
        edu_patterns = [
            r'Education[\s:]*\n(.*?)(?=\n(?:Skills|Certifications|Languages|Projects|Experience|$))',
            r'Academic[\s:]*\n(.*?)(?=\n(?:Skills|Certifications|Languages|Projects|Experience|$))'
        ]
        
        edu_text = ""
        for pattern in edu_patterns:
            match = re.search(pattern, self.raw_text, re.IGNORECASE | re.DOTALL)
            if match:
                edu_text = match.group(1)
                break
        
        if not edu_text:
            return education
        
        # Split education entries
        entries = re.split(r'\n(?=[A-Z][^•\n]{10,})', edu_text)
        
        for entry_text in entries:
            if len(entry_text.strip()) < 10:
                continue
            
            lines = [l.strip() for l in entry_text.split('\n') if l.strip()]
            if not lines:
                continue
            
            edu_entry = {
                'institution': '',
                'degree': '',
                'field': '',
                'dates': '',
                'description': []
            }
            
            edu_entry['institution'] = lines[0] if lines else ''
            
            # Look for degree and dates
            if len(lines) > 1:
                edu_entry['degree'] = lines[1]
            
            date_pattern = r'((?:\d{1,2}[/-])?\d{4})\s*[-–—]\s*(?:(?:\d{1,2}[/-])?\d{4})?'
            date_match = re.search(date_pattern, entry_text)
            if date_match:
                edu_entry['dates'] = date_match.group()
            
            if edu_entry['institution']:
                education.append(edu_entry)
        
        return education
    
    def _extract_skills(self) -> List[str]:
        """Extract skills list."""
        skills = []
        
        skills_patterns = [
            r'Skills?[\s:]*\n(.*?)(?=\n(?:Certifications|Languages|Projects|Education|Experience|$))',
            r'Technical\s+Skills?[\s:]*\n(.*?)(?=\n(?:Certifications|Languages|Projects|Education|Experience|$))'
        ]
        
        skills_text = ""
        for pattern in skills_patterns:
            match = re.search(pattern, self.raw_text, re.IGNORECASE | re.DOTALL)
            if match:
                skills_text = match.group(1)
                break
        
        if not skills_text:
            return skills
        
        # Extract skills (comma-separated, bullet points, or line-separated)
        skill_items = re.split(r'[,•\n]', skills_text)
        skills = [s.strip() for s in skill_items if s.strip() and len(s.strip()) > 2]
        
        # Remove duplicates while preserving order
        seen = set()
        unique_skills = []
        for skill in skills:
            skill_lower = skill.lower()
            if skill_lower not in seen:
                seen.add(skill_lower)
                unique_skills.append(skill)
        
        return unique_skills
    
    def _extract_certifications(self) -> List[Dict]:
        """Extract certifications."""
        certifications = []
        
        cert_patterns = [
            r'Certifications?[\s:]*\n(.*?)(?=\n(?:Languages|Projects|Skills|Education|Experience|$))',
            r'Certificates?[\s:]*\n(.*?)(?=\n(?:Languages|Projects|Skills|Education|Experience|$))'
        ]
        
        cert_text = ""
        for pattern in cert_patterns:
            match = re.search(pattern, self.raw_text, re.IGNORECASE | re.DOTALL)
            if match:
                cert_text = match.group(1)
                break
        
        if not cert_text:
            return certifications
        
        entries = re.split(r'\n(?=[A-Z])', cert_text)
        for entry in entries:
            if len(entry.strip()) < 5:
                continue
            cert_entry = {
                'name': entry.strip(),
                'issuer': '',
                'date': ''
            }
            certifications.append(cert_entry)
        
        return certifications
    
    def _extract_languages(self) -> List[str]:
        """Extract languages."""
        languages = []
        
        lang_patterns = [
            r'Languages?[\s:]*\n(.*?)(?=\n(?:Projects|Skills|Certifications|Education|Experience|$))'
        ]
        
        lang_text = ""
        for pattern in lang_patterns:
            match = re.search(pattern, self.raw_text, re.IGNORECASE | re.DOTALL)
            if match:
                lang_text = match.group(1)
                break
        
        if not lang_text:
            return languages
        
        lang_items = re.split(r'[,•\n]', lang_text)
        languages = [l.strip() for l in lang_items if l.strip()]
        
        return languages
    
    def _extract_projects(self) -> List[Dict]:
        """Extract projects."""
        projects = []
        
        proj_patterns = [
            r'Projects?[\s:]*\n(.*?)(?=\n(?:Skills|Certifications|Languages|Education|Experience|$))'
        ]
        
        proj_text = ""
        for pattern in proj_patterns:
            match = re.search(pattern, self.raw_text, re.IGNORECASE | re.DOTALL)
            if match:
                proj_text = match.group(1)
                break
        
        if not proj_text:
            return projects
        
        entries = re.split(r'\n(?=[A-Z])', proj_text)
        for entry in entries:
            if len(entry.strip()) < 10:
                continue
            proj_entry = {
                'name': '',
                'description': entry.strip()
            }
            # Try to extract project name from first line
            lines = entry.split('\n')
            if lines:
                proj_entry['name'] = lines[0].strip()
            projects.append(proj_entry)
        
        return projects

