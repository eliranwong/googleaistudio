import vertexai, os, traceback
from vertexai.language_models import CodeChatModel
from googleaistudio import config
from googleaistudio.health_check import HealthCheck
if not hasattr(config, "exit_entry"):
    HealthCheck.setBasicConfig()
    HealthCheck.saveConfig()
    print("Updated!")
HealthCheck.setPrint()
import pygments
from pygments.lexers.markup import MarkdownLexer
from prompt_toolkit.formatted_text import PygmentsTokens
from prompt_toolkit import print_formatted_text
from prompt_toolkit.styles import Style
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from pathlib import Path


# Install google-cloud-aiplatform FIRST!
#!pip install --upgrade google-cloud-aiplatform


class Codey:

    def __init__(self, name="Codey"):
        # authentication
        authpath1 = os.path.join(HealthCheck.getFiles(), "credentials_googleaistudio.json")
        if os.path.isfile(authpath1):
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = authpath1
            self.runnable = True
        else:
            print(f"API key json file '{authpath1}' not found!")
            print("Read https://github.com/eliranwong/letmedoit/wiki/Google-API-Setup for setting up Google API.")
            self.runnable = False
        # initiation
        vertexai.init()
        self.name = name

    def run(self, prompt="", model="codechat-bison-32k", temperature=0.2):
        historyFolder = os.path.join(HealthCheck.getFiles(), "history")
        Path(historyFolder).mkdir(parents=True, exist_ok=True)
        chat_history = os.path.join(historyFolder, self.name.replace(" ", "_"))
        chat_session = PromptSession(history=FileHistory(chat_history))

        promptStyle = Style.from_dict({
            # User input (default text).
            "": config.terminalCommandEntryColor2,
            # Prompt.
            "indicator": config.terminalPromptIndicatorColor2,
        })

        if not self.runnable:
            print(f"{self.name} is not running due to missing configurations!")
            return None
        model = CodeChatModel.from_pretrained(model)
        # https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/code-chat
        parameters = {
            "temperature": temperature,  # Temperature controls the degree of randomness in token selection; 0.0–1.0; Default: 0.2
            "max_output_tokens": 2048,  # Token limit determines the maximum amount of text output; 1–2048; Default: 1024
        }
        chat = model.start_chat(
            context=f"You're {self.name}, an expertise about coding.",
        )
        HealthCheck.print2(f"\n{self.name} loaded!")
        print("(To start a new chart, enter '.new')")
        print(f"(To quit, enter '{config.exit_entry}')\n")
        while True:
            if not prompt:
                prompt = HealthCheck.simplePrompt(style=promptStyle, promptSession=chat_session)
                if prompt and not prompt in (".new", config.exit_entry) and hasattr(config, "currentMessages"):
                    config.currentMessages.append({"content": prompt, "role": "user"})
            else:
                prompt = HealthCheck.simplePrompt(style=promptStyle, promptSession=chat_session, default=prompt, accept_default=True)
            if prompt == config.exit_entry:
                break
            elif prompt == ".new":
                chat = model.start_chat()
                print("New chat started!")
            elif prompt := prompt.strip():
                try:
                    # https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/text-chat
                    response = chat.send_message(
                        prompt, **parameters
                    )
                    config.pagerContent = response.text

                    # color response with markdown style
                    tokens = list(pygments.lex(config.pagerContent, lexer=MarkdownLexer()))
                    print_formatted_text(PygmentsTokens(tokens), style=HealthCheck.getPygmentsStyle())

                except:
                    HealthCheck.print2(traceback.format_exc())

            prompt = ""

        HealthCheck.print2(f"\n{self.name} closed!\n")

def main():
    Codey().run()

if __name__ == '__main__':
    main()