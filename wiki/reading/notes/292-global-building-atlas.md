---
type: Reference
title: "GlobalBuildingAtlas: 전 세계 건물 footprint·높이·LoD1 3D data"
description: "machine learning으로 생성한 global building atlas의 구성, tile 사용법, CRS·품질·혼합 license 주의점"
resource: https://github.com/zhu-xlab/GlobalBuildingAtlas
notion: https://app.notion.com/p/dd21a73cf20b8376a89781ac89ac5ec6
tags: [reading, geospatial, dataset, computer-vision]
timestamp: 2026-07-24
status: summarized
---

# 제공하는 것

GlobalBuildingAtlas는 전 세계 건물 polygon, 높이와 Level of Detail 1 3D model을 제공하는 연구 dataset이다. LoD1은 정교한 지붕·외벽 재질보다 footprint를 높이만큼 돌출한 단순 3D 형상에 가깝다. Repository에는 imagery에서 footprint와 height를 추론하고 결과를 융합해 LoD1을 만드는 `im2bf`, `im2bh`, `infer_height`, `fuse_bf`, `make_lod1` pipeline이 포함된다.

Web viewer는 지역을 살펴보는 용도이며 bulk query나 WFS streaming 용도가 아니다. 실제 분석은 Hugging Face와 mediaTUM에서 index GeoJSON으로 관심 영역과 겹치는 tile을 찾고, 필요한 polygon·height tile만 내려받은 뒤 enrichment script로 결합한다.

# 반드시 확인할 조건

모든 building polygon의 CRS는 `EPSG:3857`이다. 일부 `GBA.ODbLPolygon` file이 4326처럼 보이더라도 3857로 취급하라는 repository의 경고가 있으므로 좌표 범위와 projection을 먼저 검증해야 한다.

Dataset은 ML로 추정됐기 때문에 건물이 빠지거나 footprint·height가 틀릴 수 있다. 국가 전체를 포함한다는 목표와 특정 지역의 완전성은 다르다. 표본 지역에서 aerial image나 cadastral data와 누락률·height error를 비교한 뒤 도시 분석이나 simulation에 사용한다.

# License 분리

`GBA.ODbLPolygon`은 ODbL, `GBA.Polygon`·`GBA.LoD1`과 `GBA.Height`는 CC BY-NC 4.0이다. 서로 결합하면 파생물의 공유 의무와 비상업 제한이 함께 문제될 수 있다. Repository도 법률 자문을 제공하지 않는다고 명시하므로 상업 서비스나 재배포 전에는 component별 provenance와 license를 별도로 검토해야 한다.

Code license도 dataset license와 같다고 가정하면 안 된다. Data, model output, pipeline code의 조건을 각각 확인하고 생성 결과에 tile ID, source part와 version을 남기는 것이 좋다.

# 출처

- [GlobalBuildingAtlas 저장소](https://github.com/zhu-xlab/GlobalBuildingAtlas)
- [GlobalBuildingAtlas 논문](https://essd.copernicus.org/articles/17/6647/2025/)

