import streamlit as st
import openai
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import tempfile

st.title("🚀 AI Deployment Playbook Generator")
st.write("Generate a customized AI deployment guide based on your industry, model type, and MLOps stack.")

# Debugging Statement: Check if App is Running
st.write("✅ App is running!")

# User Inputs
industry = st.selectbox("Select Your Industry:", ["Healthcare", "Finance", "Retail", "Technology", "Manufacturing"])
model_type = st.selectbox("Select Model Type:", ["Large Language Model (LLM)", "Computer Vision", "Tabular Data", "Time Series"])
compliance = st.multiselect("Compliance Requirements:", ["GDPR", "HIPAA", "EU AI Act", "NIST", "ISO 42001"])
mlops_stack = st.selectbox("MLOps Stack:", ["AWS SageMaker", "Azure ML", "GCP Vertex AI", "Databricks", "On-Prem"])

st.write("✅ User inputs loaded!")  # Debugging statement

def generate_playbook(industry, model_type, compliance, mlops_stack):
    compliance_str = ", ".join(compliance) if compliance else "General Best Practices"

    prompt = f"""
    Generate a well-structured AI Deployment Playbook for an organization in the {industry} industry.
    
    **Key Information**:
    - **Model Type:** {model_type}
    - **MLOps Stack:** {mlops_stack}
    - **Compliance Requirements:** {compliance_str}

    The playbook should include:
    - **Deployment Pipeline** (Development → Testing → Production)
    - **Best Practices for Scaling AI**
    - **Monitoring & Risk Mitigation** (Bias detection, model drift, security)
    - **Compliance & Security Recommendations**
    - **MLOps Architecture Overview** (Diagrams and tools)

    Format the response using **Markdown** for readability.
    """

    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert in AI deployment and governance."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ OpenAI API Error: {e}"

def generate_pdf(playbook_text):
    """Create a PDF from the generated playbook."""
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf_path = temp_file.name
    
    c = canvas.Canvas(pdf_path, pagesize=letter)
    c.setFont("Helvetica", 12)

    y_position = 750  # Start position on the page

    for line in playbook_text.split("\n"):
        c.drawString(50, y_position, line)
        y_position -= 20  # Move down for the next line
        if y_position < 50:  # Create new page if needed
            c.showPage()
            c.setFont("Helvetica", 12)
            y_position = 750

    c.save()
    return pdf_path

if st.button("Generate Playbook"):
    with st.spinner("Generating AI Deployment Playbook..."):
        playbook = generate_playbook(industry, model_type, compliance, mlops_stack)

    if playbook:
        # Display Playbook
        st.markdown("## 📄 AI Deployment Playbook")
        st.text_area("Generated Playbook:", playbook, height=400)

        # Generate PDF
        pdf_path = generate_pdf(playbook)

        # Provide PDF download button
        with open(pdf_path, "rb") as pdf_file:
            st.download_button(
                label="📥 Download as PDF",
                data=pdf_file,
                file_name="AI_Deployment_Playbook.pdf",
                mime="application/pdf"
            )


st.write("✅ App successfully loaded!")  # Debugging statement
