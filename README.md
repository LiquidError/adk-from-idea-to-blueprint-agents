<div align="center">
  <img src="../banner.png" alt="Project Banner: AI Agents Built My Product Plan! (Google ADK - PRD and product lifecycle Automation)" width="600"/>
</div>

# AI Agents Built My Product Plan! (Google ADK - PRD and product lifecycle Automation)

[![YouTube Channel](https://img.shields.io/badge/YouTube-%40TonyAlfredsson-red?style=flat-square&logo=youtube)](https://www.youtube.com/@TonyAlfredsson)

Welcome to the **Idea-to-Blueprint-Pipeline (ITBP) Agent** project! This repository showcases a powerful AI agent system built using Google's Agent Development Kit (ADK) that transforms product ideas into comprehensive project blueprints through a structured, phase-based workflow.

This project serves as a practical example and is featured in a YouTube video titled "AI Agents Built My Product Plan! (Google ADK - PRD and product lifecycle Automation)" on the [@TonyAlfredsson YouTube channel](https://youtu.be/oD_zK1modBA). Follow along to see how it was built and how it can be extended!

## ✨ Introduction

This agent system demonstrates how to create a comprehensive product development pipeline using ADK-based agents. It provides a structured workflow that guides users through the entire process of transforming an idea into a detailed implementation plan:

* Brainstorm and refine initial product concepts
* Conduct market and technical research
* Create structured project briefs
* Define detailed product requirements and epics
* Design technical architecture
* Validate the plan from a product perspective
* Generate detailed user stories for implementation

Built entirely with the Google ADK framework, it uses a team of specialist agents (Analyst, PM, Architect, PO/SM) coordinated by a central orchestrator to guide users through each phase of the product development lifecycle.

## 🚀 Features

* **Idea Exploration:** Brainstorm and refine product concepts with AI assistance
* **Market Research:** Conduct research on concepts and market opportunities
* **Project Brief Creation:** Transform ideas into structured project briefs
* **PRD Generation:** Create comprehensive Product Requirements Documents
* **Epic Definition:** Structure work into logical epics with clear requirements
* **Architecture Design:** Design technical architecture based on requirements
* **Plan Validation:** Validate the plan from a product perspective
* **User Story Generation:** Create detailed user stories for implementation
* **ADK Integration:** Built entirely within the Google Agent Development Kit framework
* **Phase-Based Workflow:** Structured process with clear transitions between phases
* **Specialist Agents:** Team of expert agents with specific roles and responsibilities

## 🛠️ How It Works

The `itbp_agent` acts as an orchestrator, coordinating a team of specialist agents through a phase-based workflow:

1. **Analyst Agent:** Facilitates brainstorming, conducts research, and creates project briefs
2. **PM Agent:** Defines product requirements and structures work into epics
3. **Architect Agent:** Designs technical architecture based on requirements
4. **PO/SM Agent:** Validates the plan and generates user stories

The workflow follows these phases:
1. **GET_IDEA** - Collect the initial product/project idea from the user
2. **ANALYST_BRAINSTORM** - Explore and refine the idea
3. **ANALYST_RESEARCH** - Conduct market and technical research
4. **ANALYST_BRIEF** - Create a structured Project Brief
5. **PM_DEFINE** - Define product requirements and structure work into Epics
6. **ARCHITECT_DESIGN** - Design technical architecture
7. **POSM_VALIDATE** - Validate the plan from a product perspective
8. **POSM_STORIES** - Generate detailed user stories
9. **FINISHED** - Complete the blueprint process

## 💻 Technology Stack

* **Framework:** Google Agent Development Kit (ADK)
* **Language:** Python 3.x
* **LLMs:** Google Gemini 2.5 Pro (via `google-genai` library)
* **Core Libraries:** `google-adk`, `google-genai`
* **Package Management:** `uv` (recommended) or `pip`

## ⚙️ Setup & Installation

Follow these steps to get the agent running on your local machine.

**1. Clone the Repository**

```bash
git clone https://github.com/LiquidError/adk-from-idea-to-blueprint-agents
cd adk-from-idea-to-blueprint-agents
```

**2. Configure API Keys**

This project requires API keys for Google (for agent control and LLM access) and Tavily (for the deep research tool).

* Copy the example environment file:
    ```bash
    cp .env.example .env
    ```
* Edit the `.env` file and add your actual API keys:
    ```dotenv
    GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY_HERE"
    TAVILY_API_KEY="YOUR_TAVILY_API_KEY_HERE"
    ```
* You can get a Google API key from [Google Cloud Console](https://console.cloud.google.com/) or [Goggle AI Studio](https://aistudio.google.com/apikey)
    
* You can get a Tavily API key from [Tavily's documentation](https://docs.tavily.com/documentation/quickstart)

**3. Set Up a Virtual Environment**

It's highly recommended to use a virtual environment.

* **Using `uv` (Recommended)**
    * Install `uv` if needed (see [official `uv` documentation](https://github.com/astral-sh/uv#installation)).
    * Create and activate the virtual environment:
        ```bash
        uv venv
        source .venv/bin/activate # (or .venv\Scripts\activate on Windows)
        ```
* **Using Python's built-in `venv`**
    * Create and activate the virtual environment:
        ```bash
        # On macOS/Linux:
        python3 -m venv .venv && source .venv/bin/activate
        # On Windows:
        python -m venv .venv && .venv\Scripts\activate
        ```

**4. Install Dependencies**

* **Using `uv` (Recommended):**
    ```bash
    uv sync
    ```
* **Using `pip`:**
    ```bash
    pip install -r requirements.txt
    ```

## ▶️ Running the Agent

You can interact with the agent using the ADK CLI:

**1. Interactive Web UI (`adk web`)**

This is the easiest way to test.

```bash
adk web --port=8080 ./v1/agents/
```

Navigate to `http://localhost:8080` in your browser. Select the `itbp_agent`. You can then:
* Start by providing your product idea
* Follow the guided workflow through each phase
* Review and provide feedback on outputs at each stage
* Receive a comprehensive project blueprint at the end

## ⚠️ Known Limitations

* **No Artifact Storage:** This version does not produce persistent artifacts. All output text needs to be copied and pasted into another document for preservation.
* **API Timeouts:** Some timeouts in long and complex queries might occur due to rate limits or an overloaded API, especially when using the deep research tool.
* **Research Tool Dependencies:** The deep research functionality requires a valid Tavily API key to work properly.

## 📺 YouTube Video & Inspiration

This project is featured in a YouTube video titled "AI Agents Built My Product Plan! (Google ADK - PRD and product lifecycle Automation)".

* **Watch:** [youtube.com/@TonyAlfredsson](https://www.youtube.com/@TonyAlfredsson)
* **Inspired by:**
  * [BMadCode](https://www.youtube.com/@BMadCode) - Innovative AI methodologies
  * [BMAD METHOD](https://github.com/bmadcode/BMAD-METHOD) - Structured approach to AI development
  * [AI with Brandon](https://www.youtube.com/@aiwithbrandon) - Practical AI applications

## 🔗 References

* **Google Agent Development Kit (ADK) Documentation:** [google.github.io/adk-docs](https://google.github.io/adk-docs)
* **UV Documentation:** [astral.sh/uv](https://astral.sh/uv)

## 📜 License

This project is licensed under the Apache License 2.0. See the [LICENSE](../LICENSE) file for details.

## 🤝 Contributing & Feedback

Contributions are welcome! Please feel free to open an issue or submit a pull request.

Feedback and suggestions are also encouraged! Please leave comments on the YouTube videos or open an issue in this repository.
