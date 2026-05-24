import sys
import json
import os
import plotly.graph_objects as go

# --- 1. Load data from JSON file provided as a command-line argument ---
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# --- 2. Extract data and text from the loaded configuration ---
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

x_values = [item['x'] for item in chart_data]
y_values = [item['y'] for item in chart_data]

# --- 3. Create the Plotly figure ---
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    text=y_values,
    textposition='outside',
    marker_color=colors[0] if colors else None,
    textfont=dict(family="Arial", size=12, color='black'),
    cliponaxis=False # Prevents text from being clipped at plot boundaries
))

# --- 4. Configure the layout for accuracy and aesthetics ---

# Combine title and subtitle if they exist
title_text = texts.get('title', '') or ''
subtitle_text = texts.get('subtitle', '') or ''
if title_text and subtitle_text:
    title_text = f"{title_text}<br><sub>{subtitle_text}</sub>"
elif subtitle_text:
    title_text = f"<sub>{subtitle_text}</sub>"

# Combine source and note for the annotation
source_text = texts.get('source', '') or ''
note_text = texts.get('note', '') or ''
source_note_text = "<br>".join(filter(None, [note_text, source_text]))

fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        tickvals=x_values,
        ticktext=[str(x) for x in x_values],
        showgrid=False,
        zeroline=True,
        zerolinecolor='#333333',
        zerolinewidth=1
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 1500],
        dtick=250,
        showgrid=True,
        gridcolor='#e0e0e0',
        zeroline=False
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=100, r=40, t=60, b=120),
    annotations=[
        dict(
            showarrow=False,
            text=source_note_text,
            xref="paper",
            yref="paper",
            x=1.0,
            y=-0.20,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(size=10)
        )
    ] if source_note_text else []
)


# --- 5. Save the figure to a high-resolution PNG file ---
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved to {output_filename}")