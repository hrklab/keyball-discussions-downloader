import requests
import json
import time

github_token = "your_github_token"

import json

def run_graphql_query(query, token):
    url = "https://api.github.com/graphql"
    headers = {"Authorization": f"bearer {token}"}
    data = {"query": query}
    response = requests.post(url, headers=headers, json=data)

    if response.status_code != 200:
        raise Exception(f"Error running GraphQL query: {response.status_code}")

    return response.json()

def get_discussion_and_comments(owner, repo, discussion_number, token):
    query = f"""
    {{
      repository(owner: "{owner}", name: "{repo}") {{
        discussion(number: {discussion_number}) {{
          title
          body
          comments(first: 100) {{
            nodes {{
              author {{
                login
              }}
              body
              replies(first: 100) {{
                nodes {{
                  author {{
                    login
                  }}
                  body
                }}
              }}
            }}
          }}
        }}
      }}
    }}
    """

    response_data = run_graphql_query(query, token)
    return response_data["data"]["repository"]["discussion"]

owner = "Yowkees"
repo = "keyball"
discussion_number = 215

discussion_data = get_discussion_and_comments(owner, repo, discussion_number, github_token)

print("Title:", discussion_data["title"])
print("Body:", discussion_data["body"])

for i, comment in enumerate(discussion_data["comments"]["nodes"], 1):
    print(f"Comment {i} by {comment['author']['login']}:")
    print(comment["body"])
    for j, reply in enumerate(comment["replies"]["nodes"], 1):
        print(f"  Reply {j} by {reply['author']['login']}:")
        print("  " + reply["body"])

def format_discussion_as_markdown(discussion_data):
    markdown_output = f"# {discussion_data['title']}\n\n{discussion_data['body']}\n\n---\n\n"

    for i, comment in enumerate(discussion_data["comments"]["nodes"], 1):
        markdown_output += f"## Comment {i} by {comment['author']['login']}\n\n{comment['body']}\n\n"

        for j, reply in enumerate(comment["replies"]["nodes"], 1):
            markdown_output += f"### Reply {j} by {reply['author']['login']}\n\n{reply['body']}\n\n"

    return markdown_output


markdown_output = format_discussion_as_markdown(discussion_data)

filename = f"../docs/md/discussion_{discussion_number}_output.md"

with open(filename, "w", encoding="utf-8") as file:
    file.write(markdown_output)
