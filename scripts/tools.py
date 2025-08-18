"""
OpenTelemetry Documentation Generation Tools

This module provides tools for automatically generating and updating OpenTelemetry documentation
based on external data sources. It includes functionality for:

- Component table generation from Elastic Agent go.mod files
- SDK feature table generation from YAML configuration
- OCB (OpenTelemetry Collector Builder) file generation
- Kube-stack version extraction and docset.yml updates

The scripts fetch data from the Elastic Agent repository and generate documentation
using Jinja2 templates.
"""

from jinja2 import Environment, FileSystemLoader
import urllib.request
from collections import defaultdict
import yaml
import re
from pathlib import Path

TABLE_TAG = 'edot-collector-components-table'
DEPS_TAG = 'edot-collector-components-ocb'
FEATURES_TAG = 'edot-features'

EDOT_COLLECTOR_DIR = '../docs/reference/edot-collector'
EDOT_SDKS_DIR = '../docs/reference/edot-sdks'
TEMPLATE_COLLECTOR_COMPONENTS_TABLE = 'templates/components-table.jinja2'
TEMPLATE_COLLECTOR_OCB_FILE = 'templates/ocb.jinja2'
TEMPLATE_SDK_FEATURES = 'templates/features.jinja2'
SDK_FEATURES_YAML = '../docs/reference/edot-sdks/features.yml'

def fetch_url_content(url):
    try:
        print(f"Attempting to fetch: {url}")
        with urllib.request.urlopen(url) as response:
            # Read and decode the response
            content = response.read().decode('utf-8')
        return content
    except urllib.error.URLError as e:
        print(f"Failed to retrieve content: {e.reason}")
        return None

def get_core_components(version='main'):
    """Fetch and parse the core-components.yaml file to determine support status"""
    # Try different URL formats, similar to get_otel_components logic
    url = f'https://raw.githubusercontent.com/elastic/elastic-agent/v{version}/internal/pkg/otel/core-components.yaml'
    print(f"Trying core components URL: {url}")
    content = fetch_url_content(url)
    
    # If first attempt fails, try without the 'v' prefix
    if content is None and version != 'main':
        url = f'https://raw.githubusercontent.com/elastic/elastic-agent/{version}/internal/pkg/otel/core-components.yaml'
        print(f"Retrying core components with URL: {url}")
        content = fetch_url_content(url)
    
    # If that fails too, try with main branch
    if content is None:
        url = 'https://raw.githubusercontent.com/elastic/elastic-agent/main/internal/pkg/otel/core-components.yaml'
        print(f"Falling back to main branch for core components: {url}")
        content = fetch_url_content(url)
    
    if content is None:
        print(f"Could not fetch core components from any URL")
        return []
        
    try:
        data = yaml.safe_load(content)
        return data.get('components', [])
    except yaml.YAMLError as e:
        print(f"Error parsing core-components.yaml: {e}")
        return []

def dep_to_component(dep):
    url = dep[:dep.rfind(' v')].strip()
    html_url = url
    repo_link = '[OTel Contrib Repo](https://github.com/open-telemetry/opentelemetry-collector-contrib)'
    if url.startswith('github.com/'):
        pattern = r'github.com/(?P<org>[^/]*)/(?P<repo>[^/]*)/(?P<comp_type>[^/]*)/(?P<comp_name>.*)'
        match = re.search(pattern, url)
        if match:
            html_url = f'https://github.com/{match.group("org")}/{match.group("repo")}/tree/main/{match.group("comp_type")}/{match.group("comp_name")}'
            if match.group("repo") == 'opentelemetry-collector-components':
                repo_link = '[Elastic Repo](https://github.com/elastic/opentelemetry-collector-components)'
    elif url.startswith('go.opentelemetry.io/collector'):
        pattern = r'go.opentelemetry.io/collector/(?P<comp_type>[^/]*)/(?P<comp_name>.*)'
        match = re.search(pattern, url)
        if match:
            html_url = f'https://github.com/open-telemetry/opentelemetry-collector/tree/main/{match.group("comp_type")}/{match.group("comp_name")}'
            repo_link = '[OTel Core Repo](https://github.com/open-telemetry/opentelemetry-collector)'
        
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
    for line in lines:
        if line.strip().startswith('edot-collector-version:'):
            return line.split(':', 1)[1].strip()
    
    # If no specific version is found, use a default version that we know works
    # This should match the version used in the Elastic Agent repository
    return '9.1.2'
    
def get_otel_components(url, version='main'):
    elastic_agent_go_mod = fetch_url_content(url)
    
    if elastic_agent_go_mod is None:
        print(f"Could not fetch content from {url}")
        return None

    # Get the list of core components
    core_components = get_core_components(version)
    print(f"Found {len(core_components)} core components")

    lines = elastic_agent_go_mod.splitlines()
    components_type = ['receiver', 'connector', 'processor', 'exporter', 'extension', 'provider']
    otel_deps = [line for line in lines if (not line.endswith('// indirect') and ("=>" not in line) and (any(f'/{comp}/' in line for comp in components_type)))]
    otel_components = list(map(dep_to_component, otel_deps))
    
    # Add support status to each component
    for comp in otel_components:
        # Extract the component name without the suffix (e.g., 'filelogreceiver' from 'filelogreceiver ')
        comp_name = comp['name'].strip()
        # Check if this component is in the core components list
        if comp_name in core_components:
            comp['support_status'] = '[Core]'
        else:
            comp['support_status'] = '[Extended]'

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

def render_markdown(data, template):
    # Set up the Jinja2 environment
    env = Environment(loader=FileSystemLoader('.'))

    # Load the template
    template = env.get_template(template)

    # Define the data to pass to the template

    return template.render(data)

def render_components_into_file(dir, data, template, tag):    
    output = render_markdown(data, template)
    start_tag = f'% start:{tag}'
    end_tag = f'% end:{tag}'
    
    filesPaths = find_files_with_substring(dir, start_tag)
    
    for filePath in filesPaths:
        with open(filePath, 'r', encoding='utf-8') as file:
            content = file.read()
            
        pattern = start_tag + r'.*?' + end_tag
        new_content = f'{start_tag}\n{output}\n{end_tag}'
        updated_content = re.sub(pattern, new_content, content, flags=re.DOTALL)

        with open(filePath, 'w', encoding='utf-8') as file:
            file.write(updated_content)   

def check_markdown_generation(dir, data, template, tag):
    output = render_markdown(data, template)
    start_tag = f'% start:{tag}'
    end_tag = f'% end:{tag}'
    
    filesPaths = find_files_with_substring(dir, start_tag)
    
    for filePath in filesPaths:
        with open(filePath, 'r', encoding='utf-8') as file:
            content = file.read()
        
        pattern = start_tag + r'(.*?)' + end_tag

        matches = re.findall(pattern, content, re.DOTALL)
        
        for match in matches:
            if match.strip() != output.strip():
                print(f'Warning: Generated markdown is outdated in file {filePath}! Regenerate markdown by running `make generate`!')
                return False;
            
    return True;

def get_features_data(source_file):
    with open(source_file, 'r') as file:
        try:
            return yaml.safe_load(file)
        except yaml.YAMLError as exc:
            print(f"Error reading YAML file: {exc}")
            exit(1)

def check_markdown():
    col_version = get_collector_version('../docs/docset.yml')
    print(f"Collector version: {col_version}")
    # Try different URL formats
    url = f'https://raw.githubusercontent.com/elastic/elastic-agent/v{col_version}/go.mod'
    print(f"Trying URL: {url}")
    components = get_otel_components(url, col_version)
    
    # If first attempt fails, try without the 'v' prefix
    if components is None:
        url = f'https://raw.githubusercontent.com/elastic/elastic-agent/{col_version}/go.mod'
        print(f"Retrying with URL: {url}")
        components = get_otel_components(url, col_version)
    
    # If that fails too, try with main branch
    if components is None:
        url = 'https://raw.githubusercontent.com/elastic/elastic-agent/main/go.mod'
        print(f"Falling back to main branch: {url}")
        components = get_otel_components(url, col_version)
        
    otel_col_version = get_otel_col_upstream_version(url)
    data = {
        'grouped_components': components,
        'otel_col_version': otel_col_version
    }
    tables = check_markdown_generation(EDOT_COLLECTOR_DIR, data, TEMPLATE_COLLECTOR_COMPONENTS_TABLE, TABLE_TAG) 
    ocb = check_markdown_generation(EDOT_COLLECTOR_DIR, data, TEMPLATE_COLLECTOR_OCB_FILE, DEPS_TAG)
    
    features_data = get_features_data(SDK_FEATURES_YAML)
    features = check_markdown_generation(EDOT_SDKS_DIR, features_data, TEMPLATE_SDK_FEATURES, FEATURES_TAG)
    
    # Check kube-stack version
    kube_stack_version = get_kube_stack_version(col_version)
    if kube_stack_version:
        print(f"Found kube-stack version: {kube_stack_version}")
        # Note: We don't check if it's up to date here, just that we can fetch it
        kube_stack_ok = True
    else:
        print("Warning: Could not fetch kube-stack version")
        kube_stack_ok = False
    
    return tables and ocb and features and kube_stack_ok

def generate_markdown():
    col_version = get_collector_version('../docs/docset.yml')
    print(f"Collector version: {col_version}")
    # Try different URL formats
    url = f'https://raw.githubusercontent.com/elastic/elastic-agent/v{col_version}/go.mod'
    print(f"Trying URL: {url}")
    components = get_otel_components(url, col_version)
    
    # If first attempt fails, try without the 'v' prefix
    if components is None:
        url = f'https://raw.githubusercontent.com/elastic/elastic-agent/{col_version}/go.mod'
        print(f"Retrying with URL: {url}")
        components = get_otel_components(url, col_version)
    
    # If that fails too, try with main branch
    if components is None:
        url = 'https://raw.githubusercontent.com/elastic/elastic-agent/main/go.mod'
        print(f"Falling back to main branch: {url}")
        components = get_otel_components(url, col_version)
        
    otel_col_version = get_otel_col_upstream_version(url)
    data = {
        'grouped_components': components,
        'otel_col_version': otel_col_version
    }
    render_components_into_file(EDOT_COLLECTOR_DIR, data, TEMPLATE_COLLECTOR_COMPONENTS_TABLE, TABLE_TAG)
    render_components_into_file(EDOT_COLLECTOR_DIR, data, TEMPLATE_COLLECTOR_OCB_FILE, DEPS_TAG)
    
    features_data = get_features_data(SDK_FEATURES_YAML)
    render_components_into_file(EDOT_SDKS_DIR, features_data, TEMPLATE_SDK_FEATURES, FEATURES_TAG)
    
    # Update kube-stack version in docset.yml
    kube_stack_version = get_kube_stack_version(col_version)
    if kube_stack_version:
        print(f"Updating kube-stack version to: {kube_stack_version}")
        update_docset_kube_stack_version(kube_stack_version)
    else:
        print("Warning: Could not fetch kube-stack version, skipping update")

def get_kube_stack_version(version='main'):
    """Extract KubeStackChartVersion from elastic-agent repository"""
    # Try different URL formats for the k8s.go file
    # First try with the version as-is (in case it already has 'v' prefix)
    url = f'https://raw.githubusercontent.com/elastic/elastic-agent/{version}/testing/integration/k8s/k8s.go'
    print(f"Trying k8s.go URL: {url}")
    content = fetch_url_content(url)
    
    # If first attempt fails and version doesn't start with 'v', try with 'v' prefix
    if content is None and not version.startswith('v') and version != 'main':
        url = f'https://raw.githubusercontent.com/elastic/elastic-agent/v{version}/testing/integration/k8s/k8s.go'
        print(f"Retrying k8s.go with URL: {url}")
        content = fetch_url_content(url)
    
    # If that fails too, try with main branch
    if content is None:
        url = 'https://raw.githubusercontent.com/elastic/elastic-agent/main/testing/integration/k8s/k8s.go'
        print(f"Falling back to main branch for k8s.go: {url}")
        content = fetch_url_content(url)
    
    if content is None:
        print(f"Could not fetch k8s.go from any URL")
        return None
        
    # Look for the KubeStackChartVersion line
    lines = content.splitlines()
    for line in lines:
        if 'KubeStackChartVersion' in line and '=' in line:
            # Extract the version from the line like: KubeStackChartVersion = "0.6.3"
            match = re.search(r'KubeStackChartVersion\s*=\s*"([^"]+)"', line)
            if match:
                return match.group(1)
    
    print("Could not find KubeStackChartVersion in k8s.go")
    return None

def update_docset_kube_stack_version(version):
    """Update the kube-stack-version substitution in docset.yml"""
    docset_path = '../docs/docset.yml'
    
    try:
        with open(docset_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Replace the kube-stack-version line
        pattern = r'(kube-stack-version:\s*)[0-9]+\.[0-9]+\.[0-9]+'
        replacement = f'\\g<1>{version}'
        new_content = re.sub(pattern, replacement, content)
        
        if new_content != content:
            with open(docset_path, 'w', encoding='utf-8') as file:
                file.write(new_content)
            print(f"Updated kube-stack-version to {version} in docset.yml")
            return True
        else:
            print(f"kube-stack-version already up to date: {version}")
            return False
            
    except Exception as e:
        print(f"Error updating docset.yml: {e}")
        return False
