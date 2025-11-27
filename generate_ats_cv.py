"""
Generate ATS-optimized CV from extracted LinkedIn data.
Applies optimizations and generates multiple output formats.
"""

import re
from typing import Dict, List
from jinja2 import Template
import config


class ATSOptimizer:
    """Apply ATS optimization rules to CV data."""
    
    def __init__(self, data: Dict):
        self.data = data
        self.optimized_data = {}
    
    def optimize(self) -> Dict:
        """Apply all ATS optimizations."""
        self.optimized_data = {
            'personal_info': self._optimize_personal_info(),
            'summary': self._optimize_summary(),
            'experience': self._optimize_experience(),
            'education': self._optimize_education(),
            'skills': self._optimize_skills(),
            'certifications': self._optimize_certifications(),
            'languages': self.data.get('languages', []),
            'projects': self._optimize_projects()
        }
        return self.optimized_data
    
    def _optimize_personal_info(self) -> Dict:
        """Optimize personal information."""
        personal_info = self.data.get('personal_info', {}).copy()
        # Ensure all fields are properly formatted
        if 'name' in personal_info:
            personal_info['name'] = personal_info['name'].strip().title()
        return personal_info
    
    def _optimize_summary(self) -> str:
        """Optimize professional summary."""
        summary = self.data.get('summary', '')
        if not summary:
            # Try to use headline if summary is missing
            headline = self.data.get('personal_info', {}).get('headline', '')
            if headline:
                summary = headline
        
        # Expand abbreviations
        summary = self._expand_abbreviations(summary)
        
        # Ensure proper capitalization and spacing
        summary = re.sub(r'\s+', ' ', summary).strip()
        
        # Ensure it starts with a capital letter
        if summary and not summary[0].isupper():
            summary = summary[0].upper() + summary[1:]
        
        return summary
    
    def _optimize_experience(self) -> List[Dict]:
        """Optimize work experience entries."""
        experience = self.data.get('experience', [])
        optimized = []
        
        for job in experience:
            optimized_job = {
                'company': self._clean_text(job.get('company', '')),
                'title': self._clean_text(job.get('title', '')),
                'start_date': self._normalize_date(job.get('start_date', '')),
                'end_date': self._normalize_date(job.get('end_date', '')),
                'description': []
            }
            
            # Optimize description bullets
            descriptions = job.get('description', [])
            for desc in descriptions:
                optimized_desc = self._optimize_description(desc)
                if optimized_desc:
                    optimized_job['description'].append(optimized_desc)
            
            if optimized_job['company'] or optimized_job['title']:
                optimized.append(optimized_job)
        
        return optimized
    
    def _optimize_education(self) -> List[Dict]:
        """Optimize education entries."""
        education = self.data.get('education', [])
        optimized = []
        
        for edu in education:
            optimized_edu = {
                'institution': self._clean_text(edu.get('institution', '')),
                'degree': self._clean_text(edu.get('degree', '')),
                'field': self._clean_text(edu.get('field', '')),
                'dates': self._normalize_date_range(edu.get('dates', '')),
                'description': edu.get('description', [])
            }
            
            if optimized_edu['institution']:
                optimized.append(optimized_edu)
        
        return optimized
    
    def _optimize_skills(self) -> List[str]:
        """Optimize skills list."""
        skills = self.data.get('skills', [])
        optimized_skills = []
        
        for skill in skills:
            # Clean and expand abbreviations
            cleaned_skill = self._clean_text(skill)
            expanded_skill = self._expand_abbreviations(cleaned_skill)
            
            # Capitalize properly
            expanded_skill = expanded_skill.title()
            
            if expanded_skill and expanded_skill not in optimized_skills:
                optimized_skills.append(expanded_skill)
        
        # Sort skills alphabetically for consistency
        optimized_skills.sort()
        
        return optimized_skills
    
    def _optimize_certifications(self) -> List[Dict]:
        """Optimize certifications."""
        certifications = self.data.get('certifications', [])
        optimized = []
        
        for cert in certifications:
            optimized_cert = {
                'name': self._clean_text(cert.get('name', '')),
                'issuer': self._clean_text(cert.get('issuer', '')),
                'date': self._normalize_date(cert.get('date', ''))
            }
            
            if optimized_cert['name']:
                optimized.append(optimized_cert)
        
        return optimized
    
    def _optimize_projects(self) -> List[Dict]:
        """Optimize projects."""
        projects = self.data.get('projects', [])
        optimized = []
        
        for project in projects:
            optimized_project = {
                'name': self._clean_text(project.get('name', '')),
                'description': self._optimize_description(project.get('description', ''))
            }
            
            if optimized_project['name'] or optimized_project['description']:
                optimized.append(optimized_project)
        
        return optimized
    
    def _optimize_description(self, text: str) -> str:
        """Optimize a description bullet point."""
        if not text:
            return ""
        
        # Expand abbreviations
        text = self._expand_abbreviations(text)
        
        # Clean whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Ensure it starts with an action verb if possible
        text = self._ensure_action_verb(text)
        
        # Capitalize first letter
        if text and not text[0].isupper():
            text = text[0].upper() + text[1:]
        
        # Ensure it ends with proper punctuation
        if text and not text[-1] in '.!?':
            text = text + '.'
        
        return text
    
    def _expand_abbreviations(self, text: str) -> str:
        """Expand common abbreviations for ATS compatibility."""
        if not text:
            return text
        
        # Create a case-insensitive replacement
        text_lower = text.lower()
        for abbrev, expansion in config.ABBREVIATIONS.items():
            # Match whole word boundaries
            pattern = r'\b' + re.escape(abbrev) + r'\b'
            if re.search(pattern, text_lower, re.IGNORECASE):
                # Replace with expansion, preserving original case
                text = re.sub(pattern, expansion, text, flags=re.IGNORECASE)
        
        return text
    
    def _ensure_action_verb(self, text: str) -> str:
        """Ensure description starts with an action verb if appropriate."""
        if not text:
            return text
        
        # Check if it already starts with an action verb
        first_word = text.split()[0] if text.split() else ""
        if first_word in config.ACTION_VERBS:
            return text
        
        # Don't force action verbs if the text doesn't naturally support it
        # (e.g., "Responsible for..." is fine)
        return text
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text."""
        if not text:
            return ""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Remove special characters that might confuse ATS
        text = re.sub(r'[^\w\s\-.,()&/]', '', text)
        
        return text
    
    def _normalize_date(self, date_str: str) -> str:
        """Normalize date format for ATS compatibility."""
        if not date_str:
            return ""
        
        # Clean the date string
        date_str = date_str.strip()
        
        # Handle "Present" or "Current"
        if date_str.lower() in ['present', 'current', 'now']:
            return 'Present'
        
        # Try to parse and format dates
        # For now, return as-is if it looks like a date
        # Format: MM/YYYY or Month YYYY
        date_patterns = [
            r'(\d{1,2})[/-](\d{4})',  # MM/YYYY or M/YYYY
            r'(\d{4})',  # YYYY
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, date_str)
            if match:
                if len(match.groups()) == 2:
                    month, year = match.groups()
                    return f"{month.zfill(2)}/{year}"
                elif len(match.groups()) == 1:
                    return match.group(1)
        
        return date_str
    
    def _normalize_date_range(self, date_str: str) -> str:
        """Normalize date range format."""
        if not date_str:
            return ""
        
        # Look for date ranges
        range_pattern = r'((?:\d{1,2}[/-])?\d{4})\s*[-–—]\s*((?:\d{1,2}[/-])?\d{4}|Present|Current)'
        match = re.search(range_pattern, date_str, re.IGNORECASE)
        
        if match:
            start = self._normalize_date(match.group(1))
            end = self._normalize_date(match.group(2))
            return f"{start} - {end}"
        
        return self._normalize_date(date_str)


class CVGenerator:
    """Generate CV in multiple formats."""
    
    def __init__(self, optimized_data: Dict):
        self.data = optimized_data
    
    def generate_html(self, template_path: str = 'cv_template.html') -> str:
        """Generate HTML version of CV."""
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        template = Template(template_content)
        html = template.render(
            personal_info=self.data['personal_info'],
            summary=self.data['summary'],
            experience=self.data['experience'],
            education=self.data['education'],
            skills=self.data['skills'],
            certifications=self.data['certifications'],
            languages=self.data['languages'],
            projects=self.data['projects']
        )
        
        return html
    
    def generate_markdown(self) -> str:
        """Generate Markdown version of CV."""
        md_parts = []
        
        # Header
        personal_info = self.data['personal_info']
        md_parts.append(f"# {personal_info.get('name', 'CV')}\n")
        
        # Contact info
        contact = []
        if personal_info.get('email'):
            contact.append(personal_info['email'])
        if personal_info.get('phone'):
            contact.append(personal_info['phone'])
        if personal_info.get('location'):
            contact.append(personal_info['location'])
        if personal_info.get('linkedin'):
            contact.append(personal_info['linkedin'])
        
        if contact:
            md_parts.append(" | ".join(contact))
            md_parts.append("")
        
        # Summary
        if self.data.get('summary'):
            md_parts.append("## Professional Summary\n")
            md_parts.append(self.data['summary'])
            md_parts.append("")
        
        # Experience
        if self.data.get('experience'):
            md_parts.append("## Work Experience\n")
            for job in self.data['experience']:
                md_parts.append(f"### {job.get('title', '')}")
                md_parts.append(f"**{job.get('company', '')}**")
                if job.get('start_date') or job.get('end_date'):
                    date_range = f"{job.get('start_date', '')} - {job.get('end_date', '')}"
                    md_parts.append(f"*{date_range}*")
                md_parts.append("")
                if job.get('description'):
                    for desc in job['description']:
                        md_parts.append(f"- {desc}")
                md_parts.append("")
        
        # Education
        if self.data.get('education'):
            md_parts.append("## Education\n")
            for edu in self.data['education']:
                degree_parts = []
                if edu.get('degree'):
                    degree_parts.append(edu['degree'])
                if edu.get('field'):
                    degree_parts.append(edu['field'])
                degree_str = " in ".join(degree_parts) if len(degree_parts) > 1 else degree_parts[0] if degree_parts else ""
                
                md_parts.append(f"### {degree_str}")
                md_parts.append(f"**{edu.get('institution', '')}**")
                if edu.get('dates'):
                    md_parts.append(f"*{edu['dates']}*")
                md_parts.append("")
        
        # Skills
        if self.data.get('skills'):
            md_parts.append("## Skills\n")
            skills_str = ", ".join(self.data['skills'])
            md_parts.append(skills_str)
            md_parts.append("")
        
        # Certifications
        if self.data.get('certifications'):
            md_parts.append("## Certifications\n")
            for cert in self.data['certifications']:
                md_parts.append(f"- **{cert.get('name', '')}**")
                if cert.get('issuer'):
                    md_parts.append(f"  - {cert['issuer']}")
                if cert.get('date'):
                    md_parts.append(f"  - {cert['date']}")
                md_parts.append("")
        
        # Languages
        if self.data.get('languages'):
            md_parts.append("## Languages\n")
            languages_str = ", ".join(self.data['languages'])
            md_parts.append(languages_str)
            md_parts.append("")
        
        # Projects
        if self.data.get('projects'):
            md_parts.append("## Projects\n")
            for project in self.data['projects']:
                if project.get('name'):
                    md_parts.append(f"### {project['name']}")
                if project.get('description'):
                    md_parts.append(project['description'])
                md_parts.append("")
        
        return "\n".join(md_parts)
    
    def save_html(self, output_path: str, template_path: str = 'cv_template.html'):
        """Save HTML version to file."""
        html = self.generate_html(template_path)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
    
    def save_markdown(self, output_path: str):
        """Save Markdown version to file."""
        md = self.generate_markdown()
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(md)
    
    def save_pdf(self, output_path: str, template_path: str = 'cv_template.html'):
        """Save PDF version using WeasyPrint."""
        try:
            from weasyprint import HTML, CSS
            from weasyprint.text.fonts import FontConfiguration
            
            html_content = self.generate_html(template_path)
            html_doc = HTML(string=html_content)
            
            # Generate PDF
            html_doc.write_pdf(output_path)
        except ImportError:
            raise ImportError("WeasyPrint is required for PDF generation. Install it with: pip install weasyprint")
        except Exception as e:
            raise Exception(f"Error generating PDF: {str(e)}")

