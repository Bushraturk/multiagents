# MultiAgent AI Tutor

A Chainlit-based conversational AI tutoring system that uses multiple specialized agents to teach different subjects.

## Features

- 🤖 Multiple specialized AI tutors:
  - English Language Tutor
  - Python Programming Tutor
  - OpenAI SDK Tutor
- 🔄 Dynamic conversation routing
- 🌐 Built with Gemini AI model
- 💻 Simple and clean web interface

## Prerequisites

- Python 3.7+
- Gemini API key

## Installation

1. Clone the repository
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory and add your Gemini API key:
```env
GEMINI_API_KEY=your_api_key_here
```

## Usage

1. Start the application:
```bash
chainlit run main.py
```

2. Open your web browser and navigate to the provided local URL (typically http://localhost:8000)

3. Choose a subject you want to learn:
   - English
   - Python
   - OpenAI SDK

4. Interact with the specialized tutor for your chosen subject

## Project Structure

- `main.py` - Main application file containing agent definitions and message handling
- `requirements.txt` - Project dependencies
- `.env` - Environment variables (API keys)
- `chainlit.md` - Chainlit configuration
- `Procfile` - Deployment configuration for platforms like Railway

## Tech Stack

- [Chainlit](https://chainlit.io/) - For building conversational AI applications
- [OpenAI Agents](https://github.com/openai/openai-agents) - For agent management
- [Google Generative AI](https://cloud.google.com/generative-ai) - Gemini model for responses
- [Python-dotenv](https://pypi.org/project/python-dotenv/) - For environment variable management

## Deployment

The project is configured for deployment on Railway. Use the provided `Procfile` and `railway.json` for deployment settings.

## License

This project is open source and available under the MIT License.
