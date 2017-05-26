from __future__ import print_function
import sys
import os
import docker
from datetime import datetime

from .manifest import Manifest


def build():
    start = datetime.now()
    client = docker.from_env()
    manifest = Manifest.load()
    for main_tag, image_data in manifest.containers.items():
        result_column = 35
        building_text = "{}s: Bulding {} ... ".format(
            (datetime.now() - start).seconds, main_tag)
        spaces = result_column - len(building_text)
        if spaces < 1:
            spaces = 1

        print("{}{}".format(building_text, ' ' * spaces), end='')
        sys.stdout.flush()

        image = client.images.build(
            fileobj=file(image_data['path'], 'r'),
            tag="{}:{}".format(manifest.dockerhub_repo, main_tag),
            nocache=True)
        rustc_version = client.containers.run(image.id, command="rustc -V").strip()
        manifest.containers.update(main_tag,
                                   image=image.short_id,
                                   rustc=rustc_version,
                                   updated=datetime.now())
        for tag in image_data['tags']:
            image.tag('scorpil/rust', tag)
        print(u"\u2713 [image: {} | rustc: {}]".format(image.short_id, rustc_version))
        sys.stdout.flush()
    manifest.store()
