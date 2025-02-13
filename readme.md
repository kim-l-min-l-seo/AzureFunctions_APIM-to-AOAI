# Azure Function을 통한 Azure Infra 통신 테스트
## 파일 구성
```shell
Functions/
├── API1_apim-to-aoai/
├── API2_aoai-to-aisearch/
├── API3_apim-aoai-aisearch/
├── MI1_apim-to-aoai/
├── MI2_aoai-to-aisearch/
└── MI3_apim-aoai-aisearch/
```
- API   : API를 사용한 토큰인증 방식
- MI    : Managed Identity를 사용한 인증방식
- apim-to-aoai
  - APIM, Azure OpenAI간 통신 테스트
- aoai-to-aisearch
  - Azure OpenAI, AI Search간 통신 테스트
- apim-aoai-aisearch
  - APIM을 통한 Azure OpenAI, Azure AI Search 통신 테스트