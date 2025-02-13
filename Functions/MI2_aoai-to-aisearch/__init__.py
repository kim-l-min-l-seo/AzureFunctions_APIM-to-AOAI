import logging
import azure.functions as func
from azure.identity import DefaultAzureCredential, get_bearer_token_provider 
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
    # print(str.encode('utf-8', errors='ignore').decode('utf-8'))  
    content = req.params.get('content')

    logging.info(content)
    if not content:
        content = "서울교대부초에 원서 접수를 할 수 있는 조건은 무엇인가요?"
    else :
        logging.info(content)

    # Entra ID 인증을 사용하여 Azure OpenAI 클라이언트 초기화
    token_provider = get_bearer_token_provider(  
        DefaultAzureCredential(),  
        "https://cognitiveservices.azure.com/.default"  
    )  

    client = openai.AzureOpenAI(
        azure_endpoint=endpoint,
        # api_key=api_key,
        azure_ad_token_provider=token_provider,
        api_version="2024-05-01-preview",
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
                            # "type": "api_key",
                            # "key": aisearch_key,
                            "type": "system_assigned_managed_identity"  
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
