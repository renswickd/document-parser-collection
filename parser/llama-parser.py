import os
import logging
import nest_asyncio
from pathlib import Path
from typing import Optional, List, Dict
from llama_parse import LlamaParse
from dotenv import load_dotenv
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class LlamaDocParser:
    """Parser class for extracting content from PDFs using Llama Parse."""
    
    def __init__(self, model_name: Optional[str] = None):
        """
        Initialize parser with model configuration.
        
        Args:
            model_name (str, optional): Llama model name. Defaults to environment variable.
        """
        load_dotenv()
        nest_asyncio.apply()
        
        self.model_name = model_name or os.getenv(
            "LLAMA_MODEL_NAME", 
            "meta-llama/Meta-Llama-3-8B-Instruct"
        )
        
        # Initialize parser with configuration
        self.parser = LlamaParse(
            result_type="markdown",
            model_name=self.model_name,
            max_new_tokens=512,
            temperature=0.1,
            top_p=0.95,
            top_k=40,
            num_beams=1,
            do_sample=True,
            use_gpu=True
        )
        
        # Setup project directories
        self.project_root = Path(__file__).parent.parent.parent
        self.data_dir = self.project_root / "data"
        self.output_dir = self.project_root / "output"
        self.output_dir.mkdir(exist_ok=True)

    def process_pdf(self, file_name: str) -> Dict:
        """
        Process a single PDF file using Llama Parse.
        
        Args:
            file_name (str): Name of the PDF file in the data directory
            
        Returns:
            Dict: Processed parsing results including file info and content
        """
        input_path = self.data_dir / file_name
        
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")
        
        logger.info(f"Processing file: {file_name}")
        
        try:
            # Process document
            documents = self.parser.load_data(str(input_path))
            
            # Prepare results
            results = {
                "file_name": file_name,
                "processed_at": datetime.now().isoformat(),
                "chunks": []
            }
            
            # Extract content
            for i, doc in enumerate(documents):
                results["chunks"].append({
                    "chunk_number": i + 1,
                    "content": doc.text
                })
            
            # Save results
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = self.output_dir / f"{file_name.rsplit('.', 1)[0]}_{timestamp}.md"
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"# Parsing Results for {file_name}\n\n")
                for chunk in results["chunks"]:
                    f.write(f"## Document Chunk {chunk['chunk_number']}\n\n")
                    f.write(chunk["content"])
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
    """Main function to demonstrate PDF content extraction using Llama Parse."""
    try:
        # Initialize parser
        parser = LlamaDocParser()
        
        # Process single file
        sample_file = "sample-pdf.pdf"
        logger.info(f"Processing single file: {sample_file}")
        results = parser.process_pdf(sample_file)
        
        # Print results
        print("\nParsing Results:")
        for chunk in results["chunks"]:
            print(f"\n--- Document Chunk {chunk['chunk_number']} ---\n")
            print(chunk["content"])
            print("\n")
        
        logger.info("Processing completed successfully")
        
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        raise

if __name__ == "__main__":
    main()