from pathlib import Path
from datetime import datetime
import time

import streamlit as st


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="File Manager",
    page_icon="📁",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
<style>

@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
}

code, .mono {
    font-family: 'JetBrains Mono', monospace;
}

[data-testid="stAppViewContainer"],
[data-testid="stApp"] {
    background: #12131C;
    color: #E9E9F1;
}

[data-testid="stHeader"] {
    background: transparent;
}


/* ================= SIDEBAR ================= */

[data-testid="stSidebar"] {
    background: #15161F;
    border-right: 1px solid #2A2D40;
}

[data-testid="stSidebar"] .stRadio > label {
    display: none;
}

[data-testid="stSidebar"] .stRadio [role="radiogroup"] label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.90rem;
    color: #B8BAC9;
    padding: 9px 10px;
    border-radius: 6px;
    transition: background 0.15s ease, color 0.15s ease;
}

[data-testid="stSidebar"] .stRadio [role="radiogroup"] label:hover {
    background: #20222F;
    color: #F2A65A;
}

.sidebar-tag {
    font-family: 'JetBrains Mono', monospace;
    color: #565A72;
    font-size: 0.72rem;
    margin: 18px 0 6px 2px;
}

.sidebar-foot {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: #3E4155;
    margin-top: 24px;
}


/* ================= HEADER ================= */

.top-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    padding: 4px 2px 18px 2px;
    border-bottom: 1px solid #2A2D40;
    margin-bottom: 20px;
    box-sizing: border-box;
}

.top-title {
    font-weight: 700;
    font-size: 1.5rem;
    line-height: 1.2;
}

.top-title .dim {
    color: #565A72;
    font-weight: 500;
}

.type-line {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
    color: #57C7B0;
    text-align: right;
    white-space: nowrap;
}


/* ================= PANEL ================= */

.panel {
    background: #1B1D2A;
    border: 1px solid #2A2D40;
    border-radius: 10px;
    padding: 22px 24px;
    box-sizing: border-box;
}

.panel-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    color: #565A72;
    margin-bottom: 4px;
}


/* ================= EXPLORER ================= */

.explorer-row {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    color: #C3C5D6;
    padding: 6px 0;
    border-bottom: 1px dashed #2A2D40;
    display: flex;
    justify-content: space-between;
    gap: 12px;
}

.explorer-row .fsize {
    color: #565A72;
    white-space: nowrap;
}


/* ================= ACTIVITY ================= */

.log-row {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.76rem;
    padding: 3px 0;
    color: #8B8DA3;
    word-break: break-word;
}

.log-row .ok {
    color: #57C7B0;
}

.log-row .bad {
    color: #E8637A;
}

.log-time {
    color: #3E4155;
    margin-right: 6px;
}


/* ================= INPUTS ================= */

.stTextInput input,
.stTextArea textarea,
div[data-baseweb="select"] > div {
    background: #12131C !important;
    border: 1px solid #2A2D40 !important;
    color: #E9E9F1 !important;
    font-family: 'JetBrains Mono', monospace;
    border-radius: 6px !important;
}

.stTextInput input:focus,
.stTextArea textarea:focus {
    border-color: #F2A65A !important;
    box-shadow: none !important;
}


/* ================= BUTTON ================= */

.stButton > button {
    font-family: 'JetBrains Mono', monospace;
    font-weight: 600;
    border-radius: 6px;
    border: 1px solid #F2A65A;
    background: #F2A65A;
    color: #12131C;
    padding: 0.5rem 1.3rem;
}

.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 14px rgba(242, 166, 90, 0.25);
}


/* ================= METRICS ================= */

div[data-testid="stMetric"] {
    background: #1B1D2A;
    border: 1px solid #2A2D40;
    border-radius: 8px;
    padding: 10px 14px;
}

div[data-testid="stMetricLabel"] {
    font-family: 'JetBrains Mono', monospace;
    color: #8B8DA3;
}


/* ================= HEADINGS ================= */

h1,
h2,
h3 {
    font-family: 'Space Grotesk', sans-serif;
}

hr {
    border-color: #2A2D40 !important;
}


/* ================= DOWNLOAD BUTTON ================= */

.stDownloadButton > button {
    font-family: 'JetBrains Mono', monospace;
    border-radius: 6px;
}


/* ================= MOBILE ================= */

@media (max-width: 900px) {
    .top-header {
        align-items: flex-start;
        gap: 12px;
        flex-direction: column;
    }

    .type-line {
        text-align: left;
        white-space: normal;
    }
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# STORAGE
# ============================================================

WORKDIR = Path("file_manager_storage")
WORKDIR.mkdir(exist_ok=True)


# ============================================================
# SESSION LOG
# ============================================================

if "log" not in st.session_state:
    st.session_state.log = []


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def list_files():
    """
    Return only files from our storage folder.
    """
    return sorted(
        [
            p
            for p in WORKDIR.iterdir()
            if p.is_file()
        ],
        key=lambda p: p.name.lower()
    )


def human_size(num_bytes: int) -> str:
    n = float(num_bytes)

    for unit in ["B", "KB", "MB", "GB"]:
        if n < 1024:
            if unit == "B":
                return f"{n:.0f}{unit}"
            return f"{n:.1f}{unit}"

        n /= 1024

    return f"{n:.1f}TB"


def log_event(text: str, ok: bool = True):
    current_time = datetime.now().strftime("%H:%M:%S")

    st.session_state.log.insert(
        0,
        (current_time, text, ok)
    )

    st.session_state.log = st.session_state.log[:8]


def run_command(delay: float = 0.25):
    """
    Small UI delay so the operation feels like
    a command execution.
    """
    with st.spinner("processing..."):
        time.sleep(delay)


def safe_filename(name: str):
    """
    Prevent paths like:

        ../file.txt
        ../../something
        folder/file.txt

    Only a normal filename is allowed.
    """

    name = name.strip()

    if not name:
        return None

    path = Path(name)

    if path.name != name:
        return None

    if path.is_absolute():
        return None

    return name


def get_file(name: str):
    """
    Get a file only from WORKDIR.
    """

    filename = safe_filename(name)

    if filename is None:
        return None

    path = WORKDIR / filename

    if not path.is_file():
        return None

    return path


# ============================================================
# SIDEBAR
# ============================================================

COMMANDS = {
    "➕  Create File": ("create", "create a new file"),
    "✍️  Write File": ("write", "write content to a file"),
    "📖  Read File": ("read", "read a file's content"),
    "🔄  Update File": ("update", "rename, append or overwrite a file"),
    "🗑️  Delete File": ("delete", "delete a file"),
}


with st.sidebar:

    st.markdown("### 📁 file_manager")

    st.caption("a small file manager, wearing a UI")

    # IMPORTANT:
    # Keep HTML starting at column 0.
    st.markdown(
        '<div class="sidebar-tag">// operations</div>',
        unsafe_allow_html=True
    )

    choice_label = st.radio(
        "operations",
        list(COMMANDS.keys()),
        label_visibility="collapsed"
    )

    action, action_desc = COMMANDS[choice_label]

    st.markdown(
        '<div class="sidebar-foot">v1.0 · storage: ./file_manager_storage/</div>',
        unsafe_allow_html=True
    )


# ============================================================
# FILES
# ============================================================

files = list_files()


# ============================================================
# TOP HEADER
# ============================================================

# FIX:
# This HTML is deliberately NOT indented.
# Streamlit will render it as HTML instead of a code block.

header_html = (
    '<div class="top-header">'
    '<div class="top-title">'
    'file_manager<span class="dim">.py</span>'
    '</div>'
    '<div class="type-line">'
    f'$ {action} — {action_desc}'
    '</div>'
    '</div>'
)

st.markdown(
    header_html,
    unsafe_allow_html=True
)


# ============================================================
# TWO COLUMN LAYOUT
# ============================================================

left, right = st.columns(
    [2, 1],
    gap="large"
)


# ============================================================
# LEFT SIDE - OPERATIONS
# ============================================================

with left:

    st.markdown(
        '<div class="panel">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="panel-label">workspace</div>',
        unsafe_allow_html=True
    )

    st.subheader(choice_label)

    st.caption(action_desc)


    # ========================================================
    # CREATE FILE
    # ========================================================

    if action == "create":

        name = st.text_input(
            "filename",
            placeholder="notes.txt"
        )

        if st.button(
            "Create File",
            type="primary"
        ):

            filename = safe_filename(name)

            if filename is None:

                st.warning(
                    "Please enter a valid filename only."
                )

            else:

                path = WORKDIR / filename

                if path.exists():

                    st.error(
                        f"'{filename}' already exists."
                    )

                    log_event(
                        f"create {filename} — already exists",
                        ok=False
                    )

                else:

                    run_command()

                    path.touch()

                    log_event(
                        f"created {filename}"
                    )

                    st.success(
                        f"'{filename}' created successfully."
                    )

                    st.rerun()


    # ========================================================
    # WRITE FILE
    # ========================================================

    elif action == "write":

        st.caption(
            "If the file doesn't exist, it will be created automatically."
        )

        name = st.text_input(
            "filename",
            placeholder="notes.txt"
        )

        data = st.text_area(
            "content",
            height=180,
            placeholder="type something worth saving..."
        )

        if st.button(
            "Write File",
            type="primary"
        ):

            filename = safe_filename(name)

            if filename is None:

                st.warning(
                    "Please enter a valid filename only."
                )

            else:

                run_command()

                path = WORKDIR / filename

                path.write_text(
                    data,
                    encoding="utf-8"
                )

                log_event(
                    f"write {filename}"
                )

                st.success(
                    f"Content written to '{filename}'."
                )

                st.rerun()


    # ========================================================
    # READ FILE
    # ========================================================

    elif action == "read":

        if not files:

            st.info(
                "Nothing in storage yet."
            )

        else:

            name = st.selectbox(
                "filename",
                [f.name for f in files]
            )

            if st.button(
                "Read File",
                type="primary"
            ):

                path = get_file(name)

                if path is None:

                    st.error(
                        "File was not found."
                    )

                    log_event(
                        f"read {name} — not found",
                        ok=False
                    )

                else:

                    run_command()

                    content = path.read_text(
                        encoding="utf-8"
                    )

                    log_event(
                        f"read {name}"
                    )

                    st.code(
                        content if content else "(empty file)",
                        language=None
                    )

                    st.download_button(
                        "⬇ Download",
                        content,
                        file_name=name
                    )


    # ========================================================
    # UPDATE FILE
    # ========================================================

    elif action == "update":

        if not files:

            st.info(
                "Nothing in storage yet."
            )

        else:

            update_operation = st.selectbox(
                "select update operation",
                [
                    "Rename File",
                    "Add Content",
                    "Overwrite File"
                ]
            )


            # ------------------------------------------------
            # RENAME
            # ------------------------------------------------

            if update_operation == "Rename File":

                old_name = st.selectbox(
                    "current filename",
                    [f.name for f in files]
                )

                new_name = st.text_input(
                    "new filename",
                    placeholder="new_notes.txt"
                )

                if st.button(
                    "Rename File",
                    type="primary"
                ):

                    new_filename = safe_filename(new_name)

                    if new_filename is None:

                        st.warning(
                            "Please enter a valid filename only."
                        )

                    else:

                        old_path = get_file(old_name)

                        if old_path is None:

                            st.error(
                                "Original file was not found."
                            )

                        else:

                            new_path = WORKDIR / new_filename

                            if new_path.exists():

                                st.error(
                                    f"'{new_filename}' already exists."
                                )

                                log_event(
                                    f"rename {old_name} -> "
                                    f"{new_filename} — already exists",
                                    ok=False
                                )

                            else:

                                run_command()

                                old_path.rename(new_path)

                                log_event(
                                    f"rename {old_name} -> {new_filename}"
                                )

                                st.success(
                                    f"'{old_name}' renamed to "
                                    f"'{new_filename}'."
                                )

                                st.rerun()


            # ------------------------------------------------
            # APPEND
            # ------------------------------------------------

            elif update_operation == "Add Content":

                name = st.selectbox(
                    "filename",
                    [f.name for f in files]
                )

                data = st.text_area(
                    "content to add",
                    height=150,
                    placeholder="content you want to add..."
                )

                if st.button(
                    "Add Content",
                    type="primary"
                ):

                    path = get_file(name)

                    if path is None:

                        st.error(
                            "File was not found."
                        )

                    else:

                        run_command()

                        with open(
                            path,
                            "a",
                            encoding="utf-8"
                        ) as file:

                            file.write(data)

                        log_event(
                            f"append {name}"
                        )

                        st.success(
                            f"Content added to '{name}'."
                        )

                        st.rerun()


            # ------------------------------------------------
            # OVERWRITE
            # ------------------------------------------------

            elif update_operation == "Overwrite File":

                name = st.selectbox(
                    "filename",
                    [f.name for f in files]
                )

                data = st.text_area(
                    "new content",
                    height=180,
                    placeholder="this will replace all existing content..."
                )

                st.warning(
                    "This will replace the existing content completely."
                )

                if st.button(
                    "Overwrite File",
                    type="primary"
                ):

                    path = get_file(name)

                    if path is None:

                        st.error(
                            "File was not found."
                        )

                    else:

                        run_command()

                        path.write_text(
                            data,
                            encoding="utf-8"
                        )

                        log_event(
                            f"overwrite {name}"
                        )

                        st.success(
                            f"'{name}' overwritten successfully."
                        )

                        st.rerun()


    # ========================================================
    # DELETE FILE
    # ========================================================

    elif action == "delete":

        if not files:

            st.info(
                "Nothing in storage yet."
            )

        else:

            name = st.selectbox(
                "filename",
                [f.name for f in files]
            )

            st.warning(
                f"This will permanently delete '{name}'."
            )

            if st.button(
                "Delete File",
                type="primary"
            ):

                path = get_file(name)

                if path is None:

                    st.error(
                        "File was not found."
                    )

                else:

                    run_command()

                    path.unlink()

                    log_event(
                        f"delete {name}"
                    )

                    st.success(
                        f"'{name}' deleted successfully."
                    )

                    st.rerun()


    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# ============================================================
# RIGHT SIDE
# ============================================================

with right:

    # --------------------------------------------------------
    # METRICS
    # --------------------------------------------------------

    total_size = sum(
        f.stat().st_size
        for f in files
    )

    m1, m2 = st.columns(2)

    m1.metric(
        "files",
        len(files)
    )

    m2.metric(
        "storage",
        human_size(total_size)
    )


    # --------------------------------------------------------
    # EXPLORER
    # --------------------------------------------------------

    st.markdown(
        '<div class="panel">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="panel-label">explorer</div>',
        unsafe_allow_html=True
    )

    if files:

        for f in files:

            stat = f.stat()

            explorer_html = (
                '<div class="explorer-row">'
                f'<span>📄 {f.name}</span>'
                f'<span class="fsize">{human_size(stat.st_size)}</span>'
                '</div>'
            )

            st.markdown(
                explorer_html,
                unsafe_allow_html=True
            )

    else:

        st.markdown(
            '<div class="explorer-row">(empty directory)</div>',
            unsafe_allow_html=True
        )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # ACTIVITY
    # --------------------------------------------------------

    st.markdown(
        '<div class="panel" style="margin-top:16px;">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="panel-label">activity</div>',
        unsafe_allow_html=True
    )

    if st.session_state.log:

        for t, text, ok in st.session_state.log:

            cls = "ok" if ok else "bad"
            mark = "✓" if ok else "✗"

            activity_html = (
                '<div class="log-row">'
                f'<span class="log-time">{t}</span>'
                f'<span class="{cls}">{mark} {text}</span>'
                '</div>'
            )

            st.markdown(
                activity_html,
                unsafe_allow_html=True
            )

    else:

        st.markdown(
            '<div class="log-row">no operations performed yet.</div>',
            unsafe_allow_html=True
        )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    '<div class="sidebar-foot" style="margin-top:28px;">'
    '// built with python + streamlit'
    '</div>',
    unsafe_allow_html=True
)