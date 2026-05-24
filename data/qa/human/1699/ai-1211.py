import sys
import json
from pathlib import Path
import plotly.graph_objects as go

# --- 1. Load data from JSON file provided as a command-line argument ---
if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <path_to_json_file>")
    sys.exit(1)

json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

output_filename = json_path.with_suffix(".png")

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# --- 2. Extract data and text from the loaded JSON ---
chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']
categories = chart_data['categories']
series_data = chart_data['series']

# --- 3. Create the Plotly figure ---
fig = go.Figure()

# --- 4. Add a bar trace for each data series ---
for i, series in enumerate(series_data):
    fig.add_trace(go.Bar(
        y=categories,
        x=series['values'],
        name=series['name'],
        orientation='h',
        marker=dict(
            color=colors[i]
        ),
        text=[f"<b>{v}</b>" for v in series['values']],
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(color='white', size=16, family="Arial")
    ))

# --- 5. Configure the layout, titles, and annotations ---
title_text = f"{texts['title']}<br><span style='font-size: 18px; color: #555555;'>{texts['subtitle']}</span>"

# Annotations for the column headers above the bars
annotations = [
    dict(
        xref='x', yref='y domain',
        x=30, y=1.02,
        text=texts['series_headers'][0],
        font=dict(family='Arial', size=14, color=colors[0]),
        showarrow=False,
        xanchor='center',
        yanchor='bottom'
    ),
    dict(
        xref='x', yref='y domain',
        x=80, y=1.02,
        text=texts['series_headers'][1],
        font=dict(family='Arial', size=14, color=colors[1]),
        showarrow=False,
        xanchor='center',
        yanchor='bottom'
    )
]

fig.update_layout(
    barmode='stack',
    template='plotly_white',
    title=dict(
        text=title_text,
        y=0.98,
        x=0.01,
        xanchor='left',
        yanchor='top'
    ),
    xaxis=dict(
        showgrid=False,
        showline=False,
        showticklabels=False,
        zeroline=False,
        range=[0, 101] # Set range for percentage-based data
    ),
    yaxis=dict(
        showgrid=False,
        showline=False,
        showticklabels=True,
        zeroline=False,
        tickfont=dict(size=16)
    ),
    font=dict(
        family="Arial",
        size=12,
        color="#333333"
    ),
    title_font_size=24,
    showlegend=False,
    margin=dict(l=150, r=20, t=150, b=120),
    annotations=annotations,
    shapes=[
        # Add the subtle vertical reference line
        dict(
            type='line',
            xref='x', yref='paper',
            x0=series_data[0]['values'][-1], # Position at end of first series for the 'Total' category
            x1=series_data[0]['values'][-1],
            y0=-0.05, y1=1,
            line=dict(color='darkgrey', width=0.75)
        )
    ]
)

# Add the footer annotation, positioned relative to the entire paper
fig.add_annotation(
    text=texts['footer'],
    xref="paper", yref="paper",
    x=0.01, y=-0.22,
    showarrow=False,
    align="left",
    xanchor="left",
    yanchor="top",
    font=dict(size=13, color="#555555")
)

# --- 6. Generate the output image ---
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")