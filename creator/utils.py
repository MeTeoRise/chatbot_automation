import os
import io
import socket
import yaml


def chatbot_create(name):
    cmd = "cd chatbots && mkdir {0} && cd {0} && rasa init --no-prompt&".format(name)
    os.system(cmd)


def chatbot_delete(name):
    cmd = "cd chatbots && rm -r {0}".format(name)
    os.system(cmd)


def chatbot_train(chatbot, intents, examples, responses, stories, steps):
    write_intents(chatbot, intents, examples)
    write_responses(chatbot, responses)
    write_stories(chatbot, stories, steps)
    write_policies(chatbot)
    write_domain(chatbot, intents, responses)
    cmd = "cd chatbots && cd {0} && rasa train&".format(chatbot.name)
    os.system(cmd)


def chatbot_start(chatbot):
    cmd = "cd chatbots && cd {0} && rasa run -m models --enable-api --cors \"*\" --debug&".format(chatbot.name)
    os.system(cmd)


def chatbot_stop():
    if check_chatbot() == 0:
        cmd = "kill $(lsof -t -i:5005)"
        os.system(cmd)


def check_chatbot():
    a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    location = ("127.0.0.1", 5005)
    result_of_check = a_socket.connect_ex(location)
    a_socket.close()
    return result_of_check


def write_intents(chatbot, intents, examples):
    path = "chatbots/" + chatbot.name + "/data/nlu.yml"
    intents_list = []
    examples_list = []
    intents = list(intents)
    examples = list(examples)
    for i in intents:
        intents_list.append(list(i))

    for i in examples:
        examples_list.append(list(i))

    intents = intents_list[:]
    examples = examples_list[:]

    merged = {}
    for i in intents:
        merged[i[1]] = []
        for j in examples:
            if i[0] == j[0]:
                merged[i[1]].append(j[1])

    diction = dict()
    diction['version'] = '2.0'
    diction['nlu'] = []

    for i in range(len(intents)):
        diction['nlu'].append({"intent": intents[i][1]})
        diction['nlu'][i]['examples'] = yaml.dump(merged[intents[i][1]])

    f = open(path, 'w+')
    yaml.dump(diction, f, sort_keys=False)


def write_stories(chatbot, stories, steps):
    path = "chatbots/" + chatbot.name + "/data/stories.yml"
    stories_list = []
    steps_list = []
    stories = list(stories)
    steps = list(steps)

    for i in stories:
        stories_list.append(list(i))

    for i in steps:
        steps_list.append(list(i))

    stories = stories_list[:]
    steps = steps_list[:]

    merged = {}
    for i in stories:
        merged[i[1]] = []
        for j in steps:
            if i[0] == j[3]:
                merged[i[1]].append({'intent': j[0]})
                merged[i[1]].append({'action': j[1]})

    diction = dict()
    diction['version'] = '2.0'
    diction['stories'] = []

    for i in range(len(stories)):
        diction['stories'].append({"story": stories[i][1]})
        diction['stories'][i]['steps'] = merged[stories[i][1]]

    f = open(path, 'w+')
    yaml.dump(diction, f, sort_keys=False)


def write_responses(chatbot, responses):
    path = "chatbots/" + chatbot.name + "/data/responses.yml"
    responses_list = []
    responses = list(responses)

    for i in responses:
        responses_list.append(list(i))

    responses = responses_list[:]

    diction = dict()
    diction['responses'] = dict()

    for i in range(len(responses)):
        diction['responses'][responses[i][0]] = [{'text': responses[i][1]}]

    f = open(path, 'w+')
    yaml.dump(diction, f, sort_keys=False)


def write_policies(obj):
    path = "chatbots/" + obj.name + "/config.yml"
    source = "chatbots/default/config.yml"
    cmd = "cp -fr {0} {1}&".format(source, path)
    os.system(cmd)


def write_domain(chatbot, intents, responses):
    path = "chatbots/" + chatbot.name + "/domain.yml"
    intents = list(intents)
    responses = list(responses)
    intents_list = []
    responses_list = []

    for i in intents:
        intents_list.append(list(i))

    for i in responses:
        responses_list.append(list(i))

    intents = intents_list[:]
    responses = responses_list[:]

    diction = dict()
    diction['version'] = '2.0'
    diction['intents'] = []

    for i in range(len(intents)):
        diction['intents'].append(intents[i][1])

    diction['responses'] = dict()

    for i in range(len(responses)):
        diction['responses'][responses[i][0]] = [{'text': responses[i][1]}]

    f = open(path, 'w+')
    yaml.dump(diction, f, sort_keys=False)


# TODO Read defaults and pass them to signals
def write_default_intents(chatbot):
    default_intents = "chatbots/default/data/nlu.yml"
    with open('default/data/nlu.yml') as nlu:
        content = yaml.load(nlu, Loader=yaml.FullLoader)
        intent1 = yaml.load(content['nlu'][0]['examples'], Loader=yaml.FullLoader)

    return content


def read_default_stories():
    default_intents = "chatbots/default/data/stories.yml"
    with open(default_intents) as f:
        s = f.read()

    return s
