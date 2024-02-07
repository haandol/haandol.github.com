---
layout: post
title: Streamlit + Bedrock SDXL 로 GPU 없이 이미지 생성하기
excerpt: Use SDXL on Sagemaker Bedrock via Streamlit
author: vincent
email: ldg55d@gmail.com
tags: sdxl stable-diffusion bedrock aws streamlit
publish: true
---

## TL;DR

코드는 여기[^1]

## 시작하며

얼마전에 M1 맥북에서 SDXL-Turbo 모델을 사용해서 이미지를 생성하는 방법을 소개 했었다.[^2]

이 방법도 나쁘지 않지만, 도커랑 이것저것 띄운 M1 16GB 맥북에게는 상당히 부담스러운 작업이었다.

좀 더 가벼운 환경을 위해, Amazon Bedrock SDXL 을 통해 로컬에서 이미지를 생성하는 방법을 소개한다.

## Streamlit

원래 생성형 AI 프로젝트 데모를 UI 로 보여줄 때 가장 많이 사용하는 라이브러리는 Gradio 일 것이다. Streamlit 은 원래 데이터 분석 결과물을 보여주기 위한 라이브러리이지만, 최근에 서드파티 컴포넌트를 지원하면서 생성형 AI 프로젝트에도 많이 사용하는 것 같다.

이 정도로 간단한 예제는 둘 중 뭘 써도 상관없지만, 개인적으로는 Streamlit 이 Gradio 보다 약간 더 예쁘고 데이터 분석 결과물을 같이 보여주기에도 좋아서 자주 사용한다.

streamlit 은 pip 로 설치하고 이후,

```bash
$ pip install streamlit
```

CLI 로 파이썬 모듈을 실행할 수 있다.

```bash
$ streamlit run app.py
```

## Bedrock SDXL

Amazon Bedrock 에는 SDXL 0.8 과 1.0 두 버전을 지원한다. 0.8은 없다고 생각하면 된다. 1.0 버
전을 사용하자.

또한 현재 Amazon Bedrock 은 서울 리전에서는 지원되지 않으므로, 여기서는 us-east-1 리전을 사용한다. (이와 별개로 g5 인스턴스가 서울리전에 할당실패가 자주 일어 나므로, 생성형 AI 를 파인튜닝한다면 us-east-1 에서 학습을 하고 서울 리전으로 모델을 복사하는 것이 좋다.)

SDXL 을 사용하기 위해서는 먼저 Amazon Bedrock 에서 모델을 활성화해야 한다. [웹 콘솔](https://us-east-1.console.aws.amazon.com/bedrock/home?region=us-east-1#/modelaccess) 의 i Model access 페이지에서 `Manage model access` 버튼을 클릭한다.

![](/assets/img/2024/0207/console.png)

그리고 SDXL 1.0 모델을 선택하고 `Save changes` 버튼을 클릭한다.

![](/assets/img/2024/0207/model-access.png)

위의 과정은 마켓플레이스에서 모델을 구독하는 과정을 대신해주는 거라고 생각하면 된다.

사실 이 후부터는 웹 콘솔의 [Playground](https://us-east-1.console.aws.amazon.com/bedrock/home?region=us-east-1#/image-playground?modelId=stability.stable-diffusion-xl-v1) 에서 모델을 생성할 수도 있지만 streamlit 을 통하면 훨씬 재미있는 것들을 많이 할 수 있다.

![](/assets/img/2024/0207/playground.png)

## Streamlit + Bedrock SDXL

전체 코드는 여기[^1] 에서 확인할 수 있고, 해당 코드는 다양한 언어로 된 프롬프트를 지원하는 Amazon Bedrock SDXL 기반 UI 를 제공하는 예제이다.

Amazon Bedrock SDXL 은 한글 프롬프트를 인식하지 못한다. 그래서 한글로 된 프롬프트를 사용하려면 적절히 영어로 번역해줘야 한다.

Amazon Bedrock 의 Claude 를 통해 번역을 할수도 있겠지만, Amazon Translate 를 사용해서 번역하는 것이 더 비용효율적이므로 여기서는 Amazon Translate 를 사용한다.

streamlit 특성상 코드가 매우 직관적이고 간단하다. 따라서 여기서는 특이한 부분 한두개만 소개하고 넘어간다.

### Amazon Translate 로 다국어 번역하기

영어가 아닌 글자가 포함되어 있을 때만 번역을 하도록 만들었다. 소스 언어를 `auto` 로 하면 자동으로 언어를 인식해서 번역해준다.

```python
...

pattern = re.compile(r'[^a-zA-Z0-9 ,.]+')

# if text does contains only English letters, return as is
if not pattern.search(text):
    print('text is in English')
    return text
else:
    L = []
    for t in text.split(', '):
        response = self.client.translate_text(
            Text=t.strip(),
            SourceLanguageCode="auto",
            TargetLanguageCode=target_language,
        )
        L.append(response.get("TranslatedText", ""))
    return ', '.join(filter(None, L))
```

### 글로벌 네거티브 프롬프트 사용하기

civit.ai[^2] 같은 서비스에서 다양한 프롬프트와 네거티브 프롬프트를 찾을 수 있다.

프롬프트는 엄청 다양하기 때문에 글로벌 프롬프트라고 부를만한 내용이 없지만, 네거티브 프롬프트는 어느정도 통용되는 내용이 있다.

여기서는 다음과 같이 잘 알려진 공용 네거티브 프롬프트를 사용했다.

```python
image = None
with st.spinner("Generating image based on prompt"):
    image = sdxl.generate_image_from_prompt(
        prompt=prompt,
        negative_prompts=[
            'ugly,', 'tiling,', 'poorly', 'drawn', 'hands,',
            'poorly', 'drawn', 'feet,', 'poorly', 'drawn',
            'face,', 'out', 'of', 'frame,', 'extra', 'limbs,',
            'disfigured,', 'deformed,', 'body', 'out', 'of',
            'frame,', 'bad', 'anatomy,', 'watermark,', 'signature,',
            'cut', 'off,', 'low', 'contrast,', 'underexposed,',
            'overexposed,', 'bad', 'art,', 'beginner,', 'amateur,',
            'distorted', 'face',
        ],
    )
    st.success("Generated stable diffusion model")

if image:
    st.image(image)
```

### 테스트

이제 streamlit 을 실행하고,

```python
$ streamlit run app.py
```

웹브라우저에서 `http://localhost:8501` 로 접속하면 다음과 같은 화면을 볼 수 있다.

![](/assets/img/2024/0207/streamlit-landing.png)

왼쪽 사이드바에서 원하는 프롬프트를 선택해보거나, 아무 언어로 프롬프트를 직접 입력해보자.

#### 한글예제

```python
...
source:  검은색 대리석 벽과 타일로 구성된 럭셔리한 화장실
translated:  Luxurious bathroom with black marble walls and tiles
```

![](/assets/img/2024/0207/streamlit-prompt1.png)

#### 일본어예제

```python
...
source:  黒い大理石の壁とタイルで構成された豪華なトイレ
translated:  Luxurious toilet with black marble walls and tiles
```

![](/assets/img/2024/0207/streamlit-prompt2.png)

## 마치며

위에 이미지들의 하단은 캡쳐하는 과정에서 잘린 것이다. 원본은 깨끗하게 바닥까지 내려가는 이미지이다.

---

[^1]: [streamlit-bedrock-sdxl-example](https://github.com/haandol/streamlit-bedrock-sdxl-example)
[^2]: [civit.ai](https://civit.ai/)
