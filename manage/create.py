import os
import yaml
import pystache

from .manifest import Manifest


DFILE_PATH = './templates/Dockerfile.mustache'
DFILE_ONBUILD_PATH = './templates/Dockerfile_onbuild.mustache'

dfile_template = open(DFILE_PATH, 'r').read()
dfile_onbuild_template = open(DFILE_ONBUILD_PATH, 'r').read()

tags_file_stream = open('docker-tags.yml', 'r')


def make_dfile_path(version, channel, onbuild):
    dfile_path_items = ['.']
    if channel:
        dfile_path_items.append(channel)
    else:
        dfile_path_items.append(str(version))

    if onbuild:
        dfile_path_items.append('onbuild')

    dfile_path_items.append('Dockerfile')

    return '/'.join(dfile_path_items)

def base_template(onbuild):
    if onbuild:
        return dfile_onbuild_template
    return dfile_template

def dfile_generate(version, archive, channel=None, onbuild=False):
    dfile_path = make_dfile_path(version, channel, onbuild)
    template_vars = {}
    if onbuild:
        template_vars['parent'] = channel or version
        template_vars['app_home'] = '/rust/app'
        template = dfile_onbuild_template
    else:
        template_vars['archive'] = archive
        template_vars['rust_home'] = '/rust'
        template = dfile_template

    dfile_content = pystache.render(template, template_vars)
    return dfile_write(dfile_path, dfile_content)

def dfile_write(dfile_path, dfile_content):
    try:
        os.makedirs(os.path.dirname(dfile_path))
    except OSError:
        pass

    with open(dfile_path, 'w') as dfile:
        dfile.write(dfile_content)
    return dfile_path

def create():
    manifest = Manifest.load()
    tags_info = yaml.safe_load(tags_file_stream)
    manifest.dockerhub_repo = tags_info['dockerhub_repo']
    manifest.github_repo = tags_info['github_repo']
    for image in tags_info['images']:
        version = image['version']
        archive = image['archive']
        channel = image.get('channel')
        extra_tags = image.get('extra_tags')

        path = dfile_generate(version, archive, channel, onbuild=False)
        manifest.containers.add(path, version, archive, channel,
                                extra_tags, onbuild=False)

        onbuild_path = dfile_generate(version, archive, channel, onbuild=True)
        manifest.containers.add(onbuild_path, version, archive, channel,
                                extra_tags, onbuild=True)

    manifest.store()
