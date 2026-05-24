import sys
import json
import plotly.graph_objects as go

# Check if a command-line argument is provided
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Derive the output filename from the JSON filename
if json_path.endswith('.json'):
    output_filename = json_path[:-5] + '.png'
else:
    output_filename = json_path + '.png'

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


# Extract data and texts
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for Plotly
x_values = [item['x'] for item in chart_data]
y_values = [item['y'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(
    go.Bar(
        x=x_values,
        y=y_values,
        marker_color=colors[0] if colors else None,
        text=y_values,
        textposition='outside',
        texttemplate='%{y:.2f}',
        cliponaxis=False,
        hoverinfo='none',
        showlegend=False
    )
)

# Update layout to match the original image
fig.update_layout(
    font_family="Arial",
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=80, r=20, t=40, b=80),
    xaxis=dict(
        title_text=texts.get('xaxis_title'),
        showgrid=False,
        zeroline=False,
        linecolor='black',
        linewidth=1
    ),
    yaxis=dict(
        title_text=texts.get('yaxis_title'),
        range=[0, 10],
        tickmode='linear',
        tick0=0,
        dtick=2,
        gridcolor='#dddddd',
        griddash='dot',
        zeroline=False,
        showline=False
    ),
    annotations=[
        dict(
            text=texts.get('source', ''),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.99,
            y=-0.15,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(size=12, color='#666666')
        )
    ]
)

# Update text font on bars
fig.update_traces(
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    )
)


# Save the figure to a PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved to {output_filename}")