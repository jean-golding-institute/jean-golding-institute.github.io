import csv
from pathlib import Path
import shutil

# Empty the output directory
docs_dir = Path('docs/')
shutil.rmtree(docs_dir, ignore_errors=True)
docs_dir.mkdir()

# Prevent Jekyll from running on GitHub Pages
(docs_dir / ".nojekyll").touch()

# Load the redirects that need to be created
with open('redirects.csv') as f:
    reader = csv.reader(f)
    redirects = [
        # Change the from_url into an appropriate local path
        (from_url.lstrip('/'), to_url) if from_url.endswith('.html')
        # For directories, add an index.html
        else ('index.html', to_url) if from_url == '/'
        else (from_url.strip('/') + '/index.html', to_url)
        for (from_url, to_url) in reader
    ]

# Create the redirect files
html_template = """<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Redirecting to {to_url}</title>
    <meta http-equiv="refresh" content="0; URL={to_url}">
    <link rel="canonical" href="{to_url}">
  </head>
  <body>
    This page has moved to <a href="{to_url}">{to_url}</a>.
  </body>
</html>"""

for from_url, to_url in redirects:
    print(from_url, to_url)

    # Create any necessary folders
    output_file = docs_dir / from_url
    output_dir = output_file.parent
    output_dir.mkdir(parents=True, exist_ok=True)

    # Output a formatted template
    with open(output_file, 'w') as f:
        f.write(html_template.format(to_url=to_url))
