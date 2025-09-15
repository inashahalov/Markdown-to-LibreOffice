#!/usr/bin/env python3
import subprocess
import sys
import os
import argparse
from pathlib import Path


class MarkdownToLibreOffice:
    def __init__(self):
        self.supported_formats = ['.md', '.markdown']

    def check_dependencies(self):
        """Проверка наличия необходимых программ"""
        dependencies = ['pandoc', 'libreoffice']
        missing = []

        for dep in dependencies:
            if subprocess.call(['which', dep], stdout=subprocess.DEVNULL) != 0:
                missing.append(dep)

        if missing:
            print(f"❌ Отсутствуют зависимости: {', '.join(missing)}")
            print("Установите их командой:")
            if 'pandoc' in missing:
                print("  sudo apt install pandoc")
            if 'libreoffice' in missing:
                print("  sudo apt install libreoffice")
            return False
        return True

    def convert_to_html(self, md_file, output_file=None, with_toc=False):
        """Конвертация Markdown в HTML"""
        if not output_file:
            output_file = md_file.replace('.md', '.html').replace('.markdown', '.html')

        cmd = ['pandoc', md_file, '-s', '--css=styles.css']

        if with_toc:
            cmd.extend(['--toc', '--toc-depth=2'])

        cmd.extend(['-o', output_file])

        try:
            subprocess.run(cmd, check=True)
            print(f"✅ Конвертировано в HTML: {output_file}")
            return output_file
        except subprocess.CalledProcessError as e:
            print(f"❌ Ошибка конвертации: {e}")
            return None

    def convert_to_docx(self, md_file, output_file=None):
        """Конвертация Markdown в DOCX"""
        if not output_file:
            output_file = md_file.replace('.md', '.docx').replace('.markdown', '.docx')

        try:
            subprocess.run([
                'pandoc', md_file, '-o', output_file
            ], check=True)
            print(f"✅ Конвертировано в DOCX: {output_file}")
            return output_file
        except subprocess.CalledProcessError as e:
            print(f"❌ Ошибка конвертации: {e}")
            return None

    def convert_to_odt(self, md_file, output_file=None, template=None):
        """Конвертация Markdown в ODT с шаблоном"""
        if not output_file:
            output_file = md_file.replace('.md', '.odt').replace('.markdown', '.odt')

        cmd = ['pandoc', md_file, '-s']

        if template and os.path.exists(template):
            cmd.extend(['--reference-doc', template])
        elif os.path.exists('template.odt'):
            cmd.extend(['--reference-doc', 'template.odt'])

        cmd.extend(['-o', output_file])

        try:
            subprocess.run(cmd, check=True)
            print(f"✅ Конвертировано в ODT: {output_file}")
            return output_file
        except subprocess.CalledProcessError as e:
            print(f"❌ Ошибка конвертации: {e}")
            return None

    def open_in_libreoffice(self, file_path):
        """Открытие файла в LibreOffice"""
        try:
            subprocess.Popen(['libreoffice', file_path],
                             stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL)
            print(f"✅ Открыто в LibreOffice: {file_path}")
        except Exception as e:
            print(f"❌ Не удалось открыть LibreOffice: {e}")

    def create_template(self):
        """Создание базового шаблона"""
        template_content = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
  <meta name="generator" content="pandoc" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes" />
  <title></title>
  <style type="text/css">
    body {
      font-family: "Liberation Serif", serif;
      font-size: 12pt;
      line-height: 1.5;
      margin: 2cm;
    }
    h1 {
      font-family: "Liberation Sans", sans-serif;
      font-size: 24pt;
      color: #2c3e50;
      border-bottom: 2px solid #3498db;
      padding-bottom: 10px;
      margin-top: 0;
    }
    h2 {
      font-family: "Liberation Sans", sans-serif;
      font-size: 20pt;
      color: #34495e;
      margin-top: 24pt;
    }
    h3 {
      font-family: "Liberation Sans", sans-serif;
      font-size: 16pt;
      color: #7f8c8d;
    }
    p {
      margin: 0 0 12pt 0;
      text-align: justify;
    }
    code {
      font-family: "Liberation Mono", monospace;
      background-color: #ecf0f1;
      padding: 2px 4px;
      border-radius: 3px;
    }
    pre {
      font-family: "Liberation Mono", monospace;
      background-color: #ecf0f1;
      padding: 10px;
      border-radius: 5px;
      overflow-x: auto;
    }
    blockquote {
      border-left: 4px solid #bdc3c7;
      margin: 0 0 12pt 0;
      padding-left: 16px;
      color: #7f8c8d;
    }
    ul, ol {
      margin: 0 0 12pt 0;
      padding-left: 20px;
    }
    li {
      margin-bottom: 4px;
    }
    table {
      border-collapse: collapse;
      width: 100%;
      margin: 12pt 0;
    }
    th, td {
      border: 1px solid #bdc3c7;
      padding: 8px;
      text-align: left;
    }
    th {
      background-color: #ecf0f1;
      font-weight: bold;
    }
    a {
      color: #3498db;
      text-decoration: none;
    }
    a:hover {
      text-decoration: underline;
    }
  </style>
</head>
<body>
$body$
</body>
</html>"""

        with open('template.html', 'w', encoding='utf-8') as f:
            f.write(template_content)
        print("✅ Создан шаблон: template.html")


def main():
    parser = argparse.ArgumentParser(description='Конвертация Markdown в LibreOffice')
    parser.add_argument('input_file', help='Входной Markdown файл')
    parser.add_argument('-f', '--format', choices=['html', 'docx', 'odt'],
                        default='odt', help='Формат выходного файла')
    parser.add_argument('-o', '--output', help='Имя выходного файла')
    parser.add_argument('--toc', action='store_true', help='Добавить оглавление')
    parser.add_argument('--template', help='Путь к шаблону')
    parser.add_argument('--no-open', action='store_true', help='Не открывать в LibreOffice')

    args = parser.parse_args()

    # Проверка существования файла
    if not os.path.exists(args.input_file):
        print(f"❌ Файл не найден: {args.input_file}")
        return

    # Проверка расширения
    if not any(args.input_file.endswith(ext) for ext in ['.md', '.markdown']):
        print("❌ Файл должен иметь расширение .md или .markdown")
        return

    converter = MarkdownToLibreOffice()

    # Проверка зависимостей
    if not converter.check_dependencies():
        return

    # Конвертация
    if args.format == 'html':
        output_file = converter.convert_to_html(args.input_file, args.output, args.toc)
    elif args.format == 'docx':
        output_file = converter.convert_to_docx(args.input_file, args.output)
    elif args.format == 'odt':
        output_file = converter.convert_to_odt(args.input_file, args.output, args.template)

    # Открытие в LibreOffice
    if output_file and not args.no_open:
        converter.open_in_libreoffice(output_file)


if __name__ == "__main__":
    main()