import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
from azure.storage.blob import BlobServiceClient

def get_url_from_blob():
    load_dotenv()

    # Retrieve the connection string from environment variables
    connection_string = os.environ["AZURE_STORAGE_CONNECTION_STRING"]
    container_name = os.environ["AZURE_STORAGE_CONTAINER_NAME"]
    blob_name = os.environ["AZURE_STORAGE_BLOB_NAME"]
    
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(blob_name)
    url = blob_client.url

    return url


def analyze_layout_from_url():
    
    load_dotenv()

    endpoint = os.environ["DOCUMENTINTELLIGENCE_ENDPOINT"]
    key = os.environ["DOCUMENTINTELLIGENCE_API_KEY"]

    document_intelligence_client = DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    # Analyze a sample document layout using its URL
    formUrl = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/sample-layout.pdf"
    poller = document_intelligence_client.begin_analyze_document(
        "prebuilt-layout", AnalyzeDocumentRequest(url_source=formUrl)
    )
    result = poller.result()

    # Analyze pages
    for page in result.pages:
        print(f"----Analyzing layout from page #{page.page_number}----")

        # Analyze lines
        if page.lines:
            for line_idx, line in enumerate(page.lines):
                print(
                    f"...Line #{line_idx} has text content '{line.content}'"
                )

        # Analyze selection marks
        if page.selection_marks:
            for selection_mark in page.selection_marks:
                print(
                    f"...Selection mark is '{selection_mark.state}' "
                    f"and has a confidence of {selection_mark.confidence}"
                )

    # Analyze tables
    if result.tables:
        for table_idx, table in enumerate(result.tables):
            print(
                f"Table #{table_idx} has {table.row_count} rows and {table.column_count} columns"
            )
            for cell in table.cells:
                print(
                    f"...Cell[{cell.row_index}][{cell.column_index}] has content '{cell.content}'"
                )
