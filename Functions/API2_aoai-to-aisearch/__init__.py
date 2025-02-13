import logging
import azure.functions as func
import openai

# 변수 설정
## Azure OpenAI
endpoint = ""
api_key = ""
deployment = "gpt-4o"

## Azure AI Search
aisearch_endpoint = ""
aisearch_index = "school-index"
aisearch_key = ""

def main(req: func.HttpRequest) -> func.HttpResponse:
    content = req.params.get('content')

    logging.info(content)
    if not content:
        content = "서울교대부초에 원서 접수를 할 수 있는 조건은 무엇인가요?"
    else :
        logging.info(content)

    client = openai.AzureOpenAI(
        azure_endpoint=endpoint,
        api_key=api_key,
        api_version="2024-02-01",
    )

    completion = client.chat.completions.create(
        model=deployment,
        messages=[
            {
                "role": "user",
                "content": content,
            },
        ],
        extra_body={
            "data_sources":[
                {
                    "type": "azure_search",
                    "parameters": {
                        "endpoint": aisearch_endpoint,
                        "index_name": aisearch_index,
                        "authentication": {
                            "type": "api_key",
                            "key": aisearch_key,
                        }
                    }
                }
            ],
        }
    )
    # print(completion.model_dump_json(indent=2))
    result = "update by kms \nDate2024-12-16\nVer:0.1\n\n"
    result += "Question : "+content + "\n\nAnswor : "+completion.model_dump_json(indent=2)

    return func.HttpResponse(
            result,
            status_code=200
    )
