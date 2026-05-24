import sys
import json
import plotly.graph_objects as go
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

# Extract data from the JSON object
data_series = chart_data.get('chart_data', [])
texts = chart_data.get('texts', {})
colors = chart_data.get('colors', [])

# Create the figure
fig = go.Figure()

# Add traces by iterating through the data series
for i, series in enumerate(data_series):
    # Prepare text labels (bolded)
    text_labels = [f'<b>{y_val}</b>' if y_val is not None else None for y_val in series.get('y', [])]
    
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        name=series.get('name'),
        mode=series.get('mode'),
        line=dict(color=colors[i], width=2.5),
        marker=dict(color=colors[i], size=8),
        text=text_labels,
        textposition='top center',
        textfont=dict(
            family="Arial",
            size=12,
            color='black'
        )
    ))

# Configure layout
fig.update_layout(
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    paper_bgcolor='white',
    title=texts.get('title'),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        range=[157.5, 173],
        tickmode='linear',
        tick0=157.5,
        dtick=2.5,
        showgrid=True,
        gridcolor='#e0e0e0',
        gridwidth=1,
        zeroline=False
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#f0f0f0',
        gridwidth=1,
        tickfont=dict(color='#666666')
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.3,
        xanchor="center",
        x=0.5
    ),
    margin=dict(l=80, r=40, b=100, t=50)
)

# Add source annotation
if texts.get('source'):
    fig.add_annotation(
        text=texts.get('source'),
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1.0,
        y=-0.35,
        xanchor='right',
        yanchor='bottom'
    )

# Determine output filename and save the image
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")