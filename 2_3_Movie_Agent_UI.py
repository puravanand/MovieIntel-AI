from dotenv import load_dotenv
load_dotenv()


from tavily import TavilyClient
search= TavilyClient()

from langchain_core.tools import tool


@tool
def movie_search(query: str):
    """Search the web for movie information."""
    result = search.search(
        query=query,
        max_results=2,
        search_depth="basic",
        include_raw_content=False
    )
    return str(result)[:8000]

from langchain_groq import ChatGroq

llm = ChatGroq( model="openai/gpt-oss-120b")


# ============================================================
# STREAMLIT UI
# ============================================================

import streamlit as st
import html


st.set_page_config(
    page_title="MovieIntel AI",
    page_icon="🎬",
    layout="wide"
)


# ============================================================
# PROFESSIONAL UI CSS
# ============================================================

st.markdown("""
<style>

/* ============================================================
   GLOBAL BACKGROUND
   ============================================================ */

.stApp {
    background:
        radial-gradient(
            circle at top left,
            #e0e7ff 0%,
            #f5f3ff 25%,
            #f8fafc 55%,
            #eef2ff 100%
        );

    color: #172033;
}


/* Streamlit main area */

[data-testid="stAppViewContainer"] {
    background:
        linear-gradient(
            135deg,
            #eef2ff 0%,
            #f8fafc 45%,
            #ede9fe 100%
        );
}


/* Main container */

.block-container {
    max-width: 1250px;

    padding-top: 35px;
    padding-bottom: 55px;
}


/* ============================================================
   HEADER
   ============================================================ */

.movie-header {

    background:
        linear-gradient(
            135deg,
            #0f172a 0%,
            #1e1b4b 35%,
            #3730a3 70%,
            #2563eb 100%
        );

    border-radius: 22px;

    padding: 35px 38px;

    margin-bottom: 32px;

    text-align: center;

    border: 1px solid rgba(255,255,255,0.12);

    box-shadow:
        0 18px 45px rgba(30, 41, 59, 0.22);
}


.movie-title {

    color: #ffffff;

    font-size: 42px;

    font-weight: 850;

    letter-spacing: -1.2px;

    line-height: 1.2;
}


.movie-subtitle {

    color: #dbeafe;

    font-size: 15px;

    font-weight: 500;

    margin-top: 10px;

    letter-spacing: 0.2px;
}


/* ============================================================
   INPUT SECTION
   ============================================================ */

.input-title {

    color: #1e1b4b;

    font-size: 20px;

    font-weight: 800;

    margin-bottom: 10px;

    text-align: left;
}


/* Text area wrapper */

div[data-testid="stTextArea"] {
    width: 100%;
}


/* Text area */

div[data-testid="stTextArea"] textarea {

    background: #ffffff !important;

    color: #172033 !important;

    border: 2px solid #c7d2fe !important;

    border-radius: 16px !important;

    font-size: 17px !important;

    font-weight: 500 !important;

    line-height: 1.6 !important;

    padding: 17px !important;

    min-height: 110px !important;

    width: 100% !important;

    resize: vertical !important;

    box-shadow:
        0 6px 18px rgba(79, 70, 229, 0.08) !important;

    transition: all 0.2s ease !important;
}


/* Placeholder */

div[data-testid="stTextArea"] textarea::placeholder {

    color: #94a3b8 !important;

    opacity: 1 !important;
}


/* Focus */

div[data-testid="stTextArea"] textarea:focus {

    border: 2px solid #6366f1 !important;

    box-shadow:
        0 0 0 4px rgba(99, 102, 241, 0.12),
        0 8px 25px rgba(79, 70, 229, 0.10) !important;
}


/* ============================================================
   EXTRACT BUTTON
   ============================================================ */

.stButton > button {

    width: 100% !important;

    min-height: 54px !important;

    background:
        linear-gradient(
            135deg,
            #4f46e5,
            #6366f1,
            #2563eb
        ) !important;

    color: #ffffff !important;

    border: none !important;

    border-radius: 14px !important;

    font-size: 17px !important;

    font-weight: 800 !important;

    letter-spacing: 0.1px;

    box-shadow:
        0 10px 25px rgba(79, 70, 229, 0.25) !important;

    transition: all 0.2s ease !important;
}


.stButton > button:hover {

    background:
        linear-gradient(
            135deg,
            #4338ca,
            #4f46e5,
            #1d4ed8
        ) !important;

    transform: translateY(-2px);

    box-shadow:
        0 13px 30px rgba(79, 70, 229, 0.30) !important;
}


/* ============================================================
   SUCCESS MESSAGE
   ============================================================ */

div[data-testid="stAlert"] {

    border-radius: 14px !important;

    border: none !important;

    box-shadow:
        0 5px 15px rgba(16, 185, 129, 0.08) !important;
}


/* ============================================================
   SECTION HEADINGS
   ============================================================ */

.section-title {

    color: #1e1b4b;

    font-size: 24px;

    font-weight: 850;

    margin-top: 34px;

    margin-bottom: 17px;

    text-align: center;

    letter-spacing: -0.3px;
}


/* ============================================================
   INFORMATION CARDS
   ============================================================ */

.info-card {

    background:
        linear-gradient(
            145deg,
            #ffffff,
            #f8faff
        );

    border: 1px solid #dbe4ff;

    border-radius: 18px;

    padding: 23px 16px;

    min-height: 145px;

    display: flex;

    flex-direction: column;

    justify-content: center;

    align-items: center;

    text-align: center;

    box-shadow:
        0 7px 20px rgba(51, 65, 85, 0.07);

    overflow: hidden;

    transition: all 0.2s ease;
}


.info-card:hover {

    transform: translateY(-3px);

    border-color: #a5b4fc;

    box-shadow:
        0 12px 28px rgba(79, 70, 229, 0.12);
}


.card-label {

    color: #6366f1;

    font-size: 11px;

    font-weight: 850;

    text-transform: uppercase;

    letter-spacing: 1px;

    margin-bottom: 12px;

    text-align: center;
}


.card-value {

    color: #172033;

    font-size: 21px;

    font-weight: 850;

    line-height: 1.4;

    text-align: center;

    width: 100%;

    overflow-wrap: anywhere;

    word-break: break-word;
}


/* ============================================================
   LIST CARDS
   ============================================================ */

.list-card {

    background:
        linear-gradient(
            145deg,
            #ffffff,
            #f8faff
        );

    border: 1px solid #dbe4ff;

    border-radius: 18px;

    padding: 23px;

    min-height: 260px;

    box-shadow:
        0 7px 20px rgba(51, 65, 85, 0.07);

    text-align: center;

    transition: all 0.2s ease;
}


.list-card:hover {

    transform: translateY(-2px);

    border-color: #a5b4fc;

    box-shadow:
        0 12px 28px rgba(79, 70, 229, 0.11);
}


.list-title {

    color: #312e81;

    font-size: 18px;

    font-weight: 850;

    text-align: center;

    margin-bottom: 15px;
}


.list-item {

    color: #475569;

    font-size: 15px;

    font-weight: 500;

    line-height: 1.6;

    padding: 8px 0;

    border-bottom: 1px solid #eef2ff;

    text-align: center;

    overflow-wrap: anywhere;

    word-break: break-word;
}


.list-item:last-child {

    border-bottom: none;
}


/* ============================================================
   FINANCIAL CARDS
   ============================================================ */

.finance-card {

    background:
        linear-gradient(
            135deg,
            #ffffff,
            #eef2ff
        );

    border: 1px solid #c7d2fe;

    border-radius: 18px;

    padding: 26px;

    min-height: 145px;

    display: flex;

    flex-direction: column;

    justify-content: center;

    align-items: center;

    text-align: center;

    box-shadow:
        0 8px 22px rgba(79, 70, 229, 0.08);

    transition: all 0.2s ease;
}


.finance-card:hover {

    transform: translateY(-2px);

    box-shadow:
        0 12px 28px rgba(79, 70, 229, 0.12);
}


.finance-label {

    color: #6366f1;

    font-size: 11px;

    font-weight: 850;

    text-transform: uppercase;

    letter-spacing: 1px;

    margin-bottom: 11px;

    text-align: center;
}


.finance-value {

    color: #3730a3;

    font-size: 25px;

    font-weight: 900;

    line-height: 1.4;

    text-align: center;

    overflow-wrap: anywhere;
}


/* ============================================================
   JSON SECTION
   ============================================================ */

div[data-testid="stJson"] {

    background: #0f172a !important;

    border: 1px solid #312e81 !important;

    border-radius: 16px !important;

    padding: 12px !important;

    box-shadow:
        0 8px 25px rgba(15, 23, 42, 0.15) !important;
}


/* ============================================================
   FOOTER
   ============================================================ */

.movie-footer {

    text-align: center;

    color: #64748b;

    font-size: 13px;

    font-weight: 500;

    margin-top: 55px;

    padding-top: 22px;

    border-top: 1px solid #dbe4ff;
}


/* ============================================================
   RESPONSIVE
   ============================================================ */

@media (max-width: 768px) {

    .block-container {

        padding-left: 18px;

        padding-right: 18px;

        padding-top: 25px;
    }

    .movie-header {

        padding: 27px 20px;
    }

    .movie-title {

        font-size: 30px;
    }

    .movie-subtitle {

        font-size: 14px;
    }

    .section-title {

        font-size: 21px;
    }

    .card-value {

        font-size: 18px;
    }

    .finance-value {

        font-size: 21px;
    }

    .info-card,
    .list-card,
    .finance-card {

        min-height: 0;
    }
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# HEADER - UI ONLY
# ============================================================

st.markdown(
    '<div class="movie-header">'
    '<div class="movie-title">🎬 MovieIntel AI</div>'
    '<div class="movie-subtitle">'
    'Extracts and analyzes movie information using AI'
    '</div>'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# INPUT - UI ONLY
# ============================================================

st.markdown(
    '<div class="input-title">Movie Information</div>',
    unsafe_allow_html=True
)


query = st.text_area(
    "Movie Information",
    placeholder="Enter a movie name or paste movie information here...",
    label_visibility="collapsed",
    height=110
)


extract = st.button(
    "🎬  Extract Movie Details",
    use_container_width=True
)


# ============================================================
# YOUR ORIGINAL BACKEND
# DO NOT CHANGE
# ============================================================

from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import List, Optional


class Structure_data(BaseModel):
    Name:str=Field(description="Name of the Movie")
    cast: List[str]
    release_year: Optional[int]
    Director:str
    Actress:List[str]
    Total_cost:float
    Total_Earn:float
    Language:str
    genre:List[str]



from  langchain.agents import create_agent

prompts = ChatPromptTemplate.from_messages([
{"role":"system", "content":"You are the Movie  Extractor  Data Agent, you have to extract the Movie details from the given output "},
{"role":"user","content":"{question}"}
])

system_prompt = """
You are an intelligent Movie Information Extraction Agent.

Your task is to extract movie information according to the required Structure_data.

Follow these rules:

1. If the user provides only a movie name or a short movie query, such as "Dangal",
   "Pushpa 2", or "Inception" and any other, use the search tool to find reliable movie information
   from the web.

2. If the user provides detailed, messy, unstructured, or large movie-related data,
   first extract all available information directly from the user's provided data.
   Do NOT perform a web search if all required information is already available
   in the provided data.

3. If some required information is missing from the user's provided data,
   use the search tool only to find the missing information.

4. Never search the web unnecessarily when the required information is already
   available in the user's input.

5. Do not invent or hallucinate movie information. Use the information provided
   by the user or information obtained through the search tool.

6. Your final response should contain the movie information required for the
   Structure_data schema.

7.  If any field contains 0, 0.0, null, None, blank, empty string,
   "unknown", "N/A", or an empty list, treat that field as missing.

8. If any field is missing or contains an invalid zero/null/empty value,
   use the search tool again to find the correct information before
   returning the final result.

9. Before returning the final Structure_data, verify EVERY field.
    Do not return the result until all fields contain meaningful,
    valid, and non-empty information.

10. Total_cost and Total_Earn must never be null or zero when the
    actual movie financial information can be found online.
    Search for the correct production cost/budget and total earnings
    if either value is missing, zero, or null.

11. cast, Actress, and genre must never be empty lists.
    If any of these lists are empty, search again for the missing
    information before producing the final result.

You are a Movie Extraction Agent whose goal is to efficiently extract complete,
accurate, and structured movie information while minimizing unnecessary web searches.
"""

agent = create_agent(
model=llm,
tools=[movie_search],
system_prompt=system_prompt
)


# ============================================================
# EXTRACTION
# ============================================================

if extract:

    if not query.strip():

        st.warning("Please enter movie information first.")

    else:

        try:

            with st.spinner(
                "🔎 Searching and extracting movie information..."
            ):

                final_promts=prompts.invoke({"question": query})


                ## I  will use this commmented code when I am not using the Template chat template but 


                # res=agent.invoke({
                #     "messages":[{
                #         "role":"user",
                #         "content":final_promts
                # }]
                # })


                res=agent.invoke({
                    "messages":final_promts.messages
                })


                final_llm=llm.with_structured_output(Structure_data)

                movie_data=res['messages'][-1].content[:12000]

                structure_out= final_llm.invoke(movie_data)


            # ============================================================
            # UI HELPER FUNCTIONS
            # ============================================================

            def safe(value):

                return html.escape(
                    str(value if value is not None else "N/A")
                )


            # ============================================================
            # MONEY FORMATTER
            # UI ONLY
            # ============================================================

            def format_money(value):

                try:

                    amount = float(value)

                except:

                    return "N/A"


                # Small movie-budget values are treated
                # as Crore values for display.

                if amount < 1000:

                    return f"₹{amount:,.2f} Crore"


                # Actual rupee values

                if amount >= 10000000:

                    return f"₹{amount / 10000000:,.2f} Crore"


                if amount >= 100000:

                    return f"₹{amount / 100000:,.2f} Lakh"


                return f"₹{amount:,.0f}"


            # ============================================================
            # INFO CARD
            # ============================================================

            def info_card(label, value):

                card_html = (
                    '<div class="info-card">'
                    f'<div class="card-label">{safe(label)}</div>'
                    f'<div class="card-value">{safe(value)}</div>'
                    '</div>'
                )

                st.markdown(
                    card_html,
                    unsafe_allow_html=True
                )


            # ============================================================
            # LIST CARD
            # ============================================================

            def list_card(title, items):

                item_html = "".join(
                    f'<div class="list-item">• {safe(item)}</div>'
                    for item in items
                )

                if not item_html:

                    item_html = (
                        '<div class="list-item">'
                        'Not available'
                        '</div>'
                    )

                card_html = (
                    '<div class="list-card">'
                    f'<div class="list-title">{safe(title)}</div>'
                    f'{item_html}'
                    '</div>'
                )

                st.markdown(
                    card_html,
                    unsafe_allow_html=True
                )


            # ============================================================
            # SUCCESS
            # ============================================================

            st.success(
                "Movie information extracted successfully!"
            )


            # ============================================================
            # MOVIE OVERVIEW
            # ============================================================

            st.markdown(
                '<div class="section-title">Movie Overview</div>',
                unsafe_allow_html=True
            )


            col1, col2, col3, col4 = st.columns(
                4,
                gap="medium"
            )


            with col1:

                info_card(
                    "Movie Name",
                    structure_out.Name
                )


            with col2:

                info_card(
                    "Release Year",
                    structure_out.release_year
                )


            with col3:

                info_card(
                    "Director",
                    structure_out.Director
                )


            with col4:

                info_card(
                    "Language",
                    structure_out.Language
                )


            # ============================================================
            # CAST / ACTRESS / GENRE
            # ============================================================

            st.markdown(
                '<div class="section-title">Cast & Classification</div>',
                unsafe_allow_html=True
            )


            col1, col2, col3 = st.columns(
                3,
                gap="medium"
            )


            with col1:

                list_card(
                    "🎭 Cast",
                    structure_out.cast
                )


            with col2:

                list_card(
                    "👩 Actresses",
                    structure_out.Actress
                )


            with col3:

                list_card(
                    "🎞️ Genres",
                    structure_out.genre
                )


            # ============================================================
            # FINANCIAL INFORMATION
            # ============================================================

            st.markdown(
                '<div class="section-title">Financial Information</div>',
                unsafe_allow_html=True
            )


            col1, col2 = st.columns(
                2,
                gap="medium"
            )


            with col1:

                finance_html = (
                    '<div class="finance-card">'
                    '<div class="finance-label">'
                    'Production Cost'
                    '</div>'
                    '<div class="finance-value">'
                    f'{safe(format_money(structure_out.Total_cost))}'
                    '</div>'
                    '</div>'
                )

                st.markdown(
                    finance_html,
                    unsafe_allow_html=True
                )


            with col2:

                finance_html = (
                    '<div class="finance-card">'
                    '<div class="finance-label">'
                    'Total Earnings'
                    '</div>'
                    '<div class="finance-value">'
                    f'{safe(format_money(structure_out.Total_Earn))}'
                    '</div>'
                    '</div>'
                )

                st.markdown(
                    finance_html,
                    unsafe_allow_html=True
                )


            # ============================================================
            # STRUCTURED MOVIE DATA
            # ============================================================

            st.markdown(
                '<div class="section-title">Structured Movie Data</div>',
                unsafe_allow_html=True
            )


            st.json(
                structure_out.model_dump(),
                expanded=True
            )


        except Exception as e:

            st.error(
                "Unable to extract movie information."
            )

            st.error(str(e))


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    '<div class="movie-footer">'
    'MovieIntel AI • Powered by Groq GenAI'
    '</div>',
    unsafe_allow_html=True
)
