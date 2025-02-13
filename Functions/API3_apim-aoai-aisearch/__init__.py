import logging,requests,json
import azure.functions as func

# 변수 설정
## APIM
apim_name = ""
apim_subscription_key = ""

## Azure AI Search
aisearch_endpoint = ""
aisearch_index = "school-index"
aisearch_key = ""

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    content = req.params.get('content')

    logging.info(content)
    if not content:
        content = "서울교대부초와 중대부초 중에 원서 접수가 먼저 마감되는 곳은 어디인가요?"
    else :
        logging.info(content)

    url = "https://"+apim_name+".azure-api.net/openai/deployments/gpt-4o/chat/completions?api-version=2024-02-01"
    api_runs = []
    for i in range(1):
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
                ]
            }
        
        messages={
            "messages":[
                {"role": "system", "content": "You are an AI assistant that helps people find information."},
                {"role": "user", "content": content}
            ]
        }

        json_messages = messages | extra_body

        response = requests.post(url, headers = {'Ocp-Apim-Subscription-Key': apim_subscription_key, 'work-type': 'work'}, json = json_messages)
        message = "update by kms \nDate2024-12-16\nVer:0.1\n\n"
        message += "Question : "+content
        if (response.status_code == 200):
            print(">> Run : ", i+1, "status code: ", response.status_code, "Check")
            message += ">> Run : " + str(i+1) + "status code: " + str(response.status_code) + " Check"+"\n"
            data = json.loads(response.text)
            total_tokens = data.get("usage").get("total_tokens")
            message += "message : "+data.get("choices")[0].get("message").get("content")
        else:
            print(">> Run : ", i+1, "status code: ", response.status_code, "Error")
            message += ">> Run : " + str(i+1) + "status code: " + str(response.status_code) + " Error"+"\n"
            print(response.text)
            message += response.text
            total_tokens = 0
    
        print("x-ms-region:", '\x1b[1;31m'+response.headers.get("x-ms-region")+'\x1b[0m') # 이 헤더를 통하여 어느 Region의 Azure OpenAI 서비스에서 응답을 리턴했는지 파악할 수 있음
        message += "x-ms-region:" + '\x1b[1;31m'+response.headers.get("x-ms-region")+'\x1b[0m'
        api_runs.append((total_tokens, response.status_code))

    return func.HttpResponse(
            message,status_code=200
    )
