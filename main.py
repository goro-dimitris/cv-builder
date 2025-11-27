#!/usr/bin/env python3
"""
Main script to extract LinkedIn data and generate ATS-optimized CV.
"""

import os
import sys
from pathlib import Path
from extract_linkedin_data import LinkedInPDFParser
from generate_ats_cv import ATSOptimizer, CVGenerator


def main():
    """Main execution function."""
    # Default paths
    assets_dir = Path(__file__).parent / 'Assets'
    pdf_path = assets_dir / 'Profile.pdf'
    output_dir = Path(__file__).parent
    
    # Check if PDF exists
    if not pdf_path.exists():
        print(f"Error: LinkedIn PDF not found at {pdf_path}")
        print("Please ensure Profile.pdf is in the Assets directory.")
        sys.exit(1)
    
    print("=" * 60)
    print("ATS-Optimized CV Generator")
    print("=" * 60)
    print()
    
    # Step 1: Extract data from LinkedIn PDF
    print("Step 1: Extracting data from LinkedIn PDF...")
    try:
        parser = LinkedInPDFParser(str(pdf_path))
        raw_data = parser.parse()
        print(f"✓ Successfully extracted data from PDF")
        print(f"  - Found {len(raw_data.get('experience', []))} work experience entries")
        print(f"  - Found {len(raw_data.get('education', []))} education entries")
        print(f"  - Found {len(raw_data.get('skills', []))} skills")
    except Exception as e:
        print(f"✗ Error extracting data: {str(e)}")
        sys.exit(1)
    
    print()
    
    # Step 2: Optimize data for ATS
    print("Step 2: Optimizing data for ATS compatibility...")
    try:
        optimizer = ATSOptimizer(raw_data)
        optimized_data = optimizer.optimize()
        print("✓ Data optimized for ATS")
        print("  - Expanded abbreviations")
        print("  - Normalized dates and formatting")
        print("  - Enhanced descriptions with action verbs")
    except Exception as e:
        print(f"✗ Error optimizing data: {str(e)}")
        sys.exit(1)
    
    print()
    
    # Step 3: Generate CV in multiple formats
    print("Step 3: Generating CV outputs...")
    generator = CVGenerator(optimized_data)
    
    # Generate Markdown
    try:
        md_path = output_dir / 'cv_ats.md'
        generator.save_markdown(str(md_path))
        print(f"✓ Generated Markdown: {md_path}")
    except Exception as e:
        print(f"✗ Error generating Markdown: {str(e)}")
    
    # Generate HTML
    try:
        html_path = output_dir / 'cv_ats.html'
        template_path = output_dir / 'cv_template.html'
        generator.save_html(str(html_path), str(template_path))
        print(f"✓ Generated HTML: {html_path}")
    except Exception as e:
        print(f"✗ Error generating HTML: {str(e)}")
    
    # Generate PDF
    try:
        pdf_output_path = output_dir / 'cv_ats.pdf'
        template_path = output_dir / 'cv_template.html'
        generator.save_pdf(str(pdf_output_path), str(template_path))
        print(f"✓ Generated PDF: {pdf_output_path}")
    except Exception as e:
        print(f"✗ Error generating PDF: {str(e)}")
        print("  Note: PDF generation requires WeasyPrint. Install with: pip install weasyprint")
    
    print()
    print("=" * 60)
    print("CV Generation Complete!")
    print("=" * 60)
    print()
    print("Output files:")
    print(f"  - cv_ats.md (Markdown source)")
    print(f"  - cv_ats.html (HTML source)")
    print(f"  - cv_ats.pdf (Final ATS-optimized PDF)")
    print()
    print("Review the generated files and customize as needed.")
    print("The PDF is optimized for modern ATS systems.")


if __name__ == '__main__':
    main()

