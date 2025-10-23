#!/usr/bin/env python3
"""
Create optimized car_references.json with reference_index for faster lookups
"""

import json
from pathlib import Path
from collections import defaultdict

def optimize_references(input_path, output_path):
    """Create optimized version with reference_index"""
    
    print(f"📄 Loading references from: {input_path}")
    
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"📊 Processing {len(data['blocks'])} blocks...")
    
    # Create reference index: ref -> [block_ids]
    reference_index = defaultdict(list)
    
    for block in data['blocks']:
        block_id = block['block_id']
        
        # Process all references in this block (now an array)
        for ref in block['references']:
            reference_index[ref].append(block_id)
    
    # Add reference_index to data
    data['reference_index'] = dict(reference_index)
    
    # Save optimized version
    print(f"💾 Saving optimized version to: {output_path}")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Successfully created optimized references")
    print(f"   Unique references: {len(reference_index)}")
    print(f"   Total blocks: {len(data['blocks'])}")
    print(f"   Output size: {output_path.stat().st_size / 1024 / 1024:.2f} MB")

if __name__ == '__main__':
    input_path = Path('data/car_references.json')
    output_path = Path('data/car_references.json')  # Overwrite the same file
    
    if not input_path.exists():
        print(f"❌ Error: {input_path} not found!")
        exit(1)
    
    optimize_references(input_path, output_path)

