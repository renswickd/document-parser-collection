import nest_asyncio
import os
from llama_parse import LlamaParse
from dotenv import load_dotenv

if __name__ == "__main__":
    
    load_dotenv()
    nest_asyncio.apply()
    # parser = LlamaParse(
    #     model_name=os.getenv("LLAMA_MODEL_NAME", "meta-llama/Meta-Llama-3-8B-Instruct"),
    #     max_new_tokens=512,
    #     temperature=0.1,
    #     top_p=0.95,
    #     top_k=40,
    #     num_beams=1,
    #     do_sample=True,
    #     use_gpu=True
    # )

    document = LlamaParse(result_type="markdown").load_data("data/Renswick_Delvar_Data_Scientist.pdf")
    for i, doc in enumerate(document):
        print(f"\n--- Document Chunk {i+1} ---\n")
        print(doc.text[:1000])

    print("done")