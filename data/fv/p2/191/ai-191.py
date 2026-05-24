import sys
import json
import plotly.graph_objects as go

# Check for the JSON file path argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read the JSON data file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and texts from the JSON object
data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

categories = [d['category'] for d in data]
series1_values = [d['Bernie Sanders'] for d in data]
series2_values = [d['Hilary Clinton'] for d in data]
line_values = [d['Cumulative Gap'] for d in data]

# Create the figure object
fig = go.Figure()

# Add bar traces for the two series, assigned to the secondary y-axis
fig.add_trace(go.Bar(
    x=categories,
    y=series1_values,
    name=texts['legend_title_1'],
    marker_color=colors[0],
    yaxis='y2'
))

fig.add_trace(go.Bar(
    x=categories,
    y=series2_values,
    name=texts['legend_title_2'],
    marker_color=colors[1],
    yaxis='y2'
))

# Add the cumulative line trace, assigned to the primary y-axis
fig.add_trace(go.Scatter(
    x=categories,
    y=line_values,
    mode='lines',
    name='Cumulative Gap',
    line=dict(color=colors[2], width=2.5),
    yaxis='y1',
    showlegend=False
))

# Update layout
fig.update_layout(
    barmode='relative',
    template='plotly_white',
    font=dict(family="Arial", size=12),
    margin=dict(l=80, r=80, t=50, b=150),
    yaxis=dict(
        title=texts['y_axis_title'],
        range=[-350, 50],
        tickmode='linear',
        tick0=-350,
        dtick=50,
        gridcolor='lightgrey',
        showline=True,
        linewidth=1.5,
        linecolor='black',
        mirror=True
    ),
    yaxis2=dict(
        title=texts['y2_axis_title'],
        overlaying='y',
        side='right',
        range=[-75, 50],
        tickmode='linear',
        tick0=-75,
        dtick=25,
        showgrid=False,
        zeroline=True,
        zerolinewidth=1,
        zerolinecolor='black',
        showline=True,
        linewidth=1.5,
        linecolor='black',
        mirror=True
    ),
    xaxis=dict(
        title=texts['x_axis_title'],
        tickangle=-90,
        showgrid=False,
        showline=True,
        linewidth=1.5,
        linecolor='black',
        mirror=True
    ),
    legend=dict(
        x=0.02,
        y=0.25,
        xanchor='left',
        yanchor='bottom',
        bgcolor='rgba(255, 255, 255, 0.8)',
        bordercolor='black',
        borderwidth=0
    ),
    annotations=[
        dict(
            text=texts['source'],
            align='left',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.98,
            y=0.01,
            xanchor='right',
            yanchor='bottom',
            font=dict(size=10, color='grey')
        )
    ]
)

# Generate the output PNG file
if '.' in json_path:
    base_name = json_path.rsplit('.', 1)[0]
else:
    base_name = json_path

output_filename = f"{base_name}.png"
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")