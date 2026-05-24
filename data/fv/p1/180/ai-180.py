import sys
import json
import os
import plotly.graph_objects as go

# --- 1. Load Data from JSON ---
if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', {})

# --- 2. Create Plotly Figure ---
fig = go.Figure()

# Add the two pie chart traces
if len(chart_data) == 2:
    # Main Pie (Left)
    fig.add_trace(go.Pie(
        labels=chart_data[0]['labels'],
        values=chart_data[0]['values'],
        marker_colors=colors.get('main_pie_colors'),
        domain={'x': [0, 0.45], 'y': [0.15, 0.85]},
        pull=[0, 0.1],
        textinfo='label+percent',
        textposition='inside',
        textfont={'size': 14, 'family': 'Arial'},
        hole=0,
        sort=False,
        direction='clockwise'
    ))

    # Detail Pie (Right)
    fig.add_trace(go.Pie(
        labels=chart_data[1]['labels'],
        values=chart_data[1]['values'],
        marker_colors=colors.get('detail_pie_colors'),
        domain={'x': [0.5, 1.0], 'y': [0, 1.0]},
        pull=[0.1, 0, 0, 0, 0, 0, 0],
        textinfo='label+percent',
        textposition='auto',
        textfont={'size': 14, 'family': 'Arial'},
        hole=0,
        sort=False,
        direction='clockwise'
    ))

# --- 3. Configure Layout ---
# Combine title and subtitle
title_text = f"<b>{texts.get('title', '')}</b><br><sup>{texts.get('subtitle', '')}</sup>"

fig.update_layout(
    title={
        'text': title_text,
        'y': 0.98,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    showlegend=False,
    font={'family': "Arial", 'size': 12},
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin={'t': 130, 'b': 40, 'l': 40, 'r': 40},
    # Add shapes to connect the two pies
    shapes=[
        go.layout.Shape(
            type="line",
            xref="paper", yref="paper",
            x0=0.43, y0=0.67, x1=0.52, y1=0.88,
            line=dict(color="black", width=1)
        ),
        go.layout.Shape(
            type="line",
            xref="paper", yref="paper",
            x0=0.43, y0=0.33, x1=0.52, y1=0.12,
            line=dict(color="black", width=1)
        )
    ]
)

# --- 4. Output Image ---
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

try:
    fig.write_image(output_filename, scale=2, width=1000, height=600)
    print(f"Chart successfully generated and saved to {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)