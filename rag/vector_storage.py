import os

from dotenv import load_dotenv
from pinecone import Pinecone
from chunker import chunk_logs

load_dotenv()

pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))


def initialize_and_upsert_vector_store(recreate_index: bool = True):
    index_name = "tracelens-index"
    namespace = "tracelens-namespace"
    field_name = "chunked_logs"

    existing_indexes = [idx.name for idx in pc.list_indexes()]
    if recreate_index and index_name in existing_indexes:
        pc.delete_index(index_name)
        existing_indexes.remove(index_name)

    if index_name not in existing_indexes:
        pc.create_index_for_model(
            name=index_name,
            cloud="aws",
            region="us-east-1",
            embed={
                "model": "llama-text-embed-v2",
                "field_map": {"text": field_name},
            },
        )

    index = pc.index(index_name)
    chunks = chunk_logs()

    records = [
        {"_id": f"chunk-{i}", field_name: doc}
        for i, doc in enumerate(chunks)
    ]

    # Pinecone's upsert_records limit is 96 records per batch
    batch_size = 96
    for i in range(0, len(records), batch_size):
        batch = records[i : i + batch_size]
        index.upsert_records(namespace=namespace, records=batch)
        print(f"Upserted batch {i // batch_size + 1}: {len(batch)} records")

    return f"Successfully upserted {len(records)} records to Pinecone!"


if __name__ == "__main__":
    print(initialize_and_upsert_vector_store(recreate_index=True))