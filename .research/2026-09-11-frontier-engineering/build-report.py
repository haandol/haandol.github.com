from pathlib import Path
from html import escape
import json
from datetime import datetime
from zoneinfo import ZoneInfo

root = Path(__file__).parent
data = json.loads((root / "report-data.json").read_text())
sources = {s["id"]: s for s in data["sources"]}

def refs(*ids):
    return '<span class="refs">' + " ".join(
        f'<a href="#source-{i}" title="{escape(sources[i]["title"])}">[{i}]</a>'
        for i in ids
    ) + "</span>"

def p(text, *ids):
    return f"<p>{text} {refs(*ids) if ids else ''}</p>"

cards = []
for item in data["principles"]:
    n = item["n"]
    source = sources[f"K{n}"]
    cards.append(f"""
    <article class="principle" id="principle-{n}">
      <div class="card-top"><span class="number">{n:02}</span><span class="tag">{escape(item["verdict"])}</span></div>
      <h3>{escape(item["title"])}</h3>
      <p class="english"><a href="{source["url"]}">{escape(source["title"])}</a></p>
      <dl>
        <dt>원문 요약</dt><dd>{escape(item["summary"])} {refs(f"K{n}")}</dd>
        <dt>현재 글과 비교</dt><dd>{escape(item["user"])} {refs(f"K{n}")}</dd>
        <dt>AI-DLC와 비교</dt><dd>{escape(item["aidlc"])} {refs(*item["refs"])}</dd>
      </dl>
    </article>
    """)

source_list = "".join(
    f'<li id="source-{s["id"]}"><strong>{s["id"]}</strong> '
    f'<a href="{s["url"]}">{escape(s["title"])}</a></li>'
    for s in data["sources"]
)

body = f"""
<header>
  <p class="eyebrow">자료 비교 · 2026년 9월 11일 확인</p>
  <h1>Kiro Frontier Engineering은<br>현재 주장의 근거가 될까?</h1>
  <p class="lead">반복적인 사람 개입을 줄이자는 주장에는 강한 근거가 된다. 다만 사람이 방향과 결과를 판단하는 역할은 유지하며, 명세·작업 지침·AI 리뷰어도 권장하므로 AI-DLC 전체를 반대하는 글로 쓰기는 어렵다. {refs("K2","K5","K7","K8","K10")}</p>
  <div class="scope">읽은 범위: 상위 안내 1개 + 하위 원칙 10개 전체, AWS 공식 글 2개, 현재 AI-DLC 저장소 문서 3개.<br>
  비교 대상: 9월 6일 「AWS AI-DLC에 대한 단상」의 현재 내용, 보조적으로 8월 31일 「Frontier Development의 다섯 습관」.<br>
  아래의 ‘지지·부분 지지·차이’는 자료를 대조한 해석이며, Kiro가 이 블로그 글이나 AI-DLC를 직접 평가한 결과가 아니다.</div>
</header>
<nav aria-label="보고서 목차">
 <a href="#conclusion">판정</a><a href="#ten">10개 원칙</a><a href="#approval">승인 위치 비교</a>
 <a href="#claims">현재 글의 주장별 검토</a><a href="#quotes">직접 인용</a><a href="#limits">근거의 한계</a><a href="#sources">원문</a>
</nav>
<main>
<section id="conclusion">
 <h2>근거로 쓰되, 무엇의 근거인지 좁혀야 한다</h2>
 {p("현재 글의 중심을 <strong>‘사람이 반복해서 개입하던 일을 도구·검증·권한 설계로 줄여간다’</strong>로 잡으면 Kiro와 매우 가깝다. 원칙 2는 사람의 역할을 방향 설정과 결과 확인으로 좁혀가라고 하고, 원칙 8은 사람이 지켜보지 않아도 작동하는 권한 제한과 자동 검사를 요구한다. 원칙 10은 새 모델에서 예전 모델의 임시방편이 여전히 필요한지도 다시 보라고 한다.","K2","K8","K10")}
 {p("반대로 <strong>‘좋은 에이전틱 개발에는 사람의 검토·명세·리뷰어·작업 절차가 필요 없다’</strong>로 넓히면 이 자료와 맞지 않는다. Kiro는 사람이 의도와 완료 조건을 정하고 결과를 확인해야 한다고 하며, 방향을 정한 뒤 명세를 쓰고 AI 리뷰어와 작업 지침을 활용하도록 한다. 현재 글은 모든 사람이나 모든 절차를 당장 없애자는 글은 아니므로, 그 구분을 더 선명하게 쓰는 편이 좋다.","K1","K3","K5","K7")}
 {p("따라서 AI-DLC와의 가장 분명한 비교 지점은 <strong>‘사람이 중요한가’가 아니라 ‘어떤 지점에서 사람의 응답을 계속 기다리게 하는가’</strong>다. 목표와 품질에 대한 사람의 책임은 공통이지만, Kiro는 실행 중 개입을 줄이고 위험한 행동에 승인을 좁혀가라고 하는 반면 AI-DLC는 선택된 단계가 끝날 때의 승인도 유지한다.","K2","K7","K8","A2","A4")}
 <div class="summary-grid">
   <div><h3>강하게 인용할 수 있음</h3><p>반복 개입 축소 · 빠른 자동 검증 · 제한된 권한 · 오래된 하네스 규칙 재검토</p>{refs("K2","K4","K8","K10")}</div>
   <div><h3>다른 근거가 더 필요함</h3><p>고객 피드백을 받는 기능 단위가 항상 더 낫다는 주장 · 특정 절차가 생산성을 낮춘다는 인과관계</p>{refs("K4","K5","K6","K0")}</div>
   <div><h3>반대 근거도 함께 읽어야 함</h3><p>명세 작성과 AI 리뷰어, 필요한 작업 절차를 불필요하다고 일반화하는 주장</p>{refs("K3","K5","K7")}</div>
 </div>
</section>
<section id="overview">
 <h2>상위 페이지가 말하는 변화</h2>
 {p("상위 안내는 도구만 바꾸는 개발자와 일하는 방식을 바꾸는 개발자를 구분하며, 직접 코드를 작성하는 데서 에이전트가 코드를 만들 수 있는 환경을 준비하는 쪽으로 일이 이동한다고 설명한다. 그 환경을 만들려면 지침 작성, 코드 정리, 작업 범위 설정에 몇 주의 투자가 필요하고 초기에는 오히려 느릴 수 있다고 한다.","K0")}
 {p("동시에 사람의 주의력과 판단이 계속 필요하다고 본다. 여러 에이전트 사이에서 맥락을 전환하고 품질을 유지해야 하며, 에이전트 결과를 가장 잘 검토하는 방법도 아직 정립되지 않았다고 인정한다. 이는 완성된 무인 개발 표준이나 생산성 비교 연구가 아니라, 현재 실무에서 권장하는 방향을 설명한 안내다.","K0")}
</section>
<section id="ten">
 <h2>하위 10개 원칙 전체</h2>
 <p>각 항목에서 Kiro가 실제로 말한 내용과, 현재 글 및 AI-DLC와 비교한 해석을 분리했다.</p>
 {''.join(cards)}
</section>
<section id="approval">
 <h2>가장 분명한 차이: 사람의 승인이 들어가는 위치</h2>
 {p("아래는 두 자료의 차이를 설명하기 위한 단순화한 그림이다. Kiro도 사람이 결과를 확인하고 되돌릴 수 없는 작업을 승인하며, AI-DLC도 단계 안에서는 에이전트가 스스로 작업할 수 있다. 따라서 ‘완전 무인 대 완전 수동’의 비교가 아니다.","K2","K7","K8","A2","A4")}
 <figure>{(root / 'approval-flow.svg').read_text()}<figcaption>현재 AI-DLC 승인 문서는 초기화 3개 단계를 예외로 둔다. 생략된 단계가 아니라 실제로 선택해 실행하는 단계의 승인 위치를 비교했다. Kiro의 결과 검토는 비동기로 할 수 있고, 위험 행동의 승인은 그 행동 전에 둔다. {refs("K2","K8","A3","A4")}</figcaption></figure>
 <details><summary>Mermaid 원문 보기</summary><pre>{escape((root / 'approval-flow.mmd').read_text())}</pre></details>
 <h3>2025년 공식 설명과 현재 구현 문서를 구분해서 읽기</h3>
 {p("2025년 7월 소개 글은 AI가 계획·질문·구현을 주도하면서 사람이 중요한 판단을 확인하는 방식을 설명하고, 기존보다 짧은 작업 기간과 빠른 피드백도 강조한다. 11월 글은 불필요한 단계·문서·승인을 비판하면서 작업에 맞게 단계를 선택하도록 하되, 각 단계의 계획과 결과를 사람이 검토하고 승인하는 흐름은 명시적으로 유지한다.","A1","A2")}
 {p("현재 저장소의 Workflow Profiles 문서는 모든 작업을 동일한 과정에 넣지 않는다. 예를 들어 Express는 설계·작업 분해·일부 전달 계획 등을 건너뛰고 단계 리뷰어 호출도 끈다. 하지만 <strong>AI 리뷰어를 끄는 것과 사람의 승인을 없애는 것은 별개</strong>이며, 승인 문서는 초기화 단계를 제외한 각 단계가 승인으로 끝난다고 설명한다.","A3","A4")}
 {p("현재 문서에는 실수를 규칙이나 자동 검사로 남겨 다음 작업에 반영하는 학습 과정도 있다. 따라서 ‘AI-DLC는 학습 없이 절차만 고정한다’고 쓰는 것도 맞지 않는다. 공통된 수단을 쓸 수 있지만, 어느 판단을 계속 사람에게 맡길지는 다르게 설계하고 있다.","A5","A4","K10")}
 <p class="note">현재 저장소 비교는 2026-09-11 확인 당시 main의 <code>0865300b9de009aea3605f19af5eb6f48c1d343a</code> 문서에 한정한다. 이 커밋이 최신 안정 릴리스와 같다고 확인한 것은 아니며, 실제 설치·실행 검증도 하지 않았다.</p>
</section>
<section id="claims">
 <h2>현재 글에서 유지할 주장과 좁혀 쓸 주장</h2>
 <div class="table-wrap"><table>
 <thead><tr><th>현재 글의 주장</th><th>판정과 이유</th><th>글에 반영할 방향</th></tr></thead>
 <tbody>
 <tr><td>1절: 반복해서 개입하는 사람을 줄여가는 것이 장기 방향</td><td>강한 지지. Kiro가 직접 제시하는 방향이다. 다만 목표·결과·위험에 대한 사람의 판단은 남긴다. {refs("K2","K8")}</td><td>‘HITL 제거’가 목표 설정이나 책임의 제거를 뜻하지 않는다는 현재 설명을 유지하고 원칙 2·8을 붙일 수 있다.</td></tr>
 <tr><td>1절: AI-DLC는 사람 중심이고 내 접근은 에이전트 중심</td><td>해석으로는 가능하지만 구분이 너무 넓다. AI-DLC도 스스로를 AI 중심이라 부르며 AI가 계획과 실행을 주도한다. Kiro 역시 사람의 판단을 유지한다. {refs("A1","A2","K1","K7")}</td><td>명칭보다 ‘반복 승인을 유지하는가, 자동 검증으로 대체해 줄여가는가’를 비교한다.</td></tr>
 <tr><td>2절: 작은 기능을 만들고 고객 피드백을 자주 받는다</td><td>방향은 부분 지지. 두 시제품을 비교하거나 잘못된 제품을 버리는 원칙과 맞지만, 원칙 4의 피드백은 주로 자동 테스트다. {refs("K4","K5","K6")}</td><td>‘코드가 맞는가’와 ‘고객에게 필요한가’를 확인하는 과정을 나눠 설명한다. Kiro가 vertical slice를 유일한 정답으로 제시했다고 쓰지 않는다.</td></tr>
 <tr><td>2절: 경험한 AI-DLC는 큰 원을 더 빨리 돌리는 방식이었다</td><td>개인 경험으로는 유지 가능하지만 방법론 전체의 정의로 쓰기에는 근거가 부족하다. 공식 글도 짧은 작업 기간과 피드백, 불필요한 단계 생략을 말한다. {refs("A1","A2","A3")}</td><td>겪은 워크숍의 작업 단위와 승인 대기를 구체적으로 적고, 모든 AI-DLC 실행에 같은 문제가 있다고 일반화하지 않는다.</td></tr>
 <tr><td>3절: Planner·Reviewer 등은 약한 모델을 절차로 보완하던 시도였다</td><td>특정 방식의 역사적 설명과 모든 리뷰어의 현재 용도를 구분해야 한다. Kiro는 현재도 AI 리뷰어와 작업 절차를 권장한다. {refs("K3","K7")}</td><td>역할 이름이 아니라 실제 효과를 기준으로 비판한다. 필수 검사를 수행하는 리뷰어와 모든 작업에 불필요한 단계를 끼워 넣는 절차는 구분한다.</td></tr>
 <tr><td>3절: 새 모델에서도 남은 옛 제약이 더 나은 판단을 막을 수 있다</td><td>강한 지지. 새 모델에서 옛 임시방편이 필요한지 재검토하라는 문장이 있다. 다만 성능 저하의 실험적 증명은 아니다. {refs("K10")}</td><td>Harness Debt는 저자의 이름임을 유지하고, 원칙 10을 같은 문제의식을 보여주는 자료로 인용한다.</td></tr>
 <tr><td>3절: 하네스는 권한·도구·검증을 제공해야 한다</td><td>강한 지지. 다만 그 하네스에 필요한 작업 절차나 리뷰어가 포함되는 것까지 배제하지 않는다. {refs("K3","K4","K7","K8")}</td><td>얇은 하네스를 ‘기능이 적은 하네스’보다 ‘모델의 선택을 불필요하게 제한하지 않는 하네스’로 설명한다.</td></tr>
 <tr><td>4절: 성과가 있다는 사실만으로 AI-DLC 전체의 효과를 입증할 수 없다</td><td>이 Kiro 안내는 AI-DLC 대비 성과를 측정하지 않으며, 팀 문화와 방법론의 기여를 분리한 연구도 아니다. {refs("K0","K1")}</td><td>공개된 성공 사례를 양쪽 어느 한쪽의 인과적 승리로 사용하는 근거로 삼지 않는다.</td></tr>
 <tr><td>5절: 제품 운영을 함께 책임지고 실패에서 배운다</td><td>강한 지지이면서 AI-DLC와도 공통이다. 배포 이후 감시·수정과 반복 실패의 환경 개선을 함께 권장한다. {refs("K7","K10","A1","A5")}</td><td>내가 찾는 팀의 조건을 설명하는 근거로 쓰되 AI-DLC에 없는 가치라고 쓰지는 않는다.</td></tr>
 </tbody></table></div>
 <h3>주장을 정리한다면</h3>
 <div class="proposal">
 <p>아래 문장은 자료 비교를 바탕으로 한 제안이며, 기존 게시글에는 반영하지 않았다.</p>
 <p>내가 AI-DLC와 가장 다르게 생각하는 부분은 사람이 중요한 결정을 내려야 하는지보다, 실행 중 사람을 기다리는 지점을 얼마나 줄여갈 것인지다. Kiro의 Frontier Engineering도 사람이 방향과 결과를 판단하는 역할은 남겨두되, 테스트와 권한 제한을 갖춰 에이전트가 스스로 일할 수 있는 범위를 넓히라고 한다. 그런 점에서는 내 생각과 가깝지만, 명세 작성이나 AI 리뷰어도 적극 활용하므로 절차를 줄이는 것 자체가 목표라고 해석하고 싶지는 않다. {refs("K2","K5","K7","K8","A4")}</p>
 </div>
</section>
<section id="quotes">
 <h2>특히 직접적인 근거 세 문장</h2>
 <p>각 원문에서 짧은 부분만 발췌했다. 번역은 문맥을 설명하기 위한 것이며 원문 전체를 대체하지 않는다.</p>
 <blockquote><p lang="en">“The goal is to progressively remove yourself from the loop”</p><p>반복 실행 과정에서 사람이 빠져나오는 방향을 목표로 삼는다. 같은 문장의 뒷부분은 방향 설정과 결과 확인을 사람의 역할로 남긴다.</p>{refs("K2")}</blockquote>
 <blockquote><p lang="en">“Every guardrail you automate is one less reason to stay in the loop.”</p><p>안전장치를 자동화할 때마다 사람이 개입해야 할 이유가 하나 줄어든다. 여기서 안전장치는 실제 권한 제한과 보안 검사 등을 포함한다.</p>{refs("K8")}</blockquote>
 <blockquote><p lang="en">“When a new model comes out, re-evaluate whether workarounds you built for the old model’s weaknesses are still necessary.”</p><p>새 모델이 나오면 예전 모델의 약점을 보완하려고 만든 임시방편이 여전히 필요한지 다시 검토한다.</p>{refs("K10")}</blockquote>
</section>
<section id="limits">
 <h2>이 자료로 결론 내릴 수 없는 것</h2>
 {p("이 페이지들은 Kiro가 권장하는 실무 방향을 보여주므로 ‘이런 접근을 공개적으로 권장한다’는 근거가 된다. 그러나 원칙별 효과를 대조군과 비교한 연구가 아니므로, 이 방식이 AI-DLC보다 몇 배 빠르거나 특정 하네스가 성능을 얼마나 떨어뜨리는지는 알 수 없다. 상위 안내 역시 아직 초기 단계이며 리뷰 방법 등이 정립되지 않았다고 말한다.","K0")}
 {p("하위 10개 원칙은 각각 다른 실험의 결과 10개가 아니라 하나의 안내를 나눈 구성이다. 원칙 1의 직접 작성 코드 비율이나 원칙 2의 테스트 커버리지 예시는 보편적인 도입 기준으로 바꾸지 않는 편이 좋다.","K1","K2")}
 {p("읽은 상위 페이지와 하위 10개 원칙에서는 AI-DLC를 직접 명명해 평가하거나 대체한다고 선언하지 않는다. 그래서 ‘Kiro가 AI-DLC를 부정했다’, ‘AWS 전체의 방향이 바뀌었다’, ‘이 페이지가 2025년 AI-DLC 글을 공식적으로 대체했다’는 결론은 낼 수 없다. 비교는 서로 다른 문서가 권장하는 행동을 대조한 해석이다.","K0","K2","K8","A1","A2")}
 <p class="note">Kiro 페이지에서 명시적인 발행일은 확인하지 못했으므로 게시 순서나 정책 변경 시점을 추정하지 않았다. 원칙 페이지에 딸린 제품 사례 링크까지 모두 조사한 것은 아니며, 요청한 상위 안내와 10개 원칙의 본문은 모두 확인했다. 현재 저장소 문서는 2025년 공식 글과 구분해서 보충 자료로 사용했다.</p>
</section>
<section id="sources">
 <h2>확인한 원문</h2>
 <p>모든 비교 자료는 Kiro 또는 AWS 공식 사이트와 AWS Labs 저장소 문서다. 내부 블로그 글은 비교 대상이지 외부 사실의 독립적인 근거로 사용하지 않았다.</p>
 <ol class="sources">{source_list}</ol>
 <p class="note">열람 방법: 이 실행에서 내장 웹 검색을 사용할 수 없어 DuckDuckGo MCP의 본문 추출을 대체 경로로 사용했다. 링크 목록과 저장소 커밋은 원문 HTML 및 GitHub API로 추가 확인했다. 확인 일시: {datetime.now(ZoneInfo('Asia/Seoul')).strftime('%Y-%m-%d %H:%M KST')}.</p>
</section>
</main>
<footer>문서 비교와 인용 범위 검토 · 게시글 수정이나 공개 발행 없음</footer>
"""

css = """
:root{color-scheme:light;--ink:#17232c;--muted:#566772;--line:#d9e1e5;--accent:#125e6b;--paper:#fff;--soft:#f2f6f7}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:#f8fafb;color:var(--ink);font:17px/1.9 -apple-system,BlinkMacSystemFont,"Apple SD Gothic Neo","Noto Sans KR",sans-serif;word-break:keep-all;overflow-wrap:anywhere}
header,main,nav,footer{max-width:1120px;margin:auto;padding:0 36px}header{padding-top:64px;padding-bottom:30px}
.eyebrow{font-size:14px;color:var(--accent);font-weight:650;letter-spacing:.06em}h1{font-size:44px;line-height:1.35;letter-spacing:-.045em;margin:14px 0 26px}h2{font-size:29px;line-height:1.45;letter-spacing:-.035em;margin:0 0 22px}h3{font-size:21px;line-height:1.5;margin:12px 0}.lead{font-size:21px;line-height:1.9;max-width:1000px}
p{margin:15px 0}.scope,.note,figcaption{font-size:14px;color:var(--muted);line-height:1.85}.scope{border-left:3px solid var(--accent);padding:8px 18px;margin-top:24px}nav{display:flex;gap:10px 20px;flex-wrap:wrap;border-top:1px solid var(--line);border-bottom:1px solid var(--line);padding-top:15px;padding-bottom:15px;font-size:14px}
a{color:var(--accent);text-underline-offset:4px}section{padding:44px 0;border-bottom:1px solid var(--line);scroll-margin-top:20px}.refs{white-space:normal;font-size:12px;font-weight:650;margin-left:4px}.refs a{text-decoration:none;margin-right:3px}
.summary-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin:30px 0 0}.summary-grid>div{padding:20px;background:var(--soft);border-radius:8px}.summary-grid h3{font-size:17px}.summary-grid p{font-size:15px;margin:8px 0}
.principle{background:var(--paper);border:1px solid var(--line);border-radius:10px;padding:28px 30px;margin:24px 0;scroll-margin-top:20px}.card-top{display:flex;align-items:center;gap:14px}.number{font-size:24px;font-weight:750;color:var(--accent)}.tag{font-size:12px;border:1px solid #b9cfd4;border-radius:20px;padding:2px 12px;color:var(--accent)}.english{font-size:14px;color:var(--muted);margin:0 0 22px}.english a{color:var(--muted)}
dl{display:grid;grid-template-columns:132px 1fr;gap:15px 18px;margin:18px 0 0}dt{font-weight:650;font-size:15px}dd{margin:0;font-size:16px;line-height:1.9}
figure{margin:28px 0;background:var(--paper);padding:24px;border:1px solid var(--line);border-radius:8px}figure svg{width:100%;height:auto;display:block;max-width:100%!important}figcaption{margin-top:18px}
details{margin:20px 0}summary{cursor:pointer;color:var(--accent)}pre{font-size:13px;line-height:1.65;background:var(--soft);padding:20px;overflow:auto;word-break:normal}code{font-size:.85em}
.table-wrap{overflow-x:auto}table{width:100%;border-collapse:collapse;font-size:15px;line-height:1.8}th,td{text-align:left;vertical-align:top;padding:18px;border:1px solid var(--line)}th{background:var(--soft)}th:first-child{width:23%}th:nth-child(2){width:40%}
.proposal{padding:20px 26px;border-left:4px solid var(--accent);background:var(--soft)}.proposal>p:first-child{font-size:14px;color:var(--muted)}
blockquote{margin:24px 0;padding:16px 24px;background:var(--soft);border-left:3px solid var(--accent)}blockquote p[lang=en]{font-size:18px;font-weight:600;line-height:1.6}blockquote p{font-size:16px}
.sources{padding-left:28px;font-size:15px}.sources li{padding:9px 0;scroll-margin-top:24px}.sources strong{display:inline-block;min-width:38px}footer{font-size:13px;color:var(--muted);padding-top:24px;padding-bottom:48px}
@media(max-width:700px){body{font-size:16px}header,main,nav,footer{padding-left:20px;padding-right:20px}header{padding-top:32px}h1{font-size:32px}h2{font-size:25px}.lead{font-size:18px}.summary-grid{grid-template-columns:1fr}.principle{padding:20px}dl{display:block}dt{margin-top:18px}dd{margin-top:5px}figure{padding:10px}.table-wrap table{min-width:820px}}
@media print{body{background:white;font-size:11pt}header,main,footer{max-width:none;padding:0}nav{display:none}h1{font-size:28pt}h2{font-size:20pt}h3{font-size:14pt}.lead{font-size:14pt}section{padding:22px 0}.principle{break-inside:avoid;font-size:10pt}dd{font-size:10pt}.summary-grid{grid-template-columns:1fr}figure{break-inside:avoid}a{color:inherit}.refs{font-size:8pt}details{display:none}}
"""
(root / "report.html").write_text(
    '<!doctype html><html lang="ko"><head><meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width,initial-scale=1">'
    '<title>Kiro Frontier Engineering · 현재 주장 및 AWS AI-DLC 비교</title>'
    f"<style>{css}</style></head><body>{body}</body></html>"
)
print(root / "report.html")
