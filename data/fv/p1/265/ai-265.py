import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data_json = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data from JSON
data = chart_data_json['chart_data']
texts = chart_data_json['texts']
colors = chart_data_json['colors']

# Reverse data order for correct Plotly plotting (top-to-bottom)
data.reverse()

categories = [item['category'] for item in data]
values_left = [item['values'][0] for item in data]
values_right = [item['values'][1] for item in data]

# Create the figure
fig = go.Figure()

# Add left bar trace (Number of fatal work injuries)
fig.add_trace(go.Bar(
    x=values_left,
    y=categories,
    orientation='h',
    name=texts['x_axis_title_left'].replace('<br>', ' '),
    marker_color=colors[0],
    text=values_left,
    textposition='outside',
    xaxis='x2',
    cliponaxis=False,
    hoverinfo='none'
))

# Add right bar trace (Fatal work injury rate)
fig.add_trace(go.Bar(
    x=values_right,
    y=categories,
    orientation='h',
    name=texts['x_axis_title_right'].replace('<br>', ' '),
    marker_color=colors[1],
    text=values_right,
    textposition='outside',
    xaxis='x',
    cliponaxis=False,
    hoverinfo='none'
))

# Update layout
fig.update_layout(
    title={
        'text': f"<b>{texts['title']}</b>",
        'x': 0.5,
        'xanchor': 'center'
    },
    font={
        'family': "Arial",
        'size': 12
    },
    width=950,
    height=600,
    showlegend=False,
    plot_bgcolor='white',
    barmode='relative',
    margin=dict(l=300, r=60, t=80, b=100),
    yaxis=dict(
        showgrid=False,
        showline=True,
        linecolor='black',
        linewidth=1,
        ticks='outside',
        ticklen=5,
        autorange=True,
        zeroline=False
    ),
    xaxis=dict(
        title=texts['x_axis_title_right'],
        side='bottom',
        domain=[0.51, 1],
        range=[0, 200],
        showline=True,
        linecolor='black',
        linewidth=1,
        showgrid=True,
        gridcolor='#e0e0e0',
        zeroline=False
    ),
    xaxis2=dict(
        title=texts['x_axis_title_left'],
        side='bottom',
        domain=[0, 0.49],
        range=[1050, 0],
        tickvals=[1000, 500, 0],
        showline=True,
        linecolor='black',
        linewidth=1,
        showgrid=False,
        zeroline=False
    ),
    annotations=[
        dict(
            xref='paper', yref='paper',
            x=0, y=-0.15,
            xanchor='left', yanchor='top',
            text=texts['source'],
            showarrow=False,
            font=dict(size=10)
        )
    ]
)

fig.update_traces(textfont_size=11)

# Generate output filename from JSON path
output_filename = pathlib.Path(json_path).stem + ".png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")