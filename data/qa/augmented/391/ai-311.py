import sys
import json
import pathlib
import plotly.graph_objects as go

# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]
base_filename = pathlib.Path(json_path).stem

# Read the chart data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: The file '{json_path}' is not a valid JSON file.")
    sys.exit(1)

# Extract data, texts, and colors from the JSON object
data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for Plotly
categories = [item['category'] for item in data]
values = [item['value'] for item in data]
bar_texts = [f"<b>{v}%</b>" if v != int(v) else f"<b>{int(v)}%</b>" for v in values]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0] if colors else '#1f77b4',
    text=bar_texts,
    textposition='outside',
    textfont=dict(family="Arial", size=14, color='black'),
    cliponaxis=False
))

# Update layout
fig.update_layout(
    font=dict(family="Arial", size=12, color="#333333"),
    title_text=None,
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        zeroline=False,
        linecolor='black',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 9.5],
        tickvals=list(range(10)),
        ticktext=[f"{i}%" for i in range(10)],
        gridcolor='#e0e0e0',
        zeroline=False,
        tickfont=dict(size=12)
    ),
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=20, t=50, b=100),
    annotations=[
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.2,
            xanchor='right',
            yanchor='top',
            font=dict(family="Arial", size=10, color='#666666')
        )
    ]
)

# Define output filename and save the image
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")