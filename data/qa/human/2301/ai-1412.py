import sys
import json
import os
import plotly.graph_objects as go

# --- 1. Load data from JSON file ---
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Failed to decode JSON from '{json_path}'.")
    sys.exit(1)

# --- 2. Extract data and texts ---
chart_data = chart_config.get('chart_data', {})
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])
categories = chart_data.get('categories', [])
series = chart_data.get('series', [])

# --- 3. Create the chart figure ---
fig = go.Figure()

# --- 4. Add traces (bars) for each series ---
for i, s in enumerate(series):
    fig.add_trace(go.Bar(
        x=categories,
        y=s.get('data', []),
        name=s.get('name', ''),
        marker_color=colors[i % len(colors)],
        text=[f'{val}%' for val in s.get('data', [])],
        textposition='outside',
        textfont=dict(
            family="Arial",
            size=12,
            color='black'
        ),
        cliponaxis=False
    ))

# --- 5. Configure layout ---
title_text = texts.get('title')
full_title = f"<b>{title_text}</b>" if title_text else ""

fig.update_layout(
    barmode='group',
    title=dict(
        text=full_title,
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title=texts.get('x_axis_title', ''),
        tickfont=dict(size=12),
        showgrid=False,
        zeroline=True,
        zerolinecolor='black',
        zerolinewidth=1
    ),
    yaxis=dict(
        title=texts.get('y_axis_title', ''),
        ticksuffix='%',
        range=[0, 105],
        dtick=20,
        showgrid=True,
        gridcolor='#EAEAEA',
        gridwidth=1,
        zeroline=False
    ),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.25,
        xanchor='center',
        x=0.5
    ),
    font=dict(
        family="Arial",
        size=14,
        color="black"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=60, r=40, t=50, b=120),
    annotations=[
        dict(
            text=texts.get('source', ''),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.25,
            xanchor='right',
            yanchor='bottom',
            font=dict(
                size=12,
                color='#666666'
            )
        )
    ]
)

# --- 6. Save the chart as a PNG image ---
base_name = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_name}.png"

try:
    fig.write_image(output_filename, scale=2, width=900, height=600)
    print(f"Chart saved to {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)