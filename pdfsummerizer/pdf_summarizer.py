import os
import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader

def main():
    # Set your Gemini API key directly here
    api_key = 'AIzaSyDCI_xeL7HhthSwbGNEkbas6fgAaRZhR2s'
    genai.configure(api_key=api_key)

    # Set up the Streamlit interface
    st.title("PDF Summarizer")

    # File uploader for PDF
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if uploaded_file is not None:
        # Read the PDF content
        reader = PdfReader(uploaded_file)
        pdf_text = ""
        for page in reader.pages:
            pdf_text += page.extract_text()

        if st.button("Generate Summary"):
            if pdf_text.strip():
                # Create a prompt for summarizing the PDF content
                prompt = f"""
                Please summarize the following PDF content:

                "{pdf_text}"

                The summary should highlight the key points and main ideas.
                """

                try:
                    # Use the Gemini generative model to generate the summary
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    response = model.generate_content(prompt)
                    summary = response.text

                    # Store the generated summary in the session state to keep it persistent
                    st.session_state.generated_summary = summary
                    st.session_state.copy_status = "Copy Summary to Clipboard"  # Reset the copy button text

                except Exception as e:
                    st.error(f"An error occurred: {e}")
                    st.warning("We couldn't generate the summary. Please try again later.")
            else:
                st.warning("The PDF content is empty.")

    # Check if the generated summary is in session state
    if 'generated_summary' in st.session_state:
        st.subheader("Your Generated Summary:")
        summary_text_area = st.text_area("Generated Summary:", st.session_state.generated_summary, height=400, key="summary_content")

        # Button to copy summary to clipboard
        copy_button = st.button(st.session_state.get('copy_status', "Copy Summary to Clipboard"), key="copy_button")

        if copy_button:
            # JavaScript code to copy the text and change button text
            st.write(f"""
                <script>
                function copyToClipboard() {{
                    var summaryContent = document.querySelector('#summary_content');
                    var range = document.createRange();
                    range.selectNode(summaryContent);
                    window.getSelection().removeAllRanges();  // Clear current selection
                    window.getSelection().addRange(range);  // Select the content
                    document.execCommand('copy');  // Copy the selected content
                    window.getSelection().removeAllRanges();  // Clear selection
                    document.getElementById('copy_button').innerText = 'COPIED';
                }}
                copyToClipboard();
                </script>
                """, unsafe_allow_html=True)
            st.session_state.copy_status = "COPIED"  # Update the button text to "COPIED"

if __name__ == "__main__":
    main()
