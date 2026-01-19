---
description: 문서(들)를 분석, 검증, 고도화하는 재귀적 개선 프롬프트
version: 1.0.0
author: User
---

# 문서 고도화 프롬프트 (Document Enhancement Prompt)

> [!NOTE]
> 이 프롬프트는 LLM 에이전트에게 문서(들)의 재귀적 분석, 검증, 고도화를 지시합니다.
> 플레이스홀더(`{{...}}`)를 실제 값으로 교체하여 사용하세요.
> **언어 규칙**: 문서는 **한국어**로 작성하되, 핵심 기술 용어는 **영어**를 사용하거나 **한국어 (English)** 형식을 사용합니다.

---

## 1. 레퍼런스 (References)

다음 웹페이지의 내용을 레퍼런스로 사용하세요:

{{REFERENCE_URLS}}
<!-- 
예시:
- https://github.com/snarktank/ai-dev-tasks
- https://code.visualstudio.com/docs/copilot/customization/custom-instructions
- https://code.visualstudio.com/docs/copilot/customization/prompt-files
-->

---

## 2. 대상 파일 (Target Files)

다음 문서(들)을 분석하고 고도화하세요:

{{TARGET_FILES}}
<!--
예시:
- .agent/rules/core-principles.md
- .agent/workflows/create-prd.md
- .agent/workflows/execute-task.md
- .agent/workflows/generate-tasks.md
- .agent/workflows/run-epic.md
-->

---

## 3. 작업 목표 (Objectives)

### 3.1 분석 및 검증 항목

다음 관점에서 대상 파일(들)을 분석하고 검토하고 평가하세요:

| 검증 항목 | 설명 |
|-----------|------|
| **논리적 충돌** | 문서 내/문서 간 모순되는 지시사항이 없는지 |
| **일관성** | 용어, 형식, 스타일이 일관되게 사용되었는지 |
| **순서** | 프로세스와 단계가 논리적 순서로 배치되었는지 |
| **타당성** | 지시사항이 현실적으로 실행 가능한지 |
| **기술 근거** | 기술적 주장이 검증 가능한 근거를 가지고 있는지 |

### 3.2 추가 검증 항목 (선택)

{{ADDITIONAL_VALIDATION_CRITERIA}}
<!--
예시:
- 이중 언어 표기 일관성 (한국어 (English) 형식)
- 특정 도구 참조 구문 검증 (#tool:name)
- 워크플로우 연결성 검증
-->

---

## 4. 제약 조건 (Constraints)

### ⛔ 절대로 해서는 안 되는 일 (MUST NOT)

- **요약 (Summarization)**: 기존 내용을 축약하지 마세요
- **생략 (Omission)**: 기존 내용을 누락시키지 마세요
- **정리 (Consolidation)**: 기존 섹션을 임의로 합치지 마세요
- **삭제 (Deletion)**: 기존 내용을 제거하지 마세요

### ✅ 해야 하는 일 (MUST DO)

- **검토 (Review)**: 모든 내용을 꼼꼼히 읽고 분석하세요
- **검증 (Verify)**: 리서치를 통해 내용의 정확성을 확인하세요
- **고도화 (Enhance)**: 부족한 부분을 보완하고 개선하세요
- **개선 (Improve)**: 더 명확하고 효과적인 표현으로 다듬으세요

---

## 5. 리서치 요구사항 (Research Requirements)

> [!IMPORTANT]
> 검증은 혼자서 추측하지 말고, 반드시 리서치한 근거를 바탕으로 수행하세요.

### 5.1 리서치 소스

다음 소스에서 근거를 찾으세요:

- 공식 레퍼런스 문서
- 업계 최신 트렌드 ({{CURRENT_YEAR}} 기준)
- 우수 사례 (Best Practices)
- 학술 논문 (해당되는 경우)

### 5.2 사용할 도구

```
#tool:sequential-thinking - 복잡한 분석과 의사결정
#tool:context7 - 라이브러리/프레임워크 문서 조회
#tool:firecrawl - 웹 페이지 스크래핑
search_web() - 웹 검색
research_mode() - 심층 리서치 모드
```

---

## 6. 실행 프로세스 (Execution Process)

다음 단계를 **재귀적으로** 수행하세요:

### Phase 1: 리서치 (Research)
1. 레퍼런스 URL 분석
2. 업계 최신 트렌드 검색
3. 관련 모범 사례 수집

### Phase 2: 계획 (Planning)
4. 리서치 결과를 바탕으로 고도화 계획 수립
5. 계획의 타당성 검토
6. 계획을 구체적으로 명세화

### Phase 3: 실행 (Execution)
7. 검증된 계획에 따라 문서 수정
8. 변경 사항 적용

### Phase 4: 검증 (Verification)
9. 변경된 문서 확인 및 분석
10. 완료 기준 충족 여부 평가
11. 미충족 시 Phase 2로 복귀 (재귀)

---

## 7. 완료 기준 (Completion Criteria)

다음 기준을 **모두** 충족해야 작업이 완료됩니다:

### 7.1 개별 파일 기준

- [ ] 내부 일관성 확보
- [ ] 모순점 없음
- [ ] 논리 타당성 검증됨
- [ ] 모호한 표현 없음
- [ ] 구조가 명확함

### 7.2 전체 파일 기준 (다중 파일인 경우)

- [ ] 파일 간 일관성 확보
- [ ] 상호 충돌 없음
- [ ] 불필요한 중복 없음
- [ ] 워크플로우 연결성 확보

### 7.3 근거 기준

- [ ] 모든 개선 사항에 리서치 근거 존재
- [ ] 근거가 검토되고 검증됨

---

## 8. 추가 지시사항 (Additional Instructions)

{{ADDITIONAL_INSTRUCTIONS}}
<!--
예시:
- 이중 언어 표기는 "한국어 (English)" 형식으로 통일하세요
- 모든 MCP 도구 참조는 #tool:name 형식을 사용하세요
- 2025-2026 최신 트렌드를 반영하세요
-->

---

## 9. 출력 형식 (Output Format)

작업 완료 시 다음 정보를 포함하여 보고하세요:

```markdown
## 고도화 완료 보고

### 검증 결과 요약
| 기준 | 상태 | 비고 |
|------|------|------|
| 개별 파일 일관성 | ✅/❌ | ... |
| 파일 간 일관성 | ✅/❌ | ... |
| 리서치 근거 확보 | ✅/❌ | ... |

### 주요 변경 사항
1. [파일명]: 변경 내용 요약
2. ...

### 적용된 리서치 근거
| 출처 | 적용 내용 |
|------|----------|
| ... | ... |
```

---

## 사용 예시

```
/enhance-documents

{{TARGET_FILES}}를 고도화해줘.
{{ADDITIONAL_INSTRUCTIONS}}
```
