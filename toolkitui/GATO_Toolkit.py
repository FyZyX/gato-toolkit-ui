import streamlit

streamlit.set_page_config(page_title="GATO Data Generator")


def main():
    streamlit.title("GATO Toolkit")

    streamlit.markdown("""
    Welcome to the RLHI Data Generator. This tool is designed to facilitate 
    the generation of data for Reinforcement Learning with Heuristic Imperatives.

    The following data generation tasks are available:
    - Generate Scenarios
    - Generate Actions
    
    Please select the task you wish to perform in the sidebar.
    """)


if __name__ == '__main__':
    main()
