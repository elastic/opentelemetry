from jinja2 import Environment, FileSystemLoader
import urllib.request
from collections import defaultdict
import re

import os
import re
from pathlib import Path

TABLE_TAG = 'edot-collector-components-table'
DEPS_TAG = 'edot-collector-components-ocb'

def fetch_url_content(url):
    try:
        with urllib.request.urlopen(url) as response:
            # Read and decode the response
            content = response.read().decode('utf-8')
        return content
    except urllib.error.URLError as e:
        print(f"Failed to retrieve content: {e.reason}")
        return None

def dep_to_component(dep):
    url = dep[:dep.rfind(' v')].strip()
    html_url = url
    repo_link = '[Contrib](https://github.com/open-telemetry/opentelemetry-collector-contrib)'
    if url.startswith('github.com/'):
        pattern = r'github.com\/(?P<org>[^\/]*)\/(?P<repo>[^\/]*)\/(?P<comp_type>[^\/]*)\/(?P<comp_name>.*)'
        match = re.search(pattern, url)
        if match:
            print
            html_url = f'https://github.com/{match.group("org")}/{match.group("repo")}/tree/main/{match.group("comp_type")}/{match.group("comp_name")}'
            if match.group("repo") == 'opentelemetry-collector-components':
                repo_link = '[Elastic](https://github.com/elastic/opentelemetry-collector-components)'
    elif url.startswith('go.opentelemetry.io/collector'):
        pattern = r'go.opentelemetry.io\/collector\/(?P<comp_type>[^\/]*)\/(?P<comp_name>.*)'
        match = re.search(pattern, url)
        if match:
            html_url = f'https://github.com/open-telemetry/opentelemetry-collector/tree/main/{match.group("comp_type")}/{match.group("comp_name")}'
            repo_link = '[Core](https://github.com/open-telemetry/opentelemetry-collector)'
        
    comp = {
        'name': dep[(dep.rfind('/')+1):(dep.rfind(' ')+1)],
        'version': dep[(dep.rfind(' ')+1):],
        'html_url': html_url,
        'repo_link': repo_link,
        'dep': dep.strip()
    }
    return comp
    
def get_otel_col_upstream_version(url):
    elastic_agent_go_mod = fetch_url_content(url)
    lines = elastic_agent_go_mod.splitlines()
    for line in lines:
        if 'go.opentelemetry.io/collector/otelcol ' in line:
            return line[(line.rfind('v')+1):]
    
    return '<OTEL_COL_VERSION>'
            
def get_collector_version(filePath):
    with open(filePath, 'r', encoding='utf-8') as file:
        content = file.read()
        
    lines = content.splitlines()
    versions_section = False
    for line in lines:
        if line.startswith('edot_versions'):
            versions_section = True
        if versions_section and 'collector' in line:
            return line[(line.rfind(':') + 1):].strip()
            
    return 'main'
    
def get_otel_components(url):
    elastic_agent_go_mod = fetch_url_content(url)

    lines = elastic_agent_go_mod.splitlines()
    components_type = ['receiver', 'connector', 'processor', 'exporter', 'extension']
    otel_deps = [line for line in lines if (not line.endswith('// indirect') and any(f'/{comp}/' in line for comp in components_type))]
    otel_components = list(map(dep_to_component, otel_deps))
    
    

    components_grouped = defaultdict(list)

    for comp in otel_components:
        for substring in components_type:
            if f'/{substring}/' in comp['dep']:
                components_grouped[f'{substring.capitalize()}s'].append(comp)
                break  # Assumes each string matches only one group

    components_grouped = dict(components_grouped)

    for key, group in components_grouped.items():
        components_grouped[key] = sorted(group, key=lambda comp: comp['name'])
        
    return components_grouped

def find_files_with_substring(directory, substring):
    matching_files = []
    # Compile the substring into a regular expression for case-insensitive search
    pattern = re.compile(re.escape(substring), re.IGNORECASE)
    # Use pathlib to iterate over all files in the directory and subdirectories
    for file_path in Path(directory).rglob('*'):
        if file_path.is_file():
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    if pattern.search(content):
                        matching_files.append(str(file_path))
            except (UnicodeDecodeError, PermissionError) as e:
                # Skip files that can't be read due to encoding issues or permission errors
                print(f"Skipping {file_path}: {e}")
    return matching_files

def render_markdown(components, otel_col_version, template):
    # Set up the Jinja2 environment
    env = Environment(loader=FileSystemLoader('.'))

    # Load the template
    template = env.get_template(template)

    # Define the data to pass to the template
    data = {
        'grouped_components': components,
        'otel_col_version': otel_col_version
    }

    return template.render(data)

def render_components_into_file(dir, components, otel_col_version, template, tag):    
    
    output = render_markdown(components, otel_col_version, template)
    start_tag = f'<!-- start:{tag} -->'
    end_tag = f'<!-- end:{tag} -->'
    
    filesPaths = find_files_with_substring(dir, start_tag)
    
    for filePath in filesPaths:
        with open(filePath, 'r', encoding='utf-8') as file:
            content = file.read()
            
        pattern = start_tag + r'.*?' + end_tag
        new_content = f'{start_tag}\n{output}\n{end_tag}'
        updated_content = re.sub(pattern, new_content, content, flags=re.DOTALL)

        with open(filePath, 'w', encoding='utf-8') as file:
            file.write(updated_content)   

def check_markdown_generation(dir, components, otel_col_version, template, tag):
    output = render_markdown(components, otel_col_version, template)
    start_tag = f'<!-- start:{tag} -->'
    end_tag = f'<!-- end:{tag} -->'
    
    filesPaths = find_files_with_substring(dir, start_tag)
    
    for filePath in filesPaths:
        with open(filePath, 'r', encoding='utf-8') as file:
            content = file.read()
        
        pattern = start_tag + r'(.*?)' + end_tag

        matches = re.findall(pattern, content, re.DOTALL)
        
        for match in matches:
            if match.strip() != output.strip():
                print(f'Warning: Generated markdown for collector components is outdated in file {filePath}! Regenerate markdown by running `make generate-collector-components`!')
                return False;
            
    return True;

def check_markdown():
    col_version = get_collector_version('../_config.yml')
    url = f'https://raw.githubusercontent.com/elastic/elastic-agent/refs/tags/v{col_version}/go.mod'
    components = get_otel_components(url)
    otel_col_version = get_otel_col_upstream_version(url)
    tables = check_markdown_generation('../_edot-collector', components, otel_col_version, 'templates/components-table.jinja2', TABLE_TAG) 
    
    ocb = check_markdown_generation('../_edot-collector', components, otel_col_version, 'templates/ocb.jinja2', DEPS_TAG)
    return tables and ocb

def generate_markdown():
    col_version = get_collector_version('../_config.yml')
    url = f'https://raw.githubusercontent.com/elastic/elastic-agent/refs/tags/v{col_version}/go.mod'
    components = get_otel_components(url)
    otel_col_version = get_otel_col_upstream_version(url)
    render_components_into_file('../_edot-collector', components, otel_col_version, 'templates/components-table.jinja2', TABLE_TAG)
    render_components_into_file('../_edot-collector', components, otel_col_version, 'templates/ocb.jinja2', DEPS_TAG)
