import sys
import json
import os
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read and load the JSON data from the specified file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and texts from the JSON object
data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Prepare data for Plotly traces
categories = [item['category'] for item in data]
values_series1 = [item['values'][0] for item in data]
values_series2 = [item['values'][1] for item in data]

# Create a new figure
fig = go.Figure()

# Add the first data series (UK)
text_positions = ['bottom center' if v < 60 else 'top center' for v in values_series1]
fig.add_trace(go.Scatter(
    x=categories,
    y=values_series1,
    name=texts['legend_labels'][0],
    mode='lines+markers+text',
    line=dict(color=colors[0], width=3.5),
    marker=dict(
        color=colors[0],
        size=9,
        symbol='circle-open',
        line=dict(width=2, color=colors[0])
    ),
    text=values_series1,
    textposition=text_positions,
    textfont=dict(family="Arial", size=11, color='black')
))

# Add the second data series (Eurozone average)
fig.add_trace(go.Scatter(
    x=categories,
    y=values_series2,
    name=texts['legend_labels'][1],
    mode='lines+markers',
    line=dict(color=colors[1], width=3.5),
    marker=dict(
        color=colors[1],
        size=9,
        symbol='circle-open',
        line=dict(width=2, color=colors[1])
    )
))

# Configure the layout of the chart
fig.update_layout(
    title=dict(
        text=f"<b>{texts['title']}</b>",
        y=0.98,
        x=0.01,
        xanchor='left',
        yanchor='top'
    ),
    yaxis_title=texts['y_axis_title'],
    font=dict(family="Arial", size=14, color="black"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(
        showgrid=False,
        zeroline=False,
        tickangle=315,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        range=[0, 151],
        tickvals=[0, 30, 60, 90, 120, 150],
        gridcolor='#e0e0e0',
        zeroline=True,
        zerolinecolor='#a0a0a0',
        tickfont=dict(size=12)
    ),
    legend=dict(
        x=0.05,
        y=0.88,
        xanchor='left',
        yanchor='top',
        bgcolor='rgba(255,255,255,0)',
        bordercolor='rgba(0,0,0,0)',
        font=dict(size=14)
    ),
    margin=dict(l=70, r=20, t=80, b=120),
    annotations=[
        dict(
            text=texts['source'],
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=-0.28,
            xanchor='left',
            yanchor='top',
            align='left'
        )
    ]
)

# Add a shaded rectangle for the estimated data period
fig.add_vrect(
    x0=13.5,
    x1=16.5,
    fillcolor="lightgrey",
    opacity=0.4,
    layer="below",
    line_width=0
)

# Generate and save the output image file
base_name = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_name}.png"

try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)