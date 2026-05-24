import sys
import json
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path

# --- Argument Handling ---
if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <path_to_json_file>")
    sys.exit(1)

json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

output_filename = json_path.stem + ".png"

# --- Data Loading ---
with open(json_path, 'r', encoding='utf-8') as f:
    chart_config = json.load(f)

chart_data = chart_config["chart_data"]
texts = chart_config["texts"]
colors = chart_config["colors"]

# --- Chart Creation ---
subplot_titles = [d['name'] for d in chart_data]
fig = make_subplots(
    rows=len(chart_data),
    cols=1,
    specs=[[{'type': 'domain'}] for _ in chart_data],
    subplot_titles=subplot_titles,
    vertical_spacing=0.08
)

for i, diet in enumerate(chart_data):
    fig.add_trace(
        go.Pie(
            labels=texts["legend_labels"],
            values=diet["values"],
            marker_colors=colors,
            name=diet["name"],
            textinfo='none',
            hoverinfo='label+percent',
            sort=False,
            direction='clockwise'
        ),
        row=i + 1,
        col=1
    )

# --- Layout and Styling ---
fig.update_layout(
    title_text=f"<b>{texts['title']}</b>",
    title_x=0.5,
    title_y=0.97,
    title_font_size=18,
    
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.05,
        xanchor="center",
        x=0.5,
        traceorder="normal"
    ),
    
    paper_bgcolor='black',
    plot_bgcolor='black',
    font=dict(
        family="Arial",
        color="white"
    ),
    
    margin=dict(t=80, b=200, l=40, r=40),
)

# Style subplot titles created by make_subplots
fig.update_annotations(
    font=dict(family="Arial", size=14, color="white")
)

# Add source annotation separately
fig.add_annotation(
    text=texts['source'],
    xref="paper",
    yref="paper",
    x=0.5,
    y=-0.15, 
    showarrow=False,
    align="center",
    xanchor="center",
    yanchor="top",
    font=dict(size=10)
)

# --- Output ---
fig.write_image(output_filename, scale=2)
print(f"Chart saved as {output_filename}")