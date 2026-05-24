import sys
import json
import pathlib
import plotly.graph_objects as go

# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Read data from the JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_file_path}'")
    sys.exit(1)

# Initialize the figure
fig = go.Figure()

# Add traces for each data series
for i, series in enumerate(chart_data['chart_data']):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        name=series['name'],
        mode='lines+markers+text',
        line=dict(color=chart_data['colors'][i]),
        marker=dict(
            symbol=series['marker_symbol'],
            color=chart_data['colors'][i],
            size=8,
            line=dict(width=1, color='Black')
        ),
        text=[str(val) for val in series['y']],
        textposition='bottom right',
        textfont=dict(
            family="Arial",
            size=11,
            color='black'
        )
    ))

# Configure the layout
title_text = chart_data['texts'].get('title', '')
if chart_data['texts'].get('subtitle'):
    title_text += f"<br><sub>{chart_data['texts']['subtitle']}</sub>"

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        xanchor='center',
        font=dict(size=16, weight='bold')
    ),
    xaxis_title=chart_data['texts'].get('x_axis_title'),
    yaxis_title=chart_data['texts'].get('y_axis_title'),
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    paper_bgcolor='white',
    legend=dict(
        x=0.02,
        y=0.98,
        xanchor='left',
        yanchor='top',
        bordercolor='Black',
        borderwidth=1
    ),
    margin=dict(l=50, r=50, t=80, b=80),
    xaxis=dict(
        tickvals=chart_data['chart_data'][0]['x'],
        ticktext=[f"'{str(x)[-2:]}" for x in chart_data['chart_data'][0]['x']],
        showline=True,
        linewidth=1,
        linecolor='black',
        showgrid=False
    ),
    yaxis=dict(
        range=[0, 70],
        dtick=10,
        showline=True,
        linewidth=1,
        linecolor='black',
        showgrid=True,
        gridcolor='lightgrey'
    )
)

# Derive output filename from the input JSON filename
path_obj = pathlib.Path(json_file_path)
output_filename = f"{path_obj.stem}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")