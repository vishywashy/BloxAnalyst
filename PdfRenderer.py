import os
from jinja2 import Template
from weasyprint import HTML
def Render(title, tags, analyst_name, report_date, top_image_path, analysis_text):
    print(top_image_path)
# Setup workspace directories
    os.makedirs('temp', exist_ok=True)
    os.makedirs('generated', exist_ok=True)

# 1. Point directly to your two separate local file names
    

# 2. Build the list matching your adaptive HTML loop setup
    

# ==============================================================================
# JINJA DATA MAPPING PAYLOAD
# ==============================================================================
    report_payload = {
    "report_title": title,
    "report_tags": tags,
    "analyst_name":analyst_name,
    "report_date": report_date,
    "top_image_path":top_image_path,
    "analysis_text": analysis_text,
    
    # 🎯 Your exact list works perfectly now
    "graphs": [
        'RAPValueGraph.png', 'VolumeValueGraph.png'
    
    ],
    "data":[f"This graph displays the RAP of the {top_image_path.removesuffix(".png")} in robux", f"This graph displays the market demand of the {top_image_path.removesuffix(".png")} item"]
}


# ==============================================================================
# COMPILATION
# ==============================================================================
    with open('template.html', 'r', encoding='utf-8') as html_file:
        raw_template_string = html_file.read()

    compiled_html_output = Template(raw_template_string).render(report_payload)

    rendered_file_path = 'temp/final_rendered_output.html'
    with open(rendered_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(compiled_html_output)

# base_url="." points the engine directory path context directly to your local workspace files
    HTML(rendered_file_path, base_url=".").write_pdf('generated/final_analyst_report.pdf')
    return "Successfully generated unique charts via list tracking!"

