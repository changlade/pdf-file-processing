#!/usr/bin/env python3
"""
Extract CAR references from the PDF JSON data
Finds all text blocks containing CAR references like CAR-OTP-xxxx-xxxx, CAR-D29-xxxx-xxxx, CAR-V45-xxxx-xxxx
"""

import json
import re
from typing import List, Dict, Set
from pathlib import Path


class CARReferenceExtractor:
    """Extract and index CAR and evidence references from PDF content"""
    
    def __init__(self, json_path: str = "pdf_content.json"):
        self.json_path = Path(json_path)
        # Multiple patterns to catch CAR references and evidence references
        # With pdfplumber, CAR references are correctly extracted: "CAR-OTP-", "CAR-D29-", "CAR-V45-"
        self.patterns = {
            # CAR patterns with optional revision suffix (-R01, -R02, etc.)
            'CAR-OTP': re.compile(r'CAR-OTP-\d+-\d+(?:-R\d+)?', re.IGNORECASE),
            'CAR-D': re.compile(r'CAR-D\d+-\d+-\d+(?:-R\d+)?', re.IGNORECASE),
            'CAR-V': re.compile(r'CAR-V\d+-\d+-\d+(?:-R\d+)?', re.IGNORECASE),
            # General patterns for other CAR types
            'CAR-General': re.compile(r'CAR-[A-Z]+\d*-\d+-\d+(?:-R\d+)?', re.IGNORECASE),
            # Additional pattern for longer CAR prefixes
            'CAR-Extended': re.compile(r'CAR-[A-Z]{2,}-\d+-\d+(?:-R\d+)?', re.IGNORECASE),
            # Also include P-, D-, V- evidence references
            'P-Evidence': re.compile(r'P-\d+', re.IGNORECASE),
            'D-Evidence': re.compile(r'D-\d+', re.IGNORECASE),
            'V-Evidence': re.compile(r'V-\d+', re.IGNORECASE),
        }
        
    def load_pdf_data(self) -> Dict:
        """Load the PDF JSON data"""
        with open(self.json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def extract_references_from_text(self, text: str) -> List[str]:
        """Extract all reference patterns from a text block"""
        all_matches = []
        for pattern_name, pattern in self.patterns.items():
            matches = pattern.findall(text)
            # Normalize to uppercase
            all_matches.extend([match.upper() for match in matches])
        return list(set(all_matches))  # Remove duplicates
    
    def find_reference_blocks(self, pdf_data: Dict) -> List[Dict]:
        """Find all text blocks containing references"""
        reference_blocks = []
        
        for page in pdf_data['pages']:
            page_num = page['page_number']
            content = page['content']
            
            # Look for references in this page
            page_refs = self.extract_references_from_text(content)
            
            if page_refs:
                # Split content into sentences/paragraphs to find specific blocks
                sentences = self.split_into_sentences(content)
                
                for sentence in sentences:
                    sentence_refs = self.extract_references_from_text(sentence)
                    if sentence_refs:
                        reference_blocks.append({
                            'page_number': page_num,
                            'text_block': sentence.strip(),
                            'references': sentence_refs,
                            'block_id': f"page_{page_num}_{len(reference_blocks)}"
                        })
        
        return reference_blocks
    
    def split_into_sentences(self, text: str) -> List[str]:
        """Split text into meaningful sentences/paragraphs"""
        # Clean up the text
        text = text.replace('\n', ' ').replace('\r', ' ')
        text = re.sub(r'\s+', ' ', text)
        
        # Split on sentence endings, but be careful with abbreviations
        sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z])', text)
        
        # Also split on paragraph-like breaks (double spaces, numbered items)
        extended_sentences = []
        for sentence in sentences:
            # Split on numbered items like "123. Text here"
            parts = re.split(r'(?<=\.)\s+(\d+\.)', sentence)
            extended_sentences.extend([part.strip() for part in parts if part.strip()])
        
        # Filter out very short fragments
        return [s for s in extended_sentences if len(s) > 50]
    
    def create_reference_index(self, reference_blocks: List[Dict]) -> Dict:
        """Create an index of references to blocks"""
        reference_index = {}
        
        for block in reference_blocks:
            for ref in block['references']:
                if ref not in reference_index:
                    reference_index[ref] = []
                reference_index[ref].append(block)
        
        return reference_index
    
    def extract_and_save(self, output_path: str = "car_references.json") -> Dict:
        """Extract references and save to JSON file"""
        print("Loading PDF data...")
        pdf_data = self.load_pdf_data()
        
        print("Extracting reference blocks...")
        reference_blocks = self.find_reference_blocks(pdf_data)
        
        print("Creating reference index...")
        reference_index = self.create_reference_index(reference_blocks)
        
        # Prepare output data
        output_data = {
            'extraction_info': {
                'source_file': str(self.json_path),
                'extraction_timestamp': pdf_data['document_info']['extraction_timestamp'],
                'total_reference_blocks': len(reference_blocks),
                'unique_references': len(reference_index),
                'reference_list': sorted(reference_index.keys())
            },
            'reference_blocks': reference_blocks,
            'reference_index': reference_index
        }
        
        # Save to file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        
        print(f"Extracted {len(reference_blocks)} text blocks with references")
        print(f"Found {len(reference_index)} unique references")
        print(f"Saved to {output_path}")
        
        # Show sample references
        print(f"\nSample references found:")
        for i, ref in enumerate(sorted(reference_index.keys())[:10]):
            count = len(reference_index[ref])
            print(f"  {ref}: {count} block(s)")
        
        if len(reference_index) > 10:
            print(f"  ... and {len(reference_index) - 10} more")
        
        return output_data


def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Extract CAR references from PDF JSON data')
    parser.add_argument('--input', '-i', default='pdf_content.json', 
                       help='Input PDF JSON file (default: pdf_content.json)')
    parser.add_argument('--output', '-o', default='car_references.json', 
                       help='Output CAR references JSON file (default: car_references.json)')
    
    args = parser.parse_args()
    
    extractor = CARReferenceExtractor(args.input)
    extractor.extract_and_save(args.output)


if __name__ == "__main__":
    main()
