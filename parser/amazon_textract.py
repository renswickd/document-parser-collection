import os
import logging
from pathlib import Path
from typing import Optional, List, Dict
from datetime import datetime
import boto3
from botocore.exceptions import ClientError
from langchain_community.document_loaders import AmazonTextractPDFLoader
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AmazonTextractParser:
    """Parser class for extracting content from PDFs using Amazon Textract."""
    
    def __init__(self, region_name: Optional[str] = None):
        """
        Initialize parser with AWS configuration.
        
        Args:
            region_name (str, optional): AWS region name. Defaults to environment variable.
        """
        load_dotenv()
        
        # Initialize AWS configuration
        self.region_name = region_name or os.getenv("AWS_REGION", "us-east-1")
        self.aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
        self.aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        
        if not all([self.aws_access_key, self.aws_secret_key]):
            raise ValueError("AWS credentials not found in environment variables")
        
        # Initialize AWS client
        self.textract_client = boto3.client(
            "textract",
            region_name=self.region_name,
            aws_access_key_id=self.aws_access_key,
            aws_secret_access_key=self.aws_secret_key
        )
        
        # Setup project directories
        self.project_root = Path(__file__).parent.parent.parent
        self.data_dir = self.project_root / "data"
        self.output_dir = self.project_root / "output"
        self.output_dir.mkdir(exist_ok=True)

    def process_pdf(self, file_name: str) -> Dict:
        """
        Process a single PDF file using Amazon Textract.
        
        Args:
            file_name (str): Name of the PDF file in the data directory
            
        Returns:
            Dict: Processing results including file info and content
        """
        input_path = self.data_dir / file_name
        
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")
        
        logger.info(f"Processing file: {file_name}")
        
        try:
            # Initialize loader with Textract client
            loader = AmazonTextractPDFLoader(
                str(input_path),
                client=self.textract_client
            )
            
            # Extract content
            docs = loader.load()
            
            # Prepare results
            results = {
                "file_name": file_name,
                "processed_at": datetime.now().isoformat(),
                "pages": []
            }
            
            # Process each page
            for i, doc in enumerate(docs):
                results["pages"].append({
                    "page_number": i + 1,
                    "content": doc.page_content,
                    "metadata": doc.metadata
                })
            
            # Save results
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = self.output_dir / f"{file_name.rsplit('.', 1)[0]}_{timestamp}.md"
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"# Textract Results for {file_name}\n\n")
                f.write(f"Processed at: {results['processed_at']}\n\n")
                
                for page in results["pages"]:
                    f.write(f"## Page {page['page_number']}\n\n")
                    f.write(page["content"])
                    f.write("\n\n---\n\n")
            
            logger.info(f"Results saved to: {output_file}")
            return results
            
        except ClientError as e:
            logger.error(f"AWS Textract error: {str(e)}")
            raise
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
    """Main function to demonstrate PDF content extraction using Amazon Textract."""
    try:
        # Initialize parser
        parser = AmazonTextractParser()
        
        # Process single file
        sample_file = "sample.pdf"
        logger.info(f"Processing single file: {sample_file}")
        
        results = parser.process_pdf(sample_file)
        logger.info("Processing completed successfully")
        
        # Print sample results
        print("\nExtracted Content:")
        for page in results["pages"]:
            print(f"\n--- Page {page['page_number']} ---\n")
            print(page["content"])
        
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        raise

if __name__ == "__main__":
    main()