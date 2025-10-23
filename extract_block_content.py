#!/usr/bin/env python3
"""
Extract block content for each reference block and create block_content.json
"""

import json
from pathlib import Path

def extract_block_content(car_references_path, pdf_content_path, output_path):
    """Extract content for each block with references"""
    
    print(f"📄 Loading CAR references from: {car_references_path}")
    with open(car_references_path, 'r', encoding='utf-8') as f:
        car_data = json.load(f)
    
    print(f"📄 Loading PDF content from: {pdf_content_path}")
    with open(pdf_content_path, 'r', encoding='utf-8') as f:
        pdf_data = json.load(f)
    
    # Create page lookup
    page_content = {p['page_number']: p['content'] for p in pdf_data['pages']}
    
    print(f"📊 Processing {len(car_data['blocks'])} blocks...")
    
    # Create block content dictionary
    block_content = {}
    
    for i, block in enumerate(car_data['blocks'], 1):
        if i % 100 == 0:
            print(f"   Processing block {i}/{len(car_data['blocks'])}...")
        
        page_num = block['page_number']
        block_id = f"block_{page_num}"
        
        # Get content for this page
        content = page_content.get(page_num, "")
        
        block_content[block_id] = {
            "content": content,
            "page_number": page_num
        }
    
    # Save to JSON
    print(f"💾 Saving to: {output_path}")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(block_content, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Successfully created block content")
    print(f"   Total blocks: {len(block_content)}")
    print(f"   Output size: {output_path.stat().st_size / 1024 / 1024:.2f} MB")

if __name__ == '__main__':
    car_references_path = Path('data/car_references.json')
    pdf_content_path = Path('data/pdf_content.json')
    output_path = Path('data/block_content.json')
    
    if not car_references_path.exists():
        print(f"❌ Error: {car_references_path} not found!")
        print(f"   Run extract_car_references.py first!")
        exit(1)
    
    if not pdf_content_path.exists():
        print(f"❌ Error: {pdf_content_path} not found!")
        print(f"   Run extract_pdf_content.py first!")
        exit(1)
    
    extract_block_content(car_references_path, pdf_content_path, output_path)

