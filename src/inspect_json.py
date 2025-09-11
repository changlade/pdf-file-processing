#!/usr/bin/env python3
"""
Simple script to inspect the contents of the extracted PDF data in JSON format
"""

import json

def inspect_json_data(json_path="pdf_content.json"):
    """Load and inspect the JSON file contents"""
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("=== PDF Data Structure ===")
    print(f"Document Info:")
    for key, value in data['document_info'].items():
        print(f"  {key}: {value}")
    
    print(f"\n=== Sample Pages ===")
    # Show first few pages
    for i, page in enumerate(data['pages'][:5]):
        print(f"\nPage {page['page_number']}:")
        print(f"  Word count: {page['word_count']}")
        print(f"  Content length: {page['content_length']}")
        print(f"  Has content: {page['has_content']}")
        print(f"  Content preview: {page['content'][:150].replace(chr(10), ' ')}...")
    
    print(f"\n=== Statistics ===")
    total_pages = len(data['pages'])
    pages_with_content = sum(1 for p in data['pages'] if p['has_content'])
    avg_words_per_page = sum(p['word_count'] for p in data['pages']) / total_pages
    
    print(f"Total pages: {total_pages}")
    print(f"Pages with content: {pages_with_content}")
    print(f"Average words per page: {avg_words_per_page:.1f}")
    
    # Find pages with most and least content
    pages_by_words = sorted(data['pages'], key=lambda x: x['word_count'], reverse=True)
    print(f"\nPage with most words: Page {pages_by_words[0]['page_number']} ({pages_by_words[0]['word_count']} words)")
    print(f"Page with least words: Page {pages_by_words[-1]['page_number']} ({pages_by_words[-1]['word_count']} words)")
    
    return data

if __name__ == "__main__":
    import sys
    json_file = sys.argv[1] if len(sys.argv) > 1 else "pdf_content.json"
    inspect_json_data(json_file)
