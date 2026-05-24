import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

# Load data from JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_config = json.load(f)

chart_data = chart_config['chart_data']
texts = chart_config['texts']
colors = chart_config['colors']

# Prepare data for Plotly
x_values = [d['x'] for d in chart_data]
y_values = [d['y'] for d in chart_data]

# Create the figure
fig = go.Figure()

# Add the line trace
fig.add_trace(go.Scatter(
    x=x_values,
    y=y_values,
    mode='lines+markers',
    line=dict(color=colors[0], width=2.5),
    marker=dict(color=colors[0], size=7),
    showlegend=False
))

# Add data labels for points that have them
for point in chart_data:
    if point.get('label'):
        fig.add_annotation(
            x=point['x'],
            y=point['y'],
            text=point['label'],
            showarrow=False,
            font=dict(family="Arial", size=12, color="black"),
            xanchor='center',
            yanchor='bottom',
            yshift=10
        )

# Update layout
fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    width=800,
    height=600,
    margin=dict(l=80, r=40, t=50, b=120),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        showgrid=True,
        gridcolor='#EAEAEA',
        gridwidth=1,
        range=[30000, 40000],
        tickvals=[30000, 32000, 34000, 36000, 38000, 40000],
        ticktext=["30 000", "32 000", "34 000", "36 000", "38 000", "40 000"],
        zeroline=False,
        showline=False
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        tickmode='array',
        tickvals=list(range(2000, 2020)),
        tickangle=0,
        zeroline=False,
        showline=False
    )
)

# Add source and note as annotations
if texts.get('note'):
    fig.add_annotation(
        text=texts['note'],
        xref="paper", yref="paper",
        x=-0.1, y=-0.18,
        showarrow=False,
        xanchor='left',
        yanchor='bottom',
        font=dict(family="Arial", size=12, color="black")
    )
if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        xref="paper", yref="paper",
        x=1.0, y=-0.18,
        showarrow=False,
        xanchor='right',
        yanchor='bottom',
        font=dict(family="Arial", size=12, color="#888888")
    )

# Determine output filename from JSON path
base_name = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_name}.png"

# Save the figure
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")