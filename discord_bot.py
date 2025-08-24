
import discord
import os
from app import create_local_rag_chain, chat_whit_document

# It is recommended to run the document ingestion process first
# to have the local vector base ready.
# python app.py your-document.pdf

# Get Discord token from environment variable
# For security reasons, do not hardcode the token in the code.
# You can set the environment variable in your terminal like this:
# export DISCORD_TOKEN='your_discord_token_here'
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

if not DISCORD_TOKEN:
    print("Error: The DISCORD_TOKEN environment variable is not set.")
    print("Please set it with your Discord bot token.")
    exit()

# Create RAG chain
# This assumes that the vector store has already been created by running app.py
try:
    rag_chain = create_local_rag_chain()
    print("RAG chain created successfully.")
except Exception as e:
    print(f"Error creating RAG chain: {e}")
    print("Please make sure you have ingested a document first by running: python app.py <path_to_pdf>")
    exit()

# Configure Discord client
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    print('The bot is ready to answer questions.')

@client.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == client.user:
        return

    # The bot will only respond to messages that start with '!ask'
    if message.content.startswith('!ask'):
        question = message.content[5:].strip()

        if not question:
            await message.channel.send("Please ask a question after the `!ask` command.")
            return

        # Show that the bot is "thinking"
        async with message.channel.typing():
            print(f"Received question from {message.author}: {question}")
            # Process the question using the RAG chain
            try:
                result = chat_whit_document(rag_chain, question)
                answer = result.get("answer", "No answer found.")

                # Add sources to the answer
                if result.get("context"):
                    sources = "

**Sources:**
"
                    for i, doc in enumerate(result["context"], 1):
                        page_num = doc.metadata.get("page")
                        sources += f"{i}. Page {page_num + 1 if isinstance(page_num, int) else '?'} of document
"
                    answer += sources

                # The answer can be long, so it is sent in parts if it exceeds the Discord limit.
                if len(answer) > 2000:
                    # Split the message into chunks of 2000 characters
                    for chunk in [answer[i:i + 2000] for i in range(0, len(answer), 2000)]:
                        await message.channel.send(chunk)
                else:
                    await message.channel.send(answer)

            except Exception as e:
                print(f"Error processing question: {e}")
                await message.channel.send("An error occurred while processing your question. Please try again later.")

def main():
    print("Starting Discord bot...")
    client.run(DISCORD_TOKEN)

if __name__ == "__main__":
    main()
