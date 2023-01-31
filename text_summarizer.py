import streamlit as st
#NLP
import spacy
nlp=spacy.load('en_core_web_sm')
from spacy import displacy
import nltk
nltk.download('punkt')
HTML_WRAPPER="""<div style="overflow-x:auto; border:1px solid #e6e9ef;border-radius:0.25rem; padding:1rem">{}</div>"""
#[theme]
#primaryColor="#aa4bff"
#backgroundColor="#65c4d0"
#secondaryBackgroundColor="#b3dada"
#textColor="#31333F"
# summary pkgs
#from gensim.summarization import summarize
#sumy summary pkg
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
# function fro summy summarization
def sumy_summarizer(docx):
    parser=PlaintextParser.from_string(docx,Tokenizer("english"))
    lex_summarizer=LexRankSummarizer()
    summary=lex_summarizer(parser.document,3)
    summary_list=[str(sentence)for sentence in summary]
    result=' '.join(summary_list)
    return result
#NLP
#@st.cache(allow_output_mutation=True)
#nlp object
def analyze_text(text):
    return nlp(text)
# web scrapping pkgs
from bs4 import BeautifulSoup
from urllib.request import urlopen
def get_text(raw_url):
    page=urlopen(raw_url)
    soup=BeautifulSoup(page)
    fetch_text=' '.join(map(lambda p:p.text,soup.find_all('p')))
    return fetch_text
def main():
    """Text Summarization and Entity Checker"""
    st.title("Text Summarization and Entity Checker")
    activities=["Summarize","NER Checker","NER for URL"]
    choice=st.sidebar.selectbox("Select Activity",activities)
    
    if choice=='Summarize':
        st.subheader("Summary with NLP")
        raw_text=st.text_area("Enter Text Here","Type Here",height=140)
       
        def add_bg_from_url():
            st.markdown(
                f"""
                <style>
                .stApp {{
                    background-image: url("https://thumbs.dreamstime.com/b/conceptual-hand-writing-showing-summary-business-photo-showcasing-brief-statement-account-main-points-something-subject-148231729.jpg");
                    background-attachment: fixed;
                    background-size: cover
                }}
                </style>
                """,
                unsafe_allow_html=True
            )

        add_bg_from_url()
        if st.button("Summarize"):
            summary_result=sumy_summarizer(raw_text)
            output = summary_result # final_result_from_processing_the_input
            st.write("## Summary:")
            st.text_area(label="## :blue[**Summary:**]", value=output, height=200)
    if choice=="NER Checker":
        st.subheader("Entity Recognition with Sapcy")
        raw_text=st.text_area("# Enter Text Here","Type Here")
        def add_bg_from_url():
            st.markdown(
                f"""
                <style>
                .stApp {{
                    background-image: url("https://d2mk45aasx86xg.cloudfront.net/AI_Problem_solving_Tool_in_Machine_Learning_11zon_0e0a7dd361.webp");
                    background-attachment: fixed;
                    background-size: cover
                }}
                </style>
                """,
                unsafe_allow_html=True
            )

        add_bg_from_url() 

        if st.button("Analyze"):
            #NLP
             docx=analyze_text(raw_text)
             html=displacy.render(docx,style='ent')
             html=html.replace("\n\n","\n")
             #st.write(html,unsafe_allow_html=True)
             #or
             st.markdown(html,unsafe_allow_html=True)

    if choice=='NER for URL':
        st.subheader("Analyae text from URL")
        raw_url=st.text_input("Enter URL","Type here")
        text_lenth=st.slider("Lenth of Preview",50,100)
        def add_bg_from_url():
            st.markdown(
                f"""
                <style>
                .stApp {{
                    background-image: url("https://www.botify.com/wp-content/uploads/2020/12/3-url-parameters.jpg");
                    background-attachment: fixed;
                    background-size: cover
                }}
                </style>
                """,
                unsafe_allow_html=True
            )

        add_bg_from_url() 
        if st.button("Extract"):
            if raw_url!="Type here":
                result=get_text(raw_url)
                len_of_full_text=len(result)
                len_of_short_text=round(len(result)/text_lenth)
                st.info("Length::Full Text:: {}".format(len_of_full_text))
                st.info("length::Short Text:: {}".format(len_of_short_text))
                output1 = result[:len_of_short_text] # final_result_from_processing_the_input
                st.write("### **Preview:**")
                st.text_area(label="## blue[**Preview:**]", value=output1, height=200)
                summary_docx=sumy_summarizer(result)
                docx=analyze_text(summary_docx)
                html=displacy.render(docx,style='ent')
                html=html.replace("\n\n","\n")
                #st.write(html,unsafe_allow_html=True)
                #or
                st.markdown(html,unsafe_allow_html=True)
    

if  __name__=='__main__':
    main()
