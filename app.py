import html
import json
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Hello World Motion Lab", page_icon="✨", layout="wide")

st.title("✨ Hello World Motion Lab")
st.caption("A tiny interactive app for experimenting with names, fonts, backgrounds, and motion.")

with st.sidebar:
    st.header("Your design")
    name = st.text_input("Enter your name", value="Hello World", max_chars=80)
    font_family = st.selectbox(
        "Font type",
        ["Arial", "Courier New", "Georgia", "Times New Roman", "Verdana", "Trebuchet MS", "Impact"],
    )
    font_size = st.slider("Font size", min_value=20, max_value=100, value=48, step=2)
    background = st.selectbox(
        "Background",
        ["Light", "Dark", "Ocean", "Sunset", "Forest", "Lavender"],
    )
    name_mode = st.selectbox("Name display mode", ["Centered", "Ticker Tape", "Repeated"])
    effect = st.selectbox(
        "Dynamic action",
        ["None", "Rain", "Snow", "Hail", "Wind gust", "Confetti", "Tornado"],
    )
    speed = st.slider("Animation speed", min_value=1, max_value=10, value=5,
                      help="1 is gentle and 10 is fast.")
    st.caption("Animations run in the preview area and loop continuously.")

themes = {
    "Light": ("#f8fafc", "#111827", "#dbeafe"),
    "Dark": ("#080d1a", "#f8fafc", "#1e293b"),
    "Ocean": ("#063b52", "#ecfeff", "#0e7490"),
    "Sunset": ("#3b164b", "#fff7ed", "#9d174d"),
    "Forest": ("#102a22", "#f0fdf4", "#166534"),
    "Lavender": ("#f3e8ff", "#3b0764", "#ddd6fe"),
}
bg_color, text_color, accent_color = themes[background]

# JSON encoding safely passes user input into the embedded JavaScript.
name_json = json.dumps(name or "Hello World")
font_json = json.dumps(font_family)
bg_json = json.dumps(bg_color)
text_json = json.dumps(text_color)
accent_json = json.dumps(accent_color)
mode_json = json.dumps(name_mode)
effect_json = json.dumps(effect)
speed_value = speed

html_doc = f"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  * {{ box-sizing: border-box; }}
  html, body {{ margin: 0; padding: 0; width: 100%; height: 100%; }}
  body {{ font-family: Arial, sans-serif; }}
  #stage {{
    position: relative; height: 590px; width: 100%; overflow: hidden;
    background: {bg_json}; color: {text_json}; border-radius: 18px;
    border: 1px solid rgba(148,163,184,.35);
    isolation: isolate;
  }}
  #glow {{
    position: absolute; inset: 0; z-index: 0; pointer-events: none;
    background: radial-gradient(ellipse at 50% 45%, {accent_json} 0%, transparent 68%);
    opacity: .62;
  }}
  #particles {{ position: absolute; inset: 0; z-index: 1; overflow: hidden; pointer-events:none; }}
  .particle {{ position:absolute; top:-12%; left:var(--x); font-size:var(--size);
    opacity:var(--opacity); animation: var(--animation) var(--duration) linear infinite;
    animation-delay:var(--delay); will-change:transform; user-select:none; }}
  @keyframes fall {{ from {{ transform:translate3d(0,-8vh,0) rotate(0deg); }}
    to {{ transform:translate3d(var(--drift),115vh,0) rotate(360deg); }} }}
  @keyframes gust {{ 0% {{ transform:translate(-20vw,0) rotate(-10deg); }}
    100% {{ transform:translate(120vw, var(--drift-y)) rotate(15deg); }} }}
  @keyframes spin {{ from {{ transform:rotate(0deg) translateX(20px) rotate(0deg); }}
    to {{ transform:rotate(360deg) translateX(20px) rotate(-360deg); }} }}
  @keyframes confetti {{ from {{ transform:translateY(-10vh) rotate(0deg); }}
    to {{ transform:translateY(115vh) rotate(900deg); }} }}
  #name-wrap {{
    position:absolute; z-index:3; inset:0; display:flex; align-items:center;
    justify-content:center; padding:24px; overflow:hidden;
  }}
  #name {{
    font-family:{font_json}, sans-serif; font-size:{font_size}px; font-weight:700;
    line-height:1.18; color:{text_json}; text-align:center; overflow-wrap:anywhere;
    text-shadow: 0 3px 18px rgba(0,0,0,.18); max-width:100%;
  }}
  #name.repeated {{ display:flex; flex-direction:column; gap:.25em; align-items:center; }}
  #name.repeated span {{ display:block; }}
  #name.ticker {{ white-space:nowrap; max-width:none; animation:ticker var(--ticker-duration) linear infinite; }}
  @keyframes ticker {{ from {{ transform:translateX(105%); }} to {{ transform:translateX(-105%); }} }}
  #hint {{ position:absolute; z-index:4; bottom:14px; left:0; right:0; text-align:center;
    font:12px Arial,sans-serif; opacity:.65; padding:0 12px; }}
  @media (prefers-reduced-motion: reduce) {{
    .particle, #name.ticker {{ animation-duration: 30s !important; }}
  }}
</style>
</head>
<body>
<div id="stage">
  <div id="glow"></div>
  <div id="particles" aria-hidden="true"></div>
  <div id="name-wrap"><div id="name"></div></div>
  <div id="hint">HELLO WORLD MOTION LAB · LIVE PREVIEW</div>
</div>
<script>
(() => {{
  const nameText = {name_json};
  const mode = {mode_json};
  const effect = {effect_json};
  const speed = {speed_value};
  const nameEl = document.getElementById("name");
  const particles = document.getElementById("particles");
  const stage = document.getElementById("stage");

  if (mode === "Repeated") {{
    nameEl.className = "repeated";
    for (let i = 0; i < 5; i++) {{
      const line = document.createElement("span");
      line.textContent = nameText;
      nameEl.appendChild(line);
    }}
  }} else {{
    nameEl.textContent = nameText;
    if (mode === "Ticker Tape") {{
      nameEl.className = "ticker";
      nameEl.style.setProperty("--ticker-duration", (18 / speed) + "s");
    }}
  }}

  const sets = {{
    "Rain": ["💧", "💦"],
    "Snow": ["❄", "❅", "❆", "✳"],
    "Hail": ["🧊", "●"],
    "Wind gust": ["〰", "➝", "💨"],
    "Confetti": ["🎉", "🎊", "🟣", "🟡", "🟢", "🔵", "✦"],
    "Tornado": ["🌪"]
  }};
  const symbols = sets[effect] || [];
  const count = effect === "Tornado" ? 12 : (effect === "Wind gust" ? 26 : 65);
  for (let i = 0; i < count && symbols.length; i++) {{
    const p = document.createElement("span");
    p.className = "particle";
    p.textContent = symbols[Math.floor(Math.random() * symbols.length)];
    p.style.setProperty("--x", (Math.random() * 100) + "%");
    p.style.setProperty("--size", (effect === "Tornado" ? 20 + Math.random()*25 : 12 + Math.random()*18) + "px");
    p.style.setProperty("--opacity", (0.35 + Math.random()*0.65).toFixed(2));
    p.style.setProperty("--duration", ((effect === "Tornado" ? 5 : 9 + Math.random()*12) / (0.45 + speed/5)) + "s");
    p.style.setProperty("--delay", (-Math.random() * 20) + "s");
    p.style.setProperty("--drift", ((Math.random() - 0.5) * 220) + "px");
    p.style.setProperty("--drift-y", ((Math.random() - 0.5) * 180) + "px");
    if (effect === "Wind gust") {{
      p.style.top = (Math.random() * 90) + "%";
      p.style.setProperty("--animation", "gust");
    }} else if (effect === "Tornado") {{
      p.style.top = (15 + Math.random()*65) + "%";
      p.style.left = (40 + Math.random()*20) + "%";
      p.style.setProperty("--animation", "spin");
    }} else if (effect === "Confetti") {{
      p.style.setProperty("--animation", "confetti");
    }} else {{
      p.style.setProperty("--animation", "fall");
    }}
    particles.appendChild(p);
  }}
}})();
</script>
</body>
</html>
"""

components.html(html_doc, height=610, scrolling=False)

st.markdown("**Try it:** change your name, choose a font and background, then switch the dynamic action to see the preview update.")
