---
layout: post
title: "OpenAI Symphony의 탄생 배경과 동작 원리"
excerpt: From supervising Codex sessions to reviewing work on a project board
author: haandol
email: ldg55d@gmail.com
tags: openai symphony codex software-factory agentic-engineering
publish: true
published: true
date: 2026-11-24 17:36:13 +0900
last_modified_at: 2026-11-25 09:08:50 +0900
lang: ko
translation_key: openai-symphony-issue-workflow
english_url: /en/2026/11/24/openai-symphony-issue-workflow.html
---

## TL;DR

- Symphony는 팀의 작업 보드에 올라온 일을 코딩 에이전트에 맡긴다.
- OpenAI는 사내에서 쓰던 방식을 독립된 명세로 공개했다.
- 팀마다 다른 검증과 인계 절차는 `WORKFLOW.md`에 담긴다.

## 시작하며

**OpenAI Symphony(심포니)는 개발팀의 작업 보드와 코딩 에이전트를 연결하는 오픈소스 프로젝트다.** 예를 들어 개발자가 Linear라는 업무 관리 도구에 버그를 등록하고 작업 대상으로 표시하면, Symphony가 별도의 작업 폴더를 마련해 Codex를 실행한다. 개발자는 보드에 올라온 코드 변경 링크와 테스트 결과를 보고 수정을 더 요청하거나 변경을 승인할 수 있다.[^1]

앞서 소프트웨어 팩토리를 다룬 글에서 Symphony를 여러 에이전트에 일을 나눠 주는 예로 짧게 소개했다.[^2] Symphony를 만들기 전, OpenAI 팀의 개발자들은 어떤 일이 끝났고 어떤 일이 멈췄는지 확인하려고 Codex 대화창을 하나씩 열어 봐야 했다.[^1]

## 1. 사내 개발 실험에서 공개 명세가 되기까지

2025년 8월 말, OpenAI의 한 팀이 사내 생산성 도구를 만들면서 첫 커밋을 올렸다. 팀에는 ‘저장소의 모든 코드는 Codex가 작성한다’는 원칙이 있었다. 엔지니어는 Codex가 필요한 문서와 도구를 찾을 수 있게 저장소를 정리하고, 잘못 고쳤을 때 스스로 알아챌 수 있게 자동 검사를 갖췄다.[^3][^1]

팀의 회고에 따르면 개발자 한 사람이 무리 없이 챙길 수 있는 Codex 세션은 대개 3~5개였다. 그보다 많아지면 어느 창에서 무엇을 고치는지 잊거나, 중간에 멈춘 작업을 뒤늦게 발견했다. 팀은 이미 쓰고 있던 Linear 보드에서 에이전트가 직접 할 일을 가져가는 방식을 시험했다.[^1]

Symphony의 첫 버전은 터미널 세션을 계속 띄워 두는 도구인 `tmux` 안에서 돌아가는 Codex 세션 하나였다. 이 세션이 Linear를 주기적으로 확인하고 새 일이 들어오면 하위 에이전트를 띄웠다. 작업을 배정할 수는 있었지만 이 구성을 계속 안정적으로 돌리기는 어려웠다. 팀은 에이전트용 도구와 테스트가 갖춰진 사내 제품 저장소에 두 번째 버전을 만들었다. 기본 기능이 돌아간 뒤에는 **Symphony를 개선하는 작업도 Symphony에 맡겼다.**[^1]

사내 시연에서 에이전트는 작업을 마친 뒤 기능이 실제로 작동하는 영상을 티켓에 첨부했다. 이후 다른 팀들도 자발적으로 Symphony를 쓰기 시작하자 개발팀은 회사 밖에도 공개하기로 했다.[^1]

개발팀은 사내 저장소에 의존하던 부분을 덜어내고 핵심 동작을 `SPEC.md`라는 **명세**로 정리했다. 공개 저장소의 **Elixir 참조 구현**은 Codex에 이 명세를 주고 만들게 한 프로그램이다. 다른 팀은 같은 명세를 바탕으로 자기 환경에 맞는 서비스를 만들 수 있다.[^1]

## 2. 계속 실행되는 서비스와 작업마다 뜨는 Codex

Symphony의 Elixir 참조 구현은 계속 떠 있는 **데몬**이다. 개발자가 Linear나 GitHub Issues 같은 이슈 트래커에 일을 등록하면, 이미 실행 중인 데몬이 보드를 주기적으로 읽어 맡길 일을 찾는다. 개발자가 이슈를 만들 때마다 Symphony를 실행할 필요가 없는 이유다.[^4]

데몬을 처음 띄우기 전에 개발팀은 프로젝트 저장소에 **`WORKFLOW.md`**를 준비한다. OpenAI는 예제 파일을 복사해 팀이 쓰는 보드, 복제할 저장소, 검사와 리뷰 절차에 맞게 고치는 방법을 안내한다. 예를 들어 운영자가 프로젝트를 실행 서버의 `/srv/encbird`에 받아 뒀다면, 데몬을 시작할 때 `/srv/encbird/WORKFLOW.md`를 경로 인자로 넘긴다. 경로를 생략하면 프로세스를 시작한 디렉터리의 `WORKFLOW.md`를 사용한다.[^10][^13]

데몬은 이 파일에서 **팀의 실행 설정과 Codex 지시문을 함께 읽는다.** 워크플로 로더가 앞부분의 YAML 설정과 그 아래의 Markdown 본문을 분리한다. 데몬은 설정을 검증한 뒤 보드 조회를 시작하고, 본문은 나중에 각 이슈의 지시문을 만들 템플릿으로 보관한다.[^4][^10]

서비스 안에서 **오케스트레이터**는 어떤 작업을 언제 시작하고 멈출지 결정한다. 어댑터는 Linear와 GitHub에서 가져온 이슈를 오케스트레이터가 읽을 수 있는 공통 형식으로 바꿔 준다. 오케스트레이터가 일을 배정하면 **에이전트 러너**가 작업 공간 관리자에게 해당 이슈의 폴더를 요청하고, 그 안에서 Codex와 대화를 시작한다. 서로 다른 두 작업을 동시에 맡기면 같은 팀 규칙을 읽은 Codex 세션 둘이 각자 자기 폴더에서 코드를 고친다.[^4][^6]

{% raw %}
```mermaid
flowchart TD
    T["이슈 트래커"] -->|"현재 상태"| O["오케스트레이터"]
    W["팀 저장소의 WORKFLOW.md"] -->|"시작 시 지정한 경로"| L["데몬의 워크플로 로더"]
    L -->|"실행 조건·한도"| O
    subgraph R["작업별 러너"]
        A["러너 A<br/>폴더 A에서 Codex 실행"]
        B["러너 B<br/>폴더 B에서 Codex 실행"]
    end
    L -->|"폴더 준비 명령·지시문 템플릿"| R
    O -->|"작업 A 배정"| A
    O -->|"작업 B 배정"| B
    A -.->|"실행 결과"| O
    B -.->|"실행 결과"| O
    R -.->|"Codex가 도구로 검토 요청을 기록"| T
```
{% endraw %}

**트래커**에는 팀이 보는 진행 상태가, **오케스트레이터의 메모리**에는 현재 실행 중인 작업과 재시도 예약이, **작업 폴더**에는 에이전트가 고친 파일이 있다. 사람이 트래커에서 작업을 취소하면 오케스트레이터는 그 변경을 읽어 실행을 멈춘다. 구현을 마친 Codex는 트래커 도구를 호출해 검토를 요청한다. 이 도구가 Symphony를 실행하는 호스트의 자격 증명으로 결과를 기록하면, 사람과 오케스트레이터가 같은 상태를 볼 수 있다.[^4][^7]

## 3. WORKFLOW.md가 실행 설정과 Codex의 첫 요청이 되는 과정

아래는 OpenAI가 Symphony 저장소 개발에 쓰는 예제에서 일부를 뽑은 것이다. 위쪽 설정에는 러너를 언제 몇 개 띄울지와 빈 작업 폴더에 어떤 코드를 가져올지가 들어 있다. 아래쪽에는 Codex에게 건넬 문장이 있다.[^5]

{% raw %}
```markdown
---
tracker:
  active_states: [Todo, In Progress, Merging, Rework]
polling:
  interval_ms: 5000
hooks:
  after_create: |
    git clone --depth 1 https://github.com/openai/symphony .
agent:
  max_concurrent_agents: 10
---
You are working on a Linear ticket `{{ issue.identifier }}`
Title: {{ issue.title }}
```
{% endraw %}

**작업을 고를 때** 오케스트레이터는 5초마다 Linear를 조회해 `active_states`에 속하는 일을 찾는다. 예제의 동시 실행 한도는 열 개다. 이미 열 개가 실행 중이면 새 후보는 기다린다. 배정이 이뤄져 새 폴더를 만들면 작업 공간 관리자가 `after_create`의 명령을 그 폴더에서 실행한다. 이 예제는 Symphony 자체를 복제하므로 다른 프로젝트에 쓸 때는 팀이 복제 주소도 바꾼다.[^5][^6]

**첫 턴을 시작할 때** 러너는 데몬이 보관한 본문 템플릿과 방금 배정한 이슈를 가져온다. 예를 들어 Linear 이슈 번호가 `ENG-42`이고 제목이 ‘주간 학습 리포트’라면, Codex가 받는 첫 메시지에는 ‘You are working on a Linear ticket `ENG-42`’와 ‘Title: 주간 학습 리포트’가 들어간다. 전체 예제의 본문에는 이슈 설명과 현재 상태를 넣는 자리도 있다. 러너는 이 값들을 채운 메시지를 `codex app-server`에 보내 Codex의 첫 턴을 시작한다. 같은 대화에서 다음 턴을 열 때는 원래 지시가 남아 있으므로 이어서 작업하라는 안내만 보낸다.[^5][^12][^14]

이 지시문에 따라 Codex는 새 `Todo` 이슈를 `In Progress`로 옮기고 **`Codex Workpad`라는 댓글 하나**에 계획과 완료 조건, 실행할 검사를 적는다. 이슈에 테스트 방법이 있으면 검증 목록에 포함하고, 진행 상황은 같은 댓글을 갱신해 남긴다.[^5]

Codex는 변경 검토 요청(PR)을 이슈에 연결하고, 최신 커밋의 검사 결과와 리뷰 의견을 확인한다. 코드에 반영할 의견이 남았으면 고친 뒤 다시 검사한다. 검사가 통과하고 리뷰 의견을 모두 처리하면 이슈를 `Human Review`로 옮긴다. **이 상태는 위 설정의 활성 상태 목록에 없으므로** 오케스트레이터는 실행을 멈추고 사람이 결과를 검토할 차례가 된다.[^5]

리뷰어가 승인해 `Merging`으로 옮기면 Codex는 예제에 지정된 절차로 PR을 병합한 뒤 이슈를 `Done`으로 옮긴다. 리뷰어가 수정을 요청해 `Rework`로 보내면 Codex는 이슈와 리뷰 의견을 다시 읽고 기존 PR을 닫는다. 이 예제에서는 최신 `main`에서 새 브랜치를 만들고 새 Workpad 댓글에 계획을 적어 작업을 다시 시작한다.[^5]

## 4. 여러 세션을 돌리고 중단된 작업을 복구하는 방식

### 실행할 작업을 고를 때

오케스트레이터는 매 조회 주기마다 이미 실행 중인 작업부터 트래커와 대조한다. 그사이 실행 대상에서 빠진 작업은 멈춘다. 그런 다음 활성 상태와 필수 라벨을 만족하는 후보를 우선순위순으로 살핀다. 순위가 같으면 먼저 만들어진 이슈가 앞선다. 이미 실행 중이거나 재시도를 예약한 이슈는 건너뛰고, 전체 한도와 해당 상태의 한도에 자리가 있을 때만 러너를 띄운다. 팀이 조회 간격을 따로 정하지 않으면 명세의 기본값인 30초를 쓴다.[^4][^5][^6]

예를 들어 OpenAI 팀은 Linear에서 React 업그레이드의 선행 작업으로 Vite 마이그레이션을 지정했다. Elixir의 Linear 어댑터는 `Todo` 이슈에 아직 종료되지 않은 선행 작업이 있으면 배정 불가로 표시한다. 오케스트레이터는 그 이슈를 건너뛰고 독립적으로 시작할 수 있는 일을 고른다.[^1][^11]

### Codex가 코드를 고치는 동안

러너는 이슈 식별자로 작업 폴더를 찾아 열거나 새로 만든다. 두 에이전트가 동시에 같은 파일을 고쳐도 서로의 미완성 변경이 테스트에 섞이지 않도록 작업 사본을 나누는 것이다. 새 폴더에서 한 번만 실행하는 명령을 `after_create` 훅에 둔다. OpenAI 예제는 여기서 Symphony 저장소를 복제한다. 기존 폴더에서 다시 시도할 때도 필요한 준비는 `before_run`에 둔다. Codex가 그 폴더 밖에 쓰거나 네트워크에 접근할 수 있는 범위는 별도의 샌드박스 설정에서 정한다.[^5][^6]

준비가 끝나면 러너가 이 폴더에서 `codex app-server`를 띄운다. Elixir 구현은 먼저 연결을 초기화하고 `thread/start`로 대화를 연다. 이어 `turn/start`로 이슈 내용과 팀 지시문을 보내면 Codex가 한 번의 요청을 처리하기 시작한다. 이 요청에서 응답까지가 한 **턴**이다.[^12]

{% raw %}
```mermaid
sequenceDiagram
    participant T as 작업 보드
    participant R as 러너
    participant C as Codex
    R->>C: 작업 폴더에서 대화를 열고 첫 요청 전달
    C->>C: 코드와 테스트를 읽고 변경
    C->>C: 검사 실패 시 수정하고 재검사
    C->>T: 트래커 도구로 진행 상황과 검증 결과 기록
    C-->>R: 턴 종료 이벤트
    R->>T: 현재 상태와 배정 조건 다시 조회
    alt 여전히 실행 대상이고 턴 한도가 남음
        R->>C: 같은 대화에서 다음 턴 시작
    else 검토 대기 또는 턴 한도 도달
        R->>C: 세션 종료
    end
```
{% endraw %}

검사에서 기대값과 다른 결과가 나오면 **Codex**가 출력을 읽고 수정할 파일을 고른다. 한 턴 안에서 여러 번 고치고 검사할 수 있다. 그동안 러너는 진행 이벤트를 오케스트레이터에 전한다. **턴이 끝나면 러너가 트래커를 다시 읽는다.** 이슈가 여전히 실행 대상이고 턴 한도(기본 20턴)가 남아 있으면 같은 대화를 이어간다.[^4][^6][^12]

### 실행이 끊겼을 때 남는 것

오케스트레이터는 러너가 왜 멈췄는지와 Codex가 마지막으로 보낸 이벤트를 확인한다. 러너가 살아 있어도 설정한 시간(기본 5분) 동안 새 이벤트가 오지 않으면 실행을 중단한다. 이때 마지막 기록이 사람에게 입력이나 승인을 요청한 것이었는지에 따라 재시도 여부가 갈린다.[^4][^6]

| 실행이 멈춘 상황 | 오케스트레이터의 다음 동작 |
| --- | --- |
| 러너가 정상 종료했고 사람에게 요청한 입력이나 승인이 없다 | 1초 뒤 이슈를 다시 확인한다. 여전히 대상이고 자리가 있으면 같은 폴더에 **새 세션**을 연다. |
| 사람의 응답을 기다리는 상황이 아닌데 실행 오류나 무응답으로 러너가 멈췄다 | 재시도를 예약한다. 오류가 반복되면 간격을 10초, 20초, 40초처럼 늘린다. |
| 입력이나 승인이 필요하다고 기록된 상태에서 러너가 종료됐다 | 오케스트레이터가 그 이유를 기록하고 작업을 차단 상태로 둔다. 이 경우 재시도 타이머를 잡지 않는다. |
| Symphony 서비스 자체가 재시작됐다 | 메모리에 있던 세션과 타이머는 복구되지 않는다. 트래커를 다시 읽어 종료한 작업의 폴더를 정리하고, 여전히 맡길 일은 남아 있는 폴더에서 다시 시작할 수 있다. |

새 세션이 열리면 직전 대화의 맥락까지 돌아오지는 않는다. 예제 워크플로에서 다음 Codex가 먼저 확인하는 것은 **Workpad에 적힌 남은 검사, 작업 폴더의 변경 내용, 이슈에 이미 연결된 PR**이다. 예컨대 PR을 여는 도중 연결이 끊겼다면 에이전트는 해당 브랜치에 PR이 이미 생겼는지 확인한 뒤 작업을 이어간다. 운영자는 로그의 이슈·세션 식별자로 마지막 이벤트와 재시도 사유를 확인할 수 있다.[^5][^6][^8]

## 5. 잉크버드에서 Symphony를 쓴다면

내가 만드는 영어 학습 앱 잉크버드(EncBird)는 검증한 변경을 기본 저장소의 로컬 `main`에 먼저 합치고, 원격 저장소에 올리거나 배포하려면 별도 요청을 받는다.

잉크버드에 Symphony를 연결하고 GitHub 이슈 600번으로 **주간 학습 리포트**를 요청한다고 해 보자. 이슈 본문에는 ‘지난 7일의 총 학습 시간과 자주 틀린 표현 다섯 개, 다음 주에 연습할 표현을 보여준다. 모바일에서도 세 항목을 읽을 수 있다’고 적는다.

잉크버드에서는 열린 이슈 중 `symphony` 라벨이 붙은 일만 맡기도록 설정할 수 있다. 다음 조회 때 자리가 있으면 러너는 `GH-600` 폴더를 준비한다. `after_create`에서 기본 저장소의 로컬 `main`을 복제하고 작업 브랜치를 만들면, 아직 원격에 올리지 않은 변경도 포함된다. 이 폴더에서 실행된 Codex는 이슈에 적힌 완료 조건을 Workpad의 검증 목록으로 옮긴다.[^9]

오늘 20분, 6일 전 10분, 7일 전 5분의 학습 기록을 넣어 보자. 오늘을 포함한 최근 7일의 합계는 30분이다. 리포트에 35분이 표시되면 기간 밖의 5분까지 더한 것이다. Codex는 날짜 조건을 고치고 같은 검사를 다시 돌린다.

합계 검사를 마친 뒤 모바일 화면을 확인하기 전에 세션이 끊겼다면 어떨까? Workpad에는 ‘7일 합계 확인, 모바일 확인 남음’이 적혀 있고 작업 폴더에는 고친 코드가 남아 있다. 새 세션은 이 둘을 대조한 뒤 모바일 검사를 이어갈 수 있다.

이 팀이 검토할 결과물은 작업 폴더의 로컬 커밋이다. 주간 합계와 표현 목록, 모바일 화면까지 확인한 Codex는 웹 앱의 타입 검사·테스트·빌드 결과와 커밋 번호를 이슈에 남긴다. **마지막에** `symphony`를 `human-review` 라벨로 교체한다. 필수 라벨을 먼저 떼면 다음 조회에서 러너가 멈춰 커밋이나 검사 기록을 남길 기회를 잃을 수 있기 때문이다.[^4][^9]

리뷰어가 수정을 요청하면 의견을 댓글로 남기고 `symphony` 라벨을 되돌린다. 새 세션이 같은 폴더의 코드와 댓글을 읽어 다시 작업할 수 있다. 승인하면 `GH-600` 밖의 기본 저장소에 변경을 합친 뒤 이슈를 닫는다. 종료된 작업의 폴더는 Symphony의 정리 대상이다.[^4][^9]

## 6. 새 작업 규칙이 Symphony에 적용되는 시점

리포트 변경을 검토할 때마다 리뷰어가 “7일 범위 바깥의 기록도 넣어 봤나요?”라고 묻는다면, `WORKFLOW.md`에 기간의 양 끝을 확인한 결과를 남기도록 적을 수 있다. 이 변경도 에이전트에 맡겨 리뷰를 받을 수 있다.

Codex가 고친 파일은 작업 폴더에 있다. Symphony가 읽는 것은 **서비스를 시작할 때 지정한 경로의 파일**이다. 잉크버드 예시에서 그 경로가 기본 저장소의 `WORKFLOW.md`라면, 검토한 변경을 로컬 `main`에 합칠 때 서비스가 읽는 파일도 바뀐다. 원격 저장소를 거쳐 별도의 운영 서버로 배포하는 팀이라면, 원격 `main`에 병합한 뒤 서버의 사본까지 갱신해야 한다.[^10]

{% raw %}
```mermaid
flowchart TD
    A["검토를 마친 WORKFLOW.md"] -->|"서비스가 읽는 로컬 main에 병합"| C["Symphony가 읽는 WORKFLOW.md"]
    A -->|"원격을 통해 배포하는 팀"| B["원격 main에 병합"]
    B -->|"운영 서버의 사본 갱신"| C
    C -->|"다시 읽고 검증해 적용"| D["다음 실행 · 새 규칙으로 작업"]
```
{% endraw %}

참조 구현의 `WorkflowStore`는 지정한 경로의 파일이 바뀌었는지 주기적으로 확인한다. 파일이 바뀌면 다시 읽어 설정을 검증하고, 유효한 설정과 본문 템플릿을 함께 보관한다. 서비스나 진행 중인 세션을 다시 띄우지 않고도 다음 작업에 새 지시문을 보낼 수 있다. 동시 실행 한도를 바꾸면 이후 배정에 반영된다. `after_create`를 바꾸면 다음에 폴더를 만들 때 호스트가 실행할 명령도 달라진다. 파일을 다시 읽다가 오류가 나면 마지막 정상 설정을 보관하고 운영자에게 오류를 알린다.[^10]

잉크버드의 리포트 화면은 앱을 배포해야 사용자에게 바뀐 모습으로 보인다. 오케스트레이터의 배정 알고리즘을 고쳤다면 Symphony를 새 버전으로 배포해야 한다. 리포트를 어떻게 검사하고 넘길지만 바꿀 때는 `WORKFLOW.md`를 갱신하면 된다.

## 마치며

OpenAI의 회고에서 가장 흥미로웠던 건 PM과 디자이너가 Symphony를 쓰는 방식이다. 원하는 기능을 작업 보드에 적으면, 실제 제품에서 그 기능을 써 보는 영상이 검토 자료로 돌아온다.[^1] 기능을 요청한 사람이 Codex 세션을 열 줄 몰라도 “내가 원한 동작이 맞다”거나 “이 부분은 고쳐 달라”고 직접 말할 수 있다.

이 방식을 여러 팀이 쓰는 프로덕션 서비스로 옮기려면 손볼 곳이 많다고 생각한다. OpenAI도 Elixir 참조 구현을 평가용 프로토타입으로 소개한다. 기본 로컬 구성에서는 데몬이 배정·재시도 상태를 메모리에 두고, 러너는 호스트에서 Codex 프로세스를 띄운다. 잉크버드 예시에서 7일 합계 검사를 끝낸 직후 서버를 교체했다고 해 보자. 새 데몬은 보드를 읽어 이슈를 다시 배정할 수 있다. 하지만 새 Codex 세션이 Workpad에서 ‘모바일 검사 남음’을 읽어도, 수정한 파일이 이전 서버의 임시 디스크에만 있었다면 검사할 코드가 사라진 뒤다.[^8][^13]

클라우드 네이티브 환경에서는 **작업을 배정할 권한과 교체된 워커가 이어받을 작업 사본**부터 설계할 필요가 있다. 같은 보드를 보는 데몬 두 개가 각자 메모리로만 배정을 관리하면 같은 이슈에 러너를 하나씩 띄울 수 있다. 한 가지 방법은 리더로 선출된 데몬 하나가 작업을 배정하고, 실제 코드를 고치는 워커는 작업별 컨테이너로 분리해 필요한 만큼 늘리는 것이다. 작업 폴더를 이슈별 영속 볼륨에 두면 서버가 바뀌어도 다음 워커가 같은 폴더를 다시 연결할 수 있다. 새 워커는 합계 검사를 통과한 파일을 열고 Workpad에 남은 모바일 검사부터 이어갈 수 있다.

[^1]: Alex Kotliarskyi, Victor Zhu, Zach Brock, OpenAI. [An open-source spec for Codex orchestration: Symphony](https://openai.com/index/open-source-codex-orchestration-symphony/), 2026-04-27.
[^2]: [AWS Emulator로 배우는 소프트웨어 팩토리 구축](/2026/11/16/building-software-factory-with-aws-emulator.html)
[^3]: Ryan Lopopolo, OpenAI. [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/), 2026-02-11.
[^4]: OpenAI Symphony 명세 Draft v1 및 Elixir 참조 구현 (`be10a1b`). [전체 구조와 설계 목표](https://github.com/openai/symphony/blob/be10a1b79df723d6d7612b5651c8522704dafb2e/SPEC.md#3-system-overview), [배정과 재조정](https://github.com/openai/symphony/blob/be10a1b79df723d6d7612b5651c8522704dafb2e/SPEC.md#8-polling-scheduling-and-reconciliation)
[^5]: OpenAI Symphony. [Elixir 참조 구현의 WORKFLOW.md](https://github.com/openai/symphony/blob/be10a1b79df723d6d7612b5651c8522704dafb2e/elixir/WORKFLOW.md)
[^6]: OpenAI Symphony. [Orchestrator](https://github.com/openai/symphony/blob/be10a1b79df723d6d7612b5651c8522704dafb2e/elixir/lib/symphony_elixir/orchestrator.ex), [AgentRunner](https://github.com/openai/symphony/blob/be10a1b79df723d6d7612b5651c8522704dafb2e/elixir/lib/symphony_elixir/agent_runner.ex), [Workspace](https://github.com/openai/symphony/blob/be10a1b79df723d6d7612b5651c8522704dafb2e/elixir/lib/symphony_elixir/workspace.ex)
[^7]: OpenAI Symphony. [트래커 도구 호출과 인증](https://github.com/openai/symphony/blob/be10a1b79df723d6d7612b5651c8522704dafb2e/SPEC.md#105-approval-tool-calls-and-user-input-policy)
[^8]: OpenAI Symphony. [실행 로그와 상태 관찰](https://github.com/openai/symphony/blob/be10a1b79df723d6d7612b5651c8522704dafb2e/SPEC.md#13-logging-status-and-observability), [서비스 재시작 후 복구](https://github.com/openai/symphony/blob/be10a1b79df723d6d7612b5651c8522704dafb2e/SPEC.md#143-partial-state-recovery-restart)
[^9]: OpenAI Symphony. [GitHub Issues 어댑터](https://github.com/openai/symphony/blob/be10a1b79df723d6d7612b5651c8522704dafb2e/elixir/lib/symphony_elixir/github/adapter.ex), [이슈 식별자와 라벨](https://github.com/openai/symphony/blob/be10a1b79df723d6d7612b5651c8522704dafb2e/elixir/lib/symphony_elixir/github/client.ex)
[^10]: OpenAI Symphony. [워크플로 경로](https://github.com/openai/symphony/blob/be10a1b79df723d6d7612b5651c8522704dafb2e/SPEC.md#51-file-discovery-and-path-resolution), [동적 재적용](https://github.com/openai/symphony/blob/be10a1b79df723d6d7612b5651c8522704dafb2e/SPEC.md#62-dynamic-reload-semantics), [WorkflowStore](https://github.com/openai/symphony/blob/be10a1b79df723d6d7612b5651c8522704dafb2e/elixir/lib/symphony_elixir/workflow_store.ex)
[^11]: OpenAI Symphony. [Linear 어댑터의 선행 작업 판정](https://github.com/openai/symphony/blob/be10a1b79df723d6d7612b5651c8522704dafb2e/elixir/lib/symphony_elixir/linear/client.ex)
[^12]: OpenAI Symphony. [세션 시작과 후속 턴](https://github.com/openai/symphony/blob/be10a1b79df723d6d7612b5651c8522704dafb2e/SPEC.md#102-session-startup-responsibilities), [Codex App Server 클라이언트](https://github.com/openai/symphony/blob/be10a1b79df723d6d7612b5651c8522704dafb2e/elixir/lib/symphony_elixir/codex/app_server.ex)
[^13]: OpenAI Symphony, [Elixir 참조 구현의 용도와 프로젝트별 워크플로 설정](https://github.com/openai/symphony/blob/be10a1b79df723d6d7612b5651c8522704dafb2e/elixir/README.md), [실행 인자와 파일 경로 처리](https://github.com/openai/symphony/blob/be10a1b79df723d6d7612b5651c8522704dafb2e/elixir/lib/symphony_elixir/cli.ex)
[^14]: OpenAI Symphony, [첫 요청에 이슈와 실행 시도 정보를 채우는 PromptBuilder](https://github.com/openai/symphony/blob/be10a1b79df723d6d7612b5651c8522704dafb2e/elixir/lib/symphony_elixir/prompt_builder.ex), [첫 턴과 후속 턴을 구분하는 AgentRunner](https://github.com/openai/symphony/blob/be10a1b79df723d6d7612b5651c8522704dafb2e/elixir/lib/symphony_elixir/agent_runner.ex)
