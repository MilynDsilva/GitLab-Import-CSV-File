
import requests
import csv

# GitLab API endpoint for merge request creation
GITLAB_URL = "https://gitlab.com/api/v4/projects/{project_id}/merge_requests"

# GitLab access token with necessary permissions
GITLAB_TOKEN = "TOKEN"

# GitLab import csv file
GITLAB_MR_CSV = 'filename.csv'

# IDs of the source and target GitLab projects
SOURCE_PROJECT_ID = "56852455"
TARGET_PROJECT_ID = "57125493"

def import_merge_requests_from_csv(csv_file):
    with open(csv_file, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            create_merge_request(row)

def create_merge_request(data):
    headers = {
        "PRIVATE-TOKEN": GITLAB_TOKEN
    }
    
    # Prepare the merge request payload
    payload = {
        "title": data["Title"],
        "description": data["Description"],
        "source_branch": data["Source Branch"],
        "target_branch": data["Target Branch"],
        "source_project_id": SOURCE_PROJECT_ID,
        "target_project_id": TARGET_PROJECT_ID
    }

    # Determine the state of the merge request
    state = data["State"].lower()
    if state == "merged":
        # For merged merge requests, set the state to merged
        payload["state"] = "merged"
    elif state == "closed":
        # For closed merge requests, set the state to closed
        payload["state"] = "closed"

    # Create the merge request
    response = requests.post(GITLAB_URL.format(project_id=TARGET_PROJECT_ID), headers=headers, data=payload)
    
    if response.status_code == 201:
        merge_request_id = response.json()['id']
        print(f"Merge request created successfully with ID: {merge_request_id}")
        
    else:
        print(f"Failed to create merge request: {response.text}")

# Example usage
if __name__ == "__main__":
    csv_file = GITLAB_MR_CSV
    import_merge_requests_from_csv(csv_file)