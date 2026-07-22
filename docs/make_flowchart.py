"""Generate the MediNexus AI solution flowchart PNG for slide 3 (Napkin-style:
minimal rounded nodes, thin arrows, template purple palette)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

PURPLE = "#38327A"
FILL = "#EFEDFB"
TXT = "#251F55"

W_IN, H_IN = 3.85, 2.55
fig = plt.figure(figsize=(W_IN, H_IN), dpi=300)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")


def node(cx, cy, w, h, text, fs=6.8):
    ax.add_patch(FancyBboxPatch((cx - w / 2, cy - h / 2), w, h,
                                boxstyle="round,pad=0.008,rounding_size=0.025",
                                linewidth=1.1, edgecolor=PURPLE, facecolor=FILL))
    ax.text(cx, cy, text, ha="center", va="center", fontsize=fs,
            color=TXT, fontweight="bold", family="sans-serif")


def arrow(x1, y1, x2, y2):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                                 mutation_scale=7, linewidth=1.0, color=PURPLE))


BH = 0.115
node(0.50, 0.925, 0.62, BH, "Patient vitals  ·  records  ·  notes")
arrow(0.50, 0.862, 0.50, 0.800)
node(0.50, 0.735, 0.62, BH, "FastAPI backend  +  SQL store")
arrow(0.50, 0.672, 0.50, 0.610)
node(0.50, 0.545, 0.44, BH, "AI Orchestrator")
arrow(0.38, 0.485, 0.26, 0.415)
arrow(0.62, 0.485, 0.74, 0.415)
node(0.26, 0.325, 0.42, 0.165, "RAG copilot\nFAISS + Ollama LLM", fs=6.4)
node(0.74, 0.325, 0.42, 0.165, "ML risk engine\nearly-warning scores", fs=6.4)
arrow(0.26, 0.238, 0.40, 0.148)
arrow(0.74, 0.238, 0.60, 0.148)
node(0.50, 0.075, 0.72, BH, "Live alerts  ·  dashboard  ·  auto reports")

out = r"C:\Users\mshre\medinexus-ai\docs\solution_flow.png"
fig.savefig(out, transparent=False, facecolor="white")
print("saved", out)
