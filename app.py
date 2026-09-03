# app.py
import streamlit as st
import streamlit.components.v1 as components
from langchain_groq import ChatGroq
from tools import search_anime_web

# 1. Inject Advanced Cyberpunk Styling and Cyber Blast Regular Font Configuration
CYBER_INTERFACE_CSS = """
<style>
    /* Import Neon Tech Fonts dynamically */
    @import url('https://googleapis.com');
    
    /* Fallback layout mapping for 'Cyber Blast Regular' style */
    @font-face {
        font-family: 'Cyber Blast Regular';
        src: local('Cyber Blast Regular'), local('CyberBlast-Regular'), url('https://cdnfonts.com') format('woff');
    }

    /* Global Interface Restyling */
    .stApp {
        background: linear-gradient(135deg, #05020a 0%, #0d0614 50%, #020005 100%);
        color: #00ffcc;
        font-family: 'Share Tech Mono', monospace;
    }
    
    /* Glowing Anime Cyber Header Design */
    h1, h2, h3 {
        font-family: 'Cyber Blast Regular', 'Orbitron', sans-serif !important;
        color: #ff0055 !important;
        text-shadow: 0px 0px 15px #ff0055, 0px 0px 5px #00ffff;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    
    /* Glitch-Themed Chat Container Bubbles */
    .stChatMessage {
        background-color: rgba(13, 6, 26, 0.85) !important;
        border-radius: 4px !important;
        border-left: 4px solid #ff0055 !important;
        border-right: 1px solid rgba(0, 255, 204, 0.3) !important;
        border-top: 1px solid rgba(0, 255, 204, 0.1) !important;
        border-bottom: 1px solid rgba(0, 255, 204, 0.1) !important;
        box-shadow: 0px 0px 15px rgba(13, 6, 26, 0.5);
        margin-bottom: 12px;
    }

    /* Input Console Forms Custom Styling */
    .stTextInput>div>div>input, .stChatInput textarea {
        background-color: #08040f !important;
        color: #ffffff !important;
        font-family: 'Share Tech Mono', monospace !important;
        border: 1px solid #ff0055 !important;
        box-shadow: 0px 0px 8px rgba(255, 0, 85, 0.2);
    }
    
    .stTextInput>div>div>input:focus, .stChatInput textarea:focus {
        border-color: #00ffcc !important;
        box-shadow: 0px 0px 12px #00ffcc !important;
    }

    /* Cyber Button Terminal Submissions */
    button[kind="primary"], .stButton>button {
        background: transparent !important;
        color: #00ffcc !important;
        font-family: 'Orbitron', sans-serif;
        border: 2px solid #00ffcc !important;
        border-radius: 0px !important;
        text-shadow: 0px 0px 5px #00ffcc;
        box-shadow: inset 0px 0px 8px rgba(0, 255, 204, 0.3), 0px 0px 8px rgba(0, 255, 204, 0.3);
        transition: all 0.3s ease;
    }
    
    button[kind="primary"]:hover, .stButton>button:hover {
        color: #ffffff !important;
        background-color: #ff0055 !important;
        border-color: #ff0055 !important;
        text-shadow: 0px 0px 5px #ffffff;
        box-shadow: 0px 0px 15px #ff0055;
    }
</style>
"""
st.markdown(CYBER_INTERFACE_CSS, unsafe_allow_html=True)

# 2. Hidden HTML/JS Script Injection for Creepy Slow Background Music and Mechanical Key Clicks
# Note: Modern browsers block autoplay until a user interacts with the page (clicks anywhere).
AUDIO_AUTOMATION_HTML = """
<div style="display:none;">
    <!-- Slow Creepy Ambient Drone Track (Free-use royalty-free asset archive loop) -->
    <audio id="bg-drone" loop>
        <source src="https://soundhelix.com" type="audio/mp3">
    </audio>
    <!-- Sharp Mechanical Cyber Key Sound Effect -->
    <audio id="key-click">
        <source src="https://mixkit.co" type="audio/wav">
    </audio>
</div>

<script>
    const bgMusic = parent.document.getElementById("bg-drone");
    const keyClick = parent.document.getElementById("key-click");

    // Lower default music volume to create an ominous background tone rather than loud music
    if(bgMusic) { bgMusic.volume = 0.15; }
    if(keyClick) { keyClick.volume = 0.4; }

    // Start slow background tone loop upon first mouse click on the terminal interface
    parent.document.addEventListener('click', function() {
        if(bgMusic && bgMusic.paused) {
            bgMusic.play().catch(e => console.log("Autoplay blocked until user event."));
        }
    });

    // Monitor global keyboard keystrokes to trigger the mechanical typing feedback audio instantly
    parent.document.addEventListener('keydown', function(event) {
        if(keyClick) {
            keyClick.currentTime = 0;
            keyClick.play().catch(e => {});
        }
    });
</script>
"""
# Mount the hidden media components to the Streamlit window frame
components.html(AUDIO_AUTOMATION_HTML, height=0, width=0)

# 3. Custom System Prompt Rules
SYSTEM_PROMPT = (
    "You are an interactive Custom Anime Research Agent operating within a dark cybernetic database grid. "
    "Maintain a deeply intellectual, passionate, cyber-hacker anime expert persona. "
    "When processing plot questions, analyze character parameters, hidden world rules, and backstory context "
    "from the provided texts, explaining them in rich, highly analytical paragraphs with glowing thematic bullet points. "
    "Always begin responses with an immersive greeting sequence like 'Hi! Establishing secure link... Let's analyze this file context.' "
    "and gracefully conclude with 'Thank you for visiting!' message.\n\n"
)

# 4. Gateway Access Verification Gate
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.title("⚡ CYBER OPERATOR LOGIN")
    st.write("Secure access.")
    
    username_input = st.text_input("Username")
    password_input = st.text_input("Password", type="password")
    
    if st.button("INITIALIZE"):
        if username_input == "cyber_hacker" and password_input == "AnimePass2026!":
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("Uplink handshake failed. Access code unrecognized.")
    st.stop()

# 5. Core Operational Chat View (Launches when access state is true)
st.title("🧬  ANIME ASSISTANT ")
st.subheader("Autonomous Web-Crawl Intelligence main terminal")

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi! How are you? I'm your dedicated Anime Fandom Intelligence Agent. System connection secure.  ✨"}
    ]

for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if user_query := st.chat_input("Enter search..."):
    
    with st.chat_message("user"):
        st.write(user_query)
    st.session_state["messages"].append({"role": "user", "content": user_query})
    
    with st.chat_message("assistant"):
        with st.spinner("CRUNCHING SYSTEM LOGS & CRAWLING CORE NETWORKS..."):
            try:
                llm = ChatGroq(model="openai/gpt-oss-20b", api_key=st.secrets["GROQ_API_KEY"])
                scraped_data_context = search_anime_web.invoke(user_query)
                
                final_structured_prompt = (
                    f"{SYSTEM_PROMPT}"
                    f"Mainframe Data Stream context:\n{scraped_data_context}\n\n"
                    f"Vector parameter to analyze: {user_query}\n"
                    f"System breakdown analysis:"
                )
                
                agent_final_output = llm.invoke(final_structured_prompt)
                st.write(agent_final_output.content)
                st.session_state["messages"].append({"role": "assistant", "content": agent_final_output.content})
       
            except Exception as e:
                st.error(f"Uplink error occurred during agent compute execution loop: {str(e)}")
