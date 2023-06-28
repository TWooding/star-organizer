import argparse
import os
import requests

class StarOrganizer:
    def __init__(self, token, sort_categories=True, sort_repos=True,include_private=False, output=None):
        self.token = token
        self.sort_categories = sort_categories
        self.sort_repos = sort_repos
        self.include_private = include_private
        self.output = output if output else "README.md"

    def run(self):
        # Initialize a list to store all starred repositories
        starred_repos = []

        # Get the first page of starred repositories
        url = "https://api.github.com/user/starred"
        headers = {"Authorization": "Bearer " + self.token}
        response = requests.get(url, headers=headers)
        if response.status_code == 401:
            print("Unable to gather Starred Repositories. Invalid token")
            exit(1)
        
        starred_repos += response.json()
        if self.include_private:
            starred_repos = [repo for repo in starred_repos if not repo["private"]]

        # Get the URL of the next page of results
        next_url = None
        link_header = response.headers.get("Link")
        if link_header:
            for link in link_header.split(", "):
                if "rel=\"next\"" in link:
                    next_url = link[link.index("<") + 1:link.index(">")]

        # Loop through the remaining pages of results
        while next_url:
            response = requests.get(next_url, headers=headers)
            starred_repos += response.json()
            next_url = None
            link_header = response.headers.get("Link")
            if link_header:
                for link in link_header.split(", "):
                    if "rel=\"next\"" in link:
                        next_url = link[link.index("<") + 1:link.index(">")]

        # Loop through the starred repositories and categorize them
        categories = {}
        for repo in starred_repos:
            language = repo["language"]
            if language:
                # Normalize the language name to lowercase and remove leading/trailing whitespace
                normalized_language = language.lower().strip()

                # Check if this language has already been encountered
                if normalized_language not in categories:
                    categories[normalized_language] = []
                categories[normalized_language].append(repo["full_name"])

        # Sort the categories by language name
        if self.sort_categories:
            sorted_categories = sorted(categories.items(), key=lambda x: x[0])
        # Create the directories if necessary
        dirname = os.path.dirname(self.output)
        if dirname and not os.path.exists(dirname):
            os.makedirs(dirname)

        # Write the categorized list of starred repositories to a file
        with open(self.output, "w") as f:
            # Write the Table of Contents
            f.write("# Table of Contents\n\n")
            for language, repos in sorted_categories:
                formatted =  '-'.join(map(str.capitalize, language.split())) if ' ' in language else language.capitalize()
                f.write("- [{}](#{})\n".format(formatted.replace('-', ' '), formatted))

            # Write the list of starred repositories for each category
            f.write("\n")
            
            for language, repos in sorted_categories:
                formatted =  '-'.join(map(str.capitalize, language.split())) if ' ' in language else language.capitalize()                
                f.write(f"## {formatted.replace('-', ' ')}\n\n")
                if self.sort_repos:
                    sorted_repos = sorted(repos)
                else:
                    sorted_repos = repos
                for repo in sorted_repos:
                    f.write("- [{}]({})\n".format(repo, "https://github.com/" + repo))
                f.write("\n")
                
def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--token", required=True, help="GitHub access token")
    parser.add_argument("--include-private",action="store_false", help="include private starred repositories (default: False)")
    parser.add_argument("--sort-categories", action="store_true", default=True, help="sort categories alphabetically (default: True)")
    parser.add_argument("--sort-repos", action="store_true", default=True, help="sort starred repositories alphabetically within each category (default: True)")
    parser.add_argument("--output", help="output file path")
    args = parser.parse_args()

    # Create an instance of the StarOrganizer class and run it
    organizer = StarOrganizer(token=args.token, sort_categories=args.sort_categories, sort_repos=args.sort_repos, include_private=args.include_private, output=args.output)
    organizer.run()
    
    

if __name__ == "__main__":
    main()
   