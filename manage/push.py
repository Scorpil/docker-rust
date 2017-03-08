from __future__ import print_function
import docker
from datetime import datetime

from .manifest import Manifest


def push():
    client = docker.from_env()
    manifest = Manifest.load()
    for main_tag, image_data in manifest.containers.items():
        for tag in image_data['tags']:
            push_text = "Pushing {}:{} ... ".format(
                manifest.dockerhub_repo, tag)
            print(push_text, end='')

            client.images.push(manifest.dockerhub_repo, tag)
            print(u"\u2713")
        manifest.containers.update(main_tag, pushed=datetime.now())
    manifest.store()
