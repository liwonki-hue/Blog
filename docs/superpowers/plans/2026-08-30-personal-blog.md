# 개인 블로그 (Hugo + GitHub Pages) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Hugo 기반 정적 사이트로 철학/재테크/처세 카테고리를 가진 개인 기록용 블로그를 구축하고, GitHub Pages에 자동 배포되도록 한다.

**Architecture:** 로컬에서 Hugo로 마크다운 콘텐츠를 작성하고 `git push`하면 GitHub Actions가 자동으로 빌드하여 GitHub Pages에 배포한다. 댓글/소셜 기능 없이 글쓰기와 배포만 남긴 최소 구성.

**Tech Stack:** Hugo (Extended), PaperMod 테마, GitHub Actions, GitHub Pages.

**Spec:** [docs/superpowers/specs/2026-08-30-personal-blog-design.md](../specs/2026-08-30-personal-blog-design.md)

## Global Constraints

- 댓글, 공유 버튼, 방문자 카운터, 프로필/아바타 카드는 절대 추가하지 않는다 (스펙: 범위 밖).
- 카테고리는 `content/` 하위 폴더 단위로만 구분한다 (스펙: 콘텐츠 구조).
- 미니멀 텍스트 중심 디자인을 유지한다 — 장식 요소를 넣지 않는다 (스펙: 디자인).
- 호스팅은 GitHub Pages 무료 서브도메인만 사용한다. 커스텀 도메인 연결은 범위 밖.

---

### Task 1: Hugo 사이트 스캐폴딩

**Files:**
- Create: `hugo.toml`
- Create: `archetypes/default.md` (Hugo 기본 생성)
- Create: `content/`, `layouts/`, `static/`, `data/`, `themes/` (Hugo 기본 생성, 빈 디렉터리)

**Interfaces:**
- Consumes: 없음 (최초 작업)
- Produces: `hugo.toml` — 이후 모든 태스크가 이 파일에 설정을 추가함. Hugo 사이트 루트가 `c:/Users/PCLOVE/Downloads/BLOG` 자체임 (하위 폴더 아님).

- [ ] **Step 1: Hugo 설치 확인**

Run: `hugo version`

Expected: 버전 문자열 출력, `extended` 표기 포함 (예: `hugo v0.140.0+extended`). extended가 아니면 아래로 재설치.

미설치 또는 extended가 아니면 실행:
```powershell
winget install Hugo.Hugo.Extended
```
설치 후 새 터미널에서 `hugo version` 재확인.

- [ ] **Step 2: 현재 디렉터리에 Hugo 사이트 스캐폴딩**

이미 `docs/`와 `.git`이 존재하는 디렉터리이므로 `--force` 사용:
```powershell
hugo new site . --force
```

Expected: `Congratulations! Your new Hugo site is created in ...` 메시지. `content/`, `layouts/`, `static/`, `data/`, `themes/`, `archetypes/`, `hugo.toml` 생성 확인.

- [ ] **Step 3: 생성된 파일 확인**

Run: `Get-ChildItem` (또는 `ls`)

Expected: `hugo.toml`, `content`, `layouts`, `static`, `data`, `themes`, `archetypes`, `docs` 가 모두 보임.

- [ ] **Step 4: Commit**

```powershell
git add hugo.toml archetypes content layouts static data themes
git commit -m "Hugo 사이트 스캐폴딩"
```

---

### Task 2: PaperMod 테마 설치 및 기본 사이트 설정

**Files:**
- Create: `.gitmodules`
- Create: `themes/PaperMod/` (git submodule)
- Modify: `hugo.toml`

**Interfaces:**
- Consumes: Task 1이 만든 `hugo.toml`
- Produces: `theme = "PaperMod"` 설정 완료된 `hugo.toml`. 이후 태스크는 이 파일의 `[params]` 섹션에 이어서 옵션을 추가함.

- [ ] **Step 1: PaperMod 서브모듈 추가**

```powershell
git submodule add --depth=1 https://github.com/adityatelange/hugo-PaperMod.git themes/PaperMod
```

Expected: `themes/PaperMod` 디렉터리에 테마 파일들이 생성되고 `.gitmodules` 파일이 생성됨.

- [ ] **Step 2: `hugo.toml` 기본 설정 작성**

`hugo.toml` 파일 전체를 아래 내용으로 교체:

```toml
baseURL = "/"
languageCode = "ko-kr"
title = "기록"
theme = "PaperMod"
paginate = 10

enableRobotsTXT = true
enableEmojiSearch = false

[params]
  env = "production"
  defaultTheme = "auto"
  ShowReadingTime = false
  ShowShareButtons = false
  ShowPostNavLinks = false
  ShowBreadCrumbs = false
  ShowCodeCopyButtons = false
  ShowWordCount = false
  ShowRssButtonInSectionTermList = false
  disableSpecial1stPost = true
  hidemeta = false
  comments = false

[menu]
  [[menu.main]]
    identifier = "philosophy"
    name = "철학"
    url = "/philosophy/"
    weight = 10
  [[menu.main]]
    identifier = "finance"
    name = "재테크"
    url = "/finance/"
    weight = 20
  [[menu.main]]
    identifier = "life-wisdom"
    name = "처세"
    url = "/life-wisdom/"
    weight = 30
```

이 설정으로 프로필/아바타 카드, 공유 버튼, 읽기 시간, 관련 글, 브레드크럼 등 장식 요소가 모두 꺼진다 (Global Constraints 준수).

- [ ] **Step 3: 빌드 검증**

```powershell
hugo --minify
```

Expected: 에러 없이 완료, `Total in N ms` 형태의 요약 출력. `public/` 디렉터리 생성 확인.

- [ ] **Step 4: `public/`을 git이 추적하지 않도록 설정**

`.gitignore` 파일 생성 (없으면):
```
public/
resources/_gen/
.hugo_build.lock
```

- [ ] **Step 5: Commit**

```powershell
git add .gitmodules themes hugo.toml .gitignore
git commit -m "PaperMod 테마 설치 및 기본 설정"
```

---

### Task 3: 콘텐츠 폴더 구조 및 샘플 글 작성

**Files:**
- Create: `content/philosophy/_index.md`
- Create: `content/finance/_index.md`
- Create: `content/life-wisdom/_index.md`
- Create: `content/philosophy/stoicism-and-equanimity.md`
- Create: `content/finance/compound-interest-trap.md`
- Create: `content/life-wisdom/how-to-say-no.md`

**Interfaces:**
- Consumes: Task 2의 `hugo.toml` 메뉴 설정 (`/philosophy/`, `/finance/`, `/life-wisdom/` 경로와 일치해야 함)
- Produces: 카테고리별 콘텐츠 폴더와 샘플 글 3편. 이후 실제 글쓰기는 이 폴더 구조를 그대로 따름.

- [ ] **Step 1: 카테고리 섹션 인덱스 파일 생성**

`content/philosophy/_index.md`:
```markdown
---
title: "철학"
---
```

`content/finance/_index.md`:
```markdown
---
title: "재테크"
---
```

`content/life-wisdom/_index.md`:
```markdown
---
title: "처세"
---
```

- [ ] **Step 2: 샘플 글 3편 작성**

`content/philosophy/stoicism-and-equanimity.md`:
```markdown
---
title: "스토아철학과 평정심"
date: 2026-08-30
tags: ["스토아철학", "감정"]
---

내가 통제할 수 있는 것과 없는 것을 구분하는 것에서부터 평정심은 시작된다.
에픽테토스는 이를 "우리에게 달린 것"과 "달리지 않은 것"으로 나누었다.

타인의 평가, 날씨, 과거는 내가 통제할 수 없다. 반면 나의 판단, 반응,
선택은 온전히 내 몫이다. 이 구분을 매일 되새기는 것만으로도 불필요한
동요가 줄어든다.
```

`content/finance/compound-interest-trap.md`:
```markdown
---
title: "복리의 함정"
date: 2026-08-30
tags: ["복리", "투자심리"]
---

복리는 시간이 지날수록 강력해지지만, 그 힘을 체감하기까지 걸리는
시간이 길다는 게 함정이다. 초기 10년의 그래프는 거의 평평해 보인다.

그래서 많은 사람들이 복리의 초입에서 포기한다. 복리를 믿는다는 것은
숫자를 믿는 게 아니라, 아무 일도 일어나지 않는 것처럼 보이는 구간을
버티는 인내를 믿는 것이다.
```

`content/life-wisdom/how-to-say-no.md`:
```markdown
---
title: "거절하는 법"
date: 2026-08-30
tags: ["관계", "경계"]
---

거절은 관계를 깨는 행위가 아니라 관계의 경계를 명확히 하는 행위다.
모든 요청에 응하는 사람은 결국 자신의 우선순위를 잃는다.

이유를 장황하게 설명할 필요는 없다. "지금은 어렵다"는 한 문장으로도
충분하다. 설명이 길어질수록 오히려 상대는 협상의 여지가 있다고
느낀다.
```

- [ ] **Step 3: 로컬 서버로 렌더링 검증**

```powershell
hugo server -D
```

브라우저에서 `http://localhost:1313` 접속.

Expected: 홈페이지에 글 3개가 날짜순으로 보이고, 상단 메뉴에 철학/재테크/처세가 보이며 각 메뉴 클릭 시 해당 카테고리 글만 필터링되어 보임. 서버 종료: `Ctrl+C`.

- [ ] **Step 4: Commit**

```powershell
git add content
git commit -m "카테고리 구조 및 샘플 글 3편 추가"
```

---

### Task 4: 디자인 커스터마이징 (한글 폰트 / 본문 읽기 폭)

**Files:**
- Create: `assets/css/extended/custom.css`

**Interfaces:**
- Consumes: Task 2에서 설치된 PaperMod 테마 (PaperMod는 `assets/css/extended/*.css`가 존재하면 자동으로 로드하여 기본 스타일 뒤에 이어 붙임)
- Produces: 한글 가독성 폰트와 본문 폭이 제한된 최종 스타일. 이후 태스크에는 영향 없음.

- [ ] **Step 1: 커스텀 CSS 작성**

`assets/css/extended/custom.css`:
```css
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.css');

:root {
  --main-width: 700px;
}

body {
  font-family: 'Pretendard Variable', Pretendard, -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
}
```

`--main-width`는 PaperMod가 본문 컨테이너 폭에 사용하는 CSS 변수로, 기본값(900px)보다 좁혀 한 줄당 글자 수를 줄인다.

- [ ] **Step 2: 로컬 서버로 시각 검증**

```powershell
hugo server -D
```

`http://localhost:1313`에서 폰트가 Pretendard로 바뀌고 본문 컬럼이 이전보다 좁아진 것을 육안으로 확인. 서버 종료: `Ctrl+C`.

- [ ] **Step 3: Commit**

```powershell
git add assets
git commit -m "한글 폰트 및 본문 읽기 폭 커스터마이징"
```

---

### Task 5: GitHub Actions 배포 워크플로우 작성

**Files:**
- Create: `.github/workflows/deploy.yml`

**Interfaces:**
- Consumes: Task 1~4에서 완성된 사이트 (루트의 `hugo.toml`, `content/`, `themes/PaperMod`, `assets/css/extended/custom.css`)
- Produces: `main` 브랜치 push 시 자동으로 빌드/배포되는 워크플로우. Task 6에서 실제 push로 이 워크플로우가 실행됨.

- [ ] **Step 1: 워크플로우 파일 작성**

`.github/workflows/deploy.yml`:
```yaml
name: Deploy Hugo site to Pages

on:
  push:
    branches: ["main"]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

defaults:
  run:
    shell: bash

jobs:
  build:
    runs-on: ubuntu-latest
    env:
      HUGO_VERSION: 0.140.0
    steps:
      - name: Install Hugo CLI
        run: |
          wget -O ${{ runner.temp }}/hugo.deb https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-amd64.deb \
          && sudo dpkg -i ${{ runner.temp }}/hugo.deb
      - name: Checkout
        uses: actions/checkout@v4
        with:
          submodules: recursive
          fetch-depth: 0
      - name: Setup Pages
        id: pages
        uses: actions/configure-pages@v5
      - name: Build with Hugo
        run: |
          hugo \
            --gc \
            --minify \
            --baseURL "${{ steps.pages.outputs.base_url }}/"
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./public

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

`baseURL`은 `actions/configure-pages`가 실제 GitHub Pages URL을 자동으로 주입하므로 `hugo.toml`의 `baseURL = "/"`는 로컬 개발용으로 그대로 둔다.

- [ ] **Step 2: YAML 문법 검증**

```powershell
Get-Content .github/workflows/deploy.yml | python -c "import sys, yaml; yaml.safe_load(sys.stdin)" 2>&1
```
(python/pyyaml이 없으면: `python -m pip install pyyaml` 후 재실행, 그것도 여의치 않으면 이 단계는 건너뛰고 Task 6의 실제 push 후 Actions 탭에서 실행 결과로 검증)

Expected: 에러 없이 조용히 종료 (파싱 성공).

- [ ] **Step 3: Commit**

```powershell
git add .github/workflows/deploy.yml
git commit -m "GitHub Actions Hugo 배포 워크플로우 추가"
```

---

### Task 6: GitHub 원격 저장소 연결 및 최초 배포

**Files:**
- Modify: 없음 (원격 설정 및 push만 수행)

**Interfaces:**
- Consumes: Task 1~5에서 완성된 로컬 리포지토리 전체
- Produces: GitHub에 배포된 라이브 사이트

이 태스크는 실제 원격 저장소 생성과 push — 로컬 밖으로 나가는 동작이므로, 아래 Step 1 전에 반드시 사용자에게 GitHub 계정명과 저장소 이름을 확인하고, push 직전에 다시 한번 진행 여부를 확인한다.

- [ ] **Step 1: 사용자에게 GitHub 계정명과 저장소 이름 확인**

사용자에게 실제 GitHub 계정명(username)과 사용할 저장소 이름을 물어본다. 이후 단계의 `<username>`, `<repo>`를 그 값으로 치환해서 실행한다.

- [ ] **Step 2: GitHub에 저장소 생성**

`gh` CLI 인증이 되어 있다면:
```powershell
gh repo create <username>/<repo> --public --source=. --remote=origin
```

인증이 안 되어 있다면 사용자가 직접 https://github.com/new 에서 저장소를 생성하고 아래로 원격을 연결:
```powershell
git remote add origin https://github.com/<username>/<repo>.git
```

- [ ] **Step 3: 브랜치명을 main으로 정리 후 push (사용자 확인 후 실행)**

```powershell
git branch -M main
git push -u origin main
```

Expected: push 성공 메시지.

- [ ] **Step 4: GitHub Pages 설정을 "GitHub Actions"로 변경**

브라우저에서 `https://github.com/<username>/<repo>/settings/pages` 접속 → "Build and deployment" → Source를 "GitHub Actions"로 선택 (사용자가 직접 웹 UI에서 수행).

- [ ] **Step 5: 배포 확인**

`https://github.com/<username>/<repo>/actions`에서 워크플로우 실행 상태 확인.

Expected: `Deploy Hugo site to Pages` 워크플로우가 초록색 체크(성공)로 완료. 완료 후 `https://<username>.github.io/<repo>/` 접속해 홈페이지와 카테고리 3개, 샘플 글 3편이 정상적으로 보이는지 확인.

- [ ] **Step 6: Commit (필요 시)**

원격 설정 자체는 커밋 대상이 아니므로 이 단계에서는 커밋 없음. Task 5까지의 커밋이 이미 push되어 있음을 `git log --oneline -1`과 `git log origin/main --oneline -1`(fetch 후)이 같은 커밋을 가리키는지로 확인.

---

## 완료 기준

- `hugo --minify`가 로컬에서 에러 없이 빌드된다.
- `hugo server -D`로 접속 시 철학/재테크/처세 3개 카테고리와 각 샘플 글이 정상 렌더링된다.
- GitHub Actions 워크플로우가 `main` push 시 성공적으로 완료된다.
- `https://<username>.github.io/<repo>/`에서 실제 배포된 사이트가 열람 가능하다.
