import asyncio
import uuid
import sys
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv


# =========================================================
# Environment
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

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


# =========================================================
# Page
# =========================================================

st.set_page_config(
    page_title="StimaSaidizi",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# Small presentation layer
# =========================================================

st.markdown(
    """
    <style>
        /* Reduce Streamlit's excessive top spacing */
        .block-container {
            padding-top: 3rem;
            padding-bottom: 6rem;
            max-width: 1200px;
        }

        /* More restrained page headings */
        h1 {
            letter-spacing: -0.035em;
        }

        h2, h3 {
            letter-spacing: -0.02em;
        }

        /* Metric containers */
        [data-testid="stMetric"] {
            border: 1px solid #dde1e6;
            padding: 1rem 1.1rem;
            min-height: 112px;
            background: #ffffff;
        }

        [data-testid="stMetricLabel"] {
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }

        /* Cleaner buttons */
        .stButton > button {
            min-height: 2.5rem;
            font-weight: 500;
        }

        /* Sidebar identity */
        section[data-testid="stSidebar"] h1 {
            font-size: 1.45rem;
            letter-spacing: -0.025em;
        }

        /* Reduce visual weight of captions */
        [data-testid="stCaptionContainer"] {
            color: #525252;
        }

        /* Chat input */
        [data-testid="stChatInput"] {
            border-radius: 0.25rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# ADK
# =========================================================

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
        # Streamlit reruns frequently. An existing session is fine.
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


# =========================================================
# Sidebar
# =========================================================

with st.sidebar:
    st.title("StimaSaidizi")
    st.caption("Customer Support & Service Operations")

    st.write("")

    page = st.radio(
        "Workspace",
        [
            "Customer Support",
            "Manager Dashboard",
        ],
    )

    st.divider()

    st.caption(
        "DEMONSTRATION ENVIRONMENT"
    )
    st.caption(
        "Uses synthetic utility data. "
        "StimaSaidizi is not an official Kenya Power service."
    )


# =========================================================
# Customer workspace
# =========================================================

if page == "Customer Support":

    heading, action = st.columns([5, 1])

    with heading:
        st.title("Customer Support")
        st.caption(
            "Service enquiries, outage information, prepaid tokens, "
            "billing and case management."
        )

    with action:
        if st.button(
            "New chat",
            width="stretch",
            disabled=not st.session_state.customer_messages,
        ):
            reset_customer_chat()
            st.rerun()

    st.divider()

    # Purposeful empty state
    if not st.session_state.customer_messages:
        st.subheader("How can we assist?")

        st.write(
            "Select a common service request or describe your issue below."
        )

        st.write("")

        q1, q2 = st.columns(2)

        with q1:
            outage_clicked = st.button(
                "Report or check an outage",
                width="stretch",
            )

            token_clicked = st.button(
                "Check a prepaid token",
                width="stretch",
            )

        with q2:
            bill_clicked = st.button(
                "View billing information",
                width="stretch",
            )

            case_clicked = st.button(
                "Follow up a support case",
                width="stretch",
            )

        quick_prompt = None

        if outage_clicked:
            quick_prompt = (
                "I want to report or check an electricity outage."
            )
        elif token_clicked:
            quick_prompt = (
                "I need help checking a prepaid token transaction."
            )
        elif bill_clicked:
            quick_prompt = (
                "I want to check my electricity bill."
            )
        elif case_clicked:
            quick_prompt = (
                "I want to follow up on an existing support case."
            )

        st.write("")
        st.caption(
            "StimaSaidizi only reports information available in the "
            "demonstration dataset."
        )

    else:
        quick_prompt = None

        for message in st.session_state.customer_messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    typed_prompt = st.chat_input(
        "Describe your service request..."
    )

    prompt = typed_prompt or quick_prompt

    if prompt:
        st.session_state.customer_messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Retrieving service information..."):
                try:
                    response = run_agent(
                        st.session_state.customer_runner,
                        st.session_state.customer_session_id,
                        prompt,
                    )
                except Exception:
                    st.error(
                        "StimaSaidizi could not complete the request. "
                        "Please try again."
                    )
                    st.stop()

            st.markdown(response)

        st.session_state.customer_messages.append(
            {
                "role": "assistant",
                "content": response,
            }
        )

        # Required for quick-action buttons so the page
        # immediately transitions into conversation mode.
        if quick_prompt:
            st.rerun()


# =========================================================
# Service Operations workspace
# =========================================================

else:

    st.title("Service Operations")
    st.caption(
        "Customer support performance, case activity and "
        "operational analytics."
    )

    st.divider()

    # -----------------------------------------------------
    # KPIs
    # -----------------------------------------------------

    total = total_cases()
    resolved_rate = resolution_rate()
    escalated_rate = escalation_rate()
    avg_time = average_resolution_time()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total cases",
        total,
    )

    col2.metric(
        "Resolution rate",
        f"{resolved_rate:.1f}%",
    )

    col3.metric(
        "Escalation rate",
        f"{escalated_rate:.1f}%",
    )

    col4.metric(
        "Avg. resolution",
        f"{avg_time:.1f} min",
    )

    st.write("")

    # -----------------------------------------------------
    # Distribution
    # -----------------------------------------------------

    st.subheader("Case Distribution")

    left, right = st.columns(2)

    category_data = cases_by_category()
    status_data = cases_by_status()

    with left:
        st.caption("BY CATEGORY")

        if category_data:
            st.bar_chart(
                category_data,
                height=230,
            )
        else:
            st.info("No category data available.")

    with right:
        st.caption("BY STATUS")

        if status_data:
            st.bar_chart(
                status_data,
                height=230,
            )
        else:
            st.info("No status data available.")

    st.divider()

    # -----------------------------------------------------
    # Unresolved cases
    # -----------------------------------------------------

    unresolved = unresolved_cases()

    unresolved_heading, unresolved_count = st.columns([5, 1])

    with unresolved_heading:
        st.subheader("Unresolved Cases")
        st.caption(
            "Open and escalated customer-support cases "
            "requiring further review."
        )

    with unresolved_count:
        st.metric(
            "Current",
            len(unresolved),
        )

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
            width="stretch",
            hide_index=True,
        )

    else:
        st.success("There are currently no unresolved cases.")

    st.divider()

    # -----------------------------------------------------
    # Mkurugenzi
    # -----------------------------------------------------

    manager_heading, manager_action = st.columns([5, 1])

    with manager_heading:
        st.subheader("Mkurugenzi")
        st.caption(
            "Operational assistant for support metrics "
            "and unresolved case analysis."
        )

    with manager_action:
        if st.button(
            "New chat",
            key="manager_new_chat",
            width="stretch",
            disabled=not st.session_state.manager_messages,
        ):
            reset_manager_chat()
            st.rerun()

    if not st.session_state.manager_messages:
        st.caption(
            "Example: Summarise current customer-support performance "
            "and highlight cases requiring review."
        )

    for message in st.session_state.manager_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input(
        "Ask Mkurugenzi about service performance..."
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
            with st.spinner("Analysing operational data..."):
                try:
                    response = run_agent(
                        st.session_state.manager_runner,
                        st.session_state.manager_session_id,
                        prompt,
                    )
                except Exception:
                    st.error(
                        "Mkurugenzi could not complete the request. "
                        "Please try again."
                    )
                    st.stop()

            st.markdown(response)

        st.session_state.manager_messages.append(
            {
                "role": "assistant",
                "content": response,
            }
        )