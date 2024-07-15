import subprocess
import requests
import re
import base64
import sys

def process_file_content(content):
    # Process the content using awk script
    awk_command = ['awk', '-f', 'xscc.awk', 'extract=copyright']
    awk_process = subprocess.run(awk_command, input=content.encode(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout_text = awk_process.stdout.decode('utf-8')
    stderr_text = awk_process.stderr.decode('utf-8')

    return stdout_text, stderr_text, awk_process.returncode

def preprocess_content(content):
    # Remove the hash from each line
    processed_script = re.sub(r'^#', '', content, flags=re.MULTILINE)
    
    # Remove /* ... */ multiline comments
    processed_script = re.sub(r'/\*(.*?)\*/', lambda match: match.group(1), processed_script, flags=re.MULTILINE | re.DOTALL)

    # Remove // only from the beginning of each line
    processed_script = re.sub(r'^\s*//', '', processed_script, flags=re.MULTILINE)


    # Remove the line starting with "Copyright"
    processed_script = re.sub(r'^\s*Copyright.*\n', '', processed_script, flags=re.MULTILINE)

    # Remove newline characters and whitespace
    processed_script = re.sub(r'\s+', '', processed_script)

    return processed_script

def main(prNumber, access_token):
    print("LICENSE CHECKS: ")
    github_token = access_token

    # Replace with the pull request number you're interested in
    pull_request_number = prNumber

    # GitHub API endpoint for retrieving files modified or added in a pull request
    # url = f"https://gitenterprise.xilinx.com/api/v3/repos/suchetla/LICENSE-PR-CHECKS/pulls/{pull_request_number}/files"
    # url = f"https://gitenterprise.xilinx.com/api/v3/repos/Xilinx/kria-dashboard/pulls/{pull_request_number}/files"
    url = f"https://api.github.com/repos/Xilinx/kria-dashboard/pulls/{pull_request_number}/files"


    # Add your GitHub token to the headers for authentication
    headers = {"Authorization": f"token {github_token}"}

    # Send a GET request to the GitHub API endpoint
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        files = response.json()

        # Store processed content of modified and added files
        modified_contents = {}
        added_contents = {}

        # Extensions to exclude from processing
        excluded_extensions = {'.json', '.xml', '.yml', '.hcl'}

        # Retrieve and process content of modified and added files from raw_url
        for file_info in files:
            file_name = file_info["filename"]
            # Skip files with excluded extensions
            if any(file_name.endswith(ext) for ext in excluded_extensions):
                print(f"{file_name}: Skipping License Check for this File")
                continue

            file_status = file_info["status"]
            file_raw_url = file_info["raw_url"]
            file_content_response = requests.get(file_raw_url)

            if file_content_response.status_code == 200:
                file_content = file_content_response.text
                if file_status == "modified":
                    # Process and preprocess content for modified files
                    processed_content, _, _ = process_file_content(file_content)
                    processed_content = preprocess_content(processed_content)
                    modified_contents[file_name] = {
                        "new_content": processed_content,
                        "new_raw": file_content
                    }
                elif file_status == "added":
                    # Process and preprocess content for added files
                    processed_content, _, _ = process_file_content(file_content)
                    processed_content = preprocess_content(processed_content)
                    added_contents[file_name] = {
                        "processed_content": processed_content,
                        "raw_content": file_content
                    }
            else:
                print(f"Failed to retrieve content of the file: {file_content_response.text}")

        if not modified_contents and not added_contents:
            return

        # GitHub API endpoint for retrieving files from PR_Check repository
        # pr_check_base_url = "https://gitenterprise.xilinx.com/api/v3/repos/ssw-devops/PR_Check/contents/LICENSES/LICENSE-PR-CHECKS/"
        # pr_check_base_url = "https://gitenterprise.xilinx.com/api/v3/repos/ssw-devops/PR_Check/contents/LICENSES/kria-dashboard/"
        pr_check_base_url = "https://api.github.com/repos/suchetla/PR_Check/contents/LICENSES/kria-dashboard/"
        pr_check_response = requests.get(pr_check_base_url, headers=headers)

        if pr_check_response.status_code == 200:
            pr_check_data = pr_check_response.json()
            pr_approved = True  # Assume PR is approved by default
            added_files_valid_license = True  # Flag to track if added files have valid licenses
            license_check_passed = False  # Flag to track if license check has passed
            modified_files_checked = False  # Flag to track if any modified files were checked

            # Iterate through modified files from suchetla/LICENSE-PR-CHECKS repository and compare processed content
            if modified_contents:
                print("Modified Files:")

            for modified_file_name, modified_file_info in modified_contents.items():
                modified_files_checked = True  # Set the flag to True
                matched = False  # Flag to track if the modified file matches with any existing file

                # Retrieve old content from the source repo
                # source_file_url = f"https://gitenterprise.xilinx.com/api/v3/repos/suchetla/LICENSE-PR-CHECKS/contents/{modified_file_name}"
                # source_file_url = f"https://gitenterprise.xilinx.com/api/v3/repos/Xilinx/kria-dashboard/contents/{modified_file_name}"
                source_file_url = f"https://api.github.com/repos/Xilinx/kria-dashboard/contents/{modified_file_name}"
                source_file_response = requests.get(source_file_url, headers=headers)

                if source_file_response.status_code == 200:
                    source_file_content_base64 = source_file_response.json().get('content', '')

                    if source_file_content_base64:
                        source_file_content = base64.b64decode(source_file_content_base64).decode('utf-8')
                        source_file_processed_content, _, _ = process_file_content(source_file_content)
                        source_file_processed_content = preprocess_content(source_file_processed_content)

                        # Compare old and new contents
                        if source_file_processed_content != modified_file_info["new_content"]:
                            old_license = source_file_processed_content
                            new_license = modified_file_info["new_content"]
                            print(f"{modified_file_name}: License Change Detected")
                            print(f"Old License: {old_license}")
                            new_license_status = " (Not Approved License)"  # Default to not approved

                            # Check the new content against approved licenses
                            for pr_check_file_info in pr_check_data:
                                if pr_check_file_info["type"] == "file":
                                    pr_check_file_download_url = pr_check_file_info["download_url"]
                                    pr_check_content_response = requests.get(pr_check_file_download_url, headers=headers)

                                    if pr_check_content_response.status_code == 200:
                                        pr_check_file_content = pr_check_content_response.text
                                        pr_check_processed_content = preprocess_content(pr_check_file_content)

                                        if modified_file_info["new_content"] == pr_check_processed_content:
                                            license_check_passed = True  # Set the flag to True
                                            matched = True
                                            new_license_status = " (Approved License)"
                                            break

                            if not matched:
                                pr_approved = False  # Mark PR as not approved if a license check fails

                            print(f"New License: {new_license}{new_license_status}")
                            if len(modified_contents) > 1:
                                print()
                        else:
                            print(f"{modified_file_name}: No License Change")
                            if len(modified_contents) > 1:
                                print()
                    else:
                        print(f"Failed to retrieve the old content of the file: {modified_file_name}")
                else:
                    print(f"Failed to retrieve the old content of the file: {modified_file_name}")

            if added_contents:
                print("Added Files:")
            for added_file_name, added_file_info in added_contents.items():
                matched_filename = None  # Variable to store the matched filename
                license_content_found = bool(added_file_info["processed_content"])  # Check if license content is found
                for pr_check_file_info in pr_check_data:
                    if pr_check_file_info["type"] == "file":
                        pr_check_file_download_url = pr_check_file_info["download_url"]
                        pr_check_content_response = requests.get(pr_check_file_download_url, headers=headers)

                        if pr_check_content_response.status_code == 200:
                            pr_check_file_content = pr_check_content_response.text
                            pr_check_processed_content = preprocess_content(pr_check_file_content)

                            if added_file_info["processed_content"] == pr_check_processed_content:
                                matched_filename = pr_check_file_info["name"]  # Store the matched filename
                                break

                if matched_filename:
                    print(f"{added_file_name} - {matched_filename}")
                elif license_content_found:
                    print(f"{added_file_name} - This is not the Approved License")
                else:
                    print(f"{added_file_name} - No license content found")
                    added_files_valid_license = False
                    pr_approved = False  # Mark PR as not approved if any added file has no valid license

            # Final check to print the appropriate message
            if pr_approved and (license_check_passed or added_files_valid_license):
                if modified_files_checked and not license_check_passed:
                    print("License Check is Passed")
                else:
                    print("This is the Approved License. Hence, License Check is Passed")
            else:
                if len(modified_contents) > 1:
                    print("Found one or more licenses which are not approved.")
                print("License Check is Failed, please reach out to maintainer")

        else:
            print("Failed to retrieve files from the repositories.")
    else:
        print(f"Failed to retrieve files from the pull request: {response.text}")

if __name__ == "__main__":
    # main(sys.argv[1])
    main(sys.argv[1], sys.argv[2])
