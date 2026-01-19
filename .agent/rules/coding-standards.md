---
description: "Coding standards, naming conventions, and tech stack configurations"
version: 1.0.0
---

# 코딩 표준 및 기술 스택 (Coding Standards)

> [!NOTE]
> 이 파일은 코드를 작성하거나 설계할 때 반드시 참조해야 합니다.
> `rules/core-principles.md`의 "Dynamic Context Loading"에 의해 호출됩니다.

## 1. 기술 스택 설정 (Tech Stack)

> [!IMPORTANT]
> 프로젝트의 실제 기술 스택은 `docs/PROJECT-CONFIG.md`를 따릅니다.
> 아래 내용은 일반적인 변수 정의입니다.

| 변수 | 설명 |
|------|------|
| `[LANGUAGE]` | 주 프로그래밍 언어 (예: TypeScript, Python) |
| `[FRAMEWORK]` | 프레임워크 (예: Next.js, FastAPI) |
| `[TEST_RUNNER]` | 테스트 실행기 (예: Vitest, Pytest) |

## 2. 코딩 스타일 및 규칙 (General Style)

### 기본 원칙
- **함수형 지향**: 가능한 한 순수 함수와 불변성을 유지하십시오.
- **타입 안전성**: `any` 사용을 지양하고 명시적 타입을 사용하십시오.
- **Single Responsibility**: 파일과 함수는 하나의 역할만 수행해야 합니다.

### 네이밍 규칙 (Naming Conventions)
- **Compact & Clear**: `AbstractSingletonProxyFactoryBean` 같은 이름 금지.
- **Variables/Functions**: `camelCase` (JS/TS), `snake_case` (Python)
- **Components/Classes**: `PascalCase`
- **Files**: `kebab-case` (예: `user-profile.tsx`, `auth_service.py`)

## 3. 코드 구현 프로토콜 (Implementation Protocol)

### 3.1 Edit Safety (편집 안전)
- **Blind Edit 금지**: 코드를 수정하기 전에 파일을 읽고 컨텍스트를 파악하십시오.
- **Syntax Verification**: 수정 후 반드시 문법 검사(`py_compile`, `npx eslint` 등)를 수행하십시오.

### 3.2 TDD Protocol (Test-Driven Development)
1. **Red**: 실패하는 테스트를 먼저 작성합니다.
2. **Green**: 테스트를 통과하는 최소한의 코드를 작성합니다.
3. **Refactor**: 중복을 제거하고 가독성을 높입니다.

**커버리지 목표**:
- 비즈니스 로직/유틸리티: 100%
- UI 컴포넌트: 주요 인터랙션 및 상태 변화

## 4. Git 컨벤션 (Conventional Commits)

```
<type>(<scope>): <subject>
```

| 타입 | 용도 |
|------|------|
| `feat` | 새로운 기능 |
| `fix` | 버그 수정 |
| `refactor` | 기능 변경 없는 코드 개선 |
| `docs` | 문서 수정 |
| `test` | 테스트 코드 추가/수정 |
| `chore` | 빌드/설정 변경 |

## 5. UI/UX 가이드라인
- **Mobile First**: 반응형 디자인을 기본으로 합니다.
- **Accessibility**: 시맨틱 HTML 태그와 ARIA 속성을 적절히 사용하십시오.
- **Feedback**: 로딩(`Skeleton`), 에러(`Toast`), 성공 상태를 명시적으로 처리하십시오.

## 6. Definition of Done (DoD)
> [!IMPORTANT]
> 모든 Task는 아래 조건을 충족해야 완료(Complete)로 간주됩니다.

1. **코드 작성 완료**: 요구사항 구현, 타입 에러 0개, 린트 에러 0개.
2. **테스트 통과**: 유닛/E2E 테스트 작성 및 `npm test` 통과.
3. **코드 리뷰**: 불필요한 로그 삭제, 셀프 리뷰 완료.
4. **문서화**: 복잡한 로직 주석 및 README 업데이트.
