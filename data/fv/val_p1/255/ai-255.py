import sys
import json
import pathlib
import plotly.graph_objects as go

# --- 1. Load data from JSON file ---
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
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

# --- 2. Extract data for plotting ---
chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])

# --- 3. Create the Plotly figure ---
fig = go.Figure()

# Map internal y-axis keys to Plotly's yaxis properties
yaxis_map = {'y1': 'y', 'y2': 'y2'}

# Add traces for each data series
for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series.get("x"),
        y=series.get("y"),
        name=series.get("name"),
        mode='lines+markers',
        line=dict(color=colors[i]),
        marker=dict(color=colors[i], size=8),
        yaxis=yaxis_map.get(series.get("y_axis"))
    ))

# --- 4. Configure layout and styling ---
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        xanchor='center'
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        tickmode='array',
        tickvals=chart_data[0]['x'],
        showgrid=False,
        zeroline=False,
        linecolor='black'
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        range=[250, 750],
        tickvals=[250, 375, 500, 625, 750],
        gridcolor='#e9e9e9',
        zeroline=False,
        linecolor='black'
    ),
    yaxis2=dict(
        title=texts.get('y2_axis_title'),
        overlaying='y',
        side='right',
        range=[4, 14],
        tickvals=[4, 6.5, 9, 11.5, 14],
        showgrid=False,
        zeroline=False,
        linecolor='black'
    ),
    legend=dict(
        x=0.01,
        y=0.01,
        xanchor='left',
        yanchor='bottom',
        bgcolor='rgba(255,255,255,0.7)'
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(
        family="Arial",
        size=12
    ),
    margin=dict(l=60, r=60, t=80, b=120),
    shapes=[
        # Light blue background bands
        go.layout.Shape(type="rect", xref="paper", yref="y", x0=0, y0=500, x1=1, y1=625,
                        fillcolor="#e0f2f8", layer="below", line_width=0),
        go.layout.Shape(type="rect", xref="paper", yref="y", x0=0, y0=250, x1=1, y1=375,
                        fillcolor="#e0f2f8", layer="below", line_width=0),
    ],
    annotations=[
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.5,
            y=-0.25,
            xanchor='center',
            yanchor='top',
            font=dict(size=10, color='grey')
        )
    ]
)

# --- 5. Output the chart as a PNG image ---
output_filename_base = pathlib.Path(json_path).stem
output_png_path = f"{output_filename_base}.png"

try:
    fig.write_image(output_png_path, scale=2)
    print(f"Chart successfully generated and saved to {output_png_path}")
except Exception as e:
    print(f"Error writing image file: {e}")
    sys.exit(1)