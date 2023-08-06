import shutil
import subprocess
from pathlib import Path
from typing import List
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter


class CustomHtmlFormatter(HtmlFormatter):
    def __init__(self, lang_str='', **options):
        super().__init__(**options)
        # lang_str has the value {lang_prefix}{lang}
        # specified by the CodeHilite's options
        self.lang_str = lang_str

    def _wrap_code(self, source):
        yield 0, f'<code class="{self.lang_str}">'
        yield from source
        yield 0, '</code>'


class SourceConverter:
    """
    This class can do below.
    download GitHub repository.
    extract the zip file.
    convert source code to html.
    convert html to images.
    convert images to movie.
    :param css_style: You can select css_style from `default`, `emacs`, `friendly`, `colorful`.
    """

    def __init__(self, css_style='default'):
        css_dict = {
            'default': 'https://storage.googleapis.com/vrchat/css/default.css',
            'emacs': 'https://storage.googleapis.com/vrchat/css/emacs.css',
            'friendly': 'https://storage.googleapis.com/vrchat/css/friendly.css',
            'colorful': 'https://storage.googleapis.com/vrchat/css/colorful.css',
        }
        self.css_url = css_dict[css_style]

    def add_css(self, html: str) -> str:
        """
        Add css to html source code.
        :param html source code.
        :return: html source code with css.
        """
        return "\n".join([f'<link href="{self.css_url}" rel="stylesheet">', html])

    @staticmethod
    def add_h1(html: str, file_path: Path) -> str:
        """
        Add h1 tag to html.
        :param html:
        :param file_path:
        :return:
        """
        text = str(file_path).split('/')[1:]
        text = "/".join(text)
        return f'<h1>{text}</h1>\n{html}'

    def file_to_html(self, file_path: Path) -> Path:
        """
        Convert file to html. Output file path is `html/{file_path}`.
        :param file_path:
        :return html_file_path:
        """
        html_file_path = Path(str(file_path).replace('project', 'html') + '.html')
        print(f"html_file_path parent: {html_file_path.parent}")
        html_file_path.parent.mkdir(parents=True, exist_ok=True)
        if file_path.suffix == '.md':
            # Markdown to html with grip
            subprocess.check_output(['grip', '--export', str(file_path)])
            file_path = Path(str(file_path).replace('.md', '.html'))
            # Move file from project to html directory.
            html_file_path = Path(str(file_path).replace('project', 'html'))
            shutil.move(str(file_path), str(html_file_path))
        else:
            # Source code to html
            with open(file_path, 'r') as f:
                code = f.read()
            html = highlight(code, PythonLexer(), HtmlFormatter())
            html = self.add_h1(html, file_path)
            html = self.add_css(html)
            with open(html_file_path, 'w') as f:
                f.write(html)
        return html_file_path

    @staticmethod
    def select_target_files(project_folder_path: Path, targets: List[str]) -> List[Path]:
        """
        Select target files from project folder. filter by target types.
        :param project_folder_path:
        :param targets:
        :return: target file paths
        """
        target_paths = []
        for target in targets:
            target_paths.extend(project_folder_path.glob(f"**/{target}"))
        return target_paths

    @staticmethod
    def _is_binary_file(file_path: Path) -> bool:
        """
        Check file is binary or not.
        :param file_path:
        :return: bool
        """
        with open(file_path, 'rb') as f:
            chunk = f.read(1024)
            if b'\0' in chunk:
                return True
        with open(file_path, 'r') as f:
            try:
                f.read()
                return False
            except UnicodeDecodeError:
                return True

    def project_to_html(self, project_folder_path: Path, targets: List[str]) -> List[Path]:
        """
        Convert project to html. Please specify target files. If target file is binary file, skip it.
        :param project_folder_path:
        :param targets:
        :return: html file paths
        """
        target_files = self.select_target_files(project_folder_path, targets)
        html_files = []
        for target_file in target_files:
            if target_file.is_dir(): continue
            if self._is_binary_file(target_file): continue
            html_file = self.file_to_html(target_file)
            html_files.append(html_file)
        return html_files
