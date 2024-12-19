# How To Use qa_agent ?

Run the agent:
```
python qa_agent.py --url https://help.slack.com --api-key YOUR_GOOGLE_API_KEY
```
Ask questions interactively:

```
> What is Slack?
[Agent responds with information about Slack]

> How do I create a channel?
[Agent provides instructions]

> quit
[Agent exits]
```
Also ensure you have all required packages installed:

```
pip install langchain-google-genai langchain-community chromadb pandas beautifulsoup4 requests
```
