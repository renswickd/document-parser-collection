# import nest_asyncio
import os
from mistralai import Mistral
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()

    client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

    uploaded_file = client.files.upload(
        file={
            "file_name": "data/sample-pdf.pdf",
            "content": open("data/sample-pdf.pdf", "rb")
        },
        purpose="ocr"
    )

    file_url = client.files.get_signed_url(
        file_id=uploaded_file.id
    )

    response = client.ocr.process(
        model="mistral-ocr-latest",
        document={
            "type":"document_url",
            "document_url": file_url.url
        },
        # include_image_base64=True
    )

    print("OCR Result:")
    for page in response.pages:
        print(f"\n--- Page {page.index} ---\n")
        print(page.markdown)
        print("\n\n")
        # print(dir(page))
    print("done")