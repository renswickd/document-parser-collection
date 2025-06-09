## 🔧 Setup: Llama Cloud API, Mistral, and Azure Document Intelligence

### 1. Get Your API Keys
#### Llama Cloud API
- 🔑 **Get Your API Key**:
  - Sign up or log in to [Llama Cloud](https://cloud.llamaindex.ai/login).
  - Navigate to your dashboard and securely copy your API key.

#### Mistral API
- 🔑 **Get Your API Key**:
  - Visit the [Mistral API Documentation](https://mistral.ai/) and sign up for an account.
  - Generate an API key from your account dashboard and securely store it.

#### Azure Document Intelligence
- 🔑 **Set Up Azure Document Intelligence**:
  - Log in to the [Azure Portal](https://portal.azure.com/).
  - Create a **Cognitive Services** resource and enable **Azure Document Intelligence** (formerly known as Form Recognizer).
  - Navigate to the **Keys and Endpoint** section of your resource and copy the following:
    - **Endpoint URL**
    - **API Key**

---

### 2. Install Required Software
Ensure you have the following software installed on your system:
- **Python 3.8+**: Download and install from [python.org](https://www.python.org/downloads/).
- **Git**: Download and install from [git-scm.com](https://git-scm.com/).
- **Docker** (optional, for containerized deployments): Download and install from [docker.com](https://www.docker.com/).

---

### 3. Clone the Repository
Clone this repository to your local machine:
```bash
git clone https://github.com/your-username/document-parsing.git
cd document-parsing
```

---