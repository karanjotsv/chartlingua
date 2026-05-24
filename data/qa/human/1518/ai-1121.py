import sys
import json
import pathlib
import plotly.graph_objects as go

# --- 1. Load data from JSON file ---
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_config = json.load(f)

# --- 2. Extract and prepare data ---
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Extract data into separate lists
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Format data labels (e.g., "6" instead of "6.0")
data_label_suffix = texts.get('data_label_suffix', '')
text_labels = [
    f"{int(v) if v == int(v) else v}{data_label_suffix}" for v in values
]

# Reverse data to display from top to bottom in the correct order
categories.reverse()
values.reverse()
text_labels.reverse()

# --- 3. Create the Plotly figure ---
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    text=text_labels,
    textposition='outside',
    orientation='h',
    marker_color=colors[0] if colors else '#44718a',
    cliponaxis=False,
    textfont=dict(
        size=12
    )
))

# --- 4. Configure layout ---
title_text = f"<b>{texts.get('title', '')}</b><br><span style='font-size:14px; color:#555'>{texts.get('subtitle', '')}</span>"

fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.01,
        xanchor='left',
        yanchor='top'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title', None),
        showticklabels=True,
        ticksuffix=data_label_suffix,
        zeroline=False,
        showline=False,
        showgrid=True,
        gridwidth=1,
        gridcolor='#f0f0f0',
        griddash='dash'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title', None),
        showgrid=False,
        autorange=True,
        showline=False,
        zeroline=False
    ),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=100, r=80, t=100, b=80),
    annotations=[
        dict(
            xref='paper', yref='paper',
            x=0, y=-0.1,
            xanchor='left', yanchor='top',
            text=texts.get('source', ''),
            showarrow=False,
            font=dict(size=12, color='#666')
        ),
        dict(
            xref='paper', yref='paper',
            x=1, y=-0.1,
            xanchor='right', yanchor='top',
            text=texts.get('note', ''),
            showarrow=False,
            font=dict(size=12, color='#666')
        )
    ]
)

# --- 5. Save the chart as a PNG image ---
output_filename = json_path.stem + ".png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")