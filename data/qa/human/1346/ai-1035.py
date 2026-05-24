import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data from the loaded JSON
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', {})

# Create the figure
fig = go.Figure()

# Add traces and data point annotations
for i, series in enumerate(chart_data):
    trace_color = colors.get('traces', [])[i] if i < len(colors.get('traces', [])) else '#000000'
    marker_color = colors.get('markers', [])[i] if i < len(colors.get('markers', [])) else '#000000'
    
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        mode='lines+markers',
        name=series['name'],
        line=dict(color=trace_color, width=3),
        marker=dict(
            color=marker_color,
            size=9,
            symbol='circle',
            line=dict(color=colors.get('marker_outline', '#FFFFFF'), width=2)
        ),
        showlegend=False
    ))

    # Add data point labels as annotations
    for x_val, y_val, y_offset in zip(series['x'], series['y'], series['data_labels_y_offsets']):
        fig.add_annotation(
            x=x_val,
            y=y_val,
            text=str(y_val),
            showarrow=False,
            font=dict(family="Arial", size=11, color=marker_color),
            yshift=y_offset
        )

# Add series name annotations (e.g., "U.S.", "Japan")
for i, anno in enumerate(texts.get('series_annotations', [])):
    text_color = colors.get('text', [])[i] if i < len(colors.get('text', [])) else '#000000'
    fig.add_annotation(
        x=anno['x'],
        y=anno['y'],
        text=f"<b>{anno['text']}</b>",
        showarrow=False,
        font=dict(family="Arial", size=14, color=text_color)
    )

# Combine title and subtitle
title_text = f"<b>{texts.get('title', '')}</b><br><span style='font-size:14px; color:#555555'>{texts.get('subtitle', '')}</span>"

# Update layout
fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.05,
        xanchor='left',
        yanchor='top',
        font=dict(family="Arial", size=18)
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12, color='#333333'),
    margin=dict(l=60, r=40, b=100, t=120, pad=4),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        tickvals=chart_data[0]['x'] if chart_data else [],
        tickfont=dict(size=12),
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor=colors.get('axis_line'),
        zeroline=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 70],
        tickvals=[0, 70],
        ticktext=['0', f"70{texts.get('y_axis_suffix', '')}"],
        tickfont=dict(size=12),
        showgrid=True,
        gridcolor=colors.get('grid'),
        gridwidth=1,
        showline=False,
        zeroline=False
    )
)

# Add source annotation
fig.add_annotation(
    text=texts.get('source', ''),
    align='left',
    showarrow=False,
    xref='paper',
    yref='paper',
    x=0,
    y=0,
    xanchor='left',
    yanchor='top',
    xshift=-50,
    yshift=-60,
    font=dict(size=11, family="Arial")
)

# Generate output PNG filename from JSON path
filename_base = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{filename_base}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")