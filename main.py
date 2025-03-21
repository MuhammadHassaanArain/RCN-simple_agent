import os
from dotenv import load_dotenv
import chainlit as cl
from agents import Agent, Runner,AsyncOpenAI,OpenAIChatCompletionsModel

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

provider = AsyncOpenAI(
    api_key = gemini_api_key,
    base_url = "https://generativelanguage.googleapis.com/v1beta/openai"
)
model = OpenAIChatCompletionsModel(
    model = "gemini-2.0-flash",
    openai_client = provider
)

agent = Agent(
    name = "Greeting Agent",
    instructions="""you are a helpful assistat that talks to single 
    perosns as their girlfriend or boyfriend according to their gender after
      asking to the user and flirting with them""",
    model = model
)
# user_input = input("Enter your Message here:(type 'exit' to quit) ")

# if user_input == "exit":
#     print("Exiting the program...")
# else:
#     while user_input.lower() != "exit":
#         result = Runner.run_sync(agent, user_input)
#         print(result.final_output)
#         user_input = input("Enter your Message here:(type 'exit' to quit) ")

@cl.on_message
async def handle_message(message: cl.Message):
    """Handles user messages in Chainlit."""
    user_input = message.content  # Get user input
    result = await Runner.run(agent, user_input)  # Run the agent asynchronously
    await cl.Message(content=result.final_output).send()  # Send the response