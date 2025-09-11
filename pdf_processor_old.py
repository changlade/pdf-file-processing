#!/usr/bin/env python3
"""
Simple PDF Content Extraction Script
Reads a PDF file, extracts content with page numbers, and stores in JSON format.
"""

import json
import logging
from typing import Dict, List, Tuple
from pathlib import Path
from datetime import datetime

import PyPDF2


class PDFExtractor:
    """Simple PDF content extractor"""
    
    def __init__(self, pdf_path: str, output_path: str = "pdf_content.json"):
        self.pdf_path = Path(pdf_path)
        self.output_path = Path(output_path)
        self.logger = self._setup_logging()
        
    def _setup_logging(self) -> logging.Logger:
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        return logging.getLogger(__name__)
    
    
    def extract_pdf_content(self) -> List[Tuple[int, str]]:
        """Extract content from PDF file with page numbers"""
        self.logger.info(f"Extracting content from {self.pdf_path}")
        
        pages_content = []
        
        try:
            with open(self.pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                total_pages = len(pdf_reader.pages)
                
                self.logger.info(f"Total pages in PDF: {total_pages}")
                
                for page_num in range(total_pages):
                    try:
                        page = pdf_reader.pages[page_num]
                        text = page.extract_text()
                        
                        # Always add the page, even if empty (for consistency)
                        pages_content.append((page_num + 1, text))
                            
                    except Exception as e:
                        self.logger.warning(f"Error extracting page {page_num + 1}: {e}")
                        # Add empty content for failed pages to maintain page numbering
                        pages_content.append((page_num + 1, ""))
                        continue
        
        except Exception as e:
            self.logger.error(f"Error opening PDF file: {e}")
            raise
        
        self.logger.info(f"Extracted content from {len(pages_content)} pages")
        return pages_content
    
    def process_content(self, pages_content: List[Tuple[int, str]]) -> List[Dict]:
        """Process page content and add statistics"""
        self.logger.info("Processing content...")
        
        # Convert pages to list of dictionaries with statistics
        page_data = []
        for page_num, content in pages_content:
            page_data.append({
                'page_number': page_num,
                'content': content,
                'content_length': len(content),
                'word_count': len(content.split()) if content.strip() else 0,
                'is_empty': len(content.strip()) == 0,
                'has_content': len(content) > 0
            })
        
        self.logger.info(f"Processed {len(page_data)} pages")
        return page_data
    
    def save_to_json(self, processed_data: List[Dict]) -> None:
        """Save processed data to JSON file"""
        self.logger.info(f"Saving processed data to {self.output_path}")
        
        # Calculate some summary statistics
        total_pages = len(processed_data)
        pages_with_content = sum(1 for page in processed_data if page['has_content'])
        total_words = sum(page['word_count'] for page in processed_data)
        total_characters = sum(page['content_length'] for page in processed_data)
        
        # Prepare final data structure
        final_data = {
            'document_info': {
                'source_file': str(self.pdf_path),
                'extraction_timestamp': datetime.now().isoformat(),
                'total_pages': total_pages,
                'pages_with_content': pages_with_content,
                'total_words': total_words,
                'total_characters': total_characters
            },
            'pages': processed_data
        }
        
        with open(self.output_path, 'w', encoding='utf-8') as f:
            json.dump(final_data, f, ensure_ascii=False, indent=2)
        
        self.logger.info(f"Successfully saved {total_pages} pages to {self.output_path}")
        self.logger.info(f"Summary: {pages_with_content}/{total_pages} pages with content, "
                        f"{total_words} total words, {total_characters} total characters")
    
    def extract_and_save(self) -> None:
        """Main extraction pipeline"""
        try:
            # Extract PDF content
            pages_content = self.extract_pdf_content()
            
            # Process content
            processed_data = self.process_content(pages_content)
            
            # Save to JSON
            self.save_to_json(processed_data)
            
            self.logger.info("PDF content extraction completed successfully!")
            
        except Exception as e:
            self.logger.error(f"Error during PDF extraction: {e}")
            raise
    
    def load_extracted_data(self, json_path: str = None) -> Dict:
        """Load extracted data from JSON file"""
        path = json_path or self.output_path
        
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return data


def main():
    """Main function to run the PDF extractor"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Extract content from PDF file and store in JSON format')
    parser.add_argument('pdf_path', help='Path to the PDF file to extract')
    parser.add_argument('--output', '-o', default='pdf_content.json', 
                       help='Output JSON file path (default: pdf_content.json)')
    
    args = parser.parse_args()
    
    # Extract the document
    extractor = PDFExtractor(args.pdf_path, args.output)
    extractor.extract_and_save()
    
    # Load and display summary
    data = extractor.load_extracted_data()
    print(f"\nExtraction Summary:")
    print(f"Source file: {data['document_info']['source_file']}")
    print(f"Total pages: {data['document_info']['total_pages']}")
    print(f"Pages with content: {data['document_info']['pages_with_content']}")
    print(f"Total words: {data['document_info']['total_words']}")
    print(f"Total characters: {data['document_info']['total_characters']}")
    print(f"Extraction timestamp: {data['document_info']['extraction_timestamp']}")
    
    # Show sample pages
    print(f"\nSample pages:")
    for i, page in enumerate(data['pages'][:3]):
        if page['has_content']:
            content_preview = page['content'][:200].replace('\n', ' ')
            print(f"\nPage {page['page_number']} ({page['word_count']} words):")
            print(f"Content preview: {content_preview}...")


if __name__ == "__main__":
    main()
