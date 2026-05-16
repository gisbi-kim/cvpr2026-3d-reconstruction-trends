# CVPR 2026 3D Reconstruction 블로그 자료 처리 플랜

Source: https://gisbi-kim.github.io/cvpr2026-explorer/output/cvpr2026_explorer.html

## 처리 결과 요약

- 전체 CVPR 2026 explorer 논문: 4,070편
- 3D reconstruction broad 후보: 1,417편
- 블로그 분석용 strict 후보: 864편
- 1차 정독 seed list: 178편

## 핵심 thesis

CVPR 2026의 3D reconstruction은 더 이상 하나의 `reconstruction` 문제가 아니다. 큰 흐름은 다음 다섯 갈래로 재편되고 있다.

1. VGGT류 feed-forward visual geometry model
2. Gaussian / radiance field / view synthesis representation
3. pose, calibration, localization을 통한 metric reliability
4. dynamic / 4D scene reconstruction
5. 3D generation, editing, autonomous mapping과 reconstruction의 결합

따라서 `VGGT`는 좋은 출발점이지만, 검색어가 아니라 해석 렌즈로 써야 한다. 실제 분석은 VGGT 주변 논문만 읽는 방식이 아니라, feed-forward geometry와 Gaussian map, 4D reconstruction, pose-free / calibration-free / SLAM-like reconstruction이 어떻게 연결되는지 보는 방식이어야 한다.

## strict 후보의 클러스터 분포

- General 3D reconstruction / multiview: 592
- Mesh / surface / implicit / occupancy: 561
- Dataset / benchmark / evaluation: 425
- Gaussian / radiance field / view synthesis: 333
- Dynamic / 4D reconstruction: 271
- Depth / stereo / dense correspondence: 267
- Pose / calibration / localization: 256
- Mapping / autonomous / embodied: 251
- 3D generation / editing bridge: 151
- VGGT / feed-forward geometry: 67

## 블로그 읽기 bucket

- A. thesis anchor: representation shift: 159
- A. thesis anchor: VGGT/feed-forward geometry: 67
- A. thesis anchor: dynamic/4D recon: 40
- B. bridge: reconstruction becomes mapping/world model: 33
- B. bridge: representation meets metric pose: 13
- C. cluster representative: 284
- D. adjacent but useful context: 268

블로그 본문은 A bucket을 중심으로 쓰고, B bucket을 연구 기회와 robotics/SLAM 연결부로 쓰는 것이 좋다. C bucket은 각 섹션의 예시 논문으로 쓰고, D bucket은 false-positive 또는 주변부 맥락으로만 쓴다.

## 검색어 확장 전략

### 1. VGGT / feed-forward geometry

`VGGT`, `visual geometry`, `visual geometry grounded transformer`, `visual geometric transformer`, `feed-forward reconstruction`, `point map`, `DUSt3R`, `MASt3R`, `CroCo`

이 축은 블로그의 도입부에 쓴다. 핵심 질문은 “multi-view geometry가 optimization-heavy pipeline에서 feed-forward prior-heavy model로 이동하는가?”이다.

### 2. General reconstruction / multiview

`3D reconstruction`, `scene reconstruction`, `surface reconstruction`, `multi-view`, `multiview`, `MVS`, `SfM`, `structure from motion`, `bundle adjustment`, `triangulation`, `registration`

이 축은 전통적 3D reconstruction 문제 정의를 잡는 backbone이다. 단순히 reconstruction이라는 단어가 들어간 논문을 모으기보다, input regime과 output representation을 같이 태깅해야 한다.

### 3. Gaussian / radiance / view synthesis

`Gaussian`, `3DGS`, `splatting`, `radiance field`, `NeRF`, `novel view synthesis`, `view synthesis`, `differentiable rendering`

이 축은 “representation shift”의 중심이다. 단순 NVS 논문과, pose-free reconstruction / dynamic scene / mapping / editing으로 확장되는 논문을 분리해야 한다.

### 4. Pose / calibration / localization

`camera pose`, `pose estimation`, `pose alignment`, `calibration`, `localization`, `relocalization`, `pose graph`, `SLAM`

이 축은 robotics/SLAM 관점에서 가장 중요하다. CVPR식 reconstruction이 실제 metric system으로 가려면 pose, calibration, uncertainty, online update 문제가 남는다.

### 5. Dynamic / 4D

`4D`, `dynamic 3D`, `dynamic scene`, `deformable`, `streaming 3D`, `temporal`, `video-to-3D`

이 축은 2026년 트렌드의 pressure test다. static scene에서 그럴듯한 3D를 만드는 것과, moving objects / long sequence / streaming scene을 다루는 것은 난도가 다르다.

### 6. Robotics / mapping / world model

`mapping`, `active mapping`, `autonomous driving`, `BEV`, `world model`, `embodied`, `navigation`, `occupancy prediction`

이 축은 블로그의 마지막 연구 기회 섹션에 쓴다. reconstruction이 visual asset이 아니라 robot이 업데이트하고 질의하는 world model이 되는 흐름이다.

## 논문별 태깅 스키마

CSV에는 다음 관점이 들어가 있다.

- `matched_groups`: 어떤 검색/해석 클러스터에 걸렸는가
- `inputs`: single image, sparse multi-view, video, panorama, LiDAR/driving 등
- `outputs`: camera pose, depth, point map, Gaussian map, mesh/surface, occupancy, 4D scene 등
- `claims`: foundation/prior, unified pipeline, efficiency, scale, robustness, dynamic, benchmark/data, editing/generation 등
- `editorial_bucket`: 블로그에서 어떤 역할로 쓸지
- `strategic_note`: 왜 읽어야 하는지에 대한 자동 초안

## 좋은 논문과 지엽적 논문을 가르는 기준

좋은 논문은 다음 중 하나를 만족한다.

- input-output regime을 크게 바꾼다. 예: sparse view에서 metric 3D, unposed image에서 reconstruction, static에서 dynamic/4D.
- optimization-heavy pipeline을 feed-forward prior 또는 foundation model로 대체한다.
- representation 자체를 바꾼다. 예: Gaussian map, point map, occupancy world model.
- pose, calibration, localization, uncertainty처럼 real system bottleneck을 건드린다.
- reconstruction을 downstream task로 연결한다. 예: autonomous mapping, embodied navigation, segmentation, detection, editing.

지엽적 논문은 다음 신호를 가진다.

- 특정 object category, sensor condition, lighting condition에만 최적화되어 있다.
- 기존 VGGT/3DGS의 속도 개선, cache, token merging만 다룬다.
- dataset/benchmark는 크지만 새 문제 정의가 약하다.
- generation demo가 중심이고 실제 geometry consistency가 부차적이다.

단, 지엽적 논문도 “무엇이 bottleneck으로 남아 있는지”를 보여주는 증거로는 가치가 있다.

## 블로그 구조 초안

### 1. VGGT 검색으로는 부족하다

`VGGT`는 67편 규모의 feed-forward geometry 주변부를 잡지만, 전체 3D reconstruction 변화는 Gaussian, 4D, pose/localization, mapping까지 확장되어 있다.

### 2. Feed-forward geometry가 중심으로 올라왔다

DUSt3R/MASt3R/VGGT 계열 이후, multi-view geometry가 handcrafted correspondence + optimization pipeline에서 visual geometry prior + transformer 기반 추론 문제로 이동한다.

### 3. Gaussian은 rendering에서 map으로 이동한다

3DGS는 더 이상 novel view synthesis만의 표현이 아니다. pose-free reconstruction, dynamic scene, mapping, editing, surface reconstruction으로 확장된다.

### 4. 4D reconstruction은 진짜 난도 테스트다

static scene reconstruction은 포화되어 가고, moving object, long sequence, streaming update, deformable scene이 새 평가 축이 된다.

### 5. Metric reliability가 남은 병목이다

feed-forward geometry가 빨라져도 실제 시스템에서는 pose, scale, calibration, uncertainty, temporal consistency가 필요하다. 이 지점이 robotics/SLAM 연구자가 들어갈 수 있는 공간이다.

### 6. 연구 기회

가장 좋은 연구 wedge는 `VGGT-like prior + metric factor graph / online update + uncertainty`이다. CVPR식 feed-forward 3D와 robotics식 SLAM/mapping 사이의 간극을 메우는 방향이다.

## 산출물 사용법

1. `cvpr2026_3d_recon_blog_seed_list.csv`부터 읽는다.
2. 각 bucket에서 대표 논문 5-7개를 골라 abstract를 직접 확인한다.
3. 논문마다 “field-level meaning” 한 문장과 “limitation / narrowness” 한 문장을 쓴다.
4. 블로그에는 논문 리스트를 많이 넣기보다, cluster 간 이동을 설명한다.
5. 최종 글에서는 VGGT를 제목에 넣되, 결론은 VGGT보다 넓은 “feed-forward metric 3D”로 가져간다.

