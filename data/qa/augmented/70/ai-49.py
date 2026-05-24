import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_details = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print("Error: Could not decode JSON from the file.")
    sys.exit(1)

chart_data = chart_details.get('chart_data', [])
texts = chart_details.get('texts', {})
colors = chart_details.get('colors', [])

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

# Define text positions for each data point to match the source image
text_positions = [
    'top center', 'top center', 'top center', 'bottom center',
    'top left', 'top center', 'top right'
]

# Add the main line trace
fig.add_trace(go.Scatter(
    x=categories,
    y=values,
    mode='lines+markers+text',
    line=dict(color=colors[0], width=2.5),
    marker=dict(color=colors[0], size=7),
    text=[f"{v}%" for v in values],
    textposition=text_positions,
    textfont=dict(
        family="Arial",
        size=12,
        color='#333333'
    ),
    hoverinfo='none'
))

# Update layout
fig.update_layout(
    font=dict(family="Arial", size=12, color='#333333'),
    title=dict(
        text=texts.get('title'),
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        showline=True,
        linecolor='lightgrey',
        tickfont=dict(color='grey')
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        title_font=dict(color='grey'),
        range=[0, 23],
        dtick=2.5,
        ticksuffix='%',
        showline=False,
        gridcolor='#EAEAEA',
        gridwidth=1,
        griddash='dash',
        zeroline=False,
        tickfont=dict(color='grey')
    ),
    plot_bgcolor='white',
    paper_bgcolor='#F8F9FA',
    showlegend=False,
    margin=dict(l=80, r=40, b=100, t=50),
    annotations=[
        dict(
            text=texts.get('note'),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=-0.25,
            xanchor='left',
            yanchor='bottom',
            font=dict(color=colors[0], size=13)
        ),
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.25,
            xanchor='right',
            yanchor='bottom',
            align='right',
            font=dict(color='grey', size=12)
        )
    ]
)

# Determine output filename from input JSON path
base_filename = json_file_path.rsplit('.', 1)[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")