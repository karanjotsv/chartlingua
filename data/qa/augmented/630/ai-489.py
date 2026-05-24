import sys
import json
import plotly.graph_objects as go
import pathlib

# --- 1. Load Data from JSON file specified by command-line argument ---
if len(sys.argv) != 2:
    print("Usage: python recreate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: The file '{json_path}' contains invalid JSON.")
    sys.exit(1)

# --- 2. Extract data and text from the JSON structure ---
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# --- 3. Create the Plotly Figure ---
fig = go.Figure()

# --- 4. Add Bar Chart Trace ---
# The data is added in the order it appears in the JSON.
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=values,
    textposition='outside',
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    ),
    marker_color=colors[0] if colors else None,
    cliponaxis=False  # Prevents text labels above bars from being clipped
))

# --- 5. Configure Layout ---
# Combine title and subtitle using HTML tags if they exist
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

# Prepare annotations for source text
annotations = []
if texts.get('source'):
    annotations.append(
        dict(
            xref='paper', yref='paper',
            x=0.99, y=-0.18,
            xanchor='right', yanchor='top',
            text=texts.get('source'),
            showarrow=False,
            font=dict(family="Arial", size=12)
        )
    )

fig.update_layout(
    font=dict(family="Arial", size=12, color='#333333'),
    title_text=title_text if title_text else None,
    yaxis_title_text=texts.get('y_axis_title'),
    xaxis_title_text=texts.get('x_axis_title'),
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(l=90, r=20, b=100, t=40),
    xaxis=dict(
        showgrid=False,
        zeroline=False,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        range=[0, 1.8],
        dtick=0.25,
        showgrid=True,
        gridcolor='#e0e0e0',
        zeroline=True,
        zerolinecolor='#e0e0e0',
        tickfont=dict(size=12)
    ),
    annotations=annotations
)

# --- 6. Output the Chart to a PNG File ---
output_filename_base = pathlib.Path(json_path).stem
output_filename = f"{output_filename_base}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved to '{output_filename}'")