from logger import logger

def query_chain(chain, user_input: str):
    try:
        result = chain({"query": user_input})
        return {
            "response": result["result"],
            "sources": [doc.metadata for doc in result["source_documents"]]
        }
    except Exception as e:
        logger.exception("Query chain failed")
        raise
