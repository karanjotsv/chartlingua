import sys
import json
import pathlib
import plotly.graph_objects as go

# --- 1. Load data from JSON file ---
if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error reading or parsing JSON file: {e}")
    sys.exit(1)

chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# --- 2. Prepare data for Plotly ---
labels = [item.get('label', '') for item in chart_data]
values = [item.get('value', 0) for item in chart_data]

# --- 3. Create the chart ---
fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#FFFFFF', width=1)),
    texttemplate='%{label}<br>%{percent}',
    textposition='outside',
    textfont=dict(family="Arial", size=14, color='#333333'),
    hole=0,
    sort=False,
    direction='clockwise',
    rotation=85
))

# --- 4. Configure layout and styling ---
title_text = f"<b>{texts.get('title', '')}</b>" if texts.get('title') else None

fig.update_layout(
    title_text=title_text,
    title_x=0.5,
    title_font=dict(family="Arial", size=20, color='#3a3a3a'),
    font=dict(family="Arial", size=12, color='#333333'),
    showlegend=False,
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(t=100, b=80, l=80, r=80),
    uniformtext_minsize=12,
    uniformtext_mode='hide'
)

# --- 5. Save the chart as a PNG image ---
base_filename = pathlib.Path(json_path).stem
output_filename = f"{base_filename}.png"

try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved as {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)