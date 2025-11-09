import streamlit as st
from models.llm import get_llm
from models.embeddings import get_embedding_model
from utils.pdf_processor import process_pdf, extract_text_from_pdf
from utils.rag_engine import get_rag_engine
from utils.web_search import search_web, format_search_results
from utils.esg_scorer import calculate_overall_esg_score, generate_score_summary, analyze_esg_gaps
from config.config import CONCISE_MAX_TOKENS, DETAILED_MAX_TOKENS
import time

# Page configuration
st.set_page_config(
    page_title="ESG Risk Intelligence Assistant",
    page_icon="🌱",
    layout="wide"
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "rag_ready" not in st.session_state:
    st.session_state.rag_ready = False
if "uploaded_file_name" not in st.session_state:
    st.session_state.uploaded_file_name = None
if "full_text" not in st.session_state:
    st.session_state.full_text = None
if "esg_score" not in st.session_state:
    st.session_state.esg_score = None

# Sidebar
with st.sidebar:
    st.title("⚙️ Configuration")
    
    # LLM Provider selection
    llm_provider = st.selectbox(
        "Select LLM Provider",
        ["groq"],
        help="Choose your LLM provider (Groq is free!)"
    )
    
    # Response mode
    response_mode = st.radio(
        "Response Mode",
        ["Concise", "Detailed"],
        help="Concise: Short summaries | Detailed: In-depth analysis"
    )
    
    st.divider()
    
    # PDF Upload
    st.subheader("📄 Upload ESG Report")
    uploaded_file = st.file_uploader(
        "Upload PDF",
        type=['pdf'],
        help="Upload company ESG/Sustainability report"
    )
    
    if uploaded_file:
        if st.session_state.uploaded_file_name != uploaded_file.name:
            with st.spinner("Processing PDF..."):
                try:
                    # Extract full text for scoring
                    full_text = extract_text_from_pdf(uploaded_file)
                    st.session_state.full_text = full_text
                    
                    # Reset file pointer for chunk processing
                    uploaded_file.seek(0)
                    
                    # Process PDF
                    chunks = process_pdf(uploaded_file)
                    
                    if chunks:
                        # Build RAG index
                        rag_engine = get_rag_engine()
                        success = rag_engine.build_index(chunks)
                        
                        if success:
                            st.session_state.rag_ready = True
                            st.session_state.uploaded_file_name = uploaded_file.name
                            st.success(f"✅ Processed: {uploaded_file.name}")
                            st.info(f"📊 Created {len(chunks)} text chunks")
                        else:
                            st.error("Failed to build RAG index")
                    else:
                        st.error("Failed to process PDF")
                        
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    if st.session_state.rag_ready:
        st.success("✅ RAG System Ready")
        
        # Add ESG Score button
        if st.button("📊 Calculate ESG Score", use_container_width=True):
            if st.session_state.full_text:
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                def update_progress(progress, message):
                    progress_bar.progress(progress / 100)
                    status_text.text(message)
                
                try:
                    score_result = calculate_overall_esg_score(
                        st.session_state.full_text,
                        progress_callback=update_progress,
                        use_parallel=True
                    )
                    if score_result:
                        st.session_state.esg_score = score_result
                        progress_bar.empty()
                        status_text.empty()
                        st.success("✅ ESG analysis complete!")
                        st.rerun()
                    else:
                        st.error("Failed to calculate ESG score")
                except Exception as e:
                    st.error(f"Error during ESG scoring: {str(e)}")
                finally:
                    progress_bar.empty()
                    status_text.empty()
            else:
                st.warning("Please upload an ESG report pdf first.")
  
        # Display score if available
        if st.session_state.esg_score:
            score = st.session_state.esg_score
            st.metric(
                label="Overall ESG Score",
                value=f"{score['overall_score']}/5.0",
                delta=score['risk_level']
            )
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("🌍 Environmental", f"{score['environmental']['score']}/5")
            with col2:
                st.metric("👥 Social", f"{score['social']['score']}/5")
            with col3:
                st.metric("🏛️ Governance", f"{score['governance']['score']}/5")
    
    st.divider()
    
    # Web Search Toggle
    use_web_search = st.checkbox(
        "Enable Web Search",
        value=True,
        help="Search web for latest ESG news and regulations"
    )
    
    st.divider()
    
    # Clear chat
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Main content
st.title("🌱 ESG Risk Intelligence Assistant")
st.markdown("""
Analyze ESG reports, assess risks, and get latest sustainability insights.
Upload an ESG/Sustainability report and ask questions!
""")

# Example queries
with st.expander("💡 Example Queries"):
    st.markdown("""
    **ESG Analysis:**
    - "Calculate score" or "ESG score" - Get automated ESG risk score
    - "Analyze the ESG risks in this report"
    - "What is the company's carbon emission reduction target?"
    - "Evaluate the diversity and inclusion metrics"
    
    **Specific Queries:**
    - "What are the governance strengths and weaknesses?"
    - "Compare this against industry ESG standards"
    - "What are the latest ESG regulations in 2025?"
    - "Identify compliance gaps"
    """)

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# # Chat input
# if prompt := st.chat_input("Ask about ESG risks, sustainability metrics, or regulations..."):
#     # Add user message
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     with st.chat_message("user"):
#         st.markdown(prompt)
    
#     # Check for special commands
#     if prompt.lower() in ["calculate score", "esg score", "show score", "analyze score"]:
#         with st.chat_message("assistant"):
#             if st.session_state.full_text and st.session_state.esg_score:
#                 # Generate detailed score summary
#                 summary = generate_score_summary(st.session_state.esg_score)
#                 gaps = analyze_esg_gaps(st.session_state.esg_score)
                
#                 response = summary + "\n\n### 📋 Recommendations:\n" + "\n".join(gaps)
#                 st.markdown(response)
                
#                 st.session_state.messages.append({
#                     "role": "assistant",
#                     "content": response
#                 })
#             elif st.session_state.full_text:
#                 with st.spinner("Calculating ESG Score..."):
#                     score_result = calculate_overall_esg_score(st.session_state.full_text)
#                     st.session_state.esg_score = score_result
                    
#                     summary = generate_score_summary(score_result)
#                     gaps = analyze_esg_gaps(score_result)
                    
#                     response = summary + "\n\n### 📋 Recommendations:\n" + "\n".join(gaps)
#                     st.markdown(response)
                    
#                     st.session_state.messages.append({
#                         "role": "assistant",
#                         "content": response
#                     })
#             else:
#                 error_msg = "Please upload an ESG report first to calculate the score."
#                 st.error(error_msg)
#                 st.session_state.messages.append({
#                     "role": "assistant",
#                     "content": error_msg
#                 })
#     else:
#         with st.chat_message("assistant"):
#              with st.spinner("Analyzing..."):
#                 try:
#                     llm = get_llm(provider=llm_provider)
#                     context_parts = []

#                     # RAG context
#                     if st.session_state.rag_ready:
#                         rag_engine = get_rag_engine()
#                         relevant_chunks = rag_engine.retrieve(prompt, top_k=3)

#                         if relevant_chunks:
#                             context_parts.append("=== Document Context ===")
#                             context_parts.append("\n\n".join(relevant_chunks))

#                     # Web search context
#                     if use_web_search and any(
#                         keyword in prompt.lower()
#                         for keyword in ["latest", "recent", "current", "news", "regulation", "2025", "2024"]
#                     ):
#                         search_results = search_web(f"ESG {prompt}", max_results=3)
#                         if search_results:
#                             context_parts.append(format_search_results(search_results))
                    
#                     #Build Prompt
#                     max_tokens = (
#                         CONCISE_MAX_TOKENS 
#                         if response_mode == "Concise" 
#                         else DETAILED_MAX_TOKENS
#                     )

#                     system_context = (
#                         "\n\n".join(context_parts) 
#                         if context_parts 
#                         else "No additional context available."
#                     )

#                     if response_mode == "Concise":
#                         mode_instruction = (
#                             "Provide a concise, brief response (2-4 sentences). "
#                             "Focus on key insights only."
#                         )
#                     else:
#                         mode_instruction = (
#                             "Provide a detailed, comprehensive analysis with specific metrics, "
#                             "data points, and actionable insights."
#                         )
#                     full_prompt = f"""You are an ESG (Environmental, Social, Governance) risk analyst. Analyze the following query and provide insights.    
# Context:
# {system_context}

# Query: {prompt}

# Instructions:
# - {mode_instruction}
# - If analyzing a report, focus on ESG risks, strengths, and gaps
# - Provide specific metrics and data when available
# - Be objective and evidence-based
# - If asked for a score, use a 1-5 scale (1=High Risk, 5=Low Risk)

# Response:"""

#                 # Generate response
#                     response = llm.generate_response(full_prompt, max_tokens=max_tokens)

#                 # Display response
#                     st.markdown(response)

#                 # Add to chat history
#                     st.session_state.messages.append({
#                         "role": "assistant",
#                         "content": response
#                     })
#                 except Exception as e:
#                     error_msg = f"Error generating response: {str(e)}"
#                     st.error(error_msg)
#                     st.session_state.messages.append({
#                         "role": "assistant",
#                         "content": error_msg
#                     })

# # Footer
# st.divider()
# st.markdown(
#     """
# <div style='text-align: center; color: gray; font-size: 0.9em;'>
# 🌱 ESG Risk Intelligence Assistant | Built with Streamlit, LangChain & FAISS
# </div>
# """,
#     unsafe_allow_html=True
# )
# Chat input
if prompt := st.chat_input("Ask about ESG risks, sustainability metrics, or regulations..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Check for special commands (calculate score via chat)
    if prompt.lower() in ["calculate score", "esg score", "show score", "analyze score"]:
        with st.chat_message("assistant"):
            if st.session_state.esg_score:
                # Use existing score
                summary = generate_score_summary(st.session_state.esg_score)
                gaps = analyze_esg_gaps(st.session_state.esg_score)
                
                response = summary + "\n\n### 📋 Recommendations:\n" + "\n".join(gaps)
                st.markdown(response)
                
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response
                })
            elif st.session_state.full_text:
                # Calculate new score with real-time progress in chat
                progress_placeholder = st.empty()
                
                with progress_placeholder.container():
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    def update_progress(progress, message):
                        progress_bar.progress(progress / 100)
                        status_text.text(message)
                    
                    score_result = calculate_overall_esg_score(
                        st.session_state.full_text,
                        progress_callback=update_progress,
                        use_parallel=True
                    )
                    
                    # Clear progress UI
                    progress_placeholder.empty()
                
                if score_result:
                    st.session_state.esg_score = score_result
                    
                    summary = generate_score_summary(score_result)
                    gaps = analyze_esg_gaps(score_result)
                    
                    response = summary + "\n\n### 📋 Recommendations:\n" + "\n".join(gaps)
                    st.markdown(response)
                    
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response
                    })
                else:
                    error_msg = "Failed to calculate ESG score. Please try again."
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg
                    })
            else:
                error_msg = "Please upload an ESG report first to calculate the score."
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg
                })
    else:
        # Regular chat queries
        with st.chat_message("assistant"):
            with st.spinner("Analyzing..."):
                try:
                    llm = get_llm(provider=llm_provider)
                    context_parts = []

                    # RAG context
                    if st.session_state.rag_ready:
                        rag_engine = get_rag_engine()
                        relevant_chunks = rag_engine.retrieve(prompt, top_k=3)

                        if relevant_chunks:
                            context_parts.append("=== Document Context ===")
                            context_parts.append("\n\n".join(relevant_chunks))

                    # Web search context
                    if use_web_search and any(
                        keyword in prompt.lower()
                        for keyword in ["latest", "recent", "current", "news", "regulation", "2025", "2024"]
                    ):
                        search_results = search_web(f"ESG {prompt}", max_results=3)
                        if search_results:
                            context_parts.append(format_search_results(search_results))
                    
                    # Build Prompt
                    max_tokens = (
                        CONCISE_MAX_TOKENS 
                        if response_mode == "Concise" 
                        else DETAILED_MAX_TOKENS
                    )

                    system_context = (
                        "\n\n".join(context_parts) 
                        if context_parts 
                        else "No additional context available."
                    )

                    if response_mode == "Concise":
                        mode_instruction = (
                            "Provide a concise, brief response (2-4 sentences). "
                            "Focus on key insights only."
                        )
                    else:
                        mode_instruction = (
                            "Provide a detailed, comprehensive analysis with specific metrics, "
                            "data points, and actionable insights."
                        )
                    
                    full_prompt = f"""You are an ESG (Environmental, Social, Governance) risk analyst. Analyze the following query and provide insights.    
Context:
{system_context}

Query: {prompt}

Instructions:
- {mode_instruction}
- If analyzing a report, focus on ESG risks, strengths, and gaps
- Provide specific metrics and data when available
- Be objective and evidence-based
- If asked for a score, use a 1-5 scale (1=High Risk, 5=Low Risk)

Response:"""

                    # Generate response
                    response = llm.generate_response(full_prompt, max_tokens=max_tokens)

                    # Display response
                    st.markdown(response)

                    # Add to chat history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response
                    })
                except Exception as e:
                    error_msg = f"Error generating response: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg
                    })

# Footer
st.divider()
st.markdown(
    """
<div style='text-align: center; color: gray; font-size: 0.9em;'>
🌱 ESG Risk Intelligence Assistant | Built with Streamlit, LangChain & FAISS
</div>
""",
    unsafe_allow_html=True
)