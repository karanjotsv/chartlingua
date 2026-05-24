import sys
import json
import os
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Check if the file exists
if not os.path.exists(json_file_path):
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Read data from the specified JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data, texts, and colors from the JSON object
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Initialize the figure
fig = go.Figure()

# Add traces to the figure by iterating through the chart data
for i, series in enumerate(chart_data):
    color = colors[i % len(colors)] if colors else '#3778C2'
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        mode='lines+markers+text',
        name=series.get('name', ''),
        line=dict(color=color, width=2),
        marker=dict(color=color, size=6),
        text=[f'{val:.2f}' for val in series['y']],
        textposition='top center',
        textfont=dict(
            family="Arial",
            size=11,
            color='black'
        ),
        hoverinfo='skip'
    ))

# Update layout for a professional look, matching the source image
fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        tickmode='linear',
        tick0=2000,
        dtick=1,
        tickangle=-45,
        showgrid=True,
        gridcolor='#f0f0f0',
        gridwidth=1,
        zeroline=False,
        linecolor='lightgrey'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0.8, 2.05],
        tickmode='linear',
        dtick=0.2,
        showgrid=True,
        gridcolor='lightgrey',
        zeroline=False,
        linecolor='lightgrey'
    ),
    margin=dict(l=80, r=40, t=40, b=120),
    annotations=[
        dict(
            text=texts.get('source', ''),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.25,  # Position below the x-axis labels
            xanchor='right',
            yanchor='bottom',
            align='right',
            font=dict(size=12)
        )
    ]
)

# Derive output filename from the input JSON file path
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_image_path = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image
try:
    fig.write_image(output_image_path, scale=2)
    print(f"Chart successfully generated and saved to {output_image_path}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)