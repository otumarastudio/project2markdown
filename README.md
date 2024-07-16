# Project to Markdown Converter

이 Python 스크립트는 프로젝트 디렉토리의 구조와 코드 파일 내용을 단일 Markdown 문서로 변환합니다. 로컬 프로젝트 디렉토리뿐만 아니라 GitHub 저장소 URL도 처리할 수 있습니다. 폴더 구조를 시각화하고 지정된 파일 유형의 내용을 포함하여 프로젝트의 개요를 제공합니다.

## 주요 기능

- 프로젝트 폴더 구조를 ASCII 트리 형태로 시각화
- 지정된 파일 유형(.py, .tsx, .ts, .js, .jsx)의 내용을 Markdown 형식으로 포함
- .gitignore 파일을 참조하여 불필요한 파일 및 폴더 제외
- 추가적인 무시 패턴 지원 (env, .next, node_modules, venv 등)
- 진행 상황 표시기로 처리 과정 시각화
- GitHub 저장소 URL 지원: URL을 입력하면 자동으로 클론하여 처리

## 설치 방법

1. 이 저장소를 클론하거나 스크립트 파일을 다운로드합니다.

2. 필요한 Python 패키지를 설치합니다:

   ```
   pip install tqdm gitpython
   ```

## 사용 방법

1. 명령줄에서 스크립트를 실행합니다:

   ```
   python project_to_markdown.py [project_path_or_github_url] [-o output_file]
   ```

   - `[project_path_or_github_url]`: 변환하려는 프로젝트의 로컬 경로 또는 GitHub 저장소 URL. 생략하면 실행 시 입력을 요청합니다.
   - `[-o output_file]`: 출력 Markdown 파일의 이름. 기본값은 "project_structure.md" 입니다.

2. 현재 디렉토리를 처리하려면:

   ```
   python project_to_markdown.py .
   ```

3. 특정 경로와 출력 파일을 지정하려면:

   ```
   python project_to_markdown.py /path/to/your/project -o my_project_doc.md
   ```

4. GitHub 저장소를 처리하려면:

   ```
   python project_to_markdown.py https://github.com/username/repo.git -o github_project_doc.md
   ```

## 출력 결과

스크립트는 다음과 같은 구조의 Markdown 문서를 생성합니다:

1. 프로젝트 제목
2. 폴더 구조 다이어그램 (ASCII 트리 형태)
3. 각 코드 파일의 내용 (파일 경로를 헤더로 사용)

## 주의 사항

- 큰 프로젝트의 경우 생성된 Markdown 파일이 매우 클 수 있습니다.
- 기본적으로 .py, .tsx, .ts, .js, .jsx 파일만 처리합니다. 다른 파일 유형을 포함하려면 스크립트를 수정해야 합니다.
- 민감한 정보가 포함된 파일은 자동으로 제외되지 않을 수 있으므로 주의가 필요합니다.
- GitHub 저장소를 처리할 때는 임시 디렉토리에 클론됩니다. 대용량 저장소의 경우 시간이 오래 걸릴 수 있습니다.

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 LICENSE 파일을 참조하세요.

## 기여

버그 리포트, 기능 제안, 풀 리퀘스트를 환영합니다. 중요한 변경사항에 대해서는 먼저 이슈를 열어 논의해 주세요.

