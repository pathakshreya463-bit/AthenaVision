"""
components/hero.py

Full-viewport hero section for the AthenaVision landing page.

Renders a self-contained HTML/CSS/JS block (via streamlit.components.v1.html)
so that canvas-based starfield, floating particles, cursor-parallax, and the
looping subtitle animation all run client-side without a Streamlit rerun.

Usage:
    from components.hero import render_hero
    render_hero()
"""

import streamlit as st
import streamlit.components.v1 as components


# --------------------------------------------------------------------------
# Config
# --------------------------------------------------------------------------
HERO_HEIGHT_PX = 900          # rendered iframe height -> "first screen"
STAR_COUNT = 140              # background starfield density
PARTICLE_COUNT = 34           # floating particle density
ROTATING_WORDS = ["Observe.", "Understand.", "Optimize."]


def hero() -> None:
    """Render the AthenaVision hero section, occupying the first screen."""
    st.markdown(
        """
        <style>
        /* collapse Streamlit's default block padding above the hero iframe */
        div[data-testid="stVerticalBlock"] > div:has(> iframe[title="hero"]) {
            margin: -1rem -1rem 0 -1rem;
        }
        iframe[title="hero"] { display: block; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    words_js_array = ", ".join(f"'{w}'" for w in ROTATING_WORDS)

    hero_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8" />
<style>
  @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

  :root {{
    --bg-void: #05060f;
    --bg-deep: #0a0d1f;
    --accent-violet: #7c5cff;
    --accent-cyan: #4cc9f0;
    --accent-gold: #ffd166;
    --text-primary: #f4f5fb;
    --text-secondary: #b8bcd4;
    --text-muted: #7a7f9e;
    --font-display: 'Space Grotesk', 'Segoe UI', sans-serif;
    --font-body: 'Inter', 'Segoe UI', sans-serif;
    --font-mono: 'JetBrains Mono', Consolas, monospace;
  }}

  * {{ box-sizing: border-box; margin: 0; padding: 0; }}

  html, body {{
    width: 100%;
    height: 100%;
    background: var(--bg-void);
    overflow: hidden;
    cursor: default;
  }}

  /* ---------------------------------------------------------------- */
  /* STAGE                                                             */
  /* ---------------------------------------------------------------- */
  #hero-stage {{
    position: relative;
    width: 100%;
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    background: radial-gradient(ellipse at 50% 20%, #1a1442 0%, #0e1230 40%, #05060f 80%);
    background-size: 200% 200%;
    animation: nebulaDrift 24s ease-in-out infinite;
  }}

  @keyframes nebulaDrift {{
    0%   {{ background-position: 30% 20%; }}
    50%  {{ background-position: 70% 60%; }}
    100% {{ background-position: 30% 20%; }}
  }}

  /* canvases stack: stars (back) -> particles (mid) -> content (front) */
  #stars-canvas, #particles-canvas {{
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
  }}
  #stars-canvas {{ z-index: 1; }}
  #particles-canvas {{ z-index: 2; }}

  /* ambient light pools, react subtly to cursor via JS transform */
  #glow-layer {{
    position: absolute;
    inset: 0;
    z-index: 1;
    pointer-events: none;
    transition: transform 0.6s ease-out;
  }}

  .glow-orb {{
    position: absolute;
    border-radius: 50%;
    filter: blur(80px);
    opacity: 0.55;
  }}
  .glow-orb--violet {{
    width: 46vw; height: 46vw;
    top: 8%; left: 12%;
    background: radial-gradient(circle, rgba(124,92,255,0.55), transparent 70%);
  }}
  .glow-orb--cyan {{
    width: 38vw; height: 38vw;
    bottom: 4%; right: 10%;
    background: radial-gradient(circle, rgba(76,201,240,0.42), transparent 70%);
  }}
  .glow-orb--gold {{
    width: 22vw; height: 22vw;
    top: 46%; left: 44%;
    background: radial-gradient(circle, rgba(255,209,102,0.18), transparent 70%);
  }}

  /* ---------------------------------------------------------------- */
  /* CONTENT                                                           */
  /* ---------------------------------------------------------------- */
  #hero-content {{
    position: relative;
    z-index: 5;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    padding: 0 6vw;
    transition: transform 0.4s cubic-bezier(0.16,1,0.3,1);
    will-change: transform;
  }}

  .hero-eyebrow {{
    font-family: var(--font-mono);
    font-size: 0.8rem;
    letter-spacing: 0.35em;
    text-transform: uppercase;
    color: var(--accent-cyan);
    opacity: 0;
    animation: fadeUp 0.9s 0.15s ease-out forwards;
  }}

  .hero-title {{
    font-family: var(--font-display);
    font-weight: 700;
    font-size: clamp(3.2rem, 9vw, 7.5rem);
    letter-spacing: -0.03em;
    line-height: 1;
    margin-top: 1.1rem;
    background: linear-gradient(120deg, #ffffff 0%, #cfc9ff 35%, #7c5cff 70%, #4cc9f0 100%);
    background-size: 200% auto;
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    filter: drop-shadow(0 0 45px rgba(124, 92, 255, 0.45));
    opacity: 0;
    animation: fadeUp 1s 0.3s ease-out forwards, shimmer 6s linear infinite 1.3s;
  }}

  @keyframes shimmer {{
    0%   {{ background-position: 0% center; }}
    100% {{ background-position: 200% center; }}
  }}

  /* rotating subtitle: Observe. / Understand. / Optimize. */
  #hero-rotator {{
    margin-top: 1.6rem;
    height: 2.6rem;
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0;
    animation: fadeUp 0.9s 0.55s ease-out forwards;
  }}

  #hero-rotator span {{
    font-family: var(--font-display);
    font-weight: 600;
    font-size: clamp(1.3rem, 2.6vw, 1.9rem);
    color: var(--text-primary);
    position: relative;
  }}

  #hero-rotator span::after {{
    content: "";
    position: absolute;
    left: -0.15em; right: -0.15em; bottom: -0.35em;
    height: 2px;
    background: linear-gradient(90deg, var(--accent-violet), var(--accent-cyan));
    transform: scaleX(0.3);
    opacity: 0.7;
  }}

  .hero-description {{
    margin-top: 1.6rem;
    max-width: 620px;
    font-family: var(--font-body);
    font-size: clamp(1rem, 1.3vw, 1.15rem);
    line-height: 1.7;
    color: var(--text-secondary);
    opacity: 0;
    animation: fadeUp 0.9s 0.75s ease-out forwards;
  }}

  @keyframes fadeUp {{
    from {{ opacity: 0; transform: translateY(22px); }}
    to   {{ opacity: 1; transform: translateY(0); }}
  }}

  /* ---------------------------------------------------------------- */
  /* SCROLL INDICATOR                                                  */
  /* ---------------------------------------------------------------- */
  #scroll-indicator {{
    position: absolute;
    bottom: 5%;
    left: 50%;
    transform: translateX(-50%);
    z-index: 5;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.6rem;
    opacity: 0;
    animation: fadeUp 0.9s 1.1s ease-out forwards;
  }}

  #scroll-indicator .label {{
    font-family: var(--font-mono);
    font-size: 0.68rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: var(--text-muted);
  }}

  .scroll-mouse {{
    width: 24px;
    height: 38px;
    border: 1.5px solid rgba(184, 188, 212, 0.5);
    border-radius: 14px;
    position: relative;
  }}

  .scroll-mouse::before {{
    content: "";
    position: absolute;
    top: 6px;
    left: 50%;
    width: 4px;
    height: 8px;
    background: var(--accent-cyan);
    border-radius: 2px;
    transform: translateX(-50%);
    animation: scrollDot 1.8s ease-in-out infinite;
    box-shadow: 0 0 8px rgba(76, 201, 240, 0.8);
  }}

  @keyframes scrollDot {{
    0%   {{ opacity: 1; top: 6px; }}
    70%  {{ opacity: 0; top: 20px; }}
    100% {{ opacity: 0; top: 6px; }}
  }}

  /* vignette to keep edges of the "first screen" feeling contained */
  #vignette {{
    position: absolute;
    inset: 0;
    z-index: 4;
    pointer-events: none;
    background: radial-gradient(ellipse at center, transparent 55%, rgba(5,6,15,0.75) 100%);
  }}
</style>
</head>
<body>

  <div id="hero-stage">

    <canvas id="stars-canvas"></canvas>
    <canvas id="particles-canvas"></canvas>

    <div id="glow-layer">
      <div class="glow-orb glow-orb--violet"></div>
      <div class="glow-orb glow-orb--cyan"></div>
      <div class="glow-orb glow-orb--gold"></div>
    </div>

    <div id="vignette"></div>

    <div id="hero-content">
      <div class="hero-eyebrow">Intelligent Vision Analytics</div>
      <h1 class="hero-title">ATHENAVISION</h1>
      <div id="hero-rotator"><span id="rotator-word">Observe.</span></div>
      <p class="hero-description">
        Transforming academic spaces through intelligent vision analytics for
        classrooms, libraries and collaborative learning environments.
      </p>
    </div>

    <div id="scroll-indicator">
      <div class="scroll-mouse"></div>
      <div class="label">Scroll</div>
    </div>

  </div>

<script>
(function () {{
  const stage = document.getElementById('hero-stage');
  const starsCanvas = document.getElementById('stars-canvas');
  const particlesCanvas = document.getElementById('particles-canvas');
  const starsCtx = starsCanvas.getContext('2d');
  const particlesCtx = particlesCanvas.getContext('2d');
  const content = document.getElementById('hero-content');
  const glowLayer = document.getElementById('glow-layer');

  let W = window.innerWidth;
  let H = window.innerHeight;

  function resize() {{
    W = stage.clientWidth;
    H = stage.clientHeight;
    [starsCanvas, particlesCanvas].forEach(c => {{
      c.width = W;
      c.height = H;
    }});
  }}
  resize();
  window.addEventListener('resize', resize);

  // ---------------------------------------------------------------
  // STARFIELD — random positions, soft independent twinkle, subtle only
  // ---------------------------------------------------------------
  const STAR_COUNT = {STAR_COUNT};
  const stars = Array.from({{ length: STAR_COUNT }}).map(() => ({{
    x: Math.random() * W,
    y: Math.random() * H,
    r: Math.random() * 1.3 + 0.3,
    baseAlpha: Math.random() * 0.5 + 0.15,
    phase: Math.random() * Math.PI * 2,
    speed: Math.random() * 0.015 + 0.006,
    parallax: Math.random() * 0.02 + 0.005
  }}));

  function drawStars(t, mx, my) {{
    starsCtx.clearRect(0, 0, W, H);
    for (const s of stars) {{
      const twinkle = Math.sin(t * s.speed + s.phase) * 0.5 + 0.5;
      const alpha = s.baseAlpha * (0.5 + twinkle * 0.5);
      const px = s.x + (mx - W / 2) * s.parallax;
      const py = s.y + (my - H / 2) * s.parallax;
      starsCtx.beginPath();
      starsCtx.arc(px, py, s.r, 0, Math.PI * 2);
      starsCtx.fillStyle = `rgba(244, 245, 251, ${{alpha}})`;
      starsCtx.fill();
    }}
  }}

  // ---------------------------------------------------------------
  // FLOATING PARTICLES — slow upward drift, gentle sideways sway
  // ---------------------------------------------------------------
  const PARTICLE_COUNT = {PARTICLE_COUNT};
  const palette = ['124,92,255', '76,201,240', '255,209,102'];
  const particles = Array.from({{ length: PARTICLE_COUNT }}).map(() => resetParticle(true));

  function resetParticle(initial) {{
    return {{
      x: Math.random() * W,
      y: initial ? Math.random() * H : H + 20,
      r: Math.random() * 2.2 + 0.8,
      speedY: Math.random() * 0.35 + 0.12,
      swayAmp: Math.random() * 18 + 6,
      swaySpeed: Math.random() * 0.008 + 0.003,
      phase: Math.random() * Math.PI * 2,
      color: palette[Math.floor(Math.random() * palette.length)],
      alpha: Math.random() * 0.35 + 0.15
    }};
  }}

  function drawParticles(t) {{
    particlesCtx.clearRect(0, 0, W, H);
    for (const p of particles) {{
      p.y -= p.speedY;
      const sway = Math.sin(t * p.swaySpeed + p.phase) * p.swayAmp;
      const px = p.x + sway;
      if (p.y < -20) Object.assign(p, resetParticle(false));

      particlesCtx.beginPath();
      particlesCtx.arc(px, p.y, p.r, 0, Math.PI * 2);
      particlesCtx.fillStyle = `rgba(${{p.color}}, ${{p.alpha}})`;
      particlesCtx.shadowBlur = 8;
      particlesCtx.shadowColor = `rgba(${{p.color}}, 0.6)`;
      particlesCtx.fill();
    }}
  }}

  // ---------------------------------------------------------------
  // MOUSE INTERACTION — cursor parallax on content + glow orbs + stars
  // (placeholder hook: extend `onPointerMove` for richer interactions,
  //  e.g. custom cursor, ripple-on-click, magnetic buttons, etc.)
  // ---------------------------------------------------------------
  let mouseX = W / 2;
  let mouseY = H / 2;
  let targetMouseX = mouseX;
  let targetMouseY = mouseY;

  function onPointerMove(e) {{
    const rect = stage.getBoundingClientRect();
    targetMouseX = e.clientX - rect.left;
    targetMouseY = e.clientY - rect.top;
  }}
  stage.addEventListener('mousemove', onPointerMove);
  stage.addEventListener('touchmove', (e) => {{
    if (e.touches && e.touches[0]) {{
      const rect = stage.getBoundingClientRect();
      targetMouseX = e.touches[0].clientX - rect.left;
      targetMouseY = e.touches[0].clientY - rect.top;
    }}
  }}, {{ passive: true }});

  function updateParallax() {{
    // ease toward target for smooth motion
    mouseX += (targetMouseX - mouseX) * 0.05;
    mouseY += (targetMouseY - mouseY) * 0.05;

    const nx = (mouseX / W) - 0.5;   // -0.5 .. 0.5
    const ny = (mouseY / H) - 0.5;

    content.style.transform = `translate(${{nx * -14}}px, ${{ny * -10}}px)`;
    glowLayer.style.transform = `translate(${{nx * 22}}px, ${{ny * 18}}px)`;
  }}

  // ---------------------------------------------------------------
  // ROTATING SUBTITLE — Observe. / Understand. / Optimize.
  // ---------------------------------------------------------------
  const words = [{words_js_array}];
  const rotatorEl = document.getElementById('rotator-word');
  let wordIndex = 0;

  function cycleWord() {{
    rotatorEl.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
    rotatorEl.style.opacity = '0';
    rotatorEl.style.transform = 'translateY(8px)';
    setTimeout(() => {{
      wordIndex = (wordIndex + 1) % words.length;
      rotatorEl.textContent = words[wordIndex];
      rotatorEl.style.transform = 'translateY(-8px)';
      requestAnimationFrame(() => {{
        rotatorEl.style.opacity = '1';
        rotatorEl.style.transform = 'translateY(0)';
      }});
    }}, 420);
  }}
  setInterval(cycleWord, 2200);

  // ---------------------------------------------------------------
  // MAIN LOOP
  // ---------------------------------------------------------------
  function frame(t) {{
    updateParallax();
    drawStars(t, mouseX, mouseY);
    drawParticles(t * 0.06);
    requestAnimationFrame(frame);
  }}
  requestAnimationFrame(frame);
}})();
</script>

</body>
</html>
"""

    components.html(hero_html, height=HERO_HEIGHT_PX, scrolling=False)