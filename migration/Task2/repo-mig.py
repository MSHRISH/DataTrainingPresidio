import os
import subprocess
import requests
from requests.auth import HTTPBasicAuth

# Function to read configuration from config.txt
def read_config(file_path='config.txt'):
    config = {}
    with open(file_path, 'r') as f:
        for line in f:
            key, value = line.strip().split('=')
            config[key.strip()] = value.strip()
    return config

# Function to read the list of repositories from a file
def read_repo_list(file_path='repos.txt'):
    with open(file_path, 'r') as f:
        repo_list = [line.strip() for line in f.readlines()]
    return repo_list

# Load config
config = read_config()
organization = config.get('organization_name')
project = config.get('project_name')
pat = config.get('pat')

# Base URL for the Azure DevOps REST API
azure_devops_url = f'https://dev.azure.com/{organization}/{project}/_apis/git/repositories?api-version=7.1-preview.1'

# Basic Authentication with your PAT
auth = HTTPBasicAuth('', pat)

# Function to create a repository in Azure DevOps
def create_repo_in_azure_devops(repo_name):
    payload = {
        "name": repo_name
    }
    response = requests.post(azure_devops_url, json=payload, auth=auth)
    if response.status_code == 201:
        print(f"Repository '{repo_name}' created successfully in Azure DevOps.")
        return response.json()['remoteUrl']
    else:
        print(f"Failed to create repository '{repo_name}'. Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        return None

# Function to clone a Git repository
def clone_repo(repo_url, repo_name):
    try:
        subprocess.check_call(['git', 'clone', '--mirror', repo_url, repo_name])
        print(f"Cloned repository '{repo_name}' successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to clone repository '{repo_name}'. Error: {e}")

# Function to print available branches and tags
def print_branches_and_tags(repo_name):
    os.chdir(repo_name)
    print("Branches:")
    subprocess.check_call(['git', 'branch', '-a'])
    print("Tags:")
    subprocess.check_call(['git', 'tag'])
    os.chdir('..')

# Function to push repository to Azure DevOps
def push_to_azure_devops(repo_name, azure_repo_url):
    os.chdir(repo_name)
    try:
        subprocess.check_call(['git', 'remote', 'add', 'azure', azure_repo_url])
        subprocess.check_call(['git', 'fetch', '--all'])  # Fetch all branches and tags
        subprocess.check_call(['git', 'push', 'azure', '--all', '--force'])  # Push all branches
        subprocess.check_call(['git', 'push', 'azure', '--tags', '--force'])  # Push all tags
        print(f"Pushed repository '{repo_name}' to Azure DevOps successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to push repository '{repo_name}' to Azure DevOps. Error: {e}")
    finally:
        print_branches_and_tags(repo_name)
        os.chdir('..')

# Read the list of Git repository URLs to migrate
repo_list = read_repo_list()

# Migrate each repository
for repo_url in repo_list:
    repo_name = repo_url.split('/')[-1].replace('.git', '')
    clone_repo(repo_url, repo_name)
    azure_repo_url = create_repo_in_azure_devops(repo_name)
    if azure_repo_url:
        push_to_azure_devops(repo_name, azure_repo_url)
