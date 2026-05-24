import sys
import json
import os
import plotly.graph_objects as go

# --- 1. Load Data from JSON ---
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json>")
    sys.exit(1)

json_path = sys.argv[1]
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

# --- 2. Create Figure ---
fig = go.Figure()

# --- 3. Add Traces ---
# This chart has one data series.
series = chart_data[0]
x_values = series['x']
y_values = series['y']

line_color = colors[0]
marker_color_default = colors[1]
marker_color_special = colors[2]

# Create a list of colors for the markers, with the first one being special.
marker_colors = [marker_color_special] + [marker_color_default] * (len(x_values) - 1)

fig.add_trace(go.Scatter(
    x=x_values,
    y=y_values,
    mode='lines+markers',
    line=dict(color=line_color, width=1.5),
    marker=dict(
        color=marker_colors,
        size=6,
        line=dict(
            color=marker_colors,  # Marker outline is same as fill
            width=1
        )
    ),
    showlegend=False
))

# --- 4. Configure Layout ---
title_text = texts['title']
if texts.get('subtitle'):
    title_text += f'<br><sub>{texts["subtitle"]}</sub>'

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        xanchor='center',
        font=dict(family="Arial", size=18, color='black')
    ),
    xaxis_title=dict(
        text=texts['x_axis_title'],
        font=dict(family="Arial", size=14, color='black')
    ),
    yaxis_title=dict(
        text=texts['y_axis_title'],
        font=dict(family="Arial", size=14, color='black')
    ),
    font=dict(family="Arial", size=12, color='black'),
    plot_bgcolor='#FDF5E6',
    paper_bgcolor='white',
    margin=dict(l=90, r=40, t=90, b=80),
    xaxis=dict(
        range=[-0.5, 14.5],
        tickmode='linear',
        tick0=0,
        dtick=2,
        showgrid=True,
        gridwidth=1,
        gridcolor='#DCDCDC',
        griddash='dot',
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True
    ),
    yaxis=dict(
        range=[-0.0005, 0.0125],
        tickmode='linear',
        tick0=0,
        dtick=0.002,
        showgrid=True,
        gridwidth=1,
        gridcolor='#DCDCDC',
        griddash='dot',
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        tickformat=".3f"
    )
)

if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0,
        y=-0.15,
        xanchor='left',
        yanchor='top',
        font=dict(family="Arial", size=10, color='grey')
    )

# --- 5. Output Image ---
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    print("Please ensure you have 'kaleido' installed (`pip install kaleido`)")
    sys.exit(1)