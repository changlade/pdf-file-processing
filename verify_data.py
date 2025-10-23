#!/usr/bin/env python3
"""
Verify that all data files are correctly structured for deployment
"""

import json
from pathlib import Path

def verify_file_exists(path, description):
    """Check if file exists"""
    if path.exists():
        size_mb = path.stat().st_size / 1024 / 1024
        print(f"✅ {description}: {path.name} ({size_mb:.2f} MB)")
        return True
    else:
        print(f"❌ {description}: {path.name} NOT FOUND")
        return False

def verify_json_structure(path, required_keys, description):
    """Verify JSON file has required structure"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        missing_keys = [key for key in required_keys if key not in data]
        if missing_keys:
            print(f"❌ {description}: Missing keys: {missing_keys}")
            return False
        
        print(f"✅ {description}: All required keys present")
        return True
    except json.JSONDecodeError as e:
        print(f"❌ {description}: Invalid JSON - {e}")
        return False
    except Exception as e:
        print(f"❌ {description}: Error - {e}")
        return False

def main():
    print("🔍 Verifying data files for deployment...\n")
    
    data_dir = Path('data')
    all_good = True
    
    # Check required files
    print("📁 Checking required files:")
    all_good &= verify_file_exists(data_dir / 'JUDGMENT.pdf', 'PDF Document')
    all_good &= verify_file_exists(data_dir / 'car_references.json', 'CAR References')
    all_good &= verify_file_exists(data_dir / 'block_content.json', 'Block Content')
    all_good &= verify_file_exists(data_dir / 'pdf_content.json', 'PDF Content')
    
    print("\n📋 Verifying JSON structures:")
    
    # Verify car_references.json
    all_good &= verify_json_structure(
        data_dir / 'car_references.json',
        ['extraction_info', 'blocks', 'reference_index'],
        'car_references.json'
    )
    
    # Check specific details of car_references.json
    try:
        with open(data_dir / 'car_references.json', 'r') as f:
            ref_data = json.load(f)
        
        ref_index_size = len(ref_data.get('reference_index', {}))
        blocks_size = len(ref_data.get('blocks', []))
        unique_refs = ref_data['extraction_info']['unique_references']
        
        print(f"   - Reference index entries: {ref_index_size}")
        print(f"   - Total blocks: {blocks_size}")
        print(f"   - Unique references: {unique_refs}")
        
        if ref_index_size != unique_refs:
            print(f"   ⚠️  Warning: Reference index size doesn't match unique references count")
            all_good = False
        
    except Exception as e:
        print(f"   ❌ Error checking car_references.json details: {e}")
        all_good = False
    
    # Verify pdf_content.json
    all_good &= verify_json_structure(
        data_dir / 'pdf_content.json',
        ['document_info', 'pages'],
        'pdf_content.json'
    )
    
    # Check pdf source
    try:
        with open(data_dir / 'pdf_content.json', 'r') as f:
            pdf_data = json.load(f)
        
        source_file = pdf_data['document_info']['source_file']
        total_pages = pdf_data['document_info']['total_pages']
        
        print(f"   - Source PDF: {source_file}")
        print(f"   - Total pages: {total_pages}")
        
        if 'JUDGMENT.pdf' not in source_file:
            print(f"   ⚠️  Warning: Source is not JUDGMENT.pdf")
        
        if total_pages != 1649:
            print(f"   ⚠️  Warning: Expected 1649 pages, got {total_pages}")
        
    except Exception as e:
        print(f"   ❌ Error checking pdf_content.json details: {e}")
        all_good = False
    
    # Verify block_content.json
    try:
        with open(data_dir / 'block_content.json', 'r') as f:
            block_data = json.load(f)
        
        block_count = len(block_data)
        print(f"✅ block_content.json: {block_count} blocks")
        
    except Exception as e:
        print(f"❌ Error checking block_content.json: {e}")
        all_good = False
    
    print("\n" + "="*60)
    if all_good:
        print("✅ All data files are properly configured for deployment!")
    else:
        print("❌ Some issues found. Please fix before deploying.")
    print("="*60)
    
    return 0 if all_good else 1

if __name__ == '__main__':
    exit(main())

