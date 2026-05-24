import sys
import json
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_path = sys.argv[1]

# Read data from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and texts from the JSON structure
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Prepare data for Plotly; reverse to match visual top-to-bottom order
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]
categories.reverse()
values.reverse()

# Format text labels to remove '.0' for whole numbers
text_labels = [str(int(v)) if v == int(v) else str(v) for v in values]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0]),
    text=text_labels,
    textposition='outside',
    cliponaxis=False,
    textfont=dict(family="Arial", size=12, color='black')
))

# Update layout for a clean, professional look
fig.update_layout(
    font=dict(family="Arial", size=12, color='#333333'),
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#E5E5E5',
        griddash='dot',
        zeroline=False,
        showline=False,
        showticklabels=True,
        range=[0, max(values) * 1.25], # Ensure space for labels
        tickmode='linear',
        tick0=0,
        dtick=5
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=False,
        showticklabels=True,
        categoryorder='array',
        categoryarray=categories
    ),
    margin=dict(l=100, r=40, t=40, b=80),
    showlegend=False,
    annotations=[
        dict(
            text=texts.get('note'),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=-0.1,
            xanchor='left',
            yanchor='top',
            font=dict(family="Arial", size=12, color="#007bff")
        ),
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.1,
            xanchor='right',
            yanchor='top',
            font=dict(family="Arial", size=12, color="#666666")
        )
    ]
)

# Generate the output filename from the input JSON path
output_filename = json_path.rsplit('.', 1)[0] + '.png'

# Save the chart as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")