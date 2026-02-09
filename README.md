# Simple AI Chatbot (Bravestone)

A FastAPI-based medical assistant chatbot designed to guide users through a structured 8-step health consultation conversation. The bot acts as "Bravestone" (aka Meera), a warm and intelligent assistant from a general practice clinic.

## 🚀 Features

- **Structured Conversation Flow**: Guides users through an 8-step process from introduction to appointment scheduling.
    1.  Introduction
    2.  Patient Qualification
    3.  Service Overview
    4.  Needs Assessment (with emergency detection)
    5.  Care Recommendation
    6.  Address Concerns
    7.  Next Steps (Scheduling)
    8.  Conversation Close
- **Intelligent Step Detection**: Uses an LLM (GPT-4o-mini) to dynamically determine the appropriate conversation step based on user input.
- **Emergency Handling**: Automatically detects critical symptoms and prioritizes emergency protocols.
- **Input Validation**: Validates Indian mobile numbers (10 digits).
- **Tech Stack**:
    - [FastAPI](https://fastapi.tiangolo.com/) - Web framework
    - [Agno](https://github.com/agno-agi/agno) - Agent framework
    - [OpenAI](https://openai.com/) - LLM provider (GPT-4o-mini)

## 🛠️ Prerequisites

- Python 3.10+
- OpenAI API Key

## 📦 Installation

1.  **Clone the repository**
    ```bash
    git clone <repository-url>
    cd SimpleAgnoChatbot
    ```

2.  **Create a virtual environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables**
    Create a `.env` file in the root directory:
    ```env
    OPENAI_API_KEY=your_openai_api_key
    API_URL=https://your-external-api-endpoint.com  # For phone number submission
    DEBUG=1  # Optional, for debug mode
    ```

## 🚀 Usage

### Running Locally

You can run the server using `uvicorn` directly or the provided start script.

**Using start script:**
```bash
chmod +x start.sh
./start.sh
```

**Using Uvicorn directly:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 2090 --reload
```

The server will start at `http://0.0.0.0:2090`.

### Running with Docker

1.  **Build the image**
    ```bash
    docker-compose build
    ```

2.  **Run the container**
    ```bash
    docker-compose up -d
    ```
    The Docker container runs on port `2096` by default (as configured in `docker-compose.yaml` and `Dockerfile`).

## 📡 API Endpoints

-   `GET /gp-bot/init?uuid=<user_id>`
    -   Initializes the conversation for a user.
    -   Returns the first greeting.

-   `POST /gp-bot`
    -   **Form Data**:
        -   `uuid`: User ID
        -   `body`: User's message
    -   Returns the agent's response and current step.

## 📂 Project Structure

```
├── app/
│   ├── agent/          # Agent logic (health_agent.py)
│   ├── db/             # Database models (currently unused in main flow)
│   ├── main.py         # FastAPI entry point
│   ├── prompts.py      # Prompt templates and step definitions
│   └── memory.py       # Memory management
├── Dockerfile
├── docker-compose.yaml
├── requirements.txt
└── start.sh
```
