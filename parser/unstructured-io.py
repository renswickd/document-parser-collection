import os
import logging
from typing import List, Optional
from pathlib import Path
from langchain_unstructured import UnstructuredLoader
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class UnstructuredParser:
    """Parser class for extracting content from PDFs using Unstructured.io API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize parser with API key and base configuration.
        
        Args:
            api_key (str, optional): Unstructured.io API key. Defaults to environment variable.
        """
        self.api_key = api_key or os.getenv("UNSTRUCTURED_API_KEY")
        if not self.api_key:
            raise ValueError("UNSTRUCTURED_API_KEY not set in environment variables")
        
        # Get project root directory
        self.project_root = Path(__file__).parent.parent.parent
        
        # Create output directory if it doesn't exist
        self.output_dir = self.project_root / "output"
        self.output_dir.mkdir(exist_ok=True)

    def process_pdf(self, file_name: str) -> str:
        """
        Process a single PDF file and extract its content.
        
        Args:
            file_name (str): Name of the PDF file in the input directory
            
        Returns:
            str: Path to the output file containing extracted content
        """
        input_path = self.project_root / "input" / file_name
        
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")
        
        logger.info(f"Processing file: {file_name}")
        
        try:
            # Initialize loader with API configuration
            loader = UnstructuredLoader(
                file_path=str(input_path),
                api_key=self.api_key,
                partition_via_api=True
            )
            
            # Extract content
            docs = loader.load()
            
            # Prepare output
            extracted_content = "\n".join(doc.page_content for doc in docs)
            
            # Generate output filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = self.output_dir / f"{file_name.rsplit('.', 1)[0]}_{timestamp}.txt"
            
            # Save extracted content
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(extracted_content)
            
            logger.info(f"Content extracted and saved to: {output_file}")
            return str(output_file)
            
        except Exception as e:
            logger.error(f"Error processing {file_name}: {str(e)}")
            raise

    def process_directory(self) -> List[str]:
        """
        Process all PDF files in the input directory.
        
        Returns:
            List[str]: List of paths to output files
        """
        input_dir = self.project_root / "input"
        output_files = []
        
        for pdf_file in input_dir.glob("*.pdf"):
            try:
                output_file = self.process_pdf(pdf_file.name)
                output_files.append(output_file)
            except Exception as e:
                logger.error(f"Failed to process {pdf_file.name}: {str(e)}")
                continue
        
        return output_files

def main():
    """Main function to demonstrate PDF content extraction."""
    try:
        parser = UnstructuredParser()
        
        # Process single file
        sample_file = "sample-1.pdf"
        logger.info(f"Processing single file: {sample_file}")
        output_file = parser.process_pdf(sample_file)
        logger.info(f"Content extracted to: {output_file}")
        
        # Process all files in directory
        logger.info("Processing all PDF files in input directory")
        output_files = parser.process_directory()
        logger.info(f"Processed {len(output_files)} files successfully")
        
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        raise

if __name__ == "__main__":
    main()