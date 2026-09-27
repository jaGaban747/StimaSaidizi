import asyncio
import uuid
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

# ---------------------------------------------------------
# Environment
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / "agents" / "customer_support" / ".env")

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agents.customer_support.agent import root_agent as customer_agent
from agents.mkurugenzi.agent import root_agent as manager_agent

from services.analytics_service import (
    total_cases,
    cases_by_category,
    cases_by_status,
    resolution_rate,
    escalation_rate,
    average_resolution_time,
    unresolved_cases,
)


APP_NAME = "stimasaidizi"
USER_ID = "streamlit_user"


# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="StimaSaidizi",
    page_icon="⚡",
    layout="wide",
)


# ---------------------------------------------------------
# ADK helpers
# ---------------------------------------------------------

def initialize_state():
    if "session_service" not in st.session_state:
        st.session_state.session_service = InMemorySessionService()

    if "customer_session_id" not in st.session_state:
        st.session_state.customer_session_id = str(uuid.uuid4())

    if "manager_session_id" not in st.session_state:
        st.session_state.manager_session_id = str(uuid.uuid4())

    if "customer_messages" not in st.session_state:
        st.session_state.customer_messages = []

    if "manager_messages" not in st.session_state:
        st.session_state.manager_messages = []

    if "customer_runner" not in st.session_state:
        st.session_state.customer_runner = Runner(
            agent=customer_agent,
            app_name=APP_NAME,
            session_service=st.session_state.session_service,
        )

    if "manager_runner" not in st.session_state:
        st.session_state.manager_runner = Runner(
            agent=manager_agent,
            app_name=APP_NAME,
            session_service=st.session_state.session_service,
        )


async def ensure_session(session_id):
    try:
        await st.session_state.session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=session_id,
        )
    except Exception:
        pass


async def ask_agent(runner, session_id, message):
    await ensure_session(session_id)

    content = types.Content(
        role="user",
        parts=[types.Part(text=message)],
    )

    final_response = None

    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=session_id,
        new_message=content,
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                text_parts = [
                    part.text
                    for part in event.content.parts
                    if getattr(part, "text", None)
                ]

                if text_parts:
                    final_response = "\n".join(text_parts)

    return final_response or (
        "I couldn't complete that request. Please try again."
    )


def run_agent(runner, session_id, message):
    return asyncio.run(
        ask_agent(runner, session_id, message)
    )


def reset_customer_chat():
    st.session_state.customer_messages = []
    st.session_state.customer_session_id = str(uuid.uuid4())


def reset_manager_chat():
    st.session_state.manager_messages = []
    st.session_state.manager_session_id = str(uuid.uuid4())


initialize_state()


# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------

with st.sidebar:
    st.title("⚡ StimaSaidizi")

    st.caption(
        "AI-powered electricity customer support "
        "and service analytics."
    )

    page = st.radio(
        "Workspace",
        [
            "Customer Support",
            "Manager Dashboard",
        ],
    )

    st.divider()

    st.caption(
        "Educational prototype using synthetic utility data. "
        "Not an official Kenya Power service."
    )


# ---------------------------------------------------------
# Customer Support
# ---------------------------------------------------------

if page == "Customer Support":

    col1, col2 = st.columns([5, 1])

    with col1:
        st.title("Customer Support")
        st.caption(
            "Get help with outages, prepaid tokens, "
            "billing and support cases."
        )

    with col2:
        if st.button("New chat", use_container_width=True):
            reset_customer_chat()
            st.rerun()

    st.info(
        "This prototype uses synthetic customer and utility data."
    )

    for message in st.session_state.customer_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input(
        "Ask StimaSaidizi for help..."
    ):
        st.session_state.customer_messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Checking..."):
                try:
                    response = run_agent(
                        st.session_state.customer_runner,
                        st.session_state.customer_session_id,
                        prompt,
                    )
                except Exception:
                    st.error(
                        "StimaSaidizi could not complete "
                        "the request."
                    )
                    st.stop()

            st.markdown(response)

        st.session_state.customer_messages.append(
            {
                "role": "assistant",
                "content": response,
            }
        )


# ---------------------------------------------------------
# Manager Dashboard
# ---------------------------------------------------------

else:

    st.title("Manager Dashboard")

    st.caption(
        "Customer-support performance and operational "
        "insights from synthetic data."
    )

    # Current metrics
    total = total_cases()
    resolved_rate = resolution_rate()
    escalated_rate = escalation_rate()
    avg_time = average_resolution_time()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Cases",
        total,
    )

    col2.metric(
        "Resolution Rate",
        f"{resolved_rate:.1f}%",
    )

    col3.metric(
        "Escalation Rate",
        f"{escalated_rate:.1f}%",
    )

    col4.metric(
        "Avg. Resolution",
        f"{avg_time:.1f} min",
    )

    st.divider()

    # Case breakdown
    left, right = st.columns(2)

    with left:
        st.subheader("Cases by Category")

        category_data = cases_by_category()

        if category_data:
            st.bar_chart(category_data)
        else:
            st.info("No category data available.")

    with right:
        st.subheader("Cases by Status")

        status_data = cases_by_status()

        if status_data:
            st.bar_chart(status_data)
        else:
            st.info("No status data available.")

    st.divider()

    # Unresolved cases
    st.subheader("Unresolved Cases")

    unresolved = unresolved_cases()

    if unresolved:
        display_cases = []

        for case in unresolved:
            display_cases.append(
                {
                    "Case ID": case.get("case_id"),
                    "Customer": case.get("customer_id"),
                    "Category": case.get("category"),
                    "Status": case.get("status"),
                    "Summary": case.get("summary"),
                }
            )

        st.dataframe(
            display_cases,
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.success("No unresolved cases.")

    st.divider()

    # Mkurugenzi
    header, button = st.columns([5, 1])

    with header:
        st.subheader("Ask Mkurugenzi")
        st.caption(
            "Ask questions about current support metrics "
            "and unresolved cases."
        )

    with button:
        if st.button(
            "New chat",
            key="manager_new_chat",
            use_container_width=True,
        ):
            reset_manager_chat()
            st.rerun()

    for message in st.session_state.manager_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input(
        "Ask Mkurugenzi about support performance..."
    ):
        st.session_state.manager_messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Analysing support data..."):
                try:
                    response = run_agent(
                        st.session_state.manager_runner,
                        st.session_state.manager_session_id,
                        prompt,
                    )
                except Exception:
                    st.error(
                        "Mkurugenzi could not complete "
                        "the request."
                    )
                    st.stop()

            st.markdown(response)

        st.session_state.manager_messages.append(
            {
                "role": "assistant",
                "content": response,
            }
        )