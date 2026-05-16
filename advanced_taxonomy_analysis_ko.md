# Advanced Taxonomy Analysis: Unseen Trends를 읽기 위한 3D Reconstruction 해석틀

## 핵심 진단

현재 CVPR 2026 3D reconstruction 분석의 기존 taxonomy는 보이는 트렌드를 잘 정리한다. `3DGS`, `NeRF`, `VGGT / feed-forward 3D`, `dynamic 4D`, `SLAM / localization`, `embodied AI`, `metric evaluation` 같은 분류는 현재 논문 분포를 설명하는 데 유용하다.

하지만 교수급, 리딩그룹급 분석은 이미 이름 붙은 군집을 정리하는 데서 멈추지 않는다. 중요한 것은 아직 명명되지 않은 압력, 결핍, 전환점을 읽는 일이다. 즉, taxonomy의 역할을 "논문이 무엇을 하는가"에서 "이 논문군은 미래 stack에서 어떤 권력을 차지하려 하는가"로 올려야 한다.

따라서 기존 taxonomy를 폐기할 필요는 없다. 오히려 기존 taxonomy를 `Observed Layer`로 유지하고, 그 위에 `Functional Role`, `Hidden Pressure`, `Negative Space`, `Strategic Bet`를 얹어야 한다.

## Failure Axis Agenda: trend thesis에서 연구주제 제안으로

기존 분석의 약점은 "3D reconstruction이 spatial memory / world-state compiler / trust kernel로 간다"는 큰 방향을 말했지만, 그 방향이 곧바로 연구주제 선정의 새 축으로 바뀌지는 않았다는 점이다. 더 강한 분석은 "어떤 주제가 뜨는가"가 아니라 **"분야 전체가 반복해서 실패하지만 아직 죄목으로 부르지 못하는 것은 무엇인가"**를 정의해야 한다.

핵심 판정은 다음이다.

> CVPR 2026의 3D reconstruction은 이미 "더 잘 복원하는가"의 단계에서 "믿고 행동해도 되는가"의 단계로 넘어가고 있다. 그런데 분야는 아직 이 전환에 필요한 실패 언어를 갖고 있지 않다. 다음 강한 연구주제는 새로운 3D model이 아니라, foundation 3D가 책임져야 할 실패를 이름 붙이고 측정 가능하게 만드는 것이다.

### 새 죄목 5개

| 새 죄목 | 정의 | 측정 후보 |
|---|---|---|
| Action-Irrelevant Geometry | reconstruction score는 좋지만 downstream action에 필요한 정보가 빠져 있는 실패. geometry가 보기에는 그럴듯하지만 robot이 움직이고 잡고 피하는 데 필요한 cost, collision, affordance, freespace와 연결되지 않는다. | action-critical region error, reconstruction-to-control-cost transfer, geometry error vs navigation/manipulation failure, control-relevant uncertainty calibration |
| Confidence Without Accountability | 모델이 그럴듯한 3D를 자신 있게 내지만, 언제 틀렸는지 말하지 못하는 실패. uncertainty가 있더라도 실제 decision boundary나 abstention policy로 연결되지 않는다. | high-confidence wrong geometry rate, failure prediction AUROC, abstention precision/recall, uncertainty-to-downstream-failure calibration |
| Static-State Laundering | dynamic world를 static map처럼 그럴듯하게 세탁하는 실패. moving object, transient structure, occlusion artifact가 persistent map에 잘못 bake-in된다. | map contamination rate, dynamic object invalidation latency, reappearing object identity consistency, state revision accuracy |
| Pose-Free Amnesia | pose/calibration 없이 결과는 나오지만, 그 결과가 어떤 metric 책임을 지는지 잊어버리는 실패. pose uncertainty가 해결된 것이 아니라 model 내부로 숨겨진다. | hidden scale drift, calibration perturbation sensitivity, sparse-view pose ambiguity, metric consistency under sensor shift |
| Passive-View Bias | 주어진 view에서는 잘하지만, 언제 더 봐야 하는지 모르는 실패. embodied agent가 필요한 것은 single-shot reconstruction이 아니라 uncertainty를 줄이기 위한 acquisition policy다. | next-best-view under uncertainty, information gain per motion cost, recovery view budget, active reconstruction success after first failure |

### 왜 이것이 research topic인가

이 agenda는 trend following이 아니라 failure-axis proposal이다.

- 새로운 해법보다 아직 이름 붙지 않은 실패를 찾는다.
- VGGT/3DGS/4D의 성능 경쟁 뒤에 있는 action relevance, accountability, state contamination, hidden pose uncertainty, active acquisition을 끌어낸다.
- PSNR/Chamfer/depth error가 놓치는 liability benchmark를 제안한다.
- failure taxonomy -> benchmark -> trust kernel -> active recovery -> standardization으로 이어지는 연구 프로그램을 만든다.
- 가설이 틀려도 failure taxonomy, stress protocol, negative result, baseline comparison, benchmark가 남는다.

### 4-paper research program

| Paper | 목표 | 핵심 산출물 |
|---|---|---|
| Paper 1. Failure Taxonomy and Benchmark | Foundation 3D가 agent decision에서 실패하는 5개 죄목을 정의하고 측정한다. | failure taxonomy, stress dataset, metric suite, baseline audit |
| Paper 2. Trust Kernel | VGGT/3DGS/pose-free output을 믿을지, 보류할지, backend로 보정할지 결정하는 arbitration layer를 만든다. | uncertainty calibration, abstention policy, state invalidation rule, factor-backend interface |
| Paper 3. Active Recovery and Acquisition Policy | 실패 가능성이 높을 때 추가 관측을 요구하고, 어떤 view를 더 봐야 하는지 결정한다. | next-best-view protocol, recovery view budget, information gain vs motion cost benchmark |
| Paper 4. Standardization Across CV and Robotics | visual reconstruction metric과 robotics task metric을 연결하는 shared evaluation protocol을 만든다. | cross-domain benchmark, metadata contract, downstream task adapters, reproducible leaderboard |

### 한 문장 주제화

> 현재 3D reconstruction은 visual fidelity와 geometric accuracy를 기준으로 발전해왔지만, embodied deployment에서는 action-relevant failure, accountability, dynamic state contamination, hidden pose uncertainty, active acquisition cost가 병목이다. 본 연구 agenda는 이 실패들을 처음으로 측정 가능하고 최적화 가능한 대상으로 만들며, foundation 3D liability evaluation이라는 새로운 연구축을 제안한다.

## 기존 taxonomy의 한계

기존 taxonomy는 다음 질문에 답한다.

> 이 논문은 어떤 방법론 또는 주제군에 속하는가?

예를 들면 다음과 같다.

- 3DGS인가?
- NeRF / radiance field인가?
- VGGT / feed-forward reconstruction인가?
- Dynamic 4D인가?
- Pose / localization / SLAM인가?
- Embodied AI와 연결되는가?
- Evaluation / metric reliability 논문인가?

이 질문은 현재 field distribution을 보는 데는 충분하다. 그러나 unseen trend를 읽기에는 약하다. unseen trend는 보통 "많이 나온 키워드"가 아니라 "여러 클러스터가 동시에 압력을 가하고 있는데 아직 이름이 붙지 않은 빈칸"에서 나온다.

## 개선 방향: Method Taxonomy에서 Field-Power Taxonomy로

새 taxonomy는 다음 질문에 답해야 한다.

> 이 논문군은 미래의 spatial intelligence stack에서 어떤 기능과 권력을 차지하려 하는가?

이 관점에서는 `3DGS`, `VGGT`, `SLAM`, `4D reconstruction`을 서로 독립적인 topic으로 보지 않는다. 대신 다음 역할로 재해석한다.

- `VGGT / DUSt3R / MASt3R`: geometry prior
- `SLAM / BA / localization`: spatial state estimator
- `3DGS / occupancy / scene graph`: map-memory representation
- `Dynamic 4D`: persistent world update problem
- `Metric reliability / uncertainty`: trust boundary
- `Benchmark / evaluation`: field rule-setting mechanism

즉, taxonomy를 "method label"에서 "field role"로 바꾼다.

## 제안 taxonomy

```text
Layer 0. Observed Method
- 3DGS
- NeRF
- VGGT / feed-forward 3D
- Dynamic 4D
- SLAM / localization
- embodied AI
- evaluation / metric reliability

Layer 1. Functional Role
- Geometry Prior
- Spatial State
- Persistent Memory
- Action Interface
- Trust / Reliability Gate
- Evaluation Standard

Layer 2. Hidden Pressure
- optimization is becoming amortized
- rendering is trying to become mapping
- reconstruction is being pulled into embodied AI
- metric accuracy is becoming trust calibration
- dynamic scenes are exposing static-map assumptions

Layer 3. Negative Space
- what is missing?
- what cannot yet be evaluated?
- what breaks under real robot use?
- what has no benchmark but will matter?
- what assumptions are silently inherited?

Layer 4. Strategic Bet
- likely infrastructure
- likely demo bubble
- likely benchmark shift
- likely robotics entry point
- likely dead end unless paired with another layer
```

## 가장 중요한 새 분류축

### 1. 이 논문은 prior인가, state인가?

VGGT류 모델은 최종 map이라기보다 `geometry prior`일 가능성이 크다. 반면 SLAM, BA, localization 계열은 `state estimator`다. 둘의 충돌과 결합이 unseen trend다.

핵심 질문은 다음과 같다.

> Feed-forward geometry를 final answer로 볼 것인가, 아니면 uncertain measurement로 볼 것인가?

교수급 연구 기회는 후자에 있다. VGGT류 출력을 hard map으로 쓰는 것이 아니라, uncertainty가 붙은 factor로 받아들이고 metric backend가 이를 보정하는 구조가 더 오래간다.

### 2. 이 representation은 agent가 행동하는 데 충분한가?

3DGS는 visual representation으로 강하다. 그러나 agent가 행동하려면 freespace, collision, affordance, traversability, uncertainty, persistence가 필요하다.

따라서 중요한 질문은 "3DGS 논문이 많다"가 아니다.

> 3DGS는 map이 될 수 있는가, 아니면 rendering codec에 머무를 것인가?

3DGS가 embodied AI stack의 중심으로 가려면 occupancy, mesh, scene graph, uncertainty와 결합해야 한다.

### 3. 이 논문군은 benchmark를 바꾸는가?

방법론보다 더 큰 권력은 evaluation standard다. PSNR, LPIPS, Chamfer, F-score만으로는 embodied spatial intelligence를 평가할 수 없다.

앞으로 중요한 축은 다음으로 이동한다.

- failure prediction
- abstention
- re-localization stability
- dynamic recovery
- closed-loop navigation / manipulation success
- map update consistency
- calibration under sensor shift

따라서 benchmark를 바꾸는 논문군은 단순 성능 향상 논문보다 field-level 영향력이 크다.

### 4. 이 트렌드는 다른 분야를 침공하는가?

단일 분야 안에서 커지는 트렌드보다 분야 경계를 재배치하는 트렌드가 더 중요하다.

CVPR 3D reconstruction은 robotics, embodied AI, world model, spatial memory와 연결되면서 독립 task에서 shared infrastructure로 이동하고 있다. 이 변화는 "3D reconstruction이 커진다"가 아니라 "3D reconstruction의 소유권이 바뀐다"는 뜻이다.

### 5. 논문들이 말하지 않는 공백은 무엇인가?

unseen trend는 보통 빈칸에서 나온다. 많이 보이는 키워드보다, 다들 회피하지만 곧 시스템 병목으로 터질 문제가 중요하다.

대표적인 negative space는 다음과 같다.

- uncertainty calibration
- dynamic persistence
- map update and forgetting
- out-of-distribution geometry
- reflective / transparent / low-texture failure
- human instruction ambiguity
- closed-loop task grounding
- sensor calibration drift
- "I do not know"를 말할 수 있는 3D model

## 3D reconstruction용 개선 taxonomy 예시

| New Taxon | 기존 키워드 | 숨은 의미 | 교수급 질문 |
|---|---|---|---|
| Amortized Geometry Prior | VGGT, DUSt3R, MASt3R | reconstruction이 optimization에서 inference로 이동 | 이 prior를 SLAM factor로 쓸 수 있는가? |
| Renderable Spatial State | 3DGS, NeRF | rendering representation이 map 자리를 노림 | action 가능한 map인가, 예쁜 codec인가? |
| Persistent World Memory | 4D, dynamic scene, long-term mapping | static reconstruction의 한계 노출 | 무엇을 기억하고 무엇을 잊어야 하는가? |
| Trust Boundary | uncertainty, metric reliability | 3D가 agent decision에 들어가기 시작 | 틀렸을 때 멈출 수 있는가? |
| Embodied Interface | robotics, navigation, manipulation | 3D가 perception output에서 policy substrate로 이동 | closed-loop 성능으로 검증되는가? |
| Evaluation Regime Shift | benchmark, robustness | 평가 기준의 권력 이동 | 다음 표준 benchmark는 무엇인가? |
| Negative Space | missing calibration, bad dynamics, no failure labels | 아직 논문화되지 않은 병목 | 1년 뒤 터질 문제는 무엇인가? |

## 핵심 문장

> 보이는 taxonomy는 현재의 논문 분포를 설명한다. 그러나 중요한 것은 taxonomy의 빈칸이다. 빈칸은 아직 논문화되지 않았지만, 여러 클러스터가 동시에 압력을 가하고 있는 미래 문제다.

영어 표현:

> The visible taxonomy explains the current paper distribution. The real signal lies in the empty cells: problems not yet named as a field, but already pressured by multiple clusters at once.

## 결론

taxonomy 자체를 고쳐야 한다. 다만 기존 taxonomy를 버리는 것이 아니라 다음 3층으로 확장해야 한다.

```text
Observed Taxonomy
+ Latent Pressure Taxonomy
+ Negative Space Map
```

이 구조를 쓰면 분석은 "많이 나온 주제 정리"에서 "아직 이름 붙지 않은 다음 연구장"을 읽는 분석으로 올라간다. 이것이 unseen trend를 읽는 taxonomy다.

## 실제 적용 결과: CVPR 2026 3D Reconstruction

이 taxonomy를 실제 curated set에 적용하면 다음 결론이 나온다. 기준은 864편 strict 후보 중 `core_reconstruction` 362편과 `strong_bridge` 74편, 총 436편이다. 그중 relevance confidence가 high인 논문은 297편이다.

## 더 덜 뻔한 판정: 빈도보다 모순이 중요하다

첫 번째 적용 결과도 여전히 안전한 해석에 가까웠다. 더 높은 수준의 분석은 큰 cluster를 다시 설명하는 것이 아니라, 데이터 안의 모순과 결핍을 읽어야 한다.

### 1. VGGT는 다음 SOTA 주제가 아니라 곧 commodity가 될 가능성이 크다

VGGT lineage는 core/bridge set 안에서 48편이다. 그러나 그 안에는 `FlashVGGT`, `QVGGT`, `HTTM`, `HeSS`, `VGG-T^3`, `Scal3R`처럼 압축, 양자화, token merging, scale-up류 제목이 이미 보인다.

어떤 모델이 벌써 가속, 압축, 재사용 대상이 된다는 것은 novelty frontier가 아니라 infrastructure primitive로 내려가고 있다는 뜻이다. 따라서 "VGGT를 더 잘한다"보다 "VGGT류 prior가 틀릴 때 system이 어떻게 의심하고 보정하는가"가 더 큰 문제다.

### 2. 가장 큰 결핍은 failure language다

core/bridge set에서 `foundation/prior` claim은 210건, `robustness`는 149건이지만, keyword scan 기준 `failure`는 6건, `outlier`는 4건, `abstention`은 0건이다.

field는 3D를 agent infrastructure로 밀고 있지만, "언제 쓰면 안 되는가"의 언어가 거의 없다. 이 빈칸은 단순 robustness보다 큰 trust governance 문제다.

### 3. Generation은 reconstruction의 downstream이 아니라 경쟁 control plane이 될 수 있다

`Gen3R`, `MotionCrafter`, `WorldStereo`, `GaussFusion`, `Pano3DComposer`처럼 generation과 reconstruction이 섞인 논문들이 geometry를 생성 제어의 조건 또는 부산물로 쓴다.

이는 reconstruction이 독립 task로 남는다는 가정이 흔들린다는 뜻이다. 미래에는 geometry가 truth recovery가 아니라 video/world generation을 제어하는 latent handle로 소비될 수 있다.

### 4. Pose-free 흐름은 SLAM의 승리가 아니라 SLAM prerequisite의 해체다

`BA-GS`, `No Calibration, No Depth, No Problem`, `Pose-Free Omnidirectional Gaussian Splatting`, `Learning 3D Representations from Unposed Multi-View Images` 같은 제목들이 반복된다.

CVPR 쪽 압력은 "정확한 pose를 먼저 구하자"가 아니라 "pose/calibration 없이도 그럴듯한 3D를 만들자"다. robotics 쪽 기회는 이를 반박하는 것이 아니라, pose-free output의 epistemic uncertainty와 failure boundary를 정의하는 데 있다.

### 5. Reconstruction은 passive inference에서 acquisition policy로 이동한다

`AREA3D: Active Reconstruction Agent`, `Catch Me if You Can: Active Mapping of Moving 3D Objects`, streaming 4D reconstruction, trajectory-conditioned occupancy world model류 신호가 있다.

다음 질문은 "주어진 이미지에서 3D를 뽑는가"가 아니라 "무엇을 더 봐야 uncertainty가 줄어드는가"다. 즉 reconstruction은 perception problem에서 information-gathering policy problem으로 이동한다.

### 6. Benchmark 논문 증가는 성숙이 아니라 불안정성의 증거다

benchmark/evaluation은 core/bridge에서 195편이고, dynamic과 72편, pose/calibration과 51편 교차한다.

field가 안정되면 benchmark는 배경으로 물러난다. 지금 benchmark가 크게 보인다는 것은 아직 무엇을 잘한다고 불러야 할지 합의가 없다는 뜻이다. 이 시기에는 method보다 evaluation rule을 잡는 쪽이 더 큰 영향력을 가진다.

### 더 강한 결론

따라서 더 강한 결론은 "3D reconstruction이 spatial memory로 간다"가 아니다. 그것은 아직 안전한 문장이다.

더 불편한 결론은 다음이다.

> foundation 3D가 빠르게 commodity가 되는 동안, field는 아직 failure, abstention, acquisition policy의 언어를 갖지 못했다.

## Three Strategic Theses: taxonomy를 넘어선 field memo

아래 세 thesis는 기존 taxonomy를 더 정교하게 만드는 목적이 아니다. 오히려 taxonomy가 가리는 것을 드러내기 위한 내부 전략 메모다. 핵심 질문은 "무슨 주제가 많은가"가 아니라, "3D reconstruction이라는 이름 아래 실제로 어떤 권력과 책임 경계가 재편되는가"다.

### Thesis 1. 3D Reconstruction은 사라지고, World-State Compiler가 된다

지금 3D reconstruction을 여전히 "이미지나 비디오로부터 3D 구조를 복원하는 문제"로 보면 중요한 전환을 놓친다. CVPR 2026의 신호는 더 이상 reconstruction이 하나의 task로 커지고 있다는 것이 아니다. 오히려 reconstruction이라는 이름의 독립성은 약해지고 있다. 3D reconstruction은 점점 더 큰 system 안에서 **world state를 컴파일하는 중간 계층**으로 흡수되고 있다.

여기서 world-state compiler란 raw sensor input, learned visual prior, temporal observation, language instruction, action context를 받아서 agent가 사용할 수 있는 state representation으로 변환하는 계층을 뜻한다. 이 state는 단순 mesh도 아니고, Gaussian도 아니고, point cloud도 아니다. 그것들은 compiler가 생산하거나 사용하는 중간 표현일 뿐이다. 핵심 output은 "agent가 지금 세계를 어떻게 믿고 있는가"다.

이 관점에서 보면 VGGT, DUSt3R, MASt3R류 feed-forward geometry model은 최종 답이 아니다. 그것들은 compiler의 front-end prior가 된다. 3DGS는 최종 map이 아니다. 그것은 compiler가 appearance, visibility, editable scene representation을 유지하기 위해 사용하는 renderable memory format이다. Dynamic 4D reconstruction은 별도 분야가 아니다. 그것은 compiler가 시간이 흐를 때 state를 어떻게 update하고 invalidate하는지 묻는 문제다. Pose-free reconstruction도 마찬가지다. 그것은 pose estimation이 사라졌다는 뜻이 아니라, compiler가 pose를 explicit prerequisite로 요구하지 않는 방향으로 변하고 있다는 뜻이다.

따라서 앞으로의 핵심 질문은 "어떤 representation이 더 좋은가"가 아니다. 더 중요한 질문은 이것이다.

> 어떤 system이 heterogeneous observation을 받아서, action 가능한 world state로 안정적으로 컴파일할 수 있는가?

이 질문은 기존 reconstruction benchmark의 언어로는 충분히 평가되지 않는다. PSNR, LPIPS, Chamfer, depth error는 compiler의 일부 품질만 측정한다. 그러나 agent 입장에서는 더 중요한 것이 있다. 이 state가 오래 유지되는가? 틀렸을 때 invalidate되는가? 새 관측이 들어왔을 때 갱신되는가? 움직이는 object가 사라졌다가 다시 나타났을 때 같은 entity로 추적되는가? language query가 들어왔을 때 geometric belief와 semantic belief가 충돌하면 어떤 쪽을 믿는가? action 실패 후 state를 수정하는가?

여기서 3D reconstruction의 미래는 "더 좋은 3D 생성"이 아니라 **state compilation architecture**가 된다. 좋은 연구는 single method 성능을 높이는 것이 아니라, input, prior, representation, uncertainty, memory, action feedback 사이의 interface를 정의한다. 즉, 2027년 이후 강한 연구는 `VGGT + SLAM`, `3DGS + occupancy`, `4D + world model` 같은 조합 자체가 아니라, 그 조합을 가능하게 하는 compiler contract를 제안해야 한다.

이 thesis의 불편한 함의는 명확하다. 3D reconstruction 연구자는 더 이상 "복원 품질"만으로 field를 주도하기 어렵다. field의 주도권은 world state를 정의하는 쪽으로 이동한다. 이것은 SLAM, embodied AI, video generation, simulation, robotics evaluation이 모두 걸린 문제다. 누가 world-state compiler의 표준 interface를 잡는가가 다음 권력의 핵심이다.

### Thesis 2. SLAM은 대체되지 않는다. 대신 Trust Kernel로 축소된다

CVPR식 3D foundation model이 강해질수록 "SLAM이 대체되는가?"라는 질문이 반복된다. 이 질문은 반쯤 맞고 반쯤 틀렸다. classical SLAM pipeline의 많은 부분은 분명 약해진다. feature matching, dense correspondence, pose initialization, sparse-to-dense reconstruction 같은 모듈은 feed-forward model에 의해 압박받는다. 그러나 SLAM이 사라진다는 결론은 너무 단순하다.

더 정확한 변화는 이것이다.

> SLAM은 full-stack reconstruction pipeline에서, learned world state를 검증하고 보정하는 trust kernel로 축소된다.

Trust kernel이란 system이 어떤 3D state를 믿어도 되는지 판단하는 최소 핵심 계층이다. 이 계층은 반드시 모든 geometry를 처음부터 만들 필요가 없다. 오히려 geometry prior는 VGGT류 model이 줄 수 있다. appearance-rich representation은 3DGS가 줄 수 있다. semantic cue는 VLM이 줄 수 있다. 하지만 이 모든 것이 agent의 action으로 들어가기 전에, 누군가는 다음 질문에 답해야 한다.

이 pose는 metric하게 일관적인가? 이 depth는 scale drift가 없는가? 이 object는 실제로 움직인 것인가, 아니면 model hallucination인가? 이 map update는 이전 belief와 충돌하지 않는가? 이 visual prior가 자신 있게 틀린 경우를 어떻게 잡을 것인가? 새 관측이 기존 map을 깨뜨릴 때, state를 고칠 것인가, 관측을 버릴 것인가, 추가 관측을 요구할 것인가?

이 질문들은 classic SLAM이 잘하던 영역과 맞닿아 있다. 다만 역할이 바뀐다. 과거 SLAM은 world state를 생성하는 주체였다. 미래 SLAM은 learned prior가 생성한 world state를 검증하고, 보정하고, 실패를 선언하는 kernel이 된다. 즉 SLAM은 커다란 pipeline에서 작은 module로 줄어드는 대신, 더 critical한 책임을 갖는다.

이 변화는 robotics 연구자에게 양면적이다. 나쁜 전략은 "foundation model이 틀리니 classical SLAM이 여전히 중요하다"고 방어적으로 말하는 것이다. 그건 설득력이 약하다. 좋은 전략은 "foundation 3D가 agent stack에 들어갈수록, trust kernel 없이는 deploy될 수 없다"고 공격적으로 말하는 것이다. 즉 SLAM의 가치를 legacy로 방어하지 말고, liability layer로 재정의해야 한다.

여기서 중요한 키워드는 accuracy가 아니라 **liability**다. agent가 잘못된 3D state를 믿고 collision을 일으키거나, manipulation을 실패하거나, 잘못된 navigation decision을 내렸을 때 책임은 누구에게 있는가? VGGT prior인가? Gaussian map인가? VLM instruction parser인가? Planner인가? 이 책임 경계를 기술적으로 정의하는 계층이 trust kernel이다.

따라서 다음 세대 SLAM 연구의 핵심은 "더 좋은 trajectory estimation"만이 아니다. 더 중요한 문제는 learned prior와 metric consistency 사이의 arbitration이다. feed-forward model이 그럴듯한 depth를 주지만 loop consistency가 깨질 때 어떻게 할 것인가? dynamic object를 prior가 static structure로 hallucinate할 때 어떻게 reject할 것인가? pose-free reconstruction이 멋진 결과를 내지만 metric scale이 불안정할 때 system은 어느 수준에서 멈춰야 하는가?

이 thesis의 결론은 강하다. SLAM은 대체되지 않는다. 하지만 예전 형태로 살아남지도 않는다. SLAM은 learned spatial intelligence stack의 **trust kernel**이 된다. 그리고 그 kernel을 먼저 정의하는 연구자가, foundation 3D 시대의 robotics 접점을 장악할 가능성이 크다.

### Thesis 3. 다음 경쟁은 성능이 아니라 Liability다

현재 많은 3D foundation / reconstruction 논문은 더 빠르고, 더 일반적이고, 더 적은 view로, 더 그럴듯한 3D를 만든다고 주장한다. 그러나 field가 embodied AI와 robotics로 이동하는 순간, 성능 경쟁만으로는 부족해진다. agent가 3D state를 실제 행동에 사용하기 시작하면, 다음 질문은 "얼마나 잘 맞는가?"가 아니라 **"틀렸을 때 누가 책임지는가?"**가 된다.

이것이 liability 문제다. 여기서 liability는 법적 책임만을 뜻하지 않는다. system architecture 안에서 어떤 module이 어떤 실패를 감지하고, 어떤 module이 멈추고, 어떤 module이 추가 정보를 요구하고, 어떤 module이 state를 invalidate해야 하는지를 뜻한다. 즉 technical liability다.

현재 3D reconstruction field는 이 언어가 약하다. robustness라는 말은 많지만, robustness는 너무 넓다. uncertainty도 나오지만, uncertainty가 실제 decision boundary로 연결되는 경우는 제한적이다. failure prediction, abstention, outlier rejection, re-query, active observation, state invalidation 같은 용어는 아직 field의 중심 언어가 아니다. 그런데 embodied agent에는 바로 이것들이 필요하다.

예를 들어 robot이 컵을 집으려 할 때, Gaussian representation이 예쁜 view를 렌더링하는 것은 충분하지 않다. object boundary가 실제 grasp에 충분히 믿을 만한지, transparent surface가 hallucinated geometry인지, occluded handle이 실제로 존재하는지, depth uncertainty가 grasp planner threshold를 넘는지 알아야 한다. navigation에서도 마찬가지다. freespace가 실제 freespace인지, dynamic object가 지나간 흔적인지, reflective surface가 corridor로 잘못 복원된 것인지 판단해야 한다.

이런 상황에서 기존 benchmark는 너무 순하다. 평균 depth error, view synthesis quality, reconstruction IoU는 "성공한 상태에서 얼마나 좋은가"를 묻는다. 그러나 liability benchmark는 "실패할 때 어떻게 행동하는가"를 묻는다. 이것은 훨씬 더 어려운 질문이다.

좋은 future benchmark는 다음을 물어야 한다. 모델은 자신이 모르는 장면을 모른다고 말할 수 있는가? sparse view에서 hallucination과 valid inference를 구분하는가? calibration이 틀렸을 때 confidence가 무너지는가? dynamic object가 map에 잘못 bake-in될 때 이를 감지하는가? reflective / transparent / low-texture object에서 failure를 예측하는가? 실패 가능성이 높을 때 additional view를 요구하는가? action 전에 state를 invalidate할 수 있는가?

이 관점에서 보면 다음 field leader는 가장 높은 PSNR을 내는 팀이 아닐 수 있다. 오히려 "3D state를 믿어도 되는 조건"을 정의하는 팀이 더 중요해질 수 있다. 이것은 benchmark, dataset, metric, system protocol, uncertainty representation, active perception policy가 모두 결합된 문제다.

여기서 교수급 또는 TC급 논의의 핵심은 방법론이 아니라 rule-setting이다. 어떤 실패를 failure로 부를 것인가? 어떤 uncertainty를 actionable uncertainty로 볼 것인가? 어떤 상황에서 system이 abstain해야 하는가? 어떤 추가 관측을 요구해야 하는가? reconstruction output을 downstream agent가 사용할 때 필요한 metadata contract는 무엇인가?

따라서 다음 경쟁은 단순 성능 경쟁이 아니다.

> 다음 경쟁은 3D state의 liability boundary를 누가 정의하는가이다.

이 thesis는 3D reconstruction 연구를 훨씬 더 큰 문제로 끌어올린다. 3D는 이제 visual artifact가 아니라 decision substrate다. decision substrate가 되면 반드시 책임 경계가 필요하다. 이 경계를 정의하지 못하는 3D foundation model은 demo로는 강해도, embodied AI infrastructure로는 약하다. 반대로 이 경계를 정의하는 연구는 method 성능이 조금 낮아도 field의 룰을 바꿀 수 있다.

### 1. Geometry prior는 작은 cluster가 아니라 큰 system pressure다

VGGT / feed-forward lineage는 core/bridge set 안에서 48편이다. 숫자만 보면 Gaussian/radiance 250편이나 surface/occupancy 302편보다 작다. 그러나 VGGT류는 독립 주제라기보다 다른 cluster가 끌어다 쓰는 geometry prior로 작동한다.

실제 교차 신호:

- VGGT + pose/calibration/localization: 21편
- VGGT + dynamic/4D: 17편
- VGGT + robotics/mapping: 11편

따라서 결론은 "VGGT 논문이 많다"가 아니다. 더 정확한 결론은 feed-forward geometry prior가 SLAM, dynamic reconstruction, occupancy, embodied mapping의 measurement source로 들어오기 시작했다는 것이다.

### 2. 3DGS는 rendering representation에서 map substrate 후보로 이동한다

core/bridge set에서 Gaussian/radiance/view synthesis는 250편, surface/occupancy는 302편이며 두 축의 교차는 143편이다. Gaussian + robotics/mapping도 54편이다.

이 신호는 3DGS가 단순 novel view synthesis 표현에서 map-like representation으로 압박받고 있음을 뜻한다. 하지만 3DGS가 action 가능한 map이 되려면 freespace, collision, traversability, affordance, uncertainty, persistence가 붙어야 한다.

### 3. Dynamic 4D는 novelty topic이 아니라 static-map assumption의 붕괴다

Dynamic/4D는 core/bridge set에서 138편이다. dynamic + Gaussian은 80편, dynamic + robotics/mapping은 49편, dynamic + benchmark/evaluation은 72편이다.

따라서 dynamic 4D는 단순히 움직이는 장면을 복원하는 topic이 아니다. static map assumption이 깨지는 지점이며, persistent world memory, object identity, update/forgetting, relocalization recovery를 요구하는 pressure test다.

### 4. Evaluation은 주변부가 아니라 field rule-setting이다

Dataset / benchmark / evaluation은 core/bridge set에서 195편이다. benchmark + dynamic은 72편, benchmark + pose/calibration/localization은 51편이다.

이는 다음 field의 권력이 method가 아니라 evaluation standard에서 생길 수 있음을 뜻한다. PSNR, LPIPS, Chamfer 중심의 visual fidelity 평가는 embodied spatial intelligence를 충분히 설명하지 못한다. 다음 표준은 failure prediction, abstention, re-localization, dynamic recovery, closed-loop task success 쪽으로 이동해야 한다.

### 5. 최종 판정

CVPR 2026 3D reconstruction의 unseen trend는 `3DGS가 많다` 또는 `VGGT가 뜬다`가 아니다.

더 높은 수준의 판정은 다음이다.

> learned geometry prior, map-like representation, dynamic world update, metric trust gate가 하나의 embodied spatial state interface로 수렴하고 있다.

따라서 가장 강한 연구 agenda는 다음으로 잡는 것이 맞다.

> Reliability-Aware Spatial Memory for Embodied Foundation Models

하위 축은 `Prior as Measurement`, `Map as Memory`, `Evaluation as Trust`다.
