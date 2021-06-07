import os
import yaml
from collections import OrderedDict


def chatbot_create(name):
    cmd = "cd chatbots && mkdir {0} && cd {0} && rasa init --no-prompt&".format(name)
    os.system(cmd)


def chatbot_delete(name):
    cmd = "cd chatbots && rm -r {0}".format(name)
    os.system(cmd)


def chatbot_train(obj):
    write_intents(obj)
    write_stories(obj)
    cmd = "cd chatbots && cd {0} && rasa train&".format(obj.name)
    os.system(cmd)


def read_intents(name):
    path = "chatbots/" + name + "/data/nlu.yml"
    with open(path) as f:
        s = f.read()

    return s


def write_intents(obj):
    path = "chatbots/" + obj.name + "/data/nlu.yml"

    yaml.add_representer(OrderedDict, lambda dumper, data: dumper.represent_mapping('tag:yaml.org,2002:map', data.items()))

    with open(path, 'w') as outfile:
        yaml.dump(obj.intent.yaml, outfile, default_flow_style=False, sort_keys=False)


def read_default_intents():
    default_intents = "chatbots/default/data/nlu.yml"
    with open(default_intents) as f:
        s = f.read()

    return s


def read_stories(name):
    path = "chatbots/" + name + "/data/stories.yml"
    with open(path) as f:
        s = f.read()

    return s


def write_stories(obj):
    path = "chatbots/" + obj.name + "/data/stories.yml"

    yaml.add_representer(OrderedDict,
                         lambda dumper, data: dumper.represent_mapping('tag:yaml.org,2002:map', data.items()))

    with open(path, 'w') as outfile:
        yaml.dump(obj.story.yaml, outfile, default_flow_style=False, sort_keys=False)


def read_default_stories():
    default_intents = "chatbots/default/data/stories.yml"
    with open(default_intents) as f:
        s = f.read()

    return s

