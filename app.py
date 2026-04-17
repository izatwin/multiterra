import streamlit as st

# ── page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MultiTerra",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── global CSS injection ────────────────────────────────────────────────────────
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Syne:wght@400;600;700&display=swap');

/* ── reset & root ── */
:root {
    --bg: #0a0c10;
    --surface: #111318;
    --surface2: #181c24;
    --border: rgba(255,255,255,0.07);
    --border-accent: rgba(99,210,190,0.35);
    --text: #e8eaf0;
    --muted: #6b7280;
    --accent: #63d2be;
    --accent2: #7b8cff;
    --danger: #ff6b6b;
    --success: #63d2be;
    --tag-bg: rgba(99,210,190,0.12);
    --tag-text: #63d2be;
    --mono: 'IBM Plex Mono', monospace;
    --sans: 'Syne', sans-serif;
    --radius: 10px;
    --radius-lg: 16px;
}

html, body, [class*="css"] {
    font-family: var(--sans) !important;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

/* ── sidebar ── */
section[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
    padding-top: 0 !important;
}
section[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.5rem;
}

/* sidebar header */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    font-family: var(--sans) !important;
    font-weight: 700 !important;
    letter-spacing: -0.02em !important;
    color: var(--text) !important;
}

/* ── inputs ── */
input[type="text"],
input[type="number"],
.stTextInput > div > div > input,
.stNumberInput > div > div > input {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    color: var(--text) !important;
    font-family: var(--mono) !important;
    font-size: 13px !important;
    padding: 10px 14px !important;
    transition: border-color 0.2s;
}
input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(99,210,190,0.12) !important;
    outline: none !important;
}

/* ── selectbox / dropdown ── */
.stSelectbox > div > div {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    color: var(--text) !important;
    font-family: var(--mono) !important;
    font-size: 13px !important;
}

/* ── select slider ── */
.stSlider > div {
    color: var(--text) !important;
}
.stSlider [data-baseweb="slider"] div[role="slider"] {
    background: var(--accent) !important;
    border-color: var(--accent) !important;
}

/* ── checkbox ── */
.stCheckbox label span {
    color: var(--text) !important;
    font-size: 14px !important;
}

/* ── buttons ── */
.stButton > button {
    background: var(--accent) !important;
    color: #0a0c10 !important;
    border: none !important;
    border-radius: var(--radius) !important;
    font-family: var(--sans) !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    letter-spacing: 0.03em !important;
    padding: 10px 20px !important;
    width: 100% !important;
    transition: opacity 0.15s, transform 0.1s !important;
    cursor: pointer !important;
}
.stButton > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active {
    transform: scale(0.98) !important;
}

/* deploy button specific override */
div[data-testid="stButton"] button[kind="primary"],
.deploy-btn button {
    background: linear-gradient(135deg, var(--accent), var(--accent2)) !important;
    color: #0a0c10 !important;
}

/* ── code blocks ── */
.stCode, code, pre {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    font-family: var(--mono) !important;
    font-size: 12.5px !important;
    color: var(--accent) !important;
}

/* ── info / success / error banners ── */
.stAlert {
    border-radius: var(--radius) !important;
    border: 1px solid var(--border) !important;
    background: var(--surface2) !important;
    font-family: var(--mono) !important;
    font-size: 13px !important;
}

/* ── labels ── */
label, .stSelectbox label, .stTextInput label, .stSlider label {
    font-family: var(--sans) !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
    margin-bottom: 4px !important;
}

/* ── dividers ── */
hr {
    border-color: var(--border) !important;
    margin: 1.5rem 0 !important;
}

/* ── scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--muted); }
</style>
""",
    unsafe_allow_html=True,
)

# ── custom header ────────────────────────────────────────────────────────────────
st.markdown(
    """
<div style="
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 2rem 0 1.5rem;
    border-bottom: 1px solid rgba(255,255,255,0.07);
    margin-bottom: 2rem;
">
    <div style="
        width: 44px; height: 44px;
        background: rgba(99,210,190,0.15);
        border: 1px solid rgba(99,210,190,0.3);
        border-radius: 12px;
        display: flex; align-items: center; justify-content: center;
        font-size: 22px;
    ">🌐</div>
    <div>
        <div style="font-family:'Syne',sans-serif; font-size:22px; font-weight:700; letter-spacing:-0.03em; color:#e8eaf0; line-height:1;">
            MultiTerra <span style="color:#63d2be;">v1.5</span>
        </div>
        <div style="font-size:12px; color:#6b7280; margin-top:2px; font-family:'IBM Plex Mono',monospace;">
            Infrastructure Designer &amp; Deployment
        </div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# ── imports (guarded so file is viewable without the library installed) ────────
try:
    import pulumi.automation as auto

    from multiterra import (
        Deployment,
        GeneralizedBucket,
        GeneralizedSubnet,
        GeneralizedVM,
        GeneralizedVPC,
        GeneralizedFirewall,
    )

    MULTITERRA_AVAILABLE = True
except ImportError:
    MULTITERRA_AVAILABLE = False

    # Stub classes so the rest of the UI still renders
    class GeneralizedVPC:
        pass

    class GeneralizedSubnet:
        pass

    class GeneralizedVM:
        pass

    class GeneralizedBucket:
        pass

    class GeneralizedFirewall:
        pass


# ── session state ────────────────────────────────────────────────────────────────
if "objects" not in st.session_state:
    st.session_state.objects = {}

# ── sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        """
    <div style="padding:0 0 1.25rem; border-bottom:1px solid rgba(255,255,255,0.07); margin-bottom:1.25rem;">
        <div style="font-family:'Syne',sans-serif; font-size:14px; font-weight:700; letter-spacing:0.06em; text-transform:uppercase; color:#6b7280;">
            Component Builder
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # resource type badges
    resource_options = ["VPC", "Subnet", "VM", "Bucket", "Firewall"]
    comp_type = st.selectbox("Resource Type", options=resource_options)
    name = st.text_input("Resource Name", "my-resource")
   

    st.markdown("<hr>", unsafe_allow_html=True)

    if comp_type == "VPC":
        cidr = st.text_input("CIDR Block", "10.0.0.0/16")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("＋  Add VPC"):
            if MULTITERRA_AVAILABLE:
                st.session_state.objects[name] = {
                    "type": "VPC",
                    "args": {"cidr_block": cidr}
                }
            st.success(f"VPC `{name}` added to stack")

    elif comp_type == "Subnet":
        vpcs = [
            k
            for k, v in st.session_state.objects.items()
            if isinstance(v, GeneralizedVPC)
        ]
        vpc_name = st.selectbox("Parent VPC", vpcs if vpcs else ["— no VPCs yet —"])
        s_cidr = st.text_input("Subnet CIDR", "10.0.1.0/24")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("＋  Add Subnet"):
            if MULTITERRA_AVAILABLE and vpcs:
                st.session_state.objects[name] = {
                    "type": "Subnet",
                    "parent_vpc_name": vpc_name, 
                    "args": {"cidr_block": s_cidr}
                }
            st.success(f"Subnet `{name}` added")
    
    elif comp_type == "Firewall":
        vpcs = [k for k, v in st.session_state.objects.items() if isinstance(v, GeneralizedVPC)]
        vpc_name = st.selectbox("Parent VPC", vpcs if vpcs else ["— no VPCs yet —"])
        
        st.write("Quick Configuration")
        ssh_on = st.checkbox("Allow SSH (22)", value=True)
        web_on = st.checkbox("Allow HTTP (80)", value=False)
        
        if st.button("＋  Add Firewall"):
            ingress = []
            if ssh_on: ingress.append({"port": 22, "protocol": "tcp", "cidr": "0.0.0.0/0"})
            if web_on: ingress.append({"port": 80, "protocol": "tcp", "cidr": "0.0.0.0/0"})
            
            if MULTITERRA_AVAILABLE and vpcs:
                st.session_state.objects[name] = {
                    "type": "Firewall",
                    "parent_vpc_name": vpc_name,
                    "args": {
                        "ingress": ingress, 
                        "egress": [{"port": 0, "protocol": "-1", "cidr": "0.0.0.0/0"}]
                    }
                }
            st.success(f"Firewall `{name}` added")

    elif comp_type == "VM":
        subnets = [
            k
            for k, v in st.session_state.objects.items()
            if isinstance(v, GeneralizedSubnet)
        ]
        sub_name = st.selectbox(
            "Parent Subnet", subnets if subnets else ["— no subnets yet —"]
        )
        tier = st.select_slider(
            "Instance Tier", options=["low", "medium", "high"], value="medium"
        )
        fws = [k for k, v in st.session_state.objects.items() if isinstance(v, GeneralizedFirewall)]
        fw_name = st.selectbox("Attach Firewall", ["None"] + fws)
        
        if st.button("＋  Add VM"):
            if MULTITERRA_AVAILABLE and subnets:
                st.session_state.objects[name] = {
                    "type": "VM",
                    "parent_subnet_name": sub_name,
                    "parent_fw_name": fw_name if fw_name != "None" else None,
                    "args": {"tier": tier}
                }
            st.success(f"VM `{name}` added")

    elif comp_type == "Bucket":
        public = st.checkbox("Enable Public Access", value=False)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("＋  Add Bucket"):
            if MULTITERRA_AVAILABLE:
                st.session_state.objects[name] = {
                    "type": "Bucket",
                    "args": {"public_access": public}
                }
            st.success(f"Bucket `{name}` added")

    # sidebar footer
    st.markdown(
        """
    <div style="position:fixed; bottom:1.5rem; left:0; width:260px; padding:0 1.25rem;
                font-family:'IBM Plex Mono',monospace; font-size:11px; color:#6b7280;">
        MultiTerra v1.5 · Pulumi Automation
    </div>
    """,
        unsafe_allow_html=True,
    )


# ── main area ────────────────────────────────────────────────────────────────────
col_stack, col_deploy = st.columns([3, 2], gap="large")

with col_stack:
    # section header
    n = len(st.session_state.objects)
    st.markdown(
        f"""
    <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:1rem;">
        <div style="font-family:'Syne',sans-serif; font-size:16px; font-weight:700; letter-spacing:-0.01em; color:#e8eaf0;">
            Infrastructure Stack
        </div>
        <div style="font-family:'IBM Plex Mono',monospace; font-size:11px;
                    background:rgba(99,210,190,0.12); color:#63d2be;
                    border:1px solid rgba(99,210,190,0.25); border-radius:6px;
                    padding:3px 10px;">
            {n} resource{'s' if n != 1 else ''}
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    TYPE_COLORS = {
        "GeneralizedVPC": ("#7b8cff", "rgba(123,140,255,0.1)"),
        "GeneralizedSubnet": ("#63d2be", "rgba(99,210,190,0.1)"),
        "GeneralizedVM": ("#f5a623", "rgba(245,166,35,0.1)"),
        "GeneralizedBucket": ("#ff6b6b", "rgba(255,107,107,0.1)"),
        "GeneralizedFirewall": ("#ffcc00", "rgba(255,204,0,0.1)"),
    }

    if not st.session_state.objects:
        st.markdown(
            """
        <div style="
            border: 1px dashed rgba(255,255,255,0.1);
            border-radius: 16px;
            padding: 3rem 2rem;
            text-align: center;
            color: #6b7280;
            font-family: 'IBM Plex Mono', monospace;
            font-size: 13px;
        ">
            No resources yet.<br>
            <span style="font-size:11px;">Use the sidebar to add VPCs, Subnets, VMs, or Buckets.</span>
        </div>
        """,
            unsafe_allow_html=True,
        )
    else:
        for obj_name, obj in st.session_state.objects.items():
            type_name = type(obj).__name__
            color, bg, icon = TYPE_COLORS.get(
                type_name, ("#6b7280", "rgba(107,114,128,0.1)", "◌")
            )
            st.markdown(
                f"""
            <div style="
                background: #111318;
                border: 1px solid rgba(255,255,255,0.07);
                border-left: 3px solid {color};
                border-radius: 10px;
                padding: 14px 18px;
                margin-bottom: 10px;
                display: flex;
                align-items: center;
                gap: 14px;
            ">
                <div style="
                    width: 36px; height: 36px;
                    background: {bg};
                    border-radius: 8px;
                    display: flex; align-items: center; justify-content: center;
                    font-size: 16px; color: {color};
                    flex-shrink: 0;
                ">{icon}</div>
                <div style="flex:1; min-width:0;">
                    <div style="font-family:'Syne',sans-serif; font-weight:600; font-size:14px; color:#e8eaf0; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">
                        {obj_name}
                    </div>
                    <div style="font-family:'IBM Plex Mono',monospace; font-size:11px; color:#6b7280; margin-top:2px;">
                        {type_name}
                    </div>
                </div>
                <div style="
                    font-family:'IBM Plex Mono',monospace; font-size:10px;
                    background:{bg}; color:{color};
                    border:1px solid {color}40;
                    border-radius:5px; padding:3px 8px;
                    flex-shrink:0;
                ">active</div>
            </div>
            """,
                unsafe_allow_html=True,
            )

        # clear all button
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("✕  Clear Stack", key="clear"):
            st.session_state.objects = {}
            st.rerun()


with col_deploy:
    st.markdown(
        """
    <div style="font-family:'Syne',sans-serif; font-size:16px; font-weight:700;
                letter-spacing:-0.01em; color:#e8eaf0; margin-bottom:1rem;">
        Deploy
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
    <div style="background:#111318; border:1px solid rgba(255,255,255,0.07);
                border-radius:16px; padding:1.5rem;">
    """,
        unsafe_allow_html=True,
    )

    target_cloud = st.selectbox("Target Cloud", ["aws", "gcp"], key="cloud_select")
    c1, c2 = st.columns(2)
    with c1:
        target_region = st.text_input("Region", "us-east-1" if target_cloud == "aws" else "us-central1")
    with c2:
        target_zone = st.text_input("Zone", "us-east-1a" if target_cloud == "aws" else "us-central1-a")

    st.markdown("<br>", unsafe_allow_html=True)

    # resource summary pills
    if st.session_state.objects:
        counts = {}
        for obj in st.session_state.objects.values():
            t = type(obj).__name__
            counts[t] = counts.get(t, 0) + 1

        pills_html = " ".join(
            [
                f'<span style="font-family:IBM Plex Mono,monospace;font-size:11px;'
                f"background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);"
                f'border-radius:5px;padding:3px 8px;color:#9ca3af;">'
                f'{v}× {k.replace("Generalized","")}</span>'
                for k, v in counts.items()
            ]
        )
        st.markdown(
            f'<div style="display:flex;flex-wrap:wrap;gap:6px;margin-bottom:1rem;">{pills_html}</div>',
            unsafe_allow_html=True,
        )

    if st.button("🚀  Deploy to Cloud", key="deploy_btn"):
        if not MULTITERRA_AVAILABLE:
            st.error("multiterra / pulumi not installed.")
        elif not st.session_state.objects:
            st.warning("Stack is empty — add resources first.")
        else:

            def pulumi_program():
                Deployment(
                    "streamlit-deploy",
                    roots=list(st.session_state.objects.values()),
                    provider=target_cloud,
                    regions={target_region: target_zone}, # Dictionary format
                )

            with st.spinner("Provisioning infrastructure…"):
                try:
                    stack = auto.create_or_select_stack(
                        stack_name="dev",
                        project_name="multiterra",
                        program=pulumi_program,
                    )
                    res = stack.up(on_output=st.write)
                    st.success("✓  Deployment complete")
                except Exception as e:
                    st.error(f"Deployment failed: {e}")

    st.markdown("</div>", unsafe_allow_html=True)

    # quick-start guide
    st.markdown(
        """
    <div style="margin-top:1.5rem; background:#111318; border:1px solid rgba(255,255,255,0.07);
                border-radius:16px; padding:1.25rem;">
        <div style="font-family:'Syne',sans-serif;font-size:12px;font-weight:700;
                    letter-spacing:0.06em;text-transform:uppercase;color:#6b7280;margin-bottom:12px;">
            Quick Start
        </div>
        <div style="font-family:'IBM Plex Mono',monospace;font-size:12px;color:#9ca3af;line-height:1.8;">
            1 → Create a VPC<br>
            2 → Add a Subnet (attach to VPC)<br>
            3 → Launch VMs or Buckets<br>
            4 → Deploy to cloud
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )
