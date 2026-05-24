import sys
import json
import pathlib
import plotly.graph_objects as go

# --- 1. Load Data ---
# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) < 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data and texts from the JSON structure
chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])
categories = [d['category'] for d in chart_data]
values = [d['value'] for d in chart_data]

# --- 2. Create Figure ---
fig = go.Figure()

# --- 3. Add Bar Trace ---
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors,
    text=values,
    textposition='outside',
    texttemplate='%{text:.1f}',
    textfont=dict(
        family="Arial",
        size=12,
        color=colors
    ),
    cliponaxis=False
))

# --- 4. Customize Layout ---
# Combine title and subtitle using HTML for styling
title_text = f"<b>{texts.get('title', '')}</b><br><span style='font-size:12px; color: #555555;'>{texts.get('subtitle', '')}</span>"

fig.update_layout(
    title=dict(
        text=title_text,
        y=0.98,
        x=0.05,
        xanchor='left',
        yanchor='top'
    ),
    font=dict(
        family="Arial",
        size=12,
        color="#333333"
    ),
    xaxis=dict(
        showticklabels=False,  # Hide default labels to replace with annotations
        showgrid=False,
        showline=False,
        zeroline=False,
        tickvals=categories # Ensure annotations align with bar centers
    ),
    yaxis=dict(
        range=[0, 90],
        showgrid=True,
        gridcolor='#FFFFFF',
        zeroline=False,
        showline=False,
        tickprefix=' ',
        ticksuffix=' '
    ),
    plot_bgcolor='#EBF4F8',
    paper_bgcolor='#EBF4F8',
    showlegend=False,
    margin=dict(l=50, r=30, t=100, b=80) # Ample margin for title and rotated labels
)

# --- 5. Add Custom X-axis Labels via Annotations ---
# This is required to color each label individually, matching the bar color
annotations = []
for i, category in enumerate(categories):
    annotations.append(dict(
        x=category,
        y=0,
        yshift=-30, # Position below the x-axis
        text=category,
        showarrow=False,
        font=dict(
            color=colors[i],
            size=12
        ),
        textangle=-45
    ))
fig.update_layout(annotations=annotations)


# --- 6. Output Image ---
output_filename = json_path.stem + ".png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")