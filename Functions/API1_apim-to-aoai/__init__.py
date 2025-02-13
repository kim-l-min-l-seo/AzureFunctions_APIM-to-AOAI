import logging
import azure.functions as func
import json
import requests

# 변수 설정
## Azure OpenAI
openai_deployment_name      = "gpt-4o"
openai_api_version          = "2024-02-01"
apim_resource_gateway_url = "" # 이전 단계에서 생성한 APIM 리소스의 게이트웨이 URL을 입력합니다.
apim_subscription_key = "" # 이전 단계에서 생성한 APIM 리소스의 구독 키를 입력합니다.

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    url = apim_resource_gateway_url + "/openai/deployments/" + openai_deployment_name + "/chat/completions?api-version=" + openai_api_version
    api_runs = []

    result = "update by kms \nDate2025-12-16\nVer:0.1\n\n"
    result += "Chatting Test중이니 성공했는지 여부 알려줘\n"
    for i in range(5):
        messages={"messages":[
            {"role": "system", "content": "You are a sarcastic unhelpful assistant."},
            {"role": "user", "content": "Chatting Test중이니 성공했는지 여부 알려줘"}
        ]}
        # result += messages
        response = requests.post(url, headers = {'Ocp-Apim-Subscription-Key':apim_subscription_key}, json = messages)
        if (response.status_code == 200):
            print(">> Run: ", i+1, "status code: ", response.status_code, "Check")
            result += ">> Run: ," +str(i+1)+ ",status code: "+ str(response.status_code)+ " Check \n"
            data = json.loads(response.text)
            total_tokens = data.get("usage").get("total_tokens")
            # print("message: ", data.get("choices")[0].get("message").get("content"))
            result += "message: "+ str(data.get("choices")[0].get("message").get("content")) +"\n"
        else:
            print(">> Run: ", i+1, "status code: ", response.status_code, "Error")
            result += ">> Run: ,"+str(i+1)+ ",status code: "+ str(response.status_code)+ " Error" +"\n"
            print(response.text)
            result += response.text +"\n"
            total_tokens = 0
        api_runs.append((total_tokens, response.status_code))
    return func.HttpResponse(
            result,
            status_code=200
    )