import streamlit as st
import requests
import base64
import json
import os
import re
import streamlit.components.v1 as components


st.set_page_config(page_title="AI Carrom Coach", page_icon="🎯", layout="wide")
API_URL = "http://localhost:8000"

if "page" not in st.session_state:
    st.session_state.page = "landing"

if "current_user" not in st.session_state:
    st.session_state.current_user = None

if "coach_name" not in st.session_state:
    st.session_state.coach_name = "Maria Irudayam"

if "messages" not in st.session_state:
    st.session_state.messages = []
if "coach_q" not in st.session_state: st.session_state.coach_q = 0
if "boards_analyzed" not in st.session_state: st.session_state.boards_analyzed = 0
if "preset_q" not in st.session_state: st.session_state.preset_q = None


root_dir = os.path.dirname(os.path.abspath(__file__))
avatar_map = {
    "Maria Irudayam": os.path.join(root_dir, "assets", "Maria.png"),
    "S. Ilavazhagi": os.path.join(root_dir, "assets", "Ilavazhagi.png"),
    "Rashid Ahmed": os.path.join(root_dir, "assets", "Rashid.png"),
    "Yogesh Pardeshi": os.path.join(root_dir, "assets", "Yogesh.png"),
    "Chiedu Okonkwo": os.path.join(root_dir, "assets", "Chiedu.png")
}

def get_avatar_image(coach_name):
    path = avatar_map.get(coach_name)
    if path and os.path.exists(path):
        try:
            with open(path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode()
                return f"data:image/png;base64,{encoded_string}"
        except Exception:
            return "🎯"
    return "🎯"


st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=IBM+Plex+Mono:wght@400;500&display=swap');
    html, body, [class*="st-"] { font-family: 'IBM Plex Mono', monospace; }
    h1, h2, h3 { font-family: 'Syne', sans-serif !important; font-weight: 800 !important; }
    
    /* Landing Page Specific Styling */
    .landing-box { text-align: center; margin-top: 10vh; }
    .landing-title { font-size: 4rem; color: #e8e8e2; margin-bottom: 0px; }
    .landing-subtitle { color: #a89bff; font-size: 1.2rem; margin-bottom: 40px; }
    
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] { padding: 10px 16px; color: #555; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px; border-bottom: 2px solid transparent; }
    .stTabs [aria-selected="true"] { color: #a89bff !important; border-bottom-color: #7c6aff !important; }
    .profile-box { background: #181818; border: 1px solid #252525; border-radius: 8px; padding: 15px; margin-bottom: 20px; }
    .profile-stat { display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 8px; color: #999; }
    .profile-stat span.val { color: #e8e8e2; font-weight: bold; }
    
    /* Buttons */
    .stButton > button { background-color: #181818; color: #999; border: 1px solid #252525; border-radius: 6px; width: 100%; text-align: left; padding-left: 15px; transition: 0.2s;}
    .stButton > button:hover { border-color: #7c6aff; color: #a89bff; background: rgba(124,106,255,0.1); }
    .btn-primary > button { background-color: #7c6aff !important; color: white !important; font-weight: bold; border: none; text-align: center; padding-left: 0; }
    .btn-primary > button:hover { background-color: #a89bff !important; }
    
    /* ULTIMATE AVATAR & MEDIA CSS OVERRIDE */
    [data-testid="stChatMessage"] { gap: 1.5rem !important; align-items: flex-start !important; }
    [data-testid="stChatMessage"] > div:first-child,
    [data-testid="stChatMessageAvatar"] { width: 4.5rem !important; height: 4.5rem !important; min-width: 4.5rem !important; min-height: 4.5rem !important; background-color: transparent !important; }
    [data-testid="stChatMessage"] img,
    [data-testid="stChatMessageAvatar"] img { width: 4.5rem !important; height: 4.5rem !important; max-width: 4.5rem !important; max-height: 4.5rem !important; border-radius: 50% !important; object-fit: cover !important; border: 2px solid #7c6aff !important; box-shadow: 0 4px 10px rgba(0,0,0,0.5); }
    [data-testid="stChatMessage"] svg,
    [data-testid="stChatMessageAvatar"] svg { width: 2.5rem !important; height: 2.5rem !important; }
    
    /* Constrain the YouTube Video Size */
    [data-testid="stVideo"] { max-width: 450px !important; border-radius: 12px !important; overflow: hidden !important; border: 1px solid #303030 !important; box-shadow: 0 8px 20px rgba(0,0,0,0.4) !important; margin-top: 10px !important; margin-bottom: 10px !important; }
</style>
""", unsafe_allow_html=True)


def show_landing_page():
    st.markdown("""
        <div class="landing-box">
            <div class="landing-title"><span style='color:#7c6aff'>🎯</span> AI CARROM COACH</div>
            <div class="landing-subtitle">Your personal AI tutor for technique, strategy, and mastery.</div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
        if st.button("Let's Start ➔", use_container_width=True):
            st.session_state.page = "auth"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


def show_auth_page():
    st.markdown("<h1><span style='color:#7c6aff'>🎯</span> Welcome to AI Carrom Coach</h1>", unsafe_allow_html=True)
    st.write("Please sign in or register to track your progress.")
    
    tab_login, tab_register = st.tabs(["Sign In", "Sign Up"])
    
    with tab_login:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Sign In", use_container_width=True)
            
            if submit:
                try:
                    res = requests.post(f"{API_URL}/login/", json={"username": username, "password": password})
                    if res.status_code == 200:
                        st.session_state.current_user = res.json()["user_data"]
                        st.session_state.messages = [{"role": "assistant", "content": f"Welcome back, {username}! I'm {st.session_state.coach_name}. Let's get to work.", "coach_name": st.session_state.coach_name}]
                        st.session_state.page = "main_app"
                        st.rerun()
                    else:
                        st.error("Invalid Username or Password.")
                except Exception as e:
                    st.error(f"Backend connection failed. Ensure FastAPI is running.")
                    
    with tab_register:
        with st.form("register_form"):
            new_user = st.text_input("Username")
            new_email = st.text_input("Email")
            new_phone = st.text_input("Phone Number")
            level = st.selectbox("What's your Carrom Level?", ["Beginner", "Intermediate", "Advanced", "Professional"])
            new_pass = st.text_input("Password", type="password")
            confirm_pass = st.text_input("Confirm Password", type="password")
            
            reg_submit = st.form_submit_button("Register", use_container_width=True)
            
            if reg_submit:
                if new_pass != confirm_pass:
                    st.error("Passwords do not match!")
                elif not new_user or not new_email or not new_pass:
                    st.error("Please fill all required fields.")
                else:
                    payload = {
                        "username": new_user, "email": new_email, "phone_number": new_phone,
                        "carrom_level": level, "password": new_pass
                    }
                    try:
                        res = requests.post(f"{API_URL}/register/", json=payload)
                        if res.status_code == 200:
                            st.success("Registration successful! Please go to the 'Sign In' tab to log in.")
                        else:
                            st.error(res.json().get("detail", "Registration failed."))
                    except Exception as e:
                        st.error("Backend connection failed.")


def show_main_app():
    st.markdown("<h1><span style='color:#7c6aff'>🎯</span> AI CARROM COACH</h1>", unsafe_allow_html=True)
    st.markdown(f"<div style='margin-bottom: 20px; color: var(--acc2);'>Logged in as: <strong>{st.session_state.current_user['username']}</strong> | Level: {st.session_state.current_user['level']}</div>", unsafe_allow_html=True)

    tab_sim, tab_az, tab_coach = st.tabs(["⚡ TRICK SIMULATOR", "📸 BOARD ANALYZER", "🤖 AI COACH"])

  
    with tab_sim:
        try:
            tricks_data = requests.get(f"{API_URL}/tricks/").json()["tricks"]
            tricks_json = json.dumps(tricks_data)
            
            simulator_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
            <link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
            <style>
                body {{ margin: 0; background: #090909; color: #e8e8e2; font-family: 'IBM Plex Mono', monospace; display: flex; height: 100vh; overflow: hidden; font-size: 13px; }}
                .sidebar {{ width: 260px; border-right: 1px solid #252525; display: flex; flex-direction: column; background: #090909; }}
                .sb-head {{ padding: 14px; font-size: 10px; color: #555; text-transform: uppercase; letter-spacing: 1.5px; font-weight: 500; }}
                .sb-scroll {{ flex: 1; overflow-y: auto; padding: 0 10px; }}
                .sb-scroll::-webkit-scrollbar {{ width: 3px; }}
                .sb-scroll::-webkit-scrollbar-thumb {{ background: #303030; border-radius: 2px; }}
                .trick-card {{ padding: 10px; border: 1px solid #252525; border-radius: 8px; margin-bottom: 5px; cursor: pointer; transition: 0.15s; }}
                .trick-card:hover {{ border-color: #303030; background: #181818; }}
                .trick-card.active {{ border-color: #7c6aff; background: rgba(124,106,255,0.12); }}
                .tc-name {{ font-family: 'Syne', sans-serif; font-size: 12px; font-weight: 700; flex: 1; }}
                .tc-tag {{ font-size: 10px; color: #555; }}
                .tc-diff {{ display: flex; gap: 3px; margin-left: auto; }}
                .tc-diff span {{ width: 5px; height: 5px; border-radius: 50%; background: #303030; display: inline-block; }}
                .tc-diff span.on {{ background: #f59e0b; }}
                .speed-row {{ display: flex; gap: 8px; padding: 10px 14px; border-top: 1px solid #252525; align-items: center; }}
                .sp-btn {{ background: #1e1e1e; border: 1px solid #252525; color: #999; border-radius: 4px; padding: 3px 8px; cursor: pointer; font-size: 10px; }}
                .sp-btn.on {{ background: rgba(124,106,255,0.12); border-color: #7c6aff; color: #a89bff; }}
                .sim-center {{ flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 16px; position: relative; }}
                canvas {{ border-radius: 4px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); display: block; }}
                .step-display {{ background: #181818; border: 1px solid #252525; border-radius: 8px; padding: 10px; width: 460px; margin-top: 15px; display: flex; gap: 10px; align-items: center; transition: 0.3s; }}
                .sim-right {{ width: 280px; border-left: 1px solid #252525; display: flex; flex-direction: column; }}
                .sr-head {{ padding: 14px; border-bottom: 1px solid #252525; }}
                .sr-title {{ font-family: 'Syne', sans-serif; font-size: 16px; font-weight: 800; }}
                .sr-body {{ padding: 14px; flex: 1; overflow-y: auto; display: flex; flex-direction: column; gap: 12px; }}
                .info-box {{ background: #181818; border: 1px solid #252525; border-radius: 8px; padding: 11px; }}
                .ib-label {{ font-size: 10px; color: #555; text-transform: uppercase; margin-bottom: 7px; }}
                .ib-desc {{ font-size: 11px; color: #999; line-height: 1.6; }}
                .abtn {{ width: 100%; padding: 10px; border-radius: 7px; font-weight: 500; cursor: pointer; border: none; font-family: 'IBM Plex Mono', monospace; }}
                .abtn.primary {{ background: #7c6aff; color: #fff; }}
                .abtn.primary:hover {{ background: #a89bff; }}
                .abtn.secondary {{ background: transparent; color: #a89bff; border: 1px solid #303030; }}
                .abtn.secondary:hover {{ border-color: #7c6aff; background: rgba(124,106,255,0.12); }}
                .abtn:disabled {{ opacity: 0.4; cursor: not-allowed; }}
            </style>
            </head>
            <body>
                <div class="sidebar">
                    <div class="sb-head">Trick Library</div>
                    <div class="sb-scroll" id="trick-list"></div>
                    <div class="speed-row">
                        <span style="font-size:10px;color:#555;letter-spacing:1px;text-transform:uppercase;">Speed</span>
                        <button class="sp-btn" id="sp-slow" onclick="setSpeed(0.3)">0.3x</button>
                        <button class="sp-btn on" id="sp-norm" onclick="setSpeed(1)">1x</button>
                        <button class="sp-btn" id="sp-fast" onclick="setSpeed(2)">2x</button>
                    </div>
                </div>

                <div class="sim-center">
                    <canvas id="cv" width="460" height="460"></canvas>
                    <div class="step-display" id="step-bar">
                        <div style="background:#7c6aff;color:white;width:22px;height:22px;border-radius:50%;text-align:center;line-height:22px;font-size:10px;font-weight:500;" id="s-num">-</div>
                        <div style="font-size:11px;color:#e8e8e2;line-height:1.6;" id="s-txt">Select a trick and press Watch Demo</div>
                    </div>
                </div>

                <div class="sim-right">
                    <div class="sr-head">
                        <div class="sr-title" id="t-name">Select Trick</div>
                        <div style="font-size:10px;color:#555;margin-top:2px;" id="t-tag">Choose from the library</div>
                    </div>
                    <div class="sr-body">
                        <div class="info-box">
                            <div class="ib-label">About this trick</div>
                            <div class="ib-desc" id="t-desc">Pick any trick from the sidebar.</div>
                        </div>
                        <div class="info-box">
                            <div class="ib-label">Key Tips</div>
                            <div class="ib-desc" id="t-tips" style="display:flex;flex-direction:column;gap:5px;"></div>
                        </div>
                        <div style="margin-top:auto;display:flex;flex-direction:column;gap:6px;">
                            <button id="demoBtn" class="abtn primary" onclick="watchDemo()">▶ Watch Demo</button>
                            <button id="replayBtn" class="abtn secondary" onclick="watchDemo()" disabled>↺ Replay</button>
                        </div>
                    </div>
                </div>

                <script>
                    const TRICKS = {tricks_json};
                    const canvas = document.getElementById('cv');
                    const ctx = canvas.getContext('2d');
                    
                    const CS=460, FR=24, BS=CS-FR*2, CX=CS/2, CY=CS/2;
                    const BL=FR, BR=FR+BS, BT=FR, BB=FR+BS, PR=12, SR=15, PK=18;
                    const FRICT=0.982, WALL_R=0.72, PC_R=0.88, STOP=0.08;
                    const PI=Math.PI;
                    
                    let activeTrick = null, pieces = [], striker = null, animFrame = null;
                    let ghostTrails = [], speed = 1, stepTimers = [];

                    function buildList() {{
                        const el = document.getElementById('trick-list');
                        TRICKS.forEach((t, i) => {{
                            const d = document.createElement('div');
                            d.className = 'trick-card'; d.id = 'tc-' + i;
                            d.onclick = () => selectTrick(i);
                            const dots = [...Array(5)].map((_,j) => `<span class="${{j < t.diff ? 'on' : ''}}"></span>`).join('');
                            d.innerHTML = `
                                <div style="display:flex;align-items:center;gap:7px;margin-bottom:4px;">
                                    <span style="font-size:15px;width:22px;text-align:center;">${{t.icon}}</span>
                                    <span class="tc-name">${{t.name}}</span>
                                    <div class="tc-diff">${{dots}}</div>
                                </div>
                                <div class="tc-tag" style="padding-left:29px;">${{t.tag}}</div>
                            `;
                            el.appendChild(d);
                        }});
                    }}

                    function selectTrick(idx) {{
                        activeTrick = TRICKS[idx];
                        document.querySelectorAll('.trick-card').forEach(c => c.classList.remove('active'));
                        document.getElementById('tc-' + idx).classList.add('active');
                        
                        document.getElementById('t-name').innerText = activeTrick.name;
                        document.getElementById('t-tag').innerText = activeTrick.tag;
                        document.getElementById('t-desc').innerText = activeTrick.desc;
                        document.getElementById('t-tips').innerHTML = activeTrick.tips.map(t => `<div style="display:flex;gap:7px;"><span style="color:#a89bff;">›</span><span>${{t}}</span></div>`).join('');
                        
                        document.getElementById('demoBtn').disabled = false;
                        document.getElementById('replayBtn').disabled = true;
                        setStep('-', 'Press Watch Demo to see the technique');
                        
                        pieces = activeTrick.pieces.map(p => ({{...p, vx: 0, vy: 0, out: false}}));
                        striker = {{x: activeTrick.shot.sx, y: BB-SR-2, vx: 0, vy: 0, isStr: true, out: false}};
                        
                        ghostTrails = preSimulate(activeTrick.pieces.map(p => ({{...p, vx:0, vy:0, out:false}})), activeTrick.shot);
                        draw();
                    }}

                    function setStep(num, txt) {{
                        document.getElementById('s-num').innerText = num;
                        document.getElementById('s-txt').innerText = txt;
                    }}

                    function setSpeed(s) {{
                        speed = s;
                        document.querySelectorAll('.sp-btn').forEach(b => b.classList.remove('on'));
                        document.getElementById(s===0.3?'sp-slow':s===1?'sp-norm':'sp-fast').classList.add('on');
                    }}

                    function physStep(simPieces, simStriker) {{
                        const objs = [...simPieces.filter(p=>!p.out), simStriker].filter(o=>o&&!o.out);
                        objs.forEach(o => {{
                            o.x += o.vx; o.y += o.vy; o.vx *= FRICT; o.vy *= FRICT;
                            const r = o.isStr ? SR : PR;
                            if(o.x-r < BL) {{ o.x = BL+r; o.vx = Math.abs(o.vx)*WALL_R; }}
                            if(o.x+r > BR) {{ o.x = BR-r; o.vx = -Math.abs(o.vx)*WALL_R; }}
                            if(o.y-r < BT) {{ o.y = BT+r; o.vy = Math.abs(o.vy)*WALL_R; }}
                            if(o.y+r > BB) {{ o.y = BB-r; o.vy = -Math.abs(o.vy)*WALL_R; }}
                            if(!o.isStr) {{
                                for(const[px,py] of [[BL,BT],[BR,BT],[BL,BB],[BR,BB]]) {{
                                    if(Math.hypot(o.x-px, o.y-py) < PK) {{ o.out = true; break; }}
                                }}
                            }}
                        }});
                        
                        for(let i=0; i<objs.length; i++) {{
                            for(let j=i+1; j<objs.length; j++) {{
                                const a = objs[i], b = objs[j];
                                if(a.out || b.out) continue;
                                const ra = a.isStr ? SR : PR, rb = b.isStr ? SR : PR, mn = ra+rb;
                                const dx = b.x-a.x, dy = b.y-a.y, d = Math.hypot(dx,dy);
                                if(d < mn && d > 0.01) {{
                                    const nx = dx/d, ny = dy/d, ov = (mn-d)*0.5;
                                    a.x -= nx*ov; a.y -= ny*ov; b.x += nx*ov; b.y += ny*ov;
                                    const dvn = (b.vx-a.vx)*nx + (b.vy-a.vy)*ny;
                                    if(dvn < 0) {{
                                        const imp = dvn*PC_R;
                                        a.vx += imp*nx; a.vy += imp*ny; b.vx -= imp*nx; b.vy -= imp*ny;
                                    }}
                                }}
                            }}
                        }}
                    }}

                    function preSimulate(ps, shot) {{
                        const rad = shot.ang*PI/180; const spd = shot.force*16;
                        const str = {{x: shot.sx, y: BB-SR-2, vx: Math.cos(rad)*spd, vy: Math.sin(rad)*spd, isStr: true, out: false}};
                        const trails = [{{type: 'striker', pts: [{{x: str.x, y: str.y}}]}}];
                        ps.forEach(p => trails.push({{type: p.t, pts: [{{x: p.x, y: p.y}}]}}));
                        for(let f=0; f<600; f++) {{
                            physStep(ps, str);
                            if(!str.out) trails[0].pts.push({{x: str.x, y: str.y}});
                            ps.forEach((p,i) => {{ if(!p.out) trails[i+1].pts.push({{x: p.x, y: p.y}}); }});
                            if([...ps, str].every(o => o.out || (Math.abs(o.vx)<STOP && Math.abs(o.vy)<STOP))) break;
                        }}
                        return trails;
                    }}

                    function drawFrame(){{
                        const g=ctx.createLinearGradient(0,0,CS,CS);
                        g.addColorStop(0,'#7a3a0a'); g.addColorStop(0.5,'#5a2a06'); g.addColorStop(1,'#3a1804');
                        ctx.fillStyle=g; ctx.fillRect(0,0,CS,CS);
                        ctx.strokeStyle='rgba(255,150,50,.3)'; ctx.lineWidth=1.5;
                        ctx.strokeRect(FR-1,FR-1,BS+2,BS+2);
                    }}

                    function drawSurface(){{
                        const g=ctx.createRadialGradient(CX,CY,30,CX,CY,BS*.68);
                        g.addColorStop(0,'#e8ddb4'); g.addColorStop(1,'#d4c898');
                        ctx.fillStyle=g; ctx.fillRect(BL,BT,BS,BS);
                    }}

                    function drawPockets(){{
                        [[BL,BT],[BR,BT],[BL,BB],[BR,BB]].forEach(([px,py])=>{{
                            ctx.beginPath(); ctx.arc(px,py,PK+4,0,PI*2);
                            ctx.fillStyle='rgba(0,0,0,.35)'; ctx.fill();
                            ctx.beginPath(); ctx.arc(px,py,PK,0,PI*2);
                            const g=ctx.createRadialGradient(px-3,py-3,1,px,py,PK);
                            g.addColorStop(0,'#160800'); g.addColorStop(1,'#000');
                            ctx.fillStyle=g; ctx.fill();
                        }});
                    }}

                    function drawLines(){{
                        ctx.strokeStyle='rgba(160,120,50,.6)'; ctx.lineWidth=0.8;
                        const o=10, i=34;
                        ctx.strokeRect(BL+o,BT+o,BS-o*2,BS-o*2);
                        ctx.strokeRect(BL+i,BT+i,BS-i*2,BS-i*2);
                        ctx.beginPath();
                        [[BL+o,BT+o,BL+i,BT+i],[BR-o,BT+o,BR-i,BT+i],[BL+o,BB-o,BL+i,BB-i],[BR-o,BB-o,BR-i,BB-i]].forEach(([x1,y1,x2,y2])=>{{ctx.moveTo(x1,y1);ctx.lineTo(x2,y2);}});
                        ctx.stroke();
                        ctx.strokeStyle='rgba(160,120,50,.2)'; ctx.lineWidth=0.6;
                        ctx.beginPath(); ctx.moveTo(CX,BT+i); ctx.lineTo(CX,BB-i); ctx.stroke();
                        ctx.beginPath();
                        ctx.moveTo(BL+i,CY); ctx.lineTo(BR-i,CY); ctx.stroke();
                        const hw=BS*.36;
                        ctx.strokeStyle='rgba(100,80,180,.35)'; ctx.lineWidth=1; ctx.setLineDash([4,4]);
                        ctx.beginPath(); ctx.moveTo(CX-hw,BB-SR-2); ctx.lineTo(CX+hw,BB-SR-2); ctx.stroke();
                        ctx.setLineDash([]);
                    }}

                    function drawCenter(){{
                        ctx.strokeStyle='rgba(160,120,50,.7)'; ctx.lineWidth=1;
                        ctx.beginPath(); ctx.arc(CX,CY,42,0,PI*2); ctx.stroke();
                        ctx.beginPath(); ctx.arc(CX,CY,13,0,PI*2); ctx.stroke();
                        ctx.beginPath(); ctx.arc(CX,CY,3,0,PI*2);
                        ctx.fillStyle='#aa2020'; ctx.fill();
                    }}

                    function drawPiece(p){{
                        const base=p.t==='bk'?'#1a1a1a':p.t==='wh'?'#f2f0e8':'#c01010';
                        const shine=p.t==='bk'?'#444':p.t==='wh'?'#fff':'#ee5555';
                        ctx.beginPath(); ctx.arc(p.x+2,p.y+2,PR,0,PI*2);
                        ctx.fillStyle='rgba(0,0,0,.25)'; ctx.fill(); 
                        const g=ctx.createRadialGradient(p.x-3,p.y-3,1,p.x,p.y,PR);
                        g.addColorStop(0,shine); g.addColorStop(.4,base); g.addColorStop(1,base);
                        ctx.beginPath(); ctx.arc(p.x,p.y,PR,0,PI*2);
                        ctx.fillStyle=g; ctx.fill();
                        ctx.strokeStyle=p.t==='wh'?'rgba(0,0,0,.1)':'rgba(255,255,255,.1)';
                        ctx.lineWidth=0.5; ctx.stroke();
                    }}

                    function drawStriker(x,y){{
                        ctx.beginPath(); ctx.arc(x+2,y+2,SR,0,PI*2);
                        ctx.fillStyle='rgba(0,0,0,.25)'; ctx.fill();
                        const g=ctx.createRadialGradient(x-4,y-4,2,x,y,SR);
                        g.addColorStop(0,'#8899cc'); g.addColorStop(.5,'#334466'); g.addColorStop(1,'#111820');
                        ctx.beginPath(); ctx.arc(x,y,SR,0,PI*2);
                        ctx.fillStyle=g; ctx.fill();
                        ctx.strokeStyle='rgba(120,150,200,.4)'; ctx.lineWidth=0.8; ctx.stroke();
                    }}

                    function draw() {{
                        ctx.clearRect(0, 0, CS, CS);
                        drawFrame(); drawSurface(); drawPockets(); drawLines(); drawCenter();

                        if(ghostTrails.length > 0) {{
                            ghostTrails.forEach(trail => {{
                                if(trail.pts.length < 2) return;
                                ctx.beginPath(); ctx.moveTo(trail.pts[0].x, trail.pts[0].y);
                                for(let i=1; i<trail.pts.length; i+=3) ctx.lineTo(trail.pts[i].x, trail.pts[i].y);
                                ctx.strokeStyle = trail.type==='striker' ? 'rgba(124,106,255,0.5)' : 'rgba(180,180,160,0.5)';
                                ctx.lineWidth = 2; ctx.stroke();
                            }});
                        }}

                        pieces.filter(p=>!p.out).forEach(drawPiece);
                        if(striker && !striker.out) drawStriker(striker.x, striker.y);
                    }}

                    function watchDemo() {{
                        if(animFrame) cancelAnimationFrame(animFrame);
                        stepTimers.forEach(clearTimeout); stepTimers = [];
                        
                        document.getElementById('demoBtn').disabled = true;
                        document.getElementById('replayBtn').disabled = true;
                        
                        pieces = activeTrick.pieces.map(p => ({{...p, vx: 0, vy: 0, out: false}}));
                        striker = {{x: activeTrick.shot.sx, y: BB-SR-2, vx: 0, vy: 0, isStr: true, out: false}};
                        
                        ghostTrails = preSimulate(activeTrick.pieces.map(p => ({{...p, vx:0, vy:0, out:false}})), activeTrick.shot);
                        setStep('👀', 'Ghost trajectory preview — watch where each piece will travel');
                        
                        document.getElementById('step-bar').style.borderColor = '#7c6aff';
                        draw();
                        
                        const delay = 2200 / speed;
                        
                        setTimeout(() => {{
                            ghostTrails = []; 
                            document.getElementById('step-bar').style.borderColor = '#252525';
                            
                            const rad = activeTrick.shot.ang*PI/180; 
                            const spd = activeTrick.shot.force*16;
                            striker.vx = Math.cos(rad)*spd;
                            striker.vy = Math.sin(rad)*spd;
                            
                            activeTrick.steps.forEach((s, i) => {{
                                stepTimers.push(setTimeout(() => setStep(i+1, s.msg), s.t / speed));
                            }});
                            
                            animLoop();
                        }}, delay);
                    }}

                    function animLoop() {{
                        const steps = Math.max(1, Math.round(speed * 2));
                        for(let i=0; i<steps; i++) physStep(pieces, striker);
                        draw();
                        
                        const done = [...pieces, striker].every(o => o.out || (Math.abs(o.vx)<STOP && Math.abs(o.vy)<STOP));
                        if(!done) {{
                            animFrame = requestAnimationFrame(animLoop);
                        }} else {{
                            document.getElementById('demoBtn').disabled = false;
                            document.getElementById('replayBtn').disabled = false;
                            setStep('✓', 'Trick complete!');
                        }}
                    }}

                    buildList();
                    selectTrick(0);
                </script>
            </body>
            </html>
            """
            components.html(simulator_html, height=650)
        except Exception as e:
            pass

   
    with tab_az:
        col_az_main, col_az_side = st.columns([3, 1], gap="large")
        with col_az_main:
            st.markdown("<h3 style='color: white;'>Board Analyzer</h3>", unsafe_allow_html=True)
            uploaded_file = st.file_uploader("Upload Board Photo", label_visibility="collapsed", type=["jpg", "jpeg", "png", "webp"])
            if uploaded_file is not None:
                st.image(uploaded_file, use_container_width=True)
                
        with col_az_side:
            st.markdown("<h3 style='color: white;'>Analysis Results</h3>", unsafe_allow_html=True)
            if uploaded_file is not None:
                if st.button("🔍 Analyze Board Position", type="primary"):
                    with st.spinner("Analyzing..."):
                        img_base64 = base64.b64encode(uploaded_file.read()).decode("utf-8")
                        try:
                            res = requests.post(f"{API_URL}/analyze/", json={"image_base64": img_base64}).json()
                            st.session_state.boards_analyzed += 1 
                            st.markdown(f"**⚫ Black:** {res.get('black', '?')} | **⚪ White:** {res.get('white', '?')} | **♛ Queen:** {'Yes' if res.get('queen') else 'No'}")
                            st.info(res.get("situation", "Situation analyzed."))
                            for i, shot in enumerate(res.get("shots", [])):
                                with st.expander(f"Shot {i+1}: {shot.get('type')}"):
                                    st.write(f"**Aim:** {shot.get('direction')}")
                                    st.write(f"{shot.get('description')}")
                        except Exception as e:
                            st.error("Analysis Failed.")
            else:
                st.info("Upload a board photo to begin analysis.")

    
    with tab_coach:
        col_coach_left, col_coach_main = st.columns([1, 4], gap="large")
        
        with col_coach_left:
            st.markdown("<div class='sb-head' style='color:#555; font-size:10px; letter-spacing:1.5px;'>PLAYER PROFILE</div>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class="profile-box">
                <div class="profile-stat"><span>User</span><span class="val" style="color:#a89bff">{st.session_state.current_user['username']}</span></div>
                <div class="profile-stat"><span>Questions</span><span class="val">{st.session_state.coach_q}</span></div>
                <div class="profile-stat"><span>Boards</span><span class="val">{st.session_state.boards_analyzed}</span></div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<div class='sb-head' style='color:#555; font-size:10px; letter-spacing:1.5px;'>CHOOSE YOUR COACH</div>", unsafe_allow_html=True)
            coach_options = list(avatar_map.keys())
            selected_coach = st.selectbox("Select Coach", coach_options, index=coach_options.index(st.session_state.coach_name), label_visibility="collapsed")
            
            if selected_coach != st.session_state.coach_name:
                st.session_state.coach_name = selected_coach
                st.session_state.messages.append({"role": "assistant", "content": f"Hi! I am {selected_coach}, stepping in as your new expert coach. Let's elevate your game!", "coach_name": selected_coach})
                st.rerun()
                
            st.markdown("<br><div class='sb-head' style='color:#555; font-size:10px; letter-spacing:1.5px;'>QUICK QUESTIONS</div>", unsafe_allow_html=True)
            if st.button("📋 Official Rules"): st.session_state.preset_q = "What are the official carrom rules?"
            if st.button("👍 Thumb Shot"): st.session_state.preset_q = "Explain the thumb shot technique"
            if st.button("♛ Queen Tips"): st.session_state.preset_q = "How do I pocket the queen safely?"
            
            # Logout Button
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🚪 Logout"):
                st.session_state.clear()
                st.rerun()

        with col_coach_main:
            for message in st.session_state.messages:
                if message["role"] == "assistant":
                    msg_coach_name = message.get("coach_name", st.session_state.coach_name)
                    avatar = get_avatar_image(msg_coach_name)
                else:
                    avatar = "👤"
                    
                with st.chat_message(message["role"], avatar=avatar):
                    content = message["content"]
                    yt_links = re.findall(r'(https?://(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)[\w-]+)', content)
                    clean_content = re.sub(r'https?://(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)[\w-]+', '', content).strip()
                    
                    st.markdown(clean_content)
                    if message["role"] == "assistant":
                        seen = set()
                        for link in yt_links:
                            if link not in seen:
                                st.video(link) 
                                seen.add(link)

            user_input = st.chat_input("Ask about rules, technique, strategy...")
            prompt = st.session_state.preset_q or user_input
            
            if prompt:
                st.session_state.preset_q = None 
                st.session_state.coach_q += 1
                st.session_state.messages.append({"role": "user", "content": prompt})
                
                with st.chat_message("user", avatar="👤"):
                    st.markdown(prompt)

                safe_avatar = get_avatar_image(st.session_state.coach_name)
                with st.chat_message("assistant", avatar=safe_avatar):
                    with st.spinner(f"{st.session_state.coach_name} is thinking..."):
                        try:
                            safe_messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                            res = requests.post(f"{API_URL}/coach/", json={"messages": safe_messages, "coach_name": st.session_state.coach_name }).json()
                            raw_ai_response = res["response"]
                            
                            yt_links = re.findall(r'(https?://(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)[\w-]+)', raw_ai_response)
                            clean_content = re.sub(r'https?://(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)[\w-]+', '', raw_ai_response).strip()
                            
                            st.markdown(clean_content)
                            seen = set()
                            for link in yt_links:
                                if link not in seen:
                                    st.video(link)
                                    seen.add(link)
                            
                            st.session_state.messages.append({"role": "assistant", "content": raw_ai_response, "coach_name": st.session_state.coach_name})
                            st.rerun() 
                        except Exception as e:
                            st.error(f"Error communicating with AI Coach backend: {e}")



if st.session_state.page == "landing":
    show_landing_page()
elif st.session_state.page == "auth":
    show_auth_page()
elif st.session_state.page == "main_app":
    show_main_app()
