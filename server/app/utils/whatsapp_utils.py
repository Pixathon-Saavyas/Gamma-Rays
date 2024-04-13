from flask import current_app, jsonify
import json, requests, logging, re
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts.prompt import PromptTemplate
from langchain.chains import LLMChain

import pandas as pd




def get_top_5_therapists(city):
    df = pd.read_csv("app/data.csv")
    # Filter therapists based on the input city
    therapists_in_city = df[df["city"].str.lower() == city.lower()]

    if therapists_in_city.empty:
        print("No therapists found in the specified city.")
        return

    # Sort therapists based on years_of_exp in descending order and get the top 5
    top_5_therapists = therapists_in_city.sort_values(
        by="years_of_exp", ascending=False
    ).head(5)

    return top_5_therapists

llm = ChatGoogleGenerativeAI(
    model="gemini-pro", google_api_key="AIzaSyA0SThtOf3QoNJLr12CiDwkiTtUafL1rXE"
)
def log_http_response(response):
    logging.info(f"Status: {response.status_code}")
    logging.info(f"Content-type: {response.headers.get('content-type')}")
    logging.info(f"Body: {response.text}")


def get_text_message_input(recipient, text):
    return json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient,
            "type": "text",
            "text": {"preview_url": False, "body": text},
        }
    )
def generate_final_report(data):
    # filename=filename
    data = data
    # conversation_history=read_file_as_string(filename=filename)
    conv_prompt = PromptTemplate.from_template(
        """You are an expert mental therapist./
    We are providing you with the a conversational data between between a user and a assessment chatbot. /
    Based on the conversation history provided, you have to output a final assessment of the user. We have also tagged all the user sentences with emotions detection deep learning model, please consider the emotions while generating the response./
    Return the response only as a json object starting and ending with curly brackets with the following keys and value-/ condition_of_patient : basic/mediocre/severe/, possible_causes : [list of possible causes discussed],/
    
                                               
    **Conversation History:**

    {conversation_history}

    **Respond:** """
    )

    conv_chain = LLMChain(llm=llm, prompt=conv_prompt, verbose=False)
    # conversation_history=""
    response = conv_chain.run(conversation_history=data)
    return response

def append_to_file(filename, value):
    with open(filename, "a") as file:
        file.write(str(value) + "\n")  # Convert value to string and add newline


def read_file_as_string(filename):
    with open(filename, "r") as file:
        return file.read()

def generate_gpt_response(user_msg):
    user_message = user_msg
    # filename = filename
    conversation_history = read_file_as_string(filename="app/utils/msgs.txt")

    conv_prompt = PromptTemplate.from_template(
        """You are an expert mental therapist./
        Your task is to confront the user for his problems and ask critical questions to understand his mental health. You have to somehow ask the user about his symptoms, possible causes(relationship issues, health issues, sad demise) and carry on the conversation.Keep the coversation short(1-2 lines). The following is the conversation so far, continue asking questions. \
        Speak with the user in a very assistive and helpful manner.

    **Conversation History:**

    {conversation_history}

    **User Input:**

    {user_input}

    **Respond:**"""
    )

    conv_chain = LLMChain(llm=llm, prompt=conv_prompt, verbose=False)
    response = conv_chain.run(
        conversation_history=conversation_history, user_input=user_message
    )
    return response

def generate_response(response):
    user_resp=response
    if response.lower() == "hi":
        initial_msg = "Hello, I am Leo. I'm here to listen to your concerns and help you in any way I can. Can you tell me a little bit about what's been troubling you? "
        return initial_msg
    elif response.lower()=="bye":
        conv_history=read_file_as_string("app/utils/msgs.txt")
        response=generate_final_report(conv_history)
        response = json.loads(response)
        if response["condition_of_patient"] == "severe":
            therapists = get_top_5_therapists(city="mumbai")
            resp=f"We have analysed your condition and we think that you should consult to a therapist. Here are top 5 therapists in Mumbai : \n {therapists}"
        else:
            resp= "We have analysed your condition and we think that you can get back into shape by doing this course : "
        return resp

    else:
        response=generate_gpt_response(user_msg=response)
        response_to_store=f"User : {user_resp}, AI Agent : {response}"
        append_to_file(filename="app/utils/msgs.txt",value=response_to_store)

    return response


def send_message(data):
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {current_app.config['ACCESS_TOKEN']}",
    }

    url = f"https://graph.facebook.com/{current_app.config['VERSION']}/{current_app.config['PHONE_NUMBER_ID']}/messages"

    try:
        response = requests.post(
            url, data=data, headers=headers, timeout=10
        )  # 10 seconds timeout as an example
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
    except requests.Timeout:
        logging.error("Timeout occurred while sending message")
        return jsonify({"status": "error", "message": "Request timed out"}), 408
    except (
        requests.RequestException
    ) as e:  # This will catch any general request exception
        logging.error(f"Request failed due to: {e}")
        return jsonify({"status": "error", "message": "Failed to send message"}), 500
    else:
        # Process the response as normal
        log_http_response(response)
        return response


def process_text_for_whatsapp(text):
    pattern = r"\【.*?\】"
    text = re.sub(pattern, "", text).strip()
    pattern = r"\*\*(.*?)\*\*"
    replacement = r"*\1*"
    whatsapp_style_text = re.sub(pattern, replacement, text)
    return whatsapp_style_text


def process_whatsapp_message(body):
    wa_id = body["entry"][0]["changes"][0]["value"]["contacts"][0]["wa_id"]
    name = body["entry"][0]["changes"][0]["value"]["contacts"][0]["profile"]["name"]

    message = body["entry"][0]["changes"][0]["value"]["messages"][0]
    message_body = message["text"]["body"]

    response = generate_response(message_body)

    data = get_text_message_input(current_app.config["RECIPIENT_WAID"], response)
    send_message(data)


def is_valid_whatsapp_message(body):
    return (
        body.get("object")
        and body.get("entry")
        and body["entry"][0].get("changes")
        and body["entry"][0]["changes"][0].get("value")
        and body["entry"][0]["changes"][0]["value"].get("messages")
        and body["entry"][0]["changes"][0]["value"]["messages"][0]
    )
