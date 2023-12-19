import vertexai, os, traceback, argparse
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
from prompt_toolkit.shortcuts import clear
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

    def run(self, prompt="", model="codechat-bison-32k", temperature=0.2, max_output_tokens=2048):
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
            "max_output_tokens": max_output_tokens,  # Token limit determines the maximum amount of text output; 1–2048; Default: 1024
        }
        chat = model.start_chat(
            context=f"You're {self.name}, an expert in coding.",
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
                clear()
                chat = model.start_chat()
                print("New chat started!")
            elif prompt := prompt.strip():
                try:
                    HealthCheck.startSpinning()
                    # https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/text-chat
                    response = chat.send_message(
                        prompt, **parameters
                    )
                    HealthCheck.stopSpinning()
                    config.pagerContent = response.text.strip()
                    # color response with markdown style
                    tokens = list(pygments.lex(config.pagerContent, lexer=MarkdownLexer()))
                    print_formatted_text(PygmentsTokens(tokens), style=HealthCheck.getPygmentsStyle())
                    # integrate messages into LetMeDoIt messages
                    if hasattr(config, "currentMessages") and config.pagerContent:
                        config.currentMessages.append({"role": "assistant", "content": config.pagerContent})
                except:
                    HealthCheck.stopSpinning()
                    HealthCheck.print2(traceback.format_exc())

            prompt = ""

        HealthCheck.print2(f"\n{self.name} closed!\n")

def main():
    # Create the parser
    parser = argparse.ArgumentParser(description="codey cli options")
    # Add arguments
    parser.add_argument("default", nargs="?", default=None, help="default entry")
    parser.add_argument('-m', '--model', action='store', dest='model', help="specify language model with -m flag; default: codechat-bison-32k")
    parser.add_argument('-o', '--outputtokens', action='store', dest='outputtokens', help="specify maximum output tokens with -o flag; default: 2048")
    parser.add_argument('-t', '--temperature', action='store', dest='temperature', help="specify temperature with -t flag; default: 0.2")
    # Parse arguments
    args = parser.parse_args()
    # Get options
    prompt = args.default.strip() if args.default and args.default.strip() else ""
    model = args.model.strip() if args.model and args.model.strip() else "codechat-bison-32k"
    if args.outputtokens and args.outputtokens.strip():
        try:
            max_output_tokens = int(args.outputtokens.strip())
        except:
            max_output_tokens = 2048
    else:
        max_output_tokens = 2048
    if args.temperature and args.temperature.strip():
        try:
            temperature = float(args.temperature.strip())
        except:
            temperature = 0.2
    else:
        temperature = 0.2
    # Run codey
    Codey().run(
        prompt=prompt,
        model=model,
        temperature=temperature,
        max_output_tokens = max_output_tokens,
    )

if __name__ == '__main__':
    main()