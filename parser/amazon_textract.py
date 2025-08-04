import boto3
from langchain_community.document_loaders import AmazonTextractPDFLoader

def main():

    PROJECT_ROOT = "<YOUR_ROOT_DIRECTORY>"
    file_path = PROJECT_ROOT+"sample.pdf"

    textract_client = boto3.client("textract",region_name="us-east-1")
    loader = AmazonTextractPDFLoader(file_path,client=textract_client)
    docs = loader.load()

    extracted_content = ""
    for doc in docs:
        extracted_content += doc.page_content+ "\n"

    with open("output.txt", 'w') as file:
        file.write(extracted_content)

if __name__ == "__main__":
   main()