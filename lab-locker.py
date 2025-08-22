#!/usr/bin/env python3
"""
Simple Flask app to render Markdown files with shadcn-inspired styling.
Usage: python app.py
"""

import sys
import subprocess
import re
import json
from pathlib import Path

# Install missing packages before importing Flask modules
def install_missing_packages():
    """Install required packages if they're missing."""
    required_packages = ['flask', 'markdown', 'pygments']
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"{package} installed successfully!")

# Install packages first
install_missing_packages()

# Now import Flask modules
from flask import Flask, render_template, abort, render_template_string
import markdown
from markdown.extensions import tables, codehilite, toc

def load_config():
    """Load configuration from config.json with fallback defaults."""
    default_config = {
        "app": {
            "title": "Documentation",
            "default_file": "homelab.md",
            "port": 5000,
            "host": "0.0.0.0",
            "docs_folder": "docs"
        },
        "ui": {
            "sidebar": {
                "width": "250px",
                "files_title": "Files",
                "toc_title": "Contents"
            },
            "fonts": {
                "base_size": "14px",
                "sidebar_size": "0.875rem",
                "heading_scale": {
                    "h1": "2rem",
                    "h2": "1.5rem", 
                    "h3": "1.25rem",
                    "h4": "1.125rem",
                    "h5": "1rem",
                    "h6": "0.875rem"
                }
            },
            "spacing": {
                "content_padding": "3rem",
                "toc_indent": "0.5rem",
                "folder_indent": "2px"
            },
            "scrollbar": {
                "width": "14px"
            }
        }
    }
    
    config_path = Path(__file__).parent / "config.json"
    
    if config_path.exists():
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
            
            # Merge user config with defaults (deep merge)
            def merge_dicts(default, user):
                for key, value in user.items():
                    if key in default and isinstance(default[key], dict) and isinstance(value, dict):
                        merge_dicts(default[key], value)
                    else:
                        default[key] = value
                return default
            
            config = merge_dicts(default_config, user_config)
            print(f"Loaded configuration from {config_path}")
            
        except Exception as e:
            print(f"Error loading config.json: {e}")
            print("Using default configuration")
            config = default_config
    else:
        print("No config.json found, creating one with defaults...")
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=2)
            print(f"Created default config.json at {config_path}")
        except Exception as e:
            print(f"Could not create config.json: {e}")
        config = default_config
    
    return config

def create_toc_from_content(content):
    """Create a table of contents from markdown content."""
    heading_pattern = r'^(#{1,6})\s+(.+)$'
    headings = []
    
    for line in content.split('\n'):
        match = re.match(heading_pattern, line)
        if match:
            level = len(match.group(1))
            title = match.group(2).strip()
            # Create an anchor ID from the title
            anchor_id = re.sub(r'[^a-zA-Z0-9\s-]', '', title.lower())
            anchor_id = re.sub(r'[-\s]+', '-', anchor_id).strip('-')
            headings.append((level, title, anchor_id))
    
    if not headings:
        return '<p>No headings found</p>'
    
    # Generate TOC HTML
    toc_lines = ['<ul>']
    current_level = 1
    
    for level, title, anchor_id in headings:
        if level > current_level:
            while current_level < level:
                toc_lines.append('<li><ul>')
                current_level += 1
        elif level < current_level:
            while current_level > level:
                toc_lines.append('</ul></li>')
                current_level -= 1
        
        toc_lines.append(f'<li><a href="#{anchor_id}">{title}</a></li>')
    
    while current_level > 1:
        toc_lines.append('</ul></li>')
        current_level -= 1
    
    toc_lines.append('</ul>')
    return '\n'.join(toc_lines)

def get_markdown_files(base_path):
    """Recursively find all markdown files and organize them."""
    base_path = Path(base_path)
    files = {}
    
    for md_file in base_path.rglob("*.md"):
        # Get relative path from base
        rel_path = md_file.relative_to(base_path)
        path_parts = rel_path.parts
        
        # Organize by folder structure
        current_dict = files
        for part in path_parts[:-1]:  # All parts except filename
            if part not in current_dict:
                current_dict[part] = {}
            current_dict = current_dict[part]
        
        # Add the file
        filename = path_parts[-1]
        current_dict[filename] = str(rel_path)
    
    return files

def render_file_browser(files, current_path="", is_root=True):
    """Render a file browser for the sidebar."""
    if not files:
        return "<p>No markdown files found</p>"
    
    html = ["<ul class='file-browser'>"]
    
    # Separate files and folders
    file_items = []
    folder_items = []
    
    for name, value in sorted(files.items()):
        if isinstance(value, dict):  # It's a folder
            folder_items.append((name, value))
        else:  # It's a file
            file_items.append((name, value))
    
    # Render files first
    for name, file_path in file_items:
        file_url = file_path.replace('\\', '/')  # Ensure forward slashes for URLs
        display_name = name.replace('.md', '')
        html.append(f"<li class='file'><a href='/{file_url}'>{display_name}</a></li>")
    
    # Then render folders (collapsed by default)
    for name, folder_contents in folder_items:
        folder_path = f"{current_path}/{name}" if current_path else name
        html.append(f"<li class='folder collapsed'>")
        html.append(f"<span class='folder-name' onclick='toggleFolder(this)'>{name}<span class='toggle'>▼</span></span>")
        html.append(f"<div class='folder-contents'>{render_file_browser(folder_contents, folder_path, False)}</div>")
        html.append("</li>")
    
    html.append("</ul>")
    return "".join(html)

def load_markdown_file(filename):
    """Load and convert markdown file to HTML."""
    try:
        # Look in the configured docs folder
        script_dir = Path(__file__).parent
        docs_dir = script_dir / config['app']['docs_folder']
        file_path = docs_dir / filename
        
        # Create docs directory if it doesn't exist
        docs_dir.mkdir(exist_ok=True)
        
        # Debug info
        print(f"Script directory: {script_dir}")
        print(f"Docs directory: {docs_dir}")
        print(f"Looking for file: {file_path.absolute()}")
        print(f"File exists: {file_path.exists()}")
        
        if not file_path.exists():
            # List all .md files in docs directory and subdirectories
            md_files = list(docs_dir.rglob("*.md"))
            
            # Create a sample file if docs directory is empty
            if not md_files:
                sample_file = docs_dir / config['app']['default_file']
                sample_content = """# Welcome to Your Documentation

This is your documentation home page. Create more `.md` files in the `docs/` folder to build your documentation library.

## Getting Started

1. Add your markdown files to the `docs/` folder
2. Organize them in subfolders if needed
3. Edit `config.json` to customize the appearance
4. Your files will appear in the sidebar automatically

## Features

- **File Browser**: Navigate between documents
- **Table of Contents**: Jump to sections within documents  
- **Responsive Design**: Works on desktop and mobile
- **Dark Mode**: Automatically adapts to system preferences
- **Configurable**: Customize fonts, spacing, and colors

Happy documenting! 📚
"""
                with open(sample_file, 'w', encoding='utf-8') as f:
                    f.write(sample_content)
                print(f"Created sample file: {sample_file}")
                md_files = [sample_file]
            
            return None, None, None, f"File '{filename}' not found in {docs_dir}. Available files: {[str(f.relative_to(docs_dir)) for f in md_files]}"
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Configure markdown with extensions
        md = markdown.Markdown(
            extensions=[
                'tables',
                'codehilite',
                'toc',
                'fenced_code',
                'attr_list'
            ],
            extension_configs={
                'codehilite': {
                    'css_class': 'highlight'
                },
                'toc': {
                    'anchorlink': True,
                    'permalink': False,
                    'toc_depth': 6
                }
            }
        )
        
        html_content = md.convert(content)
        toc_html = md.toc
        
        # Debug TOC generation
        print(f"Markdown TOC: {toc_html}")
        
        # If no TOC generated, create a manual one
        if not toc_html or toc_html.strip() == '':
            print("No TOC generated by markdown, creating manual TOC...")
            toc_html = create_toc_from_content(content)
            print(f"Manual TOC created: {toc_html}")
        
        # Extract title from first h1 or use filename
        title = filename.replace('.md', '').replace('_', ' ').title()
        if content.strip().startswith('# '):
            title = content.split('\n')[0][2:].strip()
        
        # Get file browser
        markdown_files = get_markdown_files(docs_dir)
        file_browser_html = render_file_browser(markdown_files, "", True)
        
        return html_content, toc_html, file_browser_html, title
        
    except Exception as e:
        return None, None, None, f"Error reading file: {str(e)}"

def create_directories():
    """Create necessary directories for templates and static files."""
    script_dir = Path(__file__).parent
    templates_dir = script_dir / "templates"
    static_dir = script_dir / "static"
    
    templates_dir.mkdir(exist_ok=True)
    static_dir.mkdir(exist_ok=True)
    
    print(f"Using template directory: {templates_dir}")
    print(f"Using static directory: {static_dir}")
    
    return templates_dir, static_dir

# Load configuration
config = load_config()

app = Flask(__name__)

@app.route('/')
@app.route('/<path:filename>')
def render_markdown(filename=None):
    """Render markdown file as HTML."""
    if filename is None:
        filename = config['app']['default_file']
    
    content, toc, file_browser, title_or_error = load_markdown_file(filename)
    
    if content is None:
        abort(404, description=title_or_error)
    
    # Ensure directories exist
    create_directories()
    
    return render_template(
        'template.html',
        content=content,
        toc=toc,
        file_browser=file_browser,
        title=title_or_error,
        current_file=filename,
        config=config
    )

@app.errorhandler(404)
def not_found_error(error):
    """Custom 404 page."""
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>File Not Found</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                margin: 0;
                background-color: #f8f9fa;
                color: #333;
            }
            .error-container {
                text-align: center;
                max-width: 400px;
                padding: 2rem;
            }
            h1 { margin-bottom: 1rem; color: #dc2626; }
            p { margin-bottom: 1rem; color: #6b7280; }
            a { color: #2563eb; text-decoration: none; }
            a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <div class="error-container">
            <h1>404 - File Not Found</h1>
            <p>{{ error.description }}</p>
            <p><a href="/">← Back to Home</a></p>
        </div>
    </body>
    </html>
    """, error=error), 404

if __name__ == '__main__':
    print("Starting Flask Markdown Viewer...")
    print(f"Markdown files should be placed in the '{config['app']['docs_folder']}/' directory")
    print(f"Available at: http://{config['app']['host']}:{config['app']['port']}/")
    print("To view a specific file: http://localhost:5000/filename.md")
    print("Edit config.json to customize appearance and behavior")
    print("Press Ctrl+C to stop")
    
    app.run(
        debug=True, 
        host=config['app']['host'], 
        port=config['app']['port']
    )