import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check for the required command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {Path(__file__).name} <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Read and parse the JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_details = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_file_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Failed to decode JSON from '{json_file_path}'.")
    sys.exit(1)

# Extract data and text from the JSON object
chart_data = chart_details.get('chart_data', [])
texts = chart_details.get('texts', {})
colors = chart_details.get('colors', [])

# Prepare data for Plotly
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the horizontal bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0]),
    hoverinfo='none'
))

# Style the text labels on the bars
fig.update_traces(
    texttemplate='%{x}%',
    textposition='outside',
    textfont=dict(family="Arial", size=12, color='black'),
    cliponaxis=False  # Prevents text from being clipped at the plot edge
)

# Configure the layout
fig.update_layout(
    font=dict(family="Arial", size=12, color='black'),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=280, r=60, t=40, b=80),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        ticksuffix='%',
        showgrid=True,
        gridcolor='#E0E0E0',
        zeroline=False,
        # Set range dynamically to provide space for 'outside' text
        range=[0, max(values) * 1.15]
    ),
    yaxis=dict(
        # 'reversed' ensures the first category in the list is at the top
        autorange='reversed',
        showgrid=False,
        zeroline=False,
        ticks='outside',
        ticklen=5
    ),
    annotations=[
        dict(
            text=texts.get('source', ''),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.15,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(size=12)
        )
    ]
)

# Generate the output PNG file
base_filename = Path(json_file_path).stem
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved to {output_filename}")