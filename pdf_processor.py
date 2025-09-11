#!/usr/bin/env python3
"""
PDF Content Extraction Script
Reads a PDF file, extracts content with page numbers, and stores in JSON format.
Uses streaming and memory-efficient processing for large files.
"""

import json
import logging
import gc
from typing import Dict, List, Tuple, Iterator
from pathlib import Path
from datetime import datetime

import PyPDF2


class PDFExtractor:
    """Memory-efficient PDF content extractor"""
    
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
    
    def extract_pdf_pages_stream(self) -> Iterator[Tuple[int, str]]:
        """Stream PDF pages one by one to reduce memory usage"""
        self.logger.info(f"Streaming content from {self.pdf_path}")
        
        with open(self.pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            total_pages = len(pdf_reader.pages)
            
            self.logger.info(f"Total pages in PDF: {total_pages}")
            
            for page_num in range(total_pages):
                try:
                    if page_num % 100 == 0:  # Progress indicator
                        self.logger.info(f"Processing page {page_num + 1}/{total_pages}")
                    
                    page = pdf_reader.pages[page_num]
                    text = page.extract_text()
                    
                    yield (page_num + 1, text)
                    
                    # Force garbage collection every 50 pages
                    if page_num % 50 == 0:
                        gc.collect()
                        
                except Exception as e:
                    self.logger.warning(f"Error extracting page {page_num + 1}: {e}")
                    yield (page_num + 1, "")
                    continue
    
    def process_page(self, page_num: int, content: str) -> Dict:
        """Process a single page and return its data"""
        return {
            'page_number': page_num,
            'content': content,
            'content_length': len(content),
            'word_count': len(content.split()) if content.strip() else 0,
            'is_empty': len(content.strip()) == 0,
            'has_content': len(content) > 0
        }
    
    def extract_and_save_streaming(self) -> None:
        """Stream processing and save to JSON without loading everything in memory"""
        try:
            self.logger.info("Starting streaming extraction...")
            
            # Collect statistics while streaming
            total_pages = 0
            pages_with_content = 0
            total_words = 0
            total_characters = 0
            
            # Open JSON file for writing
            with open(self.output_path, 'w', encoding='utf-8') as f:
                # Write JSON header
                f.write('{\n')
                f.write('  "document_info": {\n')
                f.write(f'    "source_file": "{str(self.pdf_path)}",\n')
                f.write(f'    "extraction_timestamp": "{datetime.now().isoformat()}",\n')
                
                # We'll update these later
                f.write('    "total_pages": 0,\n')
                f.write('    "pages_with_content": 0,\n')
                f.write('    "total_words": 0,\n')
                f.write('    "total_characters": 0\n')
                f.write('  },\n')
                f.write('  "pages": [\n')
                
                # Stream and process pages
                first_page = True
                for page_num, content in self.extract_pdf_pages_stream():
                    page_data = self.process_page(page_num, content)
                    
                    # Update statistics
                    total_pages += 1
                    if page_data['has_content']:
                        pages_with_content += 1
                    total_words += page_data['word_count']
                    total_characters += page_data['content_length']
                    
                    # Write page data (compact JSON, no indentation for pages)
                    if not first_page:
                        f.write(',\n')
                    else:
                        first_page = False
                    
                    # Write compact JSON for each page to save space and time
                    json.dump(page_data, f, ensure_ascii=False, separators=(',', ':'))
                
                f.write('\n  ]\n')
                f.write('}')
            
            # Update document info with correct statistics
            self._update_document_info(total_pages, pages_with_content, total_words, total_characters)
            
            self.logger.info(f"Successfully saved {total_pages} pages to {self.output_path}")
            self.logger.info(f"Summary: {pages_with_content}/{total_pages} pages with content, "
                           f"{total_words} total words, {total_characters} total characters")
            self.logger.info("PDF content extraction completed successfully!")
            
        except Exception as e:
            self.logger.error(f"Error during PDF extraction: {e}")
            raise
    
    def _update_document_info(self, total_pages: int, pages_with_content: int, 
                             total_words: int, total_characters: int) -> None:
        """Update the document info section with correct statistics"""
        try:
            # Read the current file
            with open(self.output_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace the placeholder values
            content = content.replace('"total_pages": 0,', f'"total_pages": {total_pages},')
            content = content.replace('"pages_with_content": 0,', f'"pages_with_content": {pages_with_content},')
            content = content.replace('"total_words": 0,', f'"total_words": {total_words},')
            content = content.replace('"total_characters": 0', f'"total_characters": {total_characters}')
            
            # Write back
            with open(self.output_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
        except Exception as e:
            self.logger.warning(f"Could not update document info: {e}")
    
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
    extractor.extract_and_save_streaming()
    
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
