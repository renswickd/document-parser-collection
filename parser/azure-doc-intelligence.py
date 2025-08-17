import os
import logging
from pathlib import Path
from typing import Optional, List, Dict
from datetime import datetime
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import AzureError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AzureDocParser:
    """Parser class for extracting content from documents using Azure Document Intelligence."""
    
    def __init__(self):
        """Initialize parser with Azure credentials and configuration."""
        load_dotenv()
        
        # Initialize Azure credentials
        self.endpoint = os.getenv("DOCUMENTINTELLIGENCE_ENDPOINT")
        self.key = os.getenv("DOCUMENTINTELLIGENCE_API_KEY")
        
        if not all([self.endpoint, self.key]):
            raise ValueError("Azure Document Intelligence credentials not found in environment variables")
        
        # Initialize Azure client
        self.client = DocumentIntelligenceClient(
            endpoint=self.endpoint,
            credential=AzureKeyCredential(self.key)
        )
        
        # Setup project directories
        self.project_root = Path(__file__).parent.parent.parent
        self.data_dir = self.project_root / "data"
        self.output_dir = self.project_root / "output"
        self.output_dir.mkdir(exist_ok=True)

    def get_blob_url(self, blob_name: str) -> str:
        """
        Get URL for a blob in Azure Storage.
        
        Args:
            blob_name (str): Name of the blob
            
        Returns:
            str: URL of the blob
        """
        try:
            connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
            container_name = os.getenv("AZURE_STORAGE_CONTAINER_NAME")
            
            if not all([connection_string, container_name]):
                raise ValueError("Azure Storage credentials not found in environment variables")
            
            blob_service_client = BlobServiceClient.from_connection_string(connection_string)
            container_client = blob_service_client.get_container_client(container_name)
            blob_client = container_client.get_blob_client(blob_name)
            
            return blob_client.url
            
        except Exception as e:
            logger.error(f"Error accessing blob storage: {str(e)}")
            raise

    def analyze_document(self, document_url: str) -> Dict:
        """
        Analyze a document using Azure Document Intelligence.
        
        Args:
            document_url (str): URL of the document to analyze
            
        Returns:
            Dict: Analysis results including text content and metadata
        """
        try:
            logger.info(f"Analyzing document: {document_url}")
            
            poller = self.client.begin_analyze_document(
                "prebuilt-layout",
                AnalyzeDocumentRequest(url_source=document_url)
            )
            result = poller.result()
            
            # Prepare results
            analysis_results = {
                "analyzed_at": datetime.now().isoformat(),
                "document_url": document_url,
                "pages": []
            }
            
            # Extract content page by page
            for page in result.pages:
                page_content = {
                    "page_number": page.page_number,
                    "lines": [],
                    "tables": []
                }
                
                # Extract text lines
                if page.lines:
                    for line in page.lines:
                        page_content["lines"].append({
                            "content": line.content,
                            "bounding_box": line.bounding_box if hasattr(line, 'bounding_box') else None
                        })
                
                # Extract tables
                if page.tables:
                    for table in page.tables:
                        table_data = []
                        for cell in table.cells:
                            table_data.append({
                                "text": cell.content,
                                "row_index": cell.row_index,
                                "column_index": cell.column_index
                            })
                        page_content["tables"].append(table_data)
                
                analysis_results["pages"].append(page_content)
            
            return analysis_results
            
        except AzureError as e:
            logger.error(f"Azure service error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error analyzing document: {str(e)}")
            raise

    def process_document(self, blob_name: str) -> Dict:
        """
        Process a document from Azure Blob Storage.
        
        Args:
            blob_name (str): Name of the blob containing the document
            
        Returns:
            Dict: Processing results
        """
        try:
            # Get document URL from blob storage
            document_url = self.get_blob_url(blob_name)
            
            # Analyze document
            results = self.analyze_document(document_url)
            
            # Save results
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = self.output_dir / f"{blob_name}_{timestamp}.md"
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"# Document Analysis Results\n\n")
                f.write(f"Document: {blob_name}\n")
                f.write(f"Analyzed at: {results['analyzed_at']}\n\n")
                
                for page in results["pages"]:
                    f.write(f"## Page {page['page_number']}\n\n")
                    
                    # Write text content
                    f.write("### Text Content\n\n")
                    for line in page["lines"]:
                        f.write(f"{line['content']}\n")
                    
                    # Write table content
                    if page["tables"]:
                        f.write("\n### Tables\n\n")
                        for table_idx, table in enumerate(page["tables"], 1):
                            f.write(f"#### Table {table_idx}\n\n")
                            # Create markdown table (simplified)
                            for cell in table:
                                f.write(f"Row {cell['row_index']}, Col {cell['column_index']}: {cell['text']}\n")
                    
                    f.write("\n---\n\n")
            
            logger.info(f"Results saved to: {output_file}")
            return results
            
        except Exception as e:
            logger.error(f"Error processing document {blob_name}: {str(e)}")
            raise

def main():
    """Main function to demonstrate document analysis using Azure Document Intelligence."""
    try:
        parser = AzureDocParser()
        
        # Process sample document
        blob_name = "sample-document.pdf"
        logger.info(f"Processing document: {blob_name}")
        
        results = parser.process_document(blob_name)
        logger.info("Processing completed successfully")
        
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        raise

if __name__ == "__main__":
    main()