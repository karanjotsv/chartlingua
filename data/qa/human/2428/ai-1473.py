import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

fig = go.Figure()

# Extract data and settings from JSON
categories = chart_data['chart_data']['categories']
series_data = chart_data['chart_data']['series']
colors = chart_data['colors']
texts = chart_data['texts']

# Add bar traces for each series
for i, series in enumerate(series_data):
    fig.add_trace(go.Bar(
        x=categories,
        y=series['values'],
        name=series['name'],
        marker_color=colors[i],
        text=[f'{v}%' for v in series['values']],
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(
            family='Arial, bold',
            size=14,
            color='white'
        ),
        hoverinfo='skip'
    ))

# Update layout
fig.update_layout(
    barmode='stack',
    template='plotly_white',
    font=dict(
        family="Arial",
        size=12
    ),
    title_text=texts.get('title'),
    yaxis_title_text=texts.get('y_axis_title'),
    yaxis=dict(
        range=[0, 100.1],
        tickvals=[0, 25, 50, 75, 100],
        ticksuffix='%',
        showgrid=True,
        gridcolor='#dddddd',
        zeroline=False,
        showline=False
    ),
    xaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=False
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.25,
        xanchor="center",
        x=0.5,
        traceorder='normal'
    ),
    margin=dict(l=80, r=40, t=50, b=150)
)

# Add source annotation if present
if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        xref="paper",
        yref="paper",
        x=1,
        y=-0.3,
        xanchor='right',
        yanchor='bottom',
        showarrow=False,
        font=dict(
            family="Arial",
            size=10,
            color="grey"
        )
    )

# Define output filename and save the image
base_filename = json_path.rsplit('.', 1)[0]
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")