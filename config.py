"""
Configuration file for ATS CV optimization settings.
"""

# Standard section headers for ATS compatibility
SECTION_HEADERS = {
    'summary': ['Professional Summary', 'Summary', 'Profile', 'About'],
    'experience': ['Work Experience', 'Experience', 'Employment History', 'Professional Experience'],
    'education': ['Education', 'Academic Background', 'Qualifications'],
    'skills': ['Skills', 'Technical Skills', 'Core Competencies', 'Expertise'],
    'certifications': ['Certifications', 'Certificates', 'Professional Certifications'],
    'languages': ['Languages', 'Language Skills'],
    'projects': ['Projects', 'Key Projects', 'Notable Projects']
}

# Common abbreviations to expand for ATS optimization
ABBREVIATIONS = {
    'AI': 'Artificial Intelligence',
    'ML': 'Machine Learning',
    'API': 'Application Programming Interface',
    'AWS': 'Amazon Web Services',
    'CI/CD': 'Continuous Integration/Continuous Deployment',
    'SQL': 'Structured Query Language',
    'UI/UX': 'User Interface/User Experience',
    'CRM': 'Customer Relationship Management',
    'ERP': 'Enterprise Resource Planning',
    'SaaS': 'Software as a Service',
    'REST': 'Representational State Transfer',
    'JSON': 'JavaScript Object Notation',
    'XML': 'Extensible Markup Language',
    'HTML': 'HyperText Markup Language',
    'CSS': 'Cascading Style Sheets',
    'JS': 'JavaScript',
    'TS': 'TypeScript',
    'HTTP': 'HyperText Transfer Protocol',
    'HTTPS': 'HyperText Transfer Protocol Secure',
    'VPN': 'Virtual Private Network',
    'IoT': 'Internet of Things',
    'DevOps': 'Development Operations',
    'QA': 'Quality Assurance',
    'TDD': 'Test-Driven Development',
    'Agile': 'Agile Methodology',
    'Scrum': 'Scrum Framework'
}

# Action verbs for achievements (ATS-friendly)
ACTION_VERBS = [
    'Achieved', 'Implemented', 'Developed', 'Designed', 'Managed', 'Led',
    'Created', 'Built', 'Improved', 'Optimized', 'Increased', 'Reduced',
    'Delivered', 'Executed', 'Launched', 'Established', 'Collaborated',
    'Coordinated', 'Streamlined', 'Enhanced', 'Transformed', 'Automated',
    'Analyzed', 'Resolved', 'Maintained', 'Supported', 'Trained', 'Mentored'
]

# Date format preferences for ATS
DATE_FORMAT = 'MM/YYYY'  # Options: 'MM/YYYY', 'Month YYYY', 'YYYY-MM'

# Font preferences for ATS compatibility
ATS_FONTS = ['Arial', 'Calibri', 'Times New Roman', 'Helvetica', 'Georgia']

# Industry-specific keywords (can be customized)
INDUSTRY_KEYWORDS = {
    'general': [
        'project management', 'team leadership', 'problem solving',
        'communication', 'collaboration', 'analytical thinking',
        'strategic planning', 'process improvement', 'quality assurance'
    ],
    'tech': [
        'software development', 'programming', 'system architecture',
        'cloud computing', 'database management', 'version control',
        'code review', 'testing', 'debugging', 'deployment'
    ],
    'data': [
        'data analysis', 'data visualization', 'statistical modeling',
        'machine learning', 'data mining', 'predictive analytics',
        'ETL', 'data warehousing', 'business intelligence'
    ]
}

