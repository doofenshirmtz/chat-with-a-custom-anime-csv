import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os
from groq import Groq

load_dotenv()

def main():
    st.set_page_config(page_title="Anime Recommender")
    st.header("🎌 Chat with Anime CSV")
    
   
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    # File upload struggled a bit with stupid syntax of streamlit lol
    uploaded_file = st.file_uploader("Upload your anime CSV", type="csv")
    
    if uploaded_file:
        
        df = pd.read_csv(uploaded_file)
        good_df = df[df['Score'] >= 7.5].head(100)
        csv_text = good_df.to_string()
        
        
        system_prompt = f"""You are an anime expert. Use this database to answer:

{csv_text}"""
        
        st.success(f"Loaded {len(good_df)} top anime")
        
        # input
        user_question = st.text_input("Ask about anime:")
        
        if user_question:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_question}
                ]
            )
            st.write(response.choices[0].message.content)

if __name__ == "__main__":
    main()