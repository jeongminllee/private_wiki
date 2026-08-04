---
type: Concept
title: "Azure Machine Learning Pipelines"
description: "Algorithms (알고리즘 & 자료구조) - ChatGPT 대화 추출 노트 (2023-05-04)"
tags: [algorithms, chatgpt-export]
timestamp: 2023-05-04
status: active
---

# Azure Machine Learning Pipelines

> **카테고리**: `Algorithms (알고리즘 & 자료구조)`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2023-05-04

## 💬 대화 내용 및 Q&A

### ❓ 질문 (User)
https://westus2.api.azureml.ms/pipelines/swagger/pipelineendpointsubmit/swagger.json

### 💡 답변 (Assistant)
The URL you provided appears to be a Swagger API documentation endpoint for the Azure Machine Learning pipeline service. Swagger is a tool used to document and test APIs, and this particular Swagger JSON file describes the endpoints available for submitting pipeline endpoints to the Azure Machine Learning service.

Using this Swagger JSON file, developers can interact with the Azure Machine Learning pipeline service and programmatically submit pipeline endpoints, which are pre-configured pipelines that can be triggered with specific parameters. These pipeline endpoints can automate data preparation, model training, and deployment tasks, allowing for more efficient machine learning workflows.

However, it's worth noting that accessing this Swagger endpoint requires appropriate authorization and authentication credentials, so it's likely not publicly accessible to everyone.

---

### ❓ 질문 (User)
파이썬 코드로 짜줘

### 💡 답변 (Assistant)
저는 파이썬 코드를 작성해주는 AI 모델입니다. 그러나 위에서 제공된 URL은 Azure Machine Learning Pipeline 서비스의 Swagger API 문서 URL이며, 해당 서비스를 사용하려면 Azure 계정 및 인증키가 필요합니다. 

따라서 파이썬 코드를 작성하려면 먼저 Azure Machine Learning 서비스에 등록하고, 인증 및 인가 키를 발급받아야 합니다. 그리고 나서 해당 서비스의 Python SDK 를 사용하여 파이썬 코드를 작성할 수 있습니다. 

아래는 Azure Machine Learning Python SDK를 사용하여 파이썬 코드로 파이프라인을 작성하는 간단한 예시입니다.

```python
# 필요한 라이브러리 import
from azureml.core import Workspace, Dataset
from azureml.core.compute import ComputeTarget, AmlCompute
from azureml.core.compute_target import ComputeTargetException
from azureml.pipeline.core import Pipeline, PipelineData, PipelineEndpoint
from azureml.pipeline.steps import PythonScriptStep

# Azure Machine Learning workspace 설정
ws = Workspace.from_config()

# 데이터셋 설정
dataset = Dataset.get_by_name(ws, 'my_dataset')

# 컴퓨팅 리소스 설정
compute_target = ComputeTarget(workspace=ws, name='my_compute_target')

# 파이프라인 데이터 설정
pipeline_data = PipelineData('pipeline_data', datastore=ws.get_default_datastore())

# 파이프라인 단계 설정
step1 = PythonScriptStep(
    name='step1',
    script_name='step1.py',
    inputs=[dataset.as_named_input('input_data')],
    outputs=[pipeline_data],
    compute_target=compute_target,
    source_directory='scripts'
)

# 파이프라인 설정
pipeline = Pipeline(workspace=ws, steps=[step1])

# 파이프라인 엔드포인트 생성
pipeline_endpoint = PipelineEndpoint.publish(
    workspace=ws,
    name='my_pipeline_endpoint',
    pipeline=pipeline
)

# 파이프라인 엔드포인트 호출
pipeline_endpoint.submit('my_experiment')
```

위 코드는 Azure Machine Learning workspace를 설정하고, 데이터셋, 컴퓨팅 리소스, 파이프라인 데이터, 파이프라인 단계 및 파이프라인을 설정한 후, 파이프라인 엔드포인트를 생성하고 호출하는 예시입니다. 

하지만 이 코드는 작동하지 않을 것입니다. 이 코드를 실행하려면 작동하는 Azure Machine Learning workspace와 데이터가 필요합니다. 따라서 실제 환경에서 사용하기 위해서는 이 코드를 알맞게 수정하여 사용해야 합니다.

---

### ❓ 질문 (User)
https://westus2.api.azureml.ms/pipelines/swagger/pipelineendpointsubmit/swagger.json 를 파이썬 코드로 작성해줘

### 💡 답변 (Assistant)
제공된 URL을 사용하여 파이프라인 엔드포인트를 제출하려면 Python `requests` 모듈을 사용하여 HTTP POST 요청을 보내야 합니다. 아래는 간단한 예시 코드입니다.

```python
import requests
import json

url = 'https://westus2.api.azureml.ms/pipelines/swagger/pipelineendpointsubmit'

# 파이프라인 엔드포인트 요청의 body
payload = {
    "experimentName": "my_experiment",
    "pipelineEndpointName": "my_pipeline_endpoint",
    "pipelineParameters": {
        "param1": "value1",
        "param2": "value2"
    }
}

# 인증 및 인가 키를 헤더에 추가
headers = {
    'Authorization': 'Bearer <your_authorization_token>',
    'Content-Type': 'application/json'
}

# POST 요청 보내기
response = requests.post(url, data=json.dumps(payload), headers=headers)

# 요청에 대한 응답 출력
print(response.json())
```

위 코드에서는 `url` 변수에 제공된 URL을 할당하고, 파이프라인 엔드포인트를 제출하는 요청의 `payload`를 설정합니다. 이후, `headers`에는 인증 및 인가 키가 포함되어 있어야 합니다. 만약 키가 없다면 Azure Portal에서 인증 키를 생성하고, `<your_authorization_token>` 부분에 해당하는 값을 대체해야 합니다.

마지막으로, `requests.post()`를 사용하여 HTTP POST 요청을 보내고, 응답을 출력합니다. 이 코드를 실행하기 위해서는 `requests` 모듈이 설치되어 있어야 합니다.

---
