import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# --- 1. Load Data ---
# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {Path(__file__).name} <json_file_path>")
    sys.exit(1)

json_path = Path(sys.argv[1])

# Read and parse the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error reading or parsing JSON file: {e}")
    sys.exit(1)

# Extract data and text from the configuration
chart_data = config.get('chart_data', {})
texts = config.get('texts', {})
colors = config.get('colors', [])
categories = chart_data.get('categories', [])
series_list = chart_data.get('series', [])

# --- 2. Create Figure ---
fig = go.Figure()

# Add a bar trace for each series, preserving order
for i, series in enumerate(series_list):
    fig.add_trace(go.Bar(
        x=categories,
        y=series.get('data', []),
        name=series.get('name', ''),
        marker_color=colors[i % len(colors)],
        text=series.get('data', []),
        textposition='outside',
        cliponaxis=False  # Prevent data labels from being clipped
    ))

# --- 3. Configure Layout ---
# Combine title and subtitle using HTML tags for formatting
title_text = ""
if texts.get('title'):
    title_text += f"<b>{texts['title']}</b>"
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

fig.update_layout(
    barmode='group',
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(
        family="Arial",
        size=12
    ),
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black',
        tickfont=dict(size=11)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=True,
        gridcolor='#E5E5E5',
        range=[0, 50],
        dtick=10
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.5,  # Position legend below the multi-line x-axis labels
        xanchor="center",
        x=0.5,
        traceorder='normal'
    ),
    margin=dict(l=70, r=40, b=200, t=50) # Increased bottom margin
)

# Add faint vertical lines between categories as seen in the original chart
for i in range(len(categories) - 1):
    fig.add_shape(
        type="line",
        x0=i + 0.5, y0=0, x1=i + 0.5, y1=1,
        xref="x", yref="paper",
        line=dict(color="lightgrey", width=1)
    )

# Add source annotation if it exists
if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0.99,
        y=-0.45,  # Position below plot, aligned with legend
        xanchor='right',
        yanchor='bottom'
    )

# --- 4. Final Touches & Output ---
# Update data label appearance
fig.update_traces(textfont_size=12, textangle=0)

# Generate and save the output PNG image
output_path = json_path.with_suffix('.png')
fig.write_image(str(output_path), scale=2)

print(f"Chart saved to {output_path}")