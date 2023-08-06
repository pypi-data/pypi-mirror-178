# Source Convertor

This is a project to convert the source code on GitHub into a video.

## Installation

```bash
pip install source_converter
```

or

```bash
pip install git+https://github.com/noricha-vr/source_converter
```

## Usage

```python
from source_converter import SourceConverter, GithubDownloader

# Select the repository and file types.
url = "https://github.com/noricha-vr/source_converter"
targets = ['README.md', '*.py', ]

# Download the repository.
project_name = url.split("/")[-1]
folder_path = GithubDownloader.download_github_archive_and_unzip_to_file(url, project_name)
project_path = GithubDownloader.rename_project(folder_path, project_name)

# Convert the source codes to html files.
source_converter = SourceConverter('default')
html_file_path = source_converter.project_to_html(project_path, targets)
```