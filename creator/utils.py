import os
import io
import socket
import yaml
from rasa.shared.nlu.training_data.loading import load_data


class MyDumper(yaml.SafeDumper):
    def write_line_break(self, data=None):
        super().write_line_break(data)

        if len(self.indents) == 1:
            super().write_line_break()


def chatbot_create(name):
    cmd = "cd chatbots && mkdir \"{0}\" && cd \"{0}\" && rasa init --no-prompt&".format(name)
    os.system(cmd)


def chatbot_delete(name):
    cmd = "cd chatbots && rm -r \"{0}\"".format(name)
    os.system(cmd)


def chatbot_train(chatbot, intents, examples, responses, utterances, stories, steps, rules, actions, forms, slots):
    write_intents(chatbot, intents, examples)
    write_responses(chatbot, responses, utterances)
    write_stories(chatbot, stories, steps)
    write_rules(chatbot, rules, forms, slots)
    write_actions(chatbot, actions)
    write_policies(chatbot)
    write_domain(chatbot, intents, responses, utterances, actions, forms, slots)
    clear_models(chatbot)
    cmd = "cd chatbots && cd \"{0}\" && rasa train&".format(chatbot.name)
    os.system(cmd)


def chatbot_start(chatbot, actions):
    cmd = "cd chatbots && cd \"{0}\" && rasa run -m models --enable-api --cors \"*\" --debug&".format(chatbot.name)
    os.system(cmd)
    if len(list(actions)) != 0:
        cmd = "cd chatbots && cd \"{0}\" && rasa run actions --cors \"*\" --debug&".format(chatbot.name)
        os.system(cmd)


def chatbot_stop():
    if check_chatbot() == 0:
        cmd = "kill $(lsof -t -i:5005)"
        os.system(cmd)

    if check_chatbot_actions() == 0:
        cmd = "kill $(lsof -t -i:5055)"
        os.system(cmd)


def check_chatbot():
    a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    location = ("127.0.0.1", 5005)
    result_of_check = a_socket.connect_ex(location)
    a_socket.close()
    return result_of_check


def check_chatbot_actions():
    a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    location = ("127.0.0.1", 5055)
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
    yaml.dump(diction, f, Dumper=MyDumper, sort_keys=False)


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
            if i[0] == j[5]:
                if j[0] is not None:
                    merged[i[1]].append({'intent': j[0]})
                if j[1] is not None:
                    merged[i[1]].append({'action': j[1]})
                if j[2] is not None:
                    merged[i[1]].append({'action': j[2]})
                if j[3] is not None:
                    merged[i[1]].append({'action': j[3]})
                    merged[i[1]].append({'active_loop': j[3]})

    diction = dict()
    diction['version'] = '2.0'
    diction['stories'] = []

    for i in range(len(stories)):
        diction['stories'].append({"story": stories[i][1]})
        diction['stories'][i]['steps'] = merged[stories[i][1]]

    f = open(path, 'w+')
    yaml.dump(diction, f, Dumper=MyDumper, sort_keys=False)


def write_responses(chatbot, responses, utterances):
    path = "chatbots/" + chatbot.name + "/data/responses.yml"
    responses_list = []
    utterances_list = []
    responses = list(responses)
    utterances = list(utterances)

    for i in responses:
        responses_list.append(list(i))
    for i in utterances:
        utterances_list.append(list(i))

    responses = responses_list[:]
    utterances = utterances_list[:]

    merged = {}
    for i in responses:
        merged[i[1]] = []
        for idx, j in enumerate(utterances):
            if i[0] == j[0]:
                merged[i[1]].append({'text': j[1]})
                if j[2] is not None:
                    merged[i[1]][idx-1]['image'] = j[2]


    diction = dict()
    diction['responses'] = dict()

    for i in range(len(responses)):
        diction['responses'][responses[i][1]] = merged[responses[i][1]]

    f = open(path, 'w+')
    yaml.dump(diction, f, Dumper=MyDumper, sort_keys=False)


def write_rules(chatbot, rules, forms, slots):
    path = "chatbots/" + chatbot.name + "/data/rules.yml"
    rules_list = []
    rules = list(rules)

    for i in rules:
        rules_list.append(list(i))

    rules = rules_list[:]

    diction = dict()
    diction['version'] = '2.0'
    diction['rules'] = []

    for i in range(len(rules)):
        diction['rules'].append({"rule": rules[i][0]})
        diction['rules'][i]['steps'] = []
        diction['rules'][i]['steps'].append({"intent": rules[i][1]})
        diction['rules'][i]['steps'].append({"action": rules[i][2]})

    for i in range(len(forms)):
        diction['rules'].append({"rule": "Activate form"})
        diction['rules'][2*i+len(rules)]['steps'] = []
        diction['rules'][2*i+len(rules)]['steps'].append({"intent": forms[i][2]})
        diction['rules'][2*i+len(rules)]['steps'].append({"action": forms[i][1]})
        diction['rules'][2*i+len(rules)]['steps'].append({"active_loop": forms[i][1]})

        diction['rules'].append({"rule": "Submit form"})
        diction['rules'][2*i+1+len(rules)]['condition'] = []
        diction['rules'][2*i+1+len(rules)]['condition'].append({"active_loop": forms[i][1]})
        diction['rules'][2*i+1+len(rules)]['steps'] = []
        diction['rules'][2*i+1+len(rules)]['steps'].append({"action": forms[i][1]})
        diction['rules'][2*i+1+len(rules)]['steps'].append({"active_loop": None})
        diction['rules'][2*i+1+len(rules)]['steps'].append({"action": "utter_submit"})

    f = open(path, 'w+')
    yaml.dump(diction, f, Dumper=MyDumper, sort_keys=False)


def write_actions(chatbot, actions):
    path = "chatbots/" + chatbot.name + "/actions/actions.py"
    actions_file = open(path, "w")
    actions = list(actions)
    actions_file.write("from typing import Any, Text, Dict, List\n\n")
    actions_file.write("from rasa_sdk import Action, Tracker\nfrom rasa_sdk.executor import CollectingDispatcher\n\n")
    for action in actions:
        actions_file.write("\nclass Action{0}(Action):\n\n".format(action[0]))
        actions_file.write("    def name(self) -> Text:\n")
        actions_file.write('        return "action_{0}"\n\n'.format(action[0].lower()))
        actions_file.write("    def run(self, dispatcher: CollectingDispatcher,\n")
        actions_file.write("            tracker: Tracker,\n")
        actions_file.write("            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:\n\n")
        for line in action[1].split("\n"):
            actions_file.write("        {0}\n\n".format(line))
        actions_file.write("        return []\n\n")


def write_policies(obj):
    path = "chatbots/" + obj.name + "/config.yml"
    source = "chatbots/default/config.yml"
    cmd = "cp -fr {0} \"{1}\"&".format(source, path)
    os.system(cmd)


def write_domain(chatbot, intents, responses, utterances, actions, forms, slots):
    path = "chatbots/" + chatbot.name + "/domain.yml"
    nlu_path = "chatbots/" + chatbot.name + "/data/nlu.yml"
    data = load_data(nlu_path)
    entities = list(data.entities)

    intents = list(intents)
    responses = list(responses)
    actions = list(actions)
    forms = list(forms)
    slots = list(slots)
    intents_list = []
    responses_list = []
    utterances_list = []
    forms_list = []
    slots_list = []

    for i in intents:
        intents_list.append(list(i))

    for i in responses:
        responses_list.append(list(i))
    for i in utterances:
        utterances_list.append(list(i))

    for i in forms:
        forms_list.append(list(i))
    for i in slots:
        slots_list.append(list(i))

    utterances = utterances_list[:]

    intents = intents_list[:]
    responses = responses_list[:]

    forms = forms_list[:]
    slots = slots_list[:]

    merged = {}
    for i in responses:
        merged[i[1]] = []
        for idx, j in enumerate(utterances):
            if i[0] == j[0]:
                merged[i[1]].append({'text': j[1]})
                if j[2] is not None:
                    merged[i[1]][idx-1]['image'] = j[2]

    merged_forms = {}
    for i in forms:
        merged_forms[i[1]] = dict()
        for idx, j in enumerate(slots):
            if i[0] == j[4]:
                merged_forms[i[1]][j[0]] = []
                merged_forms[i[1]][j[0]].append({'type': 'from_text'})

    diction = dict()
    diction['version'] = '2.0'
    diction['intents'] = []

    for i in range(len(intents)):
        diction['intents'].append(intents[i][1])

    diction['entities'] = []

    for i in range(len(entities)):
        diction['entities'].append(entities[i])

    diction['slots'] = dict()

    for i in range(len(slots)):
        slot_dict = dict()
        slot_dict['type'] = slots[i][1]
        slot_dict['influence_conversation'] = slots[i][2]
        diction['slots'][slots[i][0]] = slot_dict

    diction['responses'] = dict()

    for i in range(len(responses)):
        diction['responses'][responses[i][1]] = merged[responses[i][1]]

    diction['actions'] = []

    for i in range(len(actions)):
        diction['actions'].append("{0}".format(actions[i][0].lower()))

    diction['forms'] = dict()

    for i in range(len(forms)):
        diction['forms'][forms[i][1]] = merged_forms[forms[i][1]]

    diction['session_config'] = dict()
    diction['session_config']['session_expiration_time'] = 60
    diction['session_config']['carry_over_slots_to_new_session'] = True

    f = open(path, 'w+')
    yaml.dump(diction, f, Dumper=MyDumper, sort_keys=False)


def clear_models(chatbot):
    cmd = "cd chatbots && cd \"{0}\" && cd models && rm *".format(chatbot.name)
    os.system(cmd)


# TODO Pass intents to signals
def read_default_intents(chatbot):
    default_intents = "chatbots/default/data/nlu.yml"
    data = load_data(default_intents)
    intents = data.intents

    return intents


# TODO Read default stories and pass them to signals
def read_default_stories():
    default_intents = "chatbots/default/data/stories.yml"
    data = load_data(default_intents)
    intents = data.intents

    return intents
