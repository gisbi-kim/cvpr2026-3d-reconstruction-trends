# Advanced Taxonomy Analysis: Unseen Trends를 읽기 위한 3D Reconstruction 해석틀

## 핵심 진단

현재 CVPR 2026 3D reconstruction 분석의 기존 taxonomy는 보이는 트렌드를 잘 정리한다. `3DGS`, `NeRF`, `VGGT / feed-forward 3D`, `dynamic 4D`, `SLAM / localization`, `embodied AI`, `metric evaluation` 같은 분류는 현재 논문 분포를 설명하는 데 유용하다.

하지만 교수급, 리딩그룹급 분석은 이미 이름 붙은 군집을 정리하는 데서 멈추지 않는다. 중요한 것은 아직 명명되지 않은 압력, 결핍, 전환점을 읽는 일이다. 즉, taxonomy의 역할을 "논문이 무엇을 하는가"에서 "이 논문군은 미래 stack에서 어떤 권력을 차지하려 하는가"로 올려야 한다.

따라서 기존 taxonomy를 폐기할 필요는 없다. 오히려 기존 taxonomy를 `Observed Layer`로 유지하고, 그 위에 `Functional Role`, `Hidden Pressure`, `Negative Space`, `Strategic Bet`를 얹어야 한다.

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
