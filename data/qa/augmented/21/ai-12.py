import sys
import json
import os
import plotly.graph_objects as go

# --- 1. Load data from JSON file ---
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

# --- 2. Extract data and configuration from JSON ---
chart_data = chart_config.get('chart_data', {})
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])
categories = chart_data.get('categories', [])
series_data = chart_data.get('series', [])

# --- 3. Create the Plotly figure ---
fig = go.Figure()

# Add each data series as a bar trace, in the order provided
for i, series in enumerate(series_data):
    fig.add_trace(go.Bar(
        x=categories,
        y=series['values'],
        name=series['name'],
        marker_color=colors[i % len(colors)],
        text=[f"{v}%" for v in series['values']],
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(
            family="Arial",
            size=14,
            color='white'
        )
    ))

# --- 4. Configure the layout ---
fig.update_layout(
    barmode='stack',
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=80, r=40, t=50, b=180),
    xaxis=dict(
        title_text=texts.get('xaxis_title'),
        tickangle=-30,
        showgrid=False,
        linecolor='lightgrey',
        zeroline=False
    ),
    yaxis=dict(
        title_text=texts.get('yaxis_title'),
        range=[0, 125],
        ticksuffix='%',
        gridcolor='lightgrey',
        zeroline=False
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.4,
        xanchor="center",
        x=0.5
    ),
    annotations=[]
)

# Add title if it exists
if texts.get('title'):
    fig.update_layout(
        title=dict(
            text=f"<b>{texts['title']}</b><br><sup>{texts.get('subtitle', '')}</sup>",
            x=0.05,
            xanchor='left'
        )
    )

# Add source annotation
if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        xref="paper", yref="paper",
        x=1, y=-0.45,
        xanchor='right', yanchor='bottom',
        showarrow=False,
        font=dict(
            size=12,
            color="#666666"
        )
    )

# --- 5. Export the chart as a PNG file ---
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

try:
    fig.write_image(output_filename, scale=2, width=1000, height=650)
    print(f"Chart successfully generated and saved to {output_filename}")
except Exception as e:
    print(f"Error writing image file: {e}")
    sys.exit(1)