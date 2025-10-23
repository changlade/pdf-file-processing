#!/usr/bin/env python3
"""
Extract CAR references from pdf_content.json and create car_references.json
"""

import json
import re
from datetime import datetime
from pathlib import Path
from collections import defaultdict

# CAR reference patterns
PATTERNS = {
    'CAR-D29-Standard': re.compile(r'CAR-D29-\d{4}-\d{4}'),
    'CAR-D30-Standard': re.compile(r'CAR-D30-\d{4}-\d{4}'),
    'CAR-OTP-Standard': re.compile(r'CAR-OTP-\d{4}-\d{4}'),
    'CAR-OTP-8Digits': re.compile(r'CAR-OTP-\d{8}'),
    'CAR-D29-Revision': re.compile(r'CAR-D29-\d{4}-\d{3}'),
    'CAR-D30-Revision': re.compile(r'CAR-D30-\d{4}-\d{3}'),
    'CAR-OTP-Revision': re.compile(r'CAR-OTP-\d{4}-\d{3}'),
    'D29-': re.compile(r'D29-\d{4,5}'),
    'D30-': re.compile(r'D30-\d{4,5}'),
    'P-': re.compile(r'P-\d{4}'),
    'V44-': re.compile(r'V44-\d{4}'),
    'V45-': re.compile(r'V45-\d{4}'),
}

def extract_references_from_text(text):
    """Extract all CAR references from text"""
    found_refs = {}
    
    for pattern_name, pattern in PATTERNS.items():
        matches = pattern.findall(text)
        if matches:
            found_refs[pattern_name] = matches
    
    return found_refs

def extract_car_references(pdf_content_path, output_path):
    """Extract CAR references from PDF content JSON"""
    
    print(f"📄 Loading PDF content from: {pdf_content_path}")
    
    with open(pdf_content_path, 'r', encoding='utf-8') as f:
        pdf_data = json.load(f)
    
    print(f"📊 Processing {len(pdf_data['pages'])} pages...")
    
    # Storage for results
    reference_blocks = []
    all_references = set()
    reference_type_counts = defaultdict(int)
    
    # Process each page
    for page_data in pdf_data['pages']:
        page_num = page_data['page_number']
        content = page_data['content']
        
        if page_num % 100 == 0:
            print(f"   Processing page {page_num}...")
        
        # Extract references
        refs = extract_references_from_text(content)
        
        if refs:
            # Collect all unique references for this block as a flat array
            all_block_refs = []
            for ref_type, matches in refs.items():
                unique_matches = list(set(matches))
                all_block_refs.extend(unique_matches)
                
                # Track statistics
                for ref in unique_matches:
                    all_references.add(ref)
                    reference_type_counts[ref_type] += 1
            
            # Create block entry with flat references array
            block = {
                "block_id": f"block_{page_num}",
                "page_number": page_num,
                "references": sorted(list(set(all_block_refs)))  # Remove duplicates and sort
            }
            
            reference_blocks.append(block)
    
    # Count evidence vs witness codes
    evidence_codes = sum(1 for ref in all_references if any(ref.startswith(p) for p in ['CAR-', 'D29-', 'D30-']))
    witness_codes = sum(1 for ref in all_references if any(ref.startswith(p) for p in ['P-', 'V44-', 'V45-']))
    
    # Create output structure
    output_data = {
        "extraction_info": {
            "source_file": str(pdf_content_path),
            "extraction_timestamp": datetime.now().isoformat(),
            "total_reference_blocks": len(reference_blocks),
            "unique_references": len(all_references),
            "evidence_codes": evidence_codes,
            "witness_codes": witness_codes,
            "reference_types": dict(reference_type_counts),
            "reference_list": sorted(list(all_references))
        },
        "blocks": reference_blocks
    }
    
    # Save to JSON
    print(f"💾 Saving to: {output_path}")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Successfully extracted references")
    print(f"   Total blocks with references: {len(reference_blocks)}")
    print(f"   Unique references: {len(all_references)}")
    print(f"   Evidence codes: {evidence_codes}")
    print(f"   Witness codes: {witness_codes}")
    print(f"   Output size: {output_path.stat().st_size / 1024 / 1024:.2f} MB")

if __name__ == '__main__':
    pdf_content_path = Path('data/pdf_content.json')
    output_path = Path('data/car_references.json')
    
    if not pdf_content_path.exists():
        print(f"❌ Error: {pdf_content_path} not found!")
        print(f"   Run extract_pdf_content.py first!")
        exit(1)
    
    extract_car_references(pdf_content_path, output_path)

