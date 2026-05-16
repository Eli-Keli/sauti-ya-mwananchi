from google.cloud import discoveryengine_v1 as discoveryengine

import config


def search_legal_docs(query: str) -> list[str]:
    try:
        client = discoveryengine.SearchServiceClient()
        serving_config = (
            f"projects/{config.GOOGLE_CLOUD_PROJECT}"
            "/locations/global/collections/default_collection"
            f"/dataStores/{config.VERTEX_SEARCH_DATASTORE_ID}"
            "/servingConfigs/default_config"
        )
        request = discoveryengine.SearchRequest(
            serving_config=serving_config, query=query, page_size=5
        )
        response = client.search(request)
        snippets: list[str] = []
        for result in response.results:
            derived = result.document.derived_struct_data or {}
            snippet_list = derived.get("snippets", [])
            if snippet_list:
                snippet = snippet_list[0].get("snippet", "")
                if snippet:
                    snippets.append(snippet)
        return snippets
    except Exception:
        return []
