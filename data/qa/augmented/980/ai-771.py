import sys
import json
import pathlib
import plotly.graph_objects as go

# --- 1. Load data from JSON file provided as a command-line argument ---
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
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
x_values = [d['x'] for d in chart_data]
y_values = [d['y'] for d in chart_data]

# --- 3. Create the Plotly figure ---
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    text=y_values,
    textposition='outside',
    textfont=dict(color='black', size=12),
    marker_color=colors[0] if colors else None,
    hoverinfo='none',
    cliponaxis=False
))

# --- 4. Configure layout and styling ---
# Combine title and subtitle
title_parts = [texts.get('title'), texts.get('subtitle')]
title_text = "<br>".join(filter(None, title_parts))

# Combine source and note
source_parts = [texts.get('source'), texts.get('note')]
source_text = "<br>".join(filter(None, source_parts))

fig.update_layout(
    font=dict(family="Arial"),
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left',
        y=0.95,
        yanchor='top'
    ),
    yaxis_title=texts.get('y_axis_title'),
    xaxis_title=texts.get('x_axis_title'),
    yaxis=dict(
        range=[0, 250],
        tickmode='array',
        tickvals=[0, 50, 100, 150, 200, 250],
        gridcolor='#e0e0e0',
        zeroline=False,
        showline=False
    ),
    xaxis=dict(
        showgrid=False,
        showline=True,
        linecolor='black',
        linewidth=1
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=80, b=120),
    annotations=[
        dict(
            text=source_text,
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.25,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(size=10)
        )
    ] if source_text else []
)

# --- 5. Output the chart as a PNG image ---
base_filename = pathlib.Path(json_path).stem
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")