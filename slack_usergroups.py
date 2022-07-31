from pydoc import cli
from urllib import response
# from webbrowser import get
from xml.etree.ElementTree import tostring
import slack
from slack.errors import SlackApiError
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


test_api_token = False

def initialise_api_connection(API_TOKEN):        
    while True:
        try:
            if API_TOKEN == "":
                API_TOKEN = input("Input Slack API Token: ")
            client = slack.WebClient(token=API_TOKEN)
            if (client.auth_test().get("ok")): # do more testing then maybe remove this
                print("API Connection Success")
                return client
        except:
            print("API Connection Failed")
            API_TOKEN=""
        

def usergroups_update(client: slack.WebClient):
    new_users = list_of_users_from_txt()
    try:
        usergroup_id = input("Input UsergroupID: ")
        current_users = client.usergroups_users_list(usergroup=usergroup_id).get("users")

        updated_list = current_users + new_users
        updated_list = list(dict.fromkeys(updated_list))
        
        updated_list = ",".join(updated_list)
        print(updated_list)
        client.usergroups_users_update(usergroup=usergroup_id, users=updated_list)
    except SlackApiError as e:
        assert e.response["ok"] is False
        assert e.response["error"] # str like 'invalid_auth', 'invalid_arguments', 'invalid_users'
        print(f"Got an error: {e.response['error']}")


def list_usergroups(client: slack.WebClient):
    try:
        jsonObject = client.usergroups_list()
        for group in jsonObject.get("usergroups"):
            print("Usergroup name: " + group.get("name"))
            print("ID: " + group.get("id") + "\n")

    except SlackApiError as e:
        assert e.response["ok"] is False
        assert e.response["error"]
        
        print(f"\nGot an error: {e.response['error']}")


def create_usergroup(client: slack.WebClient):
    try:
        name = input("What would you like your usergroup name to be called? ")
        handle = input("What would you like your usergroup handle (@...) to be called? ")
        description = input("What would you like the description of this handle be? (Leave blank if you don't want one)")

        client.usergroups_create(name=name, handle=handle, description=description)
        response = client.usergroups_list()
        for group in response.get("usergroups"):
            if group.get("name") == name:
                print("Here is the Usergroup ID: " + group.get("id"))
                client.usergroups_enable(group.get("id"))
                break
    except SlackApiError as e:
        assert e.response["ok"] is False
        assert e.response["error"] # str like 'invalid_auth', 'name_already_exists', 'bad_handle
        print(f"Got an error: {e.response['error']}")


def test(client: slack.WebClient):
    ...

def list_of_users_from_txt():
    file_name = input("What is your filename? ")  
    try: 
        with open(file_name, "r") as f:
            users = f.read()
    except FileNotFoundError as e:
        print("File doesn't exist or isn't in the correct directory")
    
    return users.split()


def export_user_id_from_email(client: slack.WebClient):
    email_file = input("Where is the file containing emails? ")
    try: 
        with open(email_file, "r") as f:
            emails = f.readlines()
    except FileNotFoundError as e:
        print("File doesn't exist or isn't in the correct directory")

    email_list = []
    for email in emails:
        email_list.append(email.strip())
    
    export_file_name = input("What do you want the new File to be called? ")


    for emails in email_list:
        try:
            id = client.users_lookupByEmail(email=emails).get("user").get("id")
            with open(export_file_name, "a") as f:
                f.write(id + "\n")
        except SlackApiError as e:
            assert e.response["ok"] is False
            assert e.response["error"] # str like 'invalid_auth', 'name_already_exists', 'bad_handle
            print(f"Got an error: {e.response['error']}")
    # print(json)
    # print(json.get("id"))
    # print(email_list)
    # try:
    #     for i in email_list:
    #         json = client.users_lookupByEmail(email=i).get("user")
    #         print(json)
    #         print(json.get("id"))
    #         with open(export_file_name, "a") as f:
    #             f.write(json.get("id")+"\n")
    #         f.close()
    # except e:
    #     print("Error")

def test(client: slack.WebClient):
        print(client.users_lookupByEmail(email="kelsteve021@student.wethinkcode.co.za").get("user"))



if __name__ == "__main__":
    client = initialise_api_connection(os.environ["SLACK_TOKEN"])
    user_choice = ""
    while user_choice != 0:
        try:
            user_choice = int(input("What would you like to do?\n  1. Create usergroup\n  2. List all usergroups\n  3. Update usergroups\n  4. Export UserID based on email lookup \n  0. Exit\n"))
            if user_choice == 1:
                create_usergroup(client)
            elif user_choice == 2:
                list_usergroups(client)
            elif user_choice == 3:
                usergroups_update(client)
            elif user_choice == 4:
                export_user_id_from_email(client)

        except:
            print("Only input intergers")