from .manifest import Manifest


GITHUB_BASE = 'https://github.com/'

def readme():
    manifest = Manifest.load()
    readme = "# Supported tags and respective `Dockerfile` links\n"
    for main_version, image_data in manifest.containers.items():
        dockerfile_path = image_data['path'].lstrip('.')
        tags_md = ', '.join(map(lambda t: '`{}`'.format(t), image_data['tags']))
        repo_file = "{}/{}/blob/master{}".format(
            GITHUB_BASE.rstrip('/'),
            manifest.github_repo.rstrip('/'),
            dockerfile_path)
        readme += "- [{} (*{}*)]({})\n".format(tags_md, dockerfile_path, repo_file)
    print(readme)
