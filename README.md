# Haandol Blog

Jekyll로 만든 기술 블로그입니다. https://haandol.github.io

## Dev Container에서 실행

Docker와 VS Code의 Dev Containers 확장을 설치한 뒤, 명령 팔레트에서
**Dev Containers: Reopen in Container**를 실행합니다. 기존 컨테이너를 사용 중이면
**Dev Containers: Rebuild Container**로 새 설정을 적용합니다.

컨테이너는 Ruby 3.4를 사용하고, 처음 생성할 때 `Gemfile.lock`에 지정된 Bundler와
의존성을 설치합니다. 설치가 끝나면 컨테이너 터미널에서 실행합니다.

```bash
bundle exec jekyll serve --host 0.0.0.0 --livereload
```

미리보기는 http://localhost:4000 에서 볼 수 있습니다. 초안도 보려면 `--drafts`를 추가합니다.

```bash
bundle exec jekyll build
.agents/scripts/post-lint.sh
```

SSH 키 폴더를 직접 마운트하지 않으며, Git 인증은 VS Code가 전달하는 자격 증명이나 SSH agent를 사용합니다.
