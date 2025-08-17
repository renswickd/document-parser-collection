import os
import logging
from pathlib import Path
from typing import Optional, List, Dict
from mistralai import Mistral
from dotenv import load_dotenv
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MistralOCRParser:
    """Parser class for extracting content from PDFs using Mistral OCR API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize parser with API key and base configuration.
        
        Args:
            api_key (str, optional): Mistral API key. Defaults to environment variable.
        """
        self.api_key = api_key or os.getenv("MISTRAL_API_KEY")
        if not self.api_key:
            raise ValueError("MISTRAL_API_KEY not set in environment variables")
        
        # Initialize Mistral client
        self.client = Mistral(api_key=self.api_key)
        
        # Setup project directories
        self.project_root = Path(__file__).parent.parent.parent
        self.data_dir = self.project_root / "data"
        self.output_dir = self.project_root / "output"
        self.output_dir.mkdir(exist_ok=True)

    def process_pdf(self, file_name: str) -> Dict:
        """
        Process a single PDF file using Mistral OCR.
        
        Args:
            file_name (str): Name of the PDF file in the data directory
            
        Returns:
            Dict: Processed OCR results including file info and content
        """
        input_path = self.data_dir / file_name
        
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")
        
        logger.info(f"Processing file: {file_name}")
        
        try:
            # Upload file
            with open(input_path, "rb") as f:
                uploaded_file = self.client.files.upload(
                    file={
                        "file_name": str(input_path),
                        "content": f
                    },
                    purpose="ocr"
                )
            logger.info(f"File uploaded successfully: {uploaded_file.id}")

            # Get signed URL
            file_url = self.client.files.get_signed_url(
                file_id=uploaded_file.id
            )
            
            # Process with OCR
            response = self.client.ocr.process(
                model="mistral-ocr-latest",
                document={
                    "type": "document_url",
                    "document_url": file_url.url
                }
            )
            
            # Prepare results
            results = {
                "file_name": file_name,
                "processed_at": datetime.now().isoformat(),
                "pages": []
            }
            
            # Extract content
            for page in response.pages:
                results["pages"].append({
                    "page_number": page.index,
                    "content": page.markdown
                })
            
            # Save results
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = self.output_dir / f"{file_name.rsplit('.', 1)[0]}_{timestamp}.md"
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"# OCR Results for {file_name}\n\n")
                for page in results["pages"]:
                    f.write(f"## Page {page['page_number']}\n\n")
                    f.write(page["content"])
                    f.write("\n\n---\n\n")
            
            logger.info(f"Results saved to: {output_file}")
            return results
            
        except Exception as e:
            logger.error(f"Error processing {file_name}: {str(e)}")
            raise

    def process_directory(self) -> List[Dict]:
        """
        Process all PDF files in the data directory.
        
        Returns:
            List[Dict]: List of processing results for each file
        """
        results = []
        
        for pdf_file in self.data_dir.glob("*.pdf"):
            try:
                result = self.process_pdf(pdf_file.name)
                results.append(result)
            except Exception as e:
                logger.error(f"Failed to process {pdf_file.name}: {str(e)}")
                continue
        
        return results

def main():
    """Main function to demonstrate PDF content extraction using Mistral OCR."""
    try:
        # Load environment variables
        load_dotenv()
        
        # Initialize parser
        parser = MistralOCRParser()
        
        # Process single file
        sample_file = "sample-pdf.pdf"
        logger.info(f"Processing single file: {sample_file}")
        results = parser.process_pdf(sample_file)
        
        # Print results
        print("\nOCR Results:")
        for page in results["pages"]:
            print(f"\n--- Page {page['page_number']} ---\n")
            print(page["content"])
            print("\n")
        
        logger.info("Processing completed successfully")
        
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        raise

if __name__ == "__main__":
    main()