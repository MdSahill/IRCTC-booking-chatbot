# IRCTC AI Booking Assistant 🚆
### An AI-powered chatbot for train ticket booking with email notifications and calendar integration.

## 🌟 Features
-Natural language train search & booking<br>
-Secure user authentication<br>
-Email confirmations via Gmail<br>
-Google Calendar reminders<br>
-Responsive web interface<br>

## 🛠️ End-to-End Pipeline
![deepseek_mermaid_20250507_e332c0](https://github.com/user-attachments/assets/3499626d-08a3-46b3-9ebe-d00ed86e9315)
### Pipeline Stages:
#### 1.Input Processing:

-LangChain routes user queries<br>
-GPT-3.5 extracts entities (dates/stations)
#### 2.Backend Operations:
1. Validate input<br>
2. Call IRCTC API <br>
3. Trigger email/calendar tools<br>
4. Return confirmation
#### 3.Notification System:
-Composio handles Gmail/Calendar APIs<br>
-Async execution for reliability
## 🧠 Model Architecture
![deepseek_mermaid_20250507_c38485](https://github.com/user-attachments/assets/c987fc25-72fd-48dd-af36-b79a558ac511)
### Key Components:
| Component       | Technology |        
|-----------------|------------|
| **NLU Engine**  | OpenAI GPT-3.5 |
| **Tool Agent**  | LangChain |
| **Auth System** | Flask-Login |
| **Notification**| Composio |

## 🚀 Setup Guide
#### 1. Install dependencies:
```python
pip install -r requirements.txt
```
#### 2. Configure .env:
```python
OPENAI_API_KEY=your_key
IRCTC_API_KEY=rapidapi_key
COMPOSIO_API_KEY=your_composio_key
```
#### 3. Run the app:
```python
python app.py
```
