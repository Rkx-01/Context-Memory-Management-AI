# 🧠 Context and Memory Management for AI Agents

This repository contains the architecture design and a working prototype for a **Context and Memory Management System** designed for enterprise AI Agents.

The system demonstrates how an AI agent can effectively maintain, retrieve, and utilize contextual information (similar to experienced human professionals) without suffering from cognitive overload or context-window limits.

---

## 🏗️ Architecture Design

The foundational design document is located in [`architecture.md`](./architecture.md). It addresses four core problem statements:
1. **Memory Types & Structure**: Categorizing Immediate, Historical, Temporal, and Experiential memory using a Hybrid Knowledge Graph.
2. **Context Hierarchy**: A mathematical Proximity Score ($P_{total}$) that combines Temporal decay, Relational distance, and Semantic similarity.
3. **Lifecycle Management**: Exponential decay equations that age out time-sensitive facts while preserving "evergreen" organizational rules.
4. **Retrieval Mechanisms**: Multi-stage filtering to prevent LLM information overload while maintaining deep context.

---

## 💻 Python Prototype & UI Dashboard

A working prototype of the ranking algorithm and memory manager is implemented in Python, paired with a modern Streamlit dashboard to visually demonstrate the scenarios.

### ⚙️ How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Rkx-01/Context-Memory-Management-AI.git
   cd Context-Memory-Management-AI
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the visual dashboard:**
   ```bash
   python3 -m streamlit run src/app.py
   ```

### 🧪 Scenarios Simulated

The application comes pre-loaded with two specific business scenarios demonstrating the Memory Engine:

* **Scenario 1: Invoice Processing QA**
  * Demonstrates the system retrieving a 4-month-old severe quality breach while successfully applying decay to an older, less important payment dispute. It also pulls in an active "evergreen" seasonal warning.
* **Scenario 2: Support Escalation Triage**
  * Demonstrates the system identifying churn risk by retrieving a recent contract renewal mentioning competitors, and utilizing evergreen stakeholder preferences to alter the AI's response strategy.
