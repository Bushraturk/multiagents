import chainlit as cl
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig
from dotenv import load_dotenv
import os

# ---------------------------------------------
# Text-only Chainlit app (no voice/audio code)
# - Whisper (STT) and gTTS (TTS) removed
# - Simple multi-agent tutor flow
# - Safe to deploy locally or on PaaS
# ---------------------------------------------

# Load API key from .env
load_dotenv()
gemini_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini via OpenAI-compatible client
external_client = AsyncOpenAI(
    api_key=gemini_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

# -----------------
# Agent definitions
# -----------------
manager_agent = Agent(
    name="Manager",
    instructions="""
You are the Manager. Greet the user and ask what they want to learn: English, Python, or OpenAI SDK.
Then hand off the request to the correct assistant agent.
if question is iralivent say is not my work pliatlli
"""
)

english_agent = Agent(
    name="EnglishAgent",
    instructions="You are an English teacher. Teach grammar and vocabulary simply. Encourage the user to answer questions."
)

python_agent = Agent(
    name="PythonAgent",
    instructions="You are a Python tutor. Teach basic Python syntax like print, variables, loops, and give small quizzes."
)

sdk_agent = Agent(
    name="SDKAgent",
    instructions="You teach how to use OpenAI SDK in Python. Explain functions like openai.ChatCompletion.create()."
)

# ---------------
# Simple session state
# ---------------
user_state = {}

@cl.on_chat_start
async def start():
    """
    On chat start, we begin in 'manager' stage and prompt the user to choose a topic.
    """
    user_state["stage"] = "manager"
    await cl.Message(
        "👋 Hello! I am your AI Tutor Manager.\nWhat do you want to learn?\n👉 English\n👉 Python\n👉 OpenAI SDK"
    ).send()

@cl.on_message
async def handle(message: cl.Message):
    """
    Text-only message handler:
    - No audio upload handling
    - No TTS audio response
    - Routes messages to the correct sub-agent based on the current stage
    """
    text = (message.content or "").strip().lower()

    # First choose domain
    if user_state.get("stage") == "manager":
        if "english" in text:
            user_state["stage"] = "english"
            reply = Runner.run(english_agent, input="Start the English lesson", run_config=config)
        elif "python" in text:
            user_state["stage"] = "python"
            reply = Runner.run(python_agent, input="Start the Python lesson", run_config=config)
        elif "sdk" in text or "openai" in text:
            user_state["stage"] = "sdk"
            reply = Runner.run(sdk_agent, input="Start the OpenAI SDK lesson", run_config=config)
        else:
            reply = "Please choose: English, Python, or OpenAI SDK."
    else:
        # If already in a lesson, route to sub-agent
        stage = user_state.get("stage")
        if stage == "english":
            reply = Runner.run(english_agent, input=text, run_config=config)
        elif stage == "python":
            reply = Runner.run(python_agent, input=text, run_config=config)
        elif stage == "sdk":
            reply = Runner.run(sdk_agent, input=text, run_config=config)
        else:
            reply = "Something went wrong. Please restart."

    # Send simple text reply
    # Send simple text reply
    out = None
    if hasattr(reply, "final_output"):
        fo = reply.final_output
        out = fo if isinstance(fo, str) else (fo.get("content", "") if isinstance(fo, dict) else str(fo))
    else:
        out = reply if isinstance(reply, str) else str(reply)
    await cl.Message(content=out).send()
