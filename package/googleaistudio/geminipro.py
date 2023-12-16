import vertexai, os
from vertexai.preview.generative_models import GenerativeModel, ChatSession

# Install google-cloud-aiplatform FIRST!
#!pip install --upgrade google-cloud-aiplatform

# Keep for reference; unnecessary for api key authentication with json file
# (developer): Update and un-comment below lines
#project_id = "letmedoitai"
#location = "us-central1"
#vertexai.init(project=project_id, location=location)

# authentication
authpath1 = os.path.join(os.path.expanduser('~'), "credentials_googleaistudio.json")
authpath2 = os.path.join(os.path.expanduser('~'), "letmedoit", "credentials_googleaistudio.json")
if os.path.isfile(authpath1):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = authpath1
elif os.path.isfile(authpath2):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = authpath2
else:
    print(f"API key json file '{authpath1}' not found!")
    print("Read https://github.com/eliranwong/letmedoit/wiki/Google-API-Setup for setting up Google API.")
    exit(0)
# initiation
vertexai.init()

model = GenerativeModel("gemini-pro")
chat = model.start_chat()
print("Gemini Pro Chat Launched!")
print("(To quit, enter '.quit')")

def get_chat_response(chat: ChatSession, prompt: str) -> str:
    response = chat.send_message(prompt)
    return response.text

def main():
    while True:
        print("------------------------------\n")
        print("Enter your prompt below:")
        prompt = input(">>> ")
        print("")
        if prompt == ".quit":
            break
        elif prompt := prompt.strip():
            print(get_chat_response(chat, prompt))
        print("")

if __name__ == '__main__':
    main()