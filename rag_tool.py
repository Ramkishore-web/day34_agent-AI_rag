import chromadb
from sentence_transformers import SentenceTransformer


class RAGTool:

    def __init__(self):

        print("Loading embedding model...")

        self.embedding_model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        print("Connecting to ChromaDB...")

        self.client = chromadb.PersistentClient(
            path=r"C:\Users\SDS\Day33_Advanced_Multimodal_RAG\outputs\chroma_db"
        )

        self.collection = self.client.get_collection(
            name="enterprise_documents"
        )

        print(
            "ChromaDB collection loaded. Documents:",
            self.collection.count()
        )

    def search(self, query, top_k=3):

        query_embedding = self.embedding_model.encode(
            [query]
        ).tolist()

        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=top_k,
            include=[
                "documents",
                "metadatas",
                "distances"
            ]
        )

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        output = []

        for document, metadata, distance in zip(
            documents,
            metadatas,
            distances
        ):

            output.append(
                {
                    "document": document,
                    "metadata": metadata,
                    "distance": distance
                }
            )

        return output


if __name__ == "__main__":

    rag = RAGTool()

    results = rag.search(
        "What is the total amount?"
    )

    print("\nRAG Results:")

    for result in results:

        print("\nDocument:")
        print(result["document"])

        print("Metadata:")
        print(result["metadata"])

        print("Distance:")
        print(result["distance"])
