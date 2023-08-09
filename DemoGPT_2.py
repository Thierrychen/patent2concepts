import streamlit as st
from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (ChatPromptTemplate,
                                    HumanMessagePromptTemplate,
                                    SystemMessagePromptTemplate)

import os 
# openai
openai_api_key="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"
os.environ["OPENAI_API_KEY"]=openai_api_key
model_name="gpt-3.5-turbo-0613"

st.title("Quick Patent")

patent_url = st.text_input("Enter the URL of the patent")
button_clicked = st.button("Submit")

if button_clicked and patent_url != "":
    def patentSummarizer(patent_url):
        chat = ChatOpenAI(
            temperature=0
        )
        system_template = "You are an AI assistant tasked with summarizing a patent from the given URL: '{patent_url}'."
        system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
        human_template = "Please use AI to summarize the patent from the URL: '{patent_url}' in 300 words or less."
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
        chat_prompt = ChatPromptTemplate.from_messages(
            [system_message_prompt, human_message_prompt]
        )

        chain = LLMChain(llm=chat, prompt=chat_prompt)
        result = chain.run(patent_url=patent_url)
        return result # returns string   

    summary = patentSummarizer(patent_url)

    def patentExtractor(summary):
        chat = ChatOpenAI(
            temperature=0
        )
        system_template = "You are an AI assistant tasked with extracting the top 5 technical subject:verb:object pairs from a summarized patent."
        system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
        human_template = "Please extract the top 5 technical subject:verb:object pairs from the following summarized patent: '{summary}'."
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
        chat_prompt = ChatPromptTemplate.from_messages(
            [system_message_prompt, human_message_prompt]
        )

        chain = LLMChain(llm=chat, prompt=chat_prompt)
        result = chain.run(summary=summary)
        return result # returns string   

    technical_pairs = patentExtractor(summary)

    def technicalIdeaGenerator(summary,technical_pairs):
        chat = ChatOpenAI(
            temperature=0.7
        )
        system_template = "You are an AI assistant tasked with generating 10 related technical ideas based on the responses from task 1 and task 2."
        system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
        human_template = "Using the summary '{summary}' and the technical pairs: {technical_pairs}, please generate 10 related technical ideas."
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
        chat_prompt = ChatPromptTemplate.from_messages(
            [system_message_prompt, human_message_prompt]
        )

        chain = LLMChain(llm=chat, prompt=chat_prompt)
        result = chain.run(summary=summary, technical_pairs=technical_pairs)
        return result # returns string   

    technical_ideas = technicalIdeaGenerator(summary,technical_pairs)

    def show_technical_ideas(technical_ideas):
        if technical_ideas != "":
            st.markdown(technical_ideas)
            # st.markdown("Here are 10 related technical ideas:")
            # code to retrieve and display the 10 related technical ideas
            
    st.markdown(summary)
    st.markdown(technical_pairs)
    show_technical_ideas(technical_ideas)
