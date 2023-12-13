import os
import openai
from pprint import pprint

#Glabal Variables
api_key =  os.environ["OPENAI_API_KEY"] = "token"
assistant_id = "asst_id"

def set_client():
    return openai.OpenAI()

def create_message(client, prompt):
    # Create a Thread
    thread = client.beta.threads.create()

    # Add a Message to a Thread
    message = client.beta.threads.messages.create(thread_id=thread.id,role="user",
        content=prompt
    )

    # Run the Assistant
    run = client.beta.threads.runs.create(thread_id=thread.id,assistant_id=assistant_id,instructions="Be specific and enthusiastic")
    run.model_dump_json(indent=4)

    return thread, run

def send_message(client, prompt):
    thread, run = create_message(client, prompt)
    # If run is 'completed', get messages and print
    while True:
        # Retrieve the run status
        run_status = client.beta.threads.runs.retrieve(thread_id=thread.id,run_id=run.id)
        print(run_status.model_dump_json(indent=4))
        if run_status.status == 'completed':
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            pprint(messages)
            break

    return messages.data[0].content[0].text.value