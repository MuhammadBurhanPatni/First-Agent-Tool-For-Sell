import streamlit as st
from agents import Agent, Runner
from config import config
import asyncio
from pdf_generator import generate_pdf

# Page settings
st.set_page_config(page_title="AI Proposal Agent", page_icon="🤖")

st.title("🤖 Freelance Proposal Generator")
st.markdown("Generate professional freelance proposals using AI!")

# Define the agent
agent = Agent(
    name="Proposal Agent",
    instructions=(
        "You are a helpful assistant that writes high-quality freelance proposals "
        "based on the user's skill, job description, and preferred tone."
    )
)

# Form input
with st.form("proposal_form"):
    st.subheader("📋 Job Details")
    skill = st.text_input("Your Skill", placeholder="e.g., Web Developer")
    job_desc = st.text_area("Job Description", placeholder="Paste job details here...")
    tone = st.selectbox("Tone of Proposal", ["Professional", "Friendly", "Persuasive", "Formal"])
    submit = st.form_submit_button("🔮 Generate Proposal")

if submit:
    if not skill or not job_desc:
        st.warning("⚠️ Please fill in all fields.")
    else:
        with st.spinner("Generating your proposal..."):
            prompt = f"""
            Skill: {skill}
            Job Description: {job_desc}
            Tone: {tone}

            Write a freelance proposal using the above information. 
            Be persuasive, professional, show understanding of the project, and include a call to action.
            """
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

                result = loop.run_until_complete(
                        Runner.run(starting_agent=agent, input=prompt, run_config=config)
                    )
                st.success("✅ Proposal Generated!")
                st.text_area("📝 Your AI-Generated Proposal", result.final_output, height=300)
                # PDF download
                pdf_bytes = generate_pdf(result.final_output)
                st.download_button("📄 Download as PDF", data=pdf_bytes, file_name="proposal.pdf", mime="application/pdf")

                # Download button
                st.download_button("⬇️ Download Proposal", result.final_output, file_name="proposal.txt")

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# Footer branding
st.markdown("---")
st.markdown("Made with ❤️ by Burhan using OpenAI Agent SDK")

