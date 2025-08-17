# Document Parsing Solutions 📄

A comprehensive toolkit for extracting and processing content from PDF documents using various parsing technologies.

## Overview

This project implements five different document parsing approaches:
- Unstructured.io API
- Llama Parse
- Mistral OCR
- Azure Document Intelligence
- Amazon Textract

## Parser Comparison

### 1. Unstructured.io API
**Strengths:**
- Excellent at handling complex document layouts
- Advanced table extraction capabilities
- Maintains document structure and formatting
- Supports multiple document formats

**Limitations:**
- API rate limits on free tier
- Higher latency due to cloud processing
- Cost increases with document volume

**Best For:**
- Complex documents with mixed content
- Documents with tables and structured data
- Batch processing requirements

### 2. Llama Parse
**Strengths:**
- Strong text extraction capabilities
- Good handling of simple layouts
- Local processing option available
- Efficient for text-heavy documents

**Limitations:**
- Limited table extraction capabilities
- May struggle with complex layouts
- Requires more computational resources locally

**Best For:**
- Text-heavy documents
- Simple document layouts
- Local processing requirements

### 3. Mistral OCR
**Strengths:**
- Excellent OCR accuracy
- Good language support
- Handles handwritten text well
- Real-time processing capabilities

**Limitations:**
- Limited formatting preservation
- May struggle with complex tables
- Higher cost for high-volume processing

**Best For:**
- Documents with handwritten content
- Multi-language documents
- Real-time OCR requirements

### 4. Azure Document Intelligence
**Strengths:**
- Advanced AI-powered extraction
- Excellent form field recognition
- Strong table extraction
- Built-in pretraining for common documents

**Limitations:**
- Azure platform lock-in
- Higher cost for large-scale processing
- Requires Azure subscription

**Best For:**
- Forms and structured documents
- Enterprise-scale deployments
- Integration with Azure services

### 5. Amazon Textract
**Strengths:**
- Excellent table extraction
- Good form field recognition
- Scales well for large volumes
- Strong integration with AWS

**Limitations:**
- AWS platform lock-in
- Cost can be high for large volumes
- Limited customization options

**Best For:**
- AWS ecosystem integration
- Large-scale document processing
- Forms and table extraction

## 🔧 Setup

### 1. API Keys and Credentials

#### Unstructured.io
- Sign up at [Unstructured.io](https://unstructured.io)
- Obtain API key from dashboard

#### Llama Parse
- Sign up at [Llama Cloud](https://cloud.llamaindex.ai/login)
- Generate API key from dashboard

#### Mistral API
- Visit [Mistral AI](https://mistral.ai/)
- Create account and generate API key

#### Azure Document Intelligence
- Create resource in [Azure Portal](https://portal.azure.com/)
- Get endpoint URL and API key from resource settings

#### Amazon Textract
- Set up AWS account
- Create IAM user with Textract permissions
- Get AWS access key and secret

### 2. Environment Setup

1. **Install Dependencies**
```bash
python -m venv venv
source venv/bin/activate  # For Mac/Linux
pip install -r requirements.txt
```

2. **Configure Environment Variables**
Create a `.env` file:
```ini
# Unstructured.io
UNSTRUCTURED_API_KEY=your_key

# Llama Parse
LLAMA_API_KEY=your_key

# Mistral
MISTRAL_API_KEY=your_key

# Azure
AZURE_ENDPOINT=your_endpoint
AZURE_API_KEY=your_key

# AWS
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=your_region
```

## Usage Guidelines

### Document Type Selection

1. **Simple Text Documents**
   - Recommended: Llama Parse or Unstructured.io
   - Alternative: Mistral OCR

2. **Forms and Structured Documents**
   - Recommended: Azure Document Intelligence or Amazon Textract
   - Alternative: Unstructured.io

3. **Complex Tables**
   - Recommended: Amazon Textract or Azure Document Intelligence
   - Alternative: Unstructured.io

4. **Handwritten Content**
   - Recommended: Mistral OCR
   - Alternative: Azure Document Intelligence

5. **Multi-Language Documents**
   - Recommended: Mistral OCR or Azure Document Intelligence
   - Alternative: Amazon Textract

## Contributing

Contributions are welcome! Please read our contributing guidelines and submit pull requests to our repository.