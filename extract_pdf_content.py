#!/usr/bin/env python3
"""
Extract content from JUDGMENT.pdf and create pdf_content.json
"""

import json
import pdfplumber
from datetime import datetime
from pathlib import Path

def extract_pdf_content(pdf_path, output_path):
    """Extract text content from PDF and save to JSON"""
    
    print(f"📄 Opening PDF: {pdf_path}")
    
    pages_data = []
    total_words = 0
    total_characters = 0
    
    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        print(f"📊 Total pages: {total_pages}")
        
        for page_num, page in enumerate(pdf.pages, start=1):
            if page_num % 100 == 0:
                print(f"   Processing page {page_num}/{total_pages}...")
            
            # Extract text
            text = page.extract_text() or ""
            
            # Calculate metrics
            word_count = len(text.split())
            char_count = len(text)
            
            total_words += word_count
            total_characters += char_count
            
            # Create page entry
            page_data = {
                "page_number": page_num,
                "content": text,
                "content_length": char_count,
                "word_count": word_count,
                "is_empty": len(text.strip()) == 0,
                "has_content": len(text.strip()) > 0
            }
            
            pages_data.append(page_data)
    
    # Create output structure
    output_data = {
        "document_info": {
            "source_file": pdf_path.name,
            "extraction_timestamp": datetime.now().isoformat(),
            "total_pages": total_pages,
            "pages_with_content": sum(1 for p in pages_data if p["has_content"]),
            "total_words": total_words,
            "total_characters": total_characters
        },
        "pages": pages_data
    }
    
    # Save to JSON
    print(f"💾 Saving to: {output_path}")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=None)
    
    print(f"✅ Successfully extracted {total_pages} pages")
    print(f"   Total words: {total_words:,}")
    print(f"   Total characters: {total_characters:,}")
    print(f"   Output size: {output_path.stat().st_size / 1024 / 1024:.2f} MB")

if __name__ == '__main__':
    pdf_path = Path('data/JUDGMENT.pdf')
    output_path = Path('data/pdf_content.json')
    
    if not pdf_path.exists():
        print(f"❌ Error: {pdf_path} not found!")
        exit(1)
    
    extract_pdf_content(pdf_path, output_path)

