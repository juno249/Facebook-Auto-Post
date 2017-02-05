import random
import json

import requests


def get_random_but_unique_num_in_list(attachment_list, limit=5):
    output_list = []
    for i in xrange(0, len(attachment_list)):
        random_int = random.randint(0, len(attachment_list) - 1)
        if len(output_list) < limit:
            if random_int not in output_list:
                output_list.append(random_int)
            else:
                output_list = get_random_but_unique_num_in_list(
                    attachment_list)

    return output_list


def get_child_attachments_list(attachment_list, limit=5):
    output_list = []
    random_num_list = get_random_but_unique_num_in_list(attachment_list, limit)
    for i in random_num_list:
        tmp_dict = {
            "link": attachment_list[i]["link"],
            "picture": attachment_list[i]["picture"],
            "name": attachment_list[i]["name"],
            "description": attachment_list[i]["description"]
        }
        output_list.append(tmp_dict)
    return output_list


def post_on_fb(access_tokens_list, child_attachment_list, message_list,
               post_url_link, exclude_profile_ids=[]):
    for AAD in access_tokens_list:
        if AAD["profile_id"] not in exclude_profile_ids:
            api_url = "https://graph.facebook.com/v2.8/" + AAD[
                "profile_id"] + "/feed?access_token=" + AAD["access_token"]

            child_attachments_json = json.dumps(
                get_child_attachments_list(child_attachment_list))

            post_data_dict = {
                "message": random.choice(message_list),
                "link": post_url_link,
                "child_attachments": child_attachments_json,
            }

            status = requests.post(api_url, post_data_dict)
            if status.status_code == 200:
                print("Affiliate links successfully posted on " + str(
                    AAD["name"]) + "'s timeline")
            else:
                print("An error occurred")
                print(status.text)
