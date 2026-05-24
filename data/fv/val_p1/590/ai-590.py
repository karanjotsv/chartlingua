import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Load data from JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# Extract data for the chart
data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

labels = [item['label'] for item in data]
values = [item['value'] for item in data]

# Create the pie chart trace
pie_trace = go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='black', width=1)),
    hoverinfo='label+percent',
    textinfo='none',
    sort=False,  # Preserve the original order of the data
    direction='clockwise',
    rotation=105,
    domain=dict(x=[0, 0.75]) # Allocate space on the right for the legend
)

# Create the figure
fig = go.Figure(data=[pie_trace])

# Update layout
fig.update_layout(
    font=dict(family="Arial", size=12),
    plot_bgcolor='#DCDCDC',
    paper_bgcolor='white',
    showlegend=True,
    legend=dict(
        x=0.8,
        y=0.5,
        xanchor='left',
        yanchor='middle',
        bgcolor='rgba(255,255,255,0.7)',
        bordercolor='Black',
        borderwidth=1
    ),
    width=1100,
    height=800,
    margin=dict(l=50, r=50, t=50, b=200),
    annotations=[
        dict(
            text=texts['source'],
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=0,
            xanchor='left',
            yanchor='top',
            align='left',
            font=dict(size=11)
        )
    ]
)

# Generate the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    print("Please ensure you have the 'kaleido' package installed ('pip install kaleido')")