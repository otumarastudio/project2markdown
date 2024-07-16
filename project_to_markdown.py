import os
import fnmatch
import argparse
import sys
import tempfile
import shutil
from tqdm import tqdm
from git import Repo
from urllib.parse import urlparse

def parse_gitignore(gitignore_path):
    if not os.path.exists(gitignore_path):
        return []
    
    with open(gitignore_path, 'r') as file:
        return [line.strip() for line in file if line.strip() and not line.startswith('#')]

def should_ignore(path, ignore_patterns):
    for pattern in ignore_patterns:
        if fnmatch.fnmatch(path, pattern):
            return True
    return False

def generate_tree(startpath, ignore_patterns):
    tree = []
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = '│   ' * (level - 1) + '├── ' if level > 0 else ''
        relpath = os.path.relpath(root, startpath)
        if relpath == '.':
            tree.append(os.path.basename(startpath) + '/')
        elif not should_ignore(relpath, ignore_patterns):
            tree.append(indent + os.path.basename(root) + '/')
        
        subindent = '│   ' * level + '├── '
        for f in files:
            if not should_ignore(os.path.join(relpath, f), ignore_patterns):
                tree.append(subindent + f)
    
    return '\n'.join(tree)

def create_markdown_from_project(project_path, output_file):
    gitignore_path = os.path.join(project_path, '.gitignore')
    ignore_patterns = parse_gitignore(gitignore_path)
    
    # 추가적으로 무시할 폴더나 파일들
    ignore_patterns.extend(['**/env/*', '**/.next/*', '**/node_modules/*', '**/venv/*', '**/.env', '**/*.pyc'])

    with open(output_file, 'w', encoding='utf-8') as md_file:
        md_file.write("# Project Structure and Code\n\n")
        
        # Add folder structure diagram
        md_file.write("## Folder Structure\n\n")
        md_file.write("```\n")
        md_file.write(generate_tree(project_path, ignore_patterns))
        md_file.write("\n```\n\n")
        
        md_file.write("## File Contents\n\n")
        
        total_files = sum([len(files) for r, d, files in os.walk(project_path)])
        with tqdm(total=total_files, desc="Processing files", unit="file") as pbar:
            for root, dirs, files in os.walk(project_path):
                # .gitignore에 명시된 디렉토리 제외
                dirs[:] = [d for d in dirs if not should_ignore(os.path.join(root, d), ignore_patterns)]
                
                for file in files:
                    pbar.update(1)
                    if file.endswith(('.py', '.tsx', '.ts', '.js', '.jsx')):
                        file_path = os.path.join(root, file)
                        relative_path = os.path.relpath(file_path, project_path)
                        
                        # .gitignore에 명시된 파일 제외
                        if should_ignore(relative_path, ignore_patterns):
                            continue
                        
                        md_file.write(f"### {relative_path}\n\n")
                        md_file.write("```" + file.split('.')[-1] + "\n")
                        
                        try:
                            with open(file_path, 'r', encoding='utf-8') as code_file:
                                md_file.write(code_file.read())
                        except UnicodeDecodeError:
                            md_file.write("# Unable to read file: encoding issue\n")
                        
                        md_file.write("\n```\n\n")

def clone_github_repo(url):
    with tempfile.TemporaryDirectory() as tmpdirname:
        print(f"Cloning repository from {url}...")
        Repo.clone_from(url, tmpdirname)
        return tmpdirname

def is_github_url(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc in ['github.com', 'www.github.com']

def main():
    parser = argparse.ArgumentParser(description="Convert project files to a single Markdown document.")
    parser.add_argument("project_path", nargs="?", default=None, help="Path to the project directory or GitHub repository URL")
    parser.add_argument("-o", "--output", default="project_structure.md", help="Output Markdown file name")
    
    args = parser.parse_args()
    
    if args.project_path is None:
        args.project_path = input("Enter the path to your project directory or GitHub repository URL: ").strip()
    
    if is_github_url(args.project_path):
        project_path = clone_github_repo(args.project_path)
    elif os.path.isdir(args.project_path):
        project_path = args.project_path
    else:
        print(f"Error: '{args.project_path}' is not a valid directory or GitHub URL.")
        sys.exit(1)
    
    print(f"Processing project: {project_path}")
    print(f"Output will be saved to: {args.output}")
    
    create_markdown_from_project(project_path, args.output)
    
    print(f"\nMarkdown file '{args.output}' has been created successfully.")

if __name__ == "__main__":
    main()
