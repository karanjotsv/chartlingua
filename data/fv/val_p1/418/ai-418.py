import sys
import json
import os
import plotly.graph_objects as go

# --- 1. Argument and File Handling ---
if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

# --- 2. Data Extraction ---
data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

categories = [item['category'] for item in data]
values = [item['value'] for item in data]

# --- 3. Chart Creation ---
fig = go.Figure()

# Add bar trace
if data:
    fig.add_trace(go.Bar(
        x=categories,
        y=values,
        marker_color=colors[0] if colors else '#2E5B8A',
        text=values,
        texttemplate='%{text:,.0f}',
        textposition='outside',
        textfont=dict(family="Arial", size=12, color='black', weight='bold'),
        cliponaxis=False
    ))

# --- 4. Layout Configuration ---
title_text = texts.get('title')
if title_text:
    title_text = f"<b>{title_text}</b>"

fig.update_layout(
    title_text=title_text,
    title_x=0.08,
    title_xanchor='left',
    title_y=0.95,
    title_yanchor='top',
    title_font=dict(size=18, family="Arial"),
    
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        zeroline=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, max(values) * 1.15], # Auto-range with padding for text
        gridcolor='#D3D3D3',
        zeroline=True,
        zerolinecolor='#000000',
        zerolinewidth=1
    ),
    
    font=dict(family="Arial", size=12, color='black'),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    
    margin=dict(t=80, b=50, l=80, r=40)
)

# --- 5. Output Generation ---
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2, width=800, height=500)

print(f"Chart saved to {output_filename}")