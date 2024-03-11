import litellm

# Uncomment the following line if you need verbose logging for debugging purposes
# litellm.set_verbose(True)

full_transcript = ""

# Define the roles of the agents in the negotiation
roles = {
    "alice": "You are roleplaying as a US trade policy negotiator. Your job is to represent US interests. "
             "You are aggressive, straightforward, pushing for results. Always stay in the role. "
             "Under no circumstances can you mention you are an AI model.",
    "bob": "You are roleplaying as a Chinese trade policy negotiator. Your job is to represent the interests of "
           "the People's Republic of China. You are passive aggressive, evasive, pushing for ambiguity. "
           "Always stay in the role. Under no circumstances can you mention you are an AI model."
}

# Initialize conversation histories
history = {
    "alice": [{"role": "system", "content": roles["alice"]}],
    "bob": [{"role": "system", "content": roles["bob"]}]
}

# Function to get a reply from the model
def get_reply(role, messages):
    response = litellm.completion(
        model="gpt-4-1106-preview",
        #model="perplexity/pplx-70b-online",
        messages=messages,
        max_tokens=1000
    )
    return response.choices[0].message.content

# Function to start the conversation
def start_the_convo():
    message = ("Hi. We are here to discuss trade today between the US and China. "
               "We think it's unacceptable that China doesn't let US tech companies operate in the country. "
               "How can we solve this issue?")

    to_print = f"🇺🇸 Alice says: \n{message}\n"
    print(to_print)
    global full_transcript
    full_transcript += to_print

    # Update both conversation histories
    alice_history_item = {"role": "user", "content": message}
    bob_history_item = {"role": "assistant", "content": message}
    history["alice"].append(alice_history_item)
    history["bob"].append(bob_history_item)

    # Get Bob's reply
    reply = get_reply("bob", history["bob"])
    
    to_print = f"🇨🇳 Bob says: \n{reply}\n"
    print(to_print)
    full_transcript += to_print

    # Update both conversation histories
    history["alice"].append({"role": "assistant", "content": reply})
    history["bob"].append({"role": "user", "content": reply})

# Function to handle the conversation turns
def conversation(turns):
    next_speaker = "alice"

    for _ in range(turns):
        speaker_role = "user" if next_speaker == "alice" else "assistant"
        other_role = "assistant" if next_speaker == "alice" else "user"

        reply = get_reply(next_speaker, history[next_speaker])
        to_print = f"🇺🇸 Alice says: \n{reply}\n" if next_speaker == "alice" else f"🇨🇳 Bob says: \n{reply}\n"
        print(to_print)
        global full_transcript
        full_transcript += to_print

        # Update both conversation histories
        history[next_speaker].append({"role": speaker_role, "content": reply})
        history["alice" if next_speaker == "bob" else "bob"].append({"role": other_role, "content": reply})

        # Toggle the next speaker
        next_speaker = "bob" if next_speaker == "alice" else "alice"

# Start the conversation
start_the_convo()

# To continue the conversation, uncomment the following line:
conversation(6)

filename = "negotiation_transcript.txt"

with open(filename, 'w') as file:
    file.write(full_transcript)
    
print("\n\n*** NEGOTIATION ROUND CLOSED ***\n")