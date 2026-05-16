# Advanced Taxonomy 실행 액션플랜

## 목표

기존 CVPR 2026 3D reconstruction 페이지를 단순 동향 정리에서 한 단계 올려, 다음 질문에 답하는 advanced analysis 페이지로 확장한다.

> 2026년 3D reconstruction 논문 분포는 어떤 미래 field shift를 예고하는가?

구체적으로는 기존 `Observed Topic Taxonomy`를 유지하되, 그 위에 `Latent Field-Shift Taxonomy`, `Negative Space Map`, `Strategic Bet`를 추가한다.

## 산출물

1. `advanced_taxonomy_analysis_ko.md`
   - taxonomy 개편의 철학과 분석 원문
   - method taxonomy에서 field-power taxonomy로 올리는 설명

2. `advanced_taxonomy_action_plan_ko.md`
   - 이 파일
   - 기존 페이지를 advanced analysis로 확장하기 위한 실행 단계

3. `advanced_analysis.html`
   - 공개용 Advanced Analysis 페이지
   - 기존 페이지에서 `Advanced Analysis` 탭으로 접근 가능

4. `index.html`
   - 기존 메인 페이지
   - header 영역에 `Advanced Analysis` 탭 추가

## 실행 단계

### Step 1. 기존 taxonomy를 Observed Layer로 격하하지 않고 보존

기존 분류는 삭제하지 않는다. 대신 명칭을 명확히 한다.

```text
Observed Topic Taxonomy
```

이 층은 다음을 설명한다.

- 어떤 키워드가 많이 등장했는가?
- 어떤 방법론 클러스터가 큰가?
- VGGT, 3DGS, dynamic 4D, pose/localization, embodied AI가 각각 어느 정도 신호를 갖는가?

### Step 2. Latent Field-Shift Taxonomy 추가

기존 topic을 다음 functional role로 다시 태깅한다.

| Observed Topic | Functional Role |
|---|---|
| VGGT / DUSt3R / MASt3R | Geometry Prior |
| SLAM / BA / localization | Spatial State Estimator |
| 3DGS / occupancy / scene graph | Map-Memory Representation |
| Dynamic 4D | Persistent World Update |
| Uncertainty / metric reliability | Trust Boundary |
| Benchmark / evaluation | Field Rule-Setting |

이 표는 advanced page의 중심이 된다.

### Step 3. Hidden Pressure 분석 추가

각 topic마다 다음 질문을 붙인다.

```text
Observed method:
Functional role:
Hidden pressure:
Strategic bet:
```

예시:

```text
Observed method: Feed-forward 3D reconstruction
Functional role: Geometry prior
Hidden pressure: per-scene optimization is being replaced by amortized inference
Strategic bet: future SLAM systems will treat foundation 3D outputs as uncertain measurements, not final maps
```

### Step 4. Negative Space Map 추가

별도 섹션으로 `What the Current Taxonomy Does Not Directly Say`를 만든다.

포함할 unseen trends:

- Reconstruction is becoming an interface problem, not just a geometry problem.
- 3DGS is under pressure to become a map, but lacks trust and action semantics.
- VGGT-like models will not replace SLAM directly; they will become probabilistic priors inside spatial belief systems.
- Evaluation will move from visual fidelity to decision reliability.
- The next field leader will define the interface between learned geometry and persistent spatial memory.

### Step 5. Strategic Bet을 flagship agenda로 통합

advanced page의 연구 제안은 여러 아이디어를 병렬로 나열하지 않고 하나의 agenda로 묶는다.

```text
Reliability-Aware Spatial Memory for Embodied Foundation Models
```

하위 축은 다음 3개다.

- Prior as Measurement
- Map as Memory
- Evaluation as Trust

### Step 6. 기존 페이지에 Advanced Analysis 탭 추가

메인 `index.html` header에 다음 탭을 추가한다.

```text
Core Analysis | Advanced Analysis | Methods / Results
```

`Advanced Analysis`는 `advanced_analysis.html`로 연결한다.

### Step 7. 검증

다음 항목을 확인한다.

- `index.html`에서 advanced page로 이동 가능
- `advanced_analysis.html`에서 main page와 methods page로 이동 가능
- HTML이 UTF-8로 유지됨
- 모바일 폭에서 표와 탭이 깨지지 않음
- `git diff --check` 통과

## 완료 기준

이 액션플랜은 다음 조건을 만족하면 완료다.

- 분석 원문 Markdown 저장 완료
- 실행계획 Markdown 저장 완료
- 공개 HTML advanced page 생성 완료
- 기존 메인 페이지에서 `Advanced Analysis` 탭 접근 가능
- 변경 파일이 Git에서 확인 가능
