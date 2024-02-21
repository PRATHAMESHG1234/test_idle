import imghdr


from openai import OpenAI

import difflib
import git
import os

def get_commit_history(repo):
    commit_history = []
    if repo:
        commits = list(repo.iter_commits())
        if commits:
            for commit in commits:
                commit_info = f"{commit.summary}"
                commit_history.append(commit_info)
    return commit_history

def commit_changes(repo, commit_message):
    if repo and commit_message:
        try:
            repo.git.add(all=True)
            repo.index.commit(commit_message)
            return True, f"Changes committed with message: {commit_message}"
        except git.exc.GitCommandError as e:
            return False, f"Error committing changes: {e}"
    else:
        return False, "Git repository not initialized or no commit message generated"


def push_changes(commit_message):
    repo = git.Repo(search_parent_directories=True)
    if repo and commit_message:
        try:
            repo.git.add(all=True)
            repo.index.commit(commit_message)

            # Get the current branch name
            current_branch = repo.active_branch.name

            remotes = repo.remotes
            if remotes:
                remote_url = remotes[0].url
                if remote_url:
                    try:
                        if 'origin' not in [remote.name for remote in repo.remotes]:
                            repo.create_remote('origin', remote_url)
                        # Push changes to the current branch
                        repo.git.push("origin", current_branch)
                        return True, f"Changes pushed to remote repository '{remote_url}'"
                    except git.exc.GitCommandError as e:
                        return False, f"Error pushing changes: {e}"
                else:
                    return False, "Please enter the URL of the remote repository"
            else:
                return False, "No remote repository specified"
        except git.exc.GitCommandError as e:
            return False, f"Error committing changes: {e}"
    else:
        return False, "Git repository not initialized"

def create_new_repository(github, repo_name):
    if not github:
        return False, "Please login to GitHub first"

    try:
        repo = github.get_user().create_repo(repo_name, private=True)
        repo_url = repo.clone_url
        return True, f"Repository '{repo_name}' created successfully. URL: {repo_url}"
    except Exception as e:
        return False, f"Error creating repository: {e}"

def initialize_empty_git_repo():
    try:
        repo = git.Repo.init()
        return True, "Git repository initialized"
    except git.exc.InvalidGitRepositoryError:
        return False, "Invalid Git repository"

def load_access_token():
    if os.path.exists("access_token.txt"):
        with open("access_token.txt", "r") as file:
            access_token = file.read().strip()
    else:
        access_token = ""
    return access_token

def save_access_token(access_token):
    with open("access_token.txt", "w") as file:
        file.write(access_token)

def check_git_repository():
    try:
        return git.Repo()
    except git.exc.InvalidGitRepositoryError:
        return None



def get_previous_code():
    try:
        cwd = os.getcwd()  # Get the current working directory
        repo = git.Repo(cwd)  # Open the Git repository in the current directory
        last_commit = repo.head.commit  # Get the latest commit
        
        previous_code = {}
        for item in last_commit.tree.traverse():
            try:
                if item.type == 'blob':  # Check if it's a file
                    file_content = item.data_stream.read().decode('utf-8')
                    previous_code[item.name] = file_content
                else:
                    print(f"Skipping non-file item: {item.path}")
            except UnicodeDecodeError as e:
                print(f"Error decoding file at: {item.path}: {e}")
        return previous_code
    except git.exc.InvalidGitRepositoryError as e:
        print(f"Invalid Git repository path: {e}")
        return None

def get_current_code():
    current_code = {}
    try:
        cwd = os.getcwd()
        for root, dirs, files in os.walk(cwd):
            for file_name in files:
                # Check for specific file extensions
                if file_name.endswith('.py') or file_name.endswith('.txt') or file_name.endswith('.html'):
                    file_path = os.path.join(root, file_name)
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors="ignore") as file:
                            file_content = file.read()
                            current_code[file_name] = file_content
                    except (UnicodeDecodeError, IsADirectoryError) as e:
                        print(f"Error reading {file_name}: {e}")
    except OSError as e:
        print(f"Error reading files in the current working directory: {e}")

       

    return current_code

def get_code_changes(previous_code, current_code):
    code_changes = {}

    # Find modified and added files
    for file_name in current_code:
        if file_name in previous_code:
            previous_content = previous_code[file_name]
            current_content = current_code[file_name]

            # Split content into lines and remove leading/trailing whitespace
            previous_lines = [line.strip() for line in previous_content.splitlines()]
            current_lines = [line.strip() for line in current_content.splitlines()]

            # Compare line by line and identify changed lines
            changed_lines = [
                (line_number, previous_line, current_line)
                for line_number, (previous_line, current_line) 
                in enumerate(zip(previous_lines, current_lines), start=1) 
                if previous_line != current_line
            ]

            if changed_lines:  # Check if there are changes
                code_changes[file_name] = changed_lines
        else:
            # File is present in current code but not in previous code (added file)
            code_changes[file_name] = {
                "Status": "Added",
                "Content": current_code[file_name]
            }
    
    # Find deleted files
    for file_name in previous_code:
        if file_name not in current_code:
            # File is present in previous code but not in current code (deleted file)
            code_changes[file_name] = {
                "Status": "Deleted",
                "Content": previous_code[file_name]
            }

    return code_changes

def generate_commit_message():

    repo_path = get_repo_path()
    current_code = get_current_code()
    
   

    previous_code = get_previous_code()
    

    if current_code or previous_code:
        code_changes = get_code_changes(previous_code, current_code)
        # print(code_changes)
        client = OpenAI()

        # Initialize the prompt
        prompt = "Generate a short commit message  based on the codes for the changes also mention that file and  changes in short:\n\n"

        # Append the changes to the prompt
        prompt += f"Changes in code: \n{code_changes}\n\n"
        print(prompt)
        # Generate completion based on the prompt
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            # n=1,
            # stop=["\n"]  # Stop generation at newlines to keep it concise
        )

        # Extract the commit message from the completion
        if completion.choices:
            first_choice = completion.choices[0]
            if hasattr(first_choice, "message"):
                commit_message = first_choice.message
                return commit_message.content

        # Return None if no message generated
        return None
      
    else:
        print("Unable to retrieve current or previous code.")
        # Assuming you have already set up your OpenAI client
       


def get_repo_path():
    try:
        repo = git.Repo(search_parent_directories=True)
        return repo.working_dir
    except git.exc.InvalidGitRepositoryError:
        print("Not inside a Git repository.")
        return None


# Example usage:



