import time
import os
from playwright.sync_api import sync_playwright
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def scrape_radheef():
    words_data = []
    print("Launching browser to scrape Radheef...")
    
    with sync_playwright() as p:
        # Launch browser (headless=False allows you to watch the automation)
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://radheef.mv/")
        
        # Note: Depending on radheef.mv's structure, you will need to adjust selectors 
        # to target the specific list of words, pagination, or search loops.
        # This is a generalized template for crawling dynamic elements.
        
        time.sleep(3) # Wait for initial load
        
        # Example extraction loop (customize selectors based on actual site DOM)
        # items = page.locator(".word-item-class").all()
        # for item in items:
        #     word = item.locator(".word-title").inner_text()
        #     meaning = item.locator(".word-definition").inner_text()
        #     words_data.append((word, meaning))
            
        browser.close()
    
    return words_data

def generate_pdf(data):
    pdf_filename = "radheef_dictionary.pdf"
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
    story = []
    
    styles = getSampleStyleSheet()
    
    # Custom styles (Note: For Dhivehi text rendering in ReportLab, 
    # ensure you register a Unicode-compatible font that supports Thaana script)
    title_style = ParagraphStyle(
        'WordTitle',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=6
    )
    
    body_style = ParagraphStyle(
        'WordMeaning',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=12
    )
    
    # If scraping yields no mock data yet, add a placeholder
    if not data:
        data = [("Sample Word (ބަސް)", "Sample Meaning definition goes here.")]

    for word, meaning in data:
        story.append(Paragraph(f"<b>{word}</b>", title_style))
        story.append(Paragraph(meaning, body_style))
        story.append(Spacer(1, 6))
        
    doc.build(story)
    print(f"PDF successfully generated: {pdf_filename}")

if __name__ == "__main__":
    data = scrape_radheef()
    generate_pdf(data)
