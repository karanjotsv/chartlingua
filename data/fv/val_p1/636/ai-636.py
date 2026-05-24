import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# --- 1. Load Data from JSON ---
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])

# --- 2. Create Figure ---
fig = go.Figure()

# Add traces from chart_data
for i, series in enumerate(chart_data):
    color = colors[i % len(colors)]
    fig.add_trace(go.Scatter(
        x=series.get("x"),
        y=series.get("y"),
        name=series.get("name"),
        mode='lines+markers',
        line=dict(color=color, width=2),
        marker=dict(
            symbol='circle',
            color='white',
            size=8,
            line=dict(color=color, width=2)
        )
    ))

# --- 3. Configure Layout ---
# Combine title and subtitle
title_text = texts.get("title", "")
if texts.get("subtitle"):
    title_text += f'<br><sup>{texts.get("subtitle")}</sup>'

# Combine source and notes for caption
caption_parts = []
if texts.get("notes"):
    caption_parts.append(f"<b>Notes:</b><br>{texts.get('notes')}")
if texts.get("source"):
    caption_parts.append(f"<b>Source:</b> {texts.get('source')}")
caption_text = "<br>".join(caption_parts)

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.01,
        xanchor='left',
        y=0.95,
        yanchor='top',
        font=dict(size=18)
    ),
    xaxis=dict(
        title=texts.get("x_axis_title"),
        showline=True,
        linewidth=1,
        linecolor='black',
        showgrid=False,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title=texts.get("y_axis_title"),
        range=[0, 30000000],
        tickvals=[0, 7500000, 15000000, 22500000, 30000000],
        tickformat=',.0f', # Use comma as thousands separator
        showline=True,
        linewidth=1,
        linecolor='black',
        gridcolor='lightgrey',
        gridwidth=1,
        tickfont=dict(size=12)
    ),
    showlegend=False,
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", color="black"),
    margin=dict(l=90, r=40, t=100, b=180), # Increased bottom margin for caption
    annotations=[
        dict(
            text=caption_text,
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=-0.3, # Adjust position below x-axis
            xanchor='left',
            yanchor='top',
            align='left',
            font=dict(size=12)
        )
    ]
)

# --- 4. Output Image ---
output_filename = json_path.stem + ".png"
fig.write_image(output_filename, scale=2, width=1000, height=600)
print(f"Chart saved to {output_filename}")