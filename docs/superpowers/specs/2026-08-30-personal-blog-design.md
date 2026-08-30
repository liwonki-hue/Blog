# 개인 블로그 설계 스펙

- 날짜: 2026-08-30
- 작성자: liwonki (via Claude)

## 목적

정보 전달이나 수익화가 아닌, 철학/재테크/처세 등 관심 분야에 대한 개인적인 생각을
기록해두는 노트 성격의 블로그. 분야는 계속 추가될 예정. 댓글/공유 등 독자와의
상호작용 기능은 없으며, 오직 글쓴이 자신을 위한 기록이 목적이다.

## 핵심 결정 사항

| 항목 | 결정 |
|---|---|
| 정적 사이트 생성기 | Hugo |
| 호스팅 | GitHub Pages (무료 서브도메인, `<username>.github.io/blog` 형태) |
| 배포 방식 | GitHub Actions — `main` 브랜치 push 시 자동 빌드/배포 |
| 글쓰기 워크플로우 | 로컬에서 마크다운 작성 → `git push` |
| 디자인 | 미니멀 텍스트 중심 (Typo 또는 PaperMod 계열 테마 기반) |
| 댓글/소셜 기능 | 없음 |
| 카테고리 구조 | `content/` 하위 폴더 = 카테고리, 계속 확장 가능 |

## 아키텍처

```
로컬 (Windows)
  └─ Hugo로 마크다운 글 작성
       └─ git push
            └─ GitHub Actions가 자동으로 Hugo 빌드
                 └─ GitHub Pages에 정적 파일 배포
                      └─ https://<username>.github.io/blog 에서 열람
```

- 저장소: GitHub 리포지토리 1개.
- 로컬 미리보기: `hugo server -D`로 실시간 확인.
- 버전 관리: 모든 글이 git 커밋 이력으로 남아 수정 이력 추적 가능.

## 콘텐츠 구조

```
blog/
├── content/
│   ├── philosophy/
│   ├── finance/
│   └── life-wisdom/
├── layouts/
├── static/
└── config.toml
```

- 카테고리는 `content/` 아래 폴더 단위로 관리. 새 분야가 생기면 폴더 추가 + `config.toml`
  메뉴에 한 줄 추가.
- frontmatter:
  ```yaml
  ---
  title: "글 제목"
  date: 2026-08-30
  tags: ["세부주제1", "세부주제2"]
  ---
  ```
  `tags`는 선택 사항이며 세부 주제 검색/모아보기 용도.
- 홈페이지: 최신 글 목록(날짜순) + 카테고리 네비게이션만. 광고/배너/프로필 카드 없음.
- 글 페이지: 제목/날짜/본문만. 댓글, 공유 버튼, 관련 글 추천 위젯 없음.

## 디자인

- 베이스 테마: Hugo "Typo" 또는 "PaperMod" 중 하나를 선택해 커스터마이징 (제로베이스
  CSS 작성 대신 검증된 미니멀 테마를 기반으로 시작).
- 커스터마이징 대상: 한글 가독성 좋은 폰트(Pretendard 등), 다크모드 기본 지원,
  본문 읽기 폭 제한(60~70자 내외).
- 제외 요소: 프로필 사진, 소셜 아이콘, 방문자 카운터, 관련 글 추천.

## 배포 파이프라인

- `.github/workflows/deploy.yml`: `main` push 시 트리거.
  1. Hugo 최신 버전 설치
  2. `hugo --minify` 빌드
  3. `actions/deploy-pages`로 GitHub Pages 배포
- 소요 시간: push 후 약 1분 내외로 반영.
- 실패 시 GitHub Actions 탭에서 빌드 로그 확인 (frontmatter 문법 오류가 흔한 원인).
- 비용: 무료 (개인 블로그 수준 트래픽/빌드 횟수는 GitHub Actions 무료 한도 내).

## 운영 워크플로우

1. 새 글: `hugo new <category>/<slug>.md`
2. 로컬 확인: `hugo server -D` → `localhost:1313`
3. 발행: `git add . && git commit -m "..." && git push`
4. 수정: 파일 수정 후 재 push, 과거 버전은 `git log`로 조회
5. 분야 확장: `content/` 아래 새 폴더 생성 + `config.toml` 메뉴에 항목 추가

## 범위 밖 (Out of Scope)

- 댓글/소셜 공유 기능
- 검색 기능 (필요해지면 추후 별도 스펙으로 검토)
- 커스텀 도메인 연결 (추후 필요 시 GitHub Pages 설정만 추가하면 되므로 별도 설계
  불필요)
- 다국어 지원
