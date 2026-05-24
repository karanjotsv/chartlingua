import sys
import json
import plotly.graph_objects as go
import os

# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_file_path):
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

# Read the chart data from the JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in '{json_file_path}'")
    sys.exit(1)

# Extract data for plotting
data_points = chart_data['chart_data']
categories = [d['category'] for d in data_points]
values = [d['value'] for d in data_points]
texts_data = chart_data['texts']
colors = chart_data['colors']

# Create formatted text for bar labels
bar_texts = [f"{d['value']}% ({d['year']})" for d in data_points]

# Create the bar chart trace
trace = go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors, line=dict(width=0)),
    text=bar_texts,
    textposition='outside',
    cliponaxis=False,
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    )
)

# Create the figure
fig = go.Figure(data=[trace])

# Update layout for a professional look
fig.update_layout(
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    title=dict(
        text=f"<b>{texts_data['title']}</b><br><span style='font-size:14px; color:#555555;'>{texts_data['subtitle']}</span>",
        x=0.01,
        y=0.95,
        xanchor='left',
        yanchor='top',
        font=dict(
            family="Arial",
            size=22
        )
    ),
    xaxis=dict(
        showgrid=True,
        gridcolor='#e0e0e0',
        griddash='dash',
        zeroline=False,
        showline=False,
        ticks='outside',
        tickfont=dict(size=14),
        ticksuffix='%',
        range=[0, max(values) * 1.18]
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=False,
        ticks='',
        tickfont=dict(size=14)
    ),
    plot_bgcolor='rgba(242, 242, 242, 1)',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=100, r=40, t=140, b=80),
    annotations=[
        dict(
            xref='paper',
            yref='paper',
            x=0.0,
            y=-0.15,
            xanchor='left',
            yanchor='top',
            text=texts_data['source'],
            showarrow=False,
            font=dict(size=12, color='#666666')
        ),
        dict(
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.15,
            xanchor='right',
            yanchor='top',
            text=texts_data['license'],
            showarrow=False,
            font=dict(size=12, color='#666666')
        )
    ]
)

# Generate the output filename from the input JSON filename
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_image_path = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_image_path, scale=2)

print(f"Chart saved as '{output_image_path}'")