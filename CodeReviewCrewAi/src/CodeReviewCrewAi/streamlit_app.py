import os
import streamlit as st
from crews.review_crew.CodeReview_crew import CodeReviewCrew
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import agentops

from dotenv import load_dotenv
load_dotenv()

# AgentOps is a monitoring tool for AI agents
agentops.init(  
    api_key=os.getenv("AGENTOPS_API_KEY"),
    default_tags=['crewai']
)

class CustomStreamlitClass:
    def __init__(self):
        self.initialize_session_state()

    def initialize_session_state(self):
        """Initialize all necessary session state variables."""
        if "code_dict" not in st.session_state:
            st.session_state.code_dict = {}
        if "file_list" not in st.session_state:
            st.session_state.file_list = []
        if "user_message" not in st.session_state:
            st.session_state.user_message = ""
        if "chat_output" not in st.session_state:
            st.session_state.chat_output = ""
        if "review_output" not in st.session_state:
            st.session_state.review_output = ""

    def read_python_files(self, dir_path):
        """
        Traverse the given directory to read files with specific extensions.
        Returns a dictionary with file names as keys and file content (prefixed with file path) as values.
        """
        code_dict = {}
        valid_extensions = (
            '.py', '.java', '.c', '.cpp', '.js', '.ts', '.rb',
            '.go', '.rs', '.swift', '.kt', '.php'
        )
        for root, _, files in os.walk(dir_path):
            for file in files:
                if file.endswith(valid_extensions):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r') as f:
                            content = f.read()
                        code_dict[file] = f"# File: {file_path}\n{content}"
                    except Exception as e:
                        st.error(f"Error reading {file_path}: {e}")
        return code_dict

    def load_files_section(self):
        """Sidebar section for loading code files from a user-specified directory."""
        with st.sidebar:
            st.header("File Loader")
            dir_path = st.text_input("Enter the directory path containing your code:")
            if st.button("Load Files") and dir_path:
                if not os.path.isdir(dir_path):
                    st.error(f"Directory '{dir_path}' not found.")
                else:
                    code_dict = self.read_python_files(dir_path)    # Read code files from the directory and store in a dictionary
                    if not code_dict:
                        st.error("No valid code files found in the directory.")
                    else:
                        st.session_state.code_dict = code_dict
                        st.session_state.file_list = list(code_dict.keys())
                        st.success(f"Loaded {len(code_dict)} files.")
            if st.session_state.file_list:
                selected_file = st.selectbox("Select the file you want to review:", st.session_state.file_list)
                st.session_state.selected_file = selected_file

    def review_file_section(self):
        """Sidebar section to generate a code review for the selected file."""
        with st.sidebar:
            if "selected_file" in st.session_state:
                st.subheader(f"Reviewing: {st.session_state.selected_file}")
                user_prompt = st.text_area("Enter an additional prompt (optional):")
                if st.button("Generate Review"):

                    # Generate the review using CodeReviewCrew
                    crew_instance = CodeReviewCrew().crew()
                    inputs = {
                        "code": st.session_state.code_dict,
                        "which_file": st.session_state.selected_file,
                        "user_prompt": user_prompt
                    }
                    result = crew_instance.kickoff(inputs=inputs)
                    st.session_state.review_output = str(result)

    def follow_up_chat_section(self):
        """Sidebar section to handle follow-up chat using review and completion reports."""
        with st.sidebar:
            # Load external markdown outputs if available
            review_output = "No review output available"
            completion_output = "No completion output available"
            try:
                with open("review_output.md", "r") as f:
                    review_output = f.read()
                with open("completion_output.md", "r") as f:
                    completion_output = f.read()
            except Exception as e:
                st.error(f"Error loading output files: {e}")

            if "selected_file" in st.session_state:
                st.subheader("Follow up Chat")
                st.session_state.user_message = st.text_input("Enter your message:", value=st.session_state.user_message)
                if st.button("Send Message"):
                    llm = ChatOpenAI(model="gpt-4o-mini")
                    system_msg = (
                        "I'm an AI assistant here to help you with your follow up questions. "
                        "I will use the information you provide to generate a response. "
                        "I will use reviews and completions from the code review and code completion tasks. "
                        "I will answer questions according to the context of the code review and code completion tasks."                        
                    )
                    prompt = ChatPromptTemplate.from_messages(
                        [
                            ("system", system_msg),
                            (
                                "human",
                                "Code Review Report : {review_output} , Code Completion Report : {completion_output}, User Question: {user_message}"
                            )
                        ]
                    )
                    llm_prompted = prompt | llm
                    result = llm_prompted.invoke(input={
                        "user_message": st.session_state.user_message,
                        "review_output": review_output,
                        "completion_output": completion_output
                    })
                    st.session_state.chat_output = str(result.content)
                    st.text_area("Chat Output", value=st.session_state.chat_output, height=300)

    def display_review_output(self):
        """Display the generated review output in the main area."""
        if st.session_state.get("review_output"):
            st.markdown("### Review Output")
            st.code(st.session_state.review_output)

    def run(self):
        """Set up the Streamlit app and execute the sections."""
        st.set_page_config(page_title="Code Review", page_icon="📝")
        st.title("Code Review Application")
        
        self.initialize_session_state()
        self.load_files_section()
        self.review_file_section()
        self.follow_up_chat_section()
        self.display_review_output()


def main():
    app = CustomStreamlitClass()
    app.run()


if __name__ == "__main__":
    main()
