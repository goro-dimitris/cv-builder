# ATS-Optimized CV Generator

A Python tool to extract data from LinkedIn PDF exports and generate ATS (Applicant Tracking System) optimized CVs in multiple formats (PDF, HTML, Markdown).

## Features

- **LinkedIn PDF Parsing**: Automatically extracts information from LinkedIn profile PDF exports
- **ATS Optimization**: Applies best practices for ATS compatibility:
  - Expands abbreviations to full terms
  - Normalizes date formats
  - Enhances descriptions with action verbs
  - Ensures keyword-rich content
  - Clean, parseable formatting
- **Multiple Output Formats**: Generates CV in PDF, HTML, and Markdown formats
- **Reusable Template**: Includes a blank template with ATS optimization guidelines

## Installation

1. **Clone or download this repository**

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install system dependencies for PDF generation:**
   
   For macOS:
   ```bash
   brew install cairo pango gdk-pixbuf libffi
   ```
   
   For Ubuntu/Debian:
   ```bash
   sudo apt-get install python3-cffi python3-brotli libpango-1.0-0 libpangoft2-1.0-0
   ```
   
   For Windows:
   - Install GTK+ runtime from: https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer

## Usage

1. **Place your LinkedIn PDF export in the Assets folder:**
   - Rename it to `Profile.pdf`
   - Or update the path in `main.py`

2. **Run the generator:**
   ```bash
   python main.py
   ```

3. **Output files will be generated in the project root:**
   - `cv_ats.html` - HTML source version (use this to generate PDF)
   - `cv_ats.md` - Markdown source version
   - `cv_ats.pdf` - Final ATS-optimized PDF (if PDF generation succeeds)

4. **Generate PDF from HTML (if automatic PDF generation fails):**
   - **Option 1 - Browser (Recommended):** Open `cv_ats.html` in your browser (Chrome, Safari, or Firefox), then:
     - Press `Cmd+P` (Mac) or `Ctrl+P` (Windows/Linux)
     - Select "Save as PDF" as the destination
     - Ensure "Background graphics" is enabled
     - Click "Save"
   - **Option 2 - Command line:** Use `wkhtmltopdf` if installed:
     ```bash
     wkhtmltopdf cv_ats.html cv_ats.pdf
     ```

## Manual Template Usage

If you prefer to create your CV manually, use the `cv_template_blank.md` file as a starting point. It includes:
- Standard CV sections
- ATS optimization tips as comments
- Best practices and guidelines

## ATS Optimization Features

This tool automatically applies the following optimizations:

### 1. Abbreviation Expansion
Common abbreviations are expanded to full terms for better ATS parsing:
- AI → Artificial Intelligence
- ML → Machine Learning
- API → Application Programming Interface
- AWS → Amazon Web Services
- And many more...

### 2. Date Normalization
Dates are normalized to consistent formats (MM/YYYY) for better parsing.

### 3. Action Verbs
Descriptions are enhanced to start with action verbs when appropriate.

### 4. Clean Formatting
- Simple, linear layout (no complex tables)
- Standard section headers
- Consistent spacing and hierarchy
- Standard fonts (Arial, Calibri, Times New Roman)

### 5. Keyword Optimization
- Ensures keyword-rich content
- Maintains natural language flow
- Uses industry-standard terminology

## Customization

### Modify Abbreviations
Edit `config.py` to add or modify abbreviations that should be expanded.

### Adjust Date Format
Change the `DATE_FORMAT` setting in `config.py`:
- `'MM/YYYY'` - 01/2024
- `'Month YYYY'` - January 2024
- `'YYYY-MM'` - 2024-01

### Customize Template
Edit `cv_template.html` to modify the CV layout and styling.

## Troubleshooting

### PDF Generation Fails
If automatic PDF generation fails (common on macOS), you can generate the PDF manually:

**Recommended Method - Browser:**
1. Open `cv_ats.html` in Chrome, Safari, or Firefox
2. Press `Cmd+P` (Mac) or `Ctrl+P` (Windows/Linux)
3. Select "Save as PDF"
4. Enable "Background graphics" in print settings
5. Save as `cv_ats.pdf`

This method produces ATS-compatible PDFs and is often more reliable than WeasyPrint.

**Alternative - Install WeasyPrint dependencies:**
If you want automatic PDF generation, ensure all WeasyPrint dependencies are installed:
```bash
brew install cairo pango gdk-pixbuf libffi glib
pip3 install weasyprint
```

Note: WeasyPrint can be finicky on macOS. The browser method is recommended.

### Parsing Issues
LinkedIn PDF exports can vary in format. If data extraction is incomplete:
1. Review the extracted data in the console output
2. Manually edit the generated Markdown file
3. Re-run the generator or manually convert to PDF

### Missing Information
If some sections are not extracted:
1. Check the original PDF format
2. Manually add missing information to the generated Markdown file
3. The generator will preserve manually added content

## Best Practices for ATS Compatibility

1. **Use Standard Section Headers**
   - Work Experience (not "Professional Experience" or "Employment")
   - Education (not "Academic Background")
   - Skills (not "Core Competencies")

2. **Avoid Complex Formatting**
   - No tables or columns
   - No graphics or images
   - No special characters or symbols

3. **Keyword Optimization**
   - Research job descriptions for target roles
   - Include relevant keywords naturally
   - Use industry-standard terminology

4. **Quantify Achievements**
   - Use numbers, percentages, and metrics
   - Show impact and results

5. **Consistent Formatting**
   - Use the same date format throughout
   - Maintain consistent spacing
   - Use standard fonts

## Testing Your CV

Before submitting, test your CV with ATS analysis tools:
- [Jobscan](https://www.jobscan.co/)
- [Resume Worded](https://resumeworded.com/)
- [VMock](https://www.vmock.com/)

## File Structure

```
ATS Comp/
├── Assets/
│   └── Profile.pdf          # LinkedIn PDF export (input)
├── cv_ats.pdf               # Generated ATS-optimized PDF (output)
├── cv_ats.html              # Generated HTML version (output)
├── cv_ats.md                # Generated Markdown version (output)
├── cv_template.html         # HTML template for CV generation
├── cv_template_blank.md     # Blank template with guidelines
├── config.py                # Configuration and settings
├── extract_linkedin_data.py # PDF parser module
├── generate_ats_cv.py       # CV generator and optimizer
├── main.py                  # Main execution script
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

## License

This project is provided as-is for personal use.

## Contributing

Feel free to customize and adapt this tool for your needs. Suggestions for improvements are welcome!

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the code comments
3. Test with a sample LinkedIn PDF export

---

**Note**: Always review and customize the generated CV before submitting. The tool provides a solid foundation, but personalization is key to standing out to both ATS systems and human recruiters.

