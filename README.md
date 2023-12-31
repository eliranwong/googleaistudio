# Google AI Studio

A collection of AI tools built on Google Vertex AI APIs. It works even in EU / UK.

At the time of writing, web-based Google AI Studio is not accessible in [EU / UK / some other regions](https://ai.google.dev/available_regions#available_regions).  As this python package is based on Google Vertex AI APIs, there is no such restriction.

Current available features:

* geminipro - a multiturn chat bot built on Google [Gemini Pro & Gemini Pro Vision](https://cloud.google.com/vertex-ai/docs/generative-ai/multimodal/overview) (LLM: Gemini Pro)

* palm2 - a multiturn chat bot built on Google [PaLM 2](https://cloud.google.com/vertex-ai/docs/generative-ai/language-model-overview) (LLM: chat-bison-32k)

* codey - a multiturn chat bot built on [Codey](https://cloud.google.com/vertex-ai/docs/generative-ai/code/code-models-overview) (LLM: codechat-bison-32k)

These are part of integrated tools, developed in our [LetMeDoIt AI project](https://github.com/eliranwong/letmedoit).

# Screenshot

<img width="1440" alt="geminipro_palm2" src="https://github.com/eliranwong/letmedoit/assets/25262722/dc6f874e-ae11-4514-9ed0-3d22f2b1985c">

# Install or Upgrade

> pip install --upgrade googleaistudio

# Google API Setup

Save a copy of your API key JSON file as "\~/googleaistudio/credentials_googleaistudio.json", where "\~" denotes your home directory.

Read https://github.com/eliranwong/letmedoit/wiki/Google-API-Setup for setting up Google API.

# Usage

Run in terminal:

> geminipro

> geminiprovision

> palm2

> codey

# CLI options

> geminipro -h

> geminipro -t 0.5 -o 1024 "Hello!"

> geminiprovision -h

> geminiprovision -f image.png -t 0.5 -o 1024 "Describe this image file"

> palm2 -h

> palm2 -m "chat-bison" -t 0.5 -o 1024 "Hello!"

> codey -h

> codey -m "codechat-bison" -t 0.5 -o 1024 "How to use decorators in python?"

# Integration in LetMeDoIt AI project

https://github.com/eliranwong/letmedoit/wiki/Integration-with-Google-AI-Tools

# Documentation for Developers

https://cloud.google.com/vertex-ai/docs/generative-ai/learn/overview

https://cloud.google.com/vertex-ai/docs/generative-ai/learn/models

https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/overview

https://cloud.google.com/vertex-ai/docs/generative-ai/sdk-for-llm/llm-sdk-overview

https://cloud.google.com/vertex-ai/docs/generative-ai/multimodal/function-calling

https://spec.openapis.org/oas/v3.0.3#schema

