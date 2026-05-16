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
