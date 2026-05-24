import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Prepare data for Plotly
chart_data = chart_info['chart_data']
categories = [d['category'] for d in chart_data]
values = [d['value'] for d in chart_data]
display_texts = [d['text'] for d in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=display_texts,
    textposition='outside',
    marker_color=chart_info['colors'][0],
    cliponaxis=False
))

# Style the data labels on top of the bars
fig.update_traces(textfont=dict(color='black', size=12))

# Create annotations list for source text
annotations = []
if chart_info['texts'].get('source'):
    annotations.append(
        go.layout.Annotation(
            xref='paper', yref='paper',
            x=0.99, y=-0.22,
            xanchor='right', yanchor='top',
            text=chart_info['texts']['source'],
            showarrow=False,
            font=dict(size=12, color='grey')
        )
    )

# Update layout for a clean and accurate appearance
fig.update_layout(
    title_text=chart_info['texts'].get('title'),
    font=dict(family="Arial"),
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=50, b=120),
    yaxis=dict(
        title_text=chart_info['texts'].get('y_axis_title'),
        range=[0, 70000],
        tickvals=[0, 10000, 20000, 30000, 40000, 50000, 60000, 70000],
        ticktext=["0", "10 000", "20 000", "30 000", "40 000", "50 000", "60 000", "70 000"],
        showgrid=True,
        gridcolor='#e0e0e0',
        griddash='dash',
        zeroline=False,
        showline=False
    ),
    xaxis=dict(
        title_text=chart_info['texts'].get('x_axis_title'),
        showgrid=False,
        zeroline=False,
        showline=True,
        linecolor='black'
    ),
    annotations=annotations
)

# Determine output filename from JSON path
base_filename = pathlib.Path(json_path).stem
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")