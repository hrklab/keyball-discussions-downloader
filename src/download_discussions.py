import requests
import json
import time
import os

class GitHubDiscussion:
    def __init__(self, token, owner, repo):
        self.token = token
        self.owner = owner
        self.repo = repo
        self.url = "https://api.github.com/graphql"
        self.headers = {"Authorization": f"bearer {self.token}"}

    def run_graphql_query(self, query):
        data = {"query": query}
        response = requests.post(self.url, headers=self.headers, json=data)

        if response.status_code != 200:
            raise Exception(f"Error running GraphQL query: {response.status_code}")

        return response.json()

    def get_discussion_and_comments(self, discussion_number):
        query = f"""
        {{
          repository(owner: "{self.owner}", name: "{self.repo}") {{
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

        response_data = self.run_graphql_query(query)
        return response_data["data"]["repository"]["discussion"]

    @staticmethod
    def format_discussion_as_markdown(discussion_data):
        markdown_output = f"# {discussion_data['title']}\n\n{discussion_data['body']}\n\n---\n\n"

        for i, comment in enumerate(discussion_data["comments"]["nodes"], 1):
            markdown_output += f"## Comment {i} by {comment['author']['login']}\n\n{comment['body']}\n\n"

            for j, reply in enumerate(comment["replies"]["nodes"], 1):
                markdown_output += f"### Reply {j} by {reply['author']['login']}\n\n{reply['body']}\n\n"

        return markdown_output


    def save_markdown_output(self, discussion_number):
        discussion_data = self.get_discussion_and_comments(discussion_number)
        markdown_output = self.format_discussion_as_markdown(discussion_data)

        directory = "./../docs/md/"
        if not os.path.exists(directory):
            os.makedirs(directory)

        filename = f"{directory}discussion_{discussion_number}_output.md"

        with open(filename, "w", encoding="utf-8") as file:
            file.write(markdown_output)


github_token = "your_github_token"
owner = "Yowkees"
repo = "keyball"

start_discussion_number = 1
end_discussion_number = 221

for discussion_number in range(start_discussion_number, end_discussion_number + 1):
    try:
        github_discussion = GitHubDiscussion(github_token, owner, repo)
        github_discussion.save_markdown_output(discussion_number)
        print(f"Saved discussion {discussion_number}.")
    except Exception as e:
        print(f"Error in saving discussion {discussion_number}: {e}")
