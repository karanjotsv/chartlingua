import sys
import json
import pathlib
import plotly.graph_objects as go

# --- 1. Load data from JSON file specified by command-line argument ---
if len(sys.argv) < 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_file_path = pathlib.Path(sys.argv[1])
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_config = json.load(f)

# --- 2. Extract and prepare data for Plotly ---
chart_data = chart_config['chart_data']
texts = chart_config['texts']
bar_color = chart_config['colors'][0]

# Extract categories and values from the data structure
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Reverse data for top-to-bottom display in a horizontal bar chart
categories.reverse()
values.reverse()

# Format text labels: show integers without decimal, hide labels for zero values
text_labels = []
for v in values:
    if v > 0:
        if v == int(v):
            text_labels.append(str(int(v)))
        else:
            text_labels.append(f"{v:.2f}")
    else:
        text_labels.append('') # Empty string for zero or non-positive values

# --- 3. Create the chart using Plotly ---
fig = go.Figure()

# Add the horizontal bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=bar_color, line=dict(width=0)),
    text=text_labels,
    textposition='outside',
    cliponaxis=False,  # Allow text labels to be drawn outside the plot area
    insidetextanchor='end'
))

# --- 4. Configure layout and styling for accuracy and readability ---
fig.update_layout(
    font=dict(family="Arial", size=12, color="#333333"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(
        showgrid=True,
        gridcolor='rgba(230, 230, 230, 0.8)',
        gridwidth=1,
        zeroline=False,
        showline=False,
        showticklabels=False,
        title=dict(
            text=texts['x_axis_title'],
            standoff=10,
            font=dict(size=12, color='gray')
        ),
        # Extend range to provide space for text labels on the right
        range=[0, max(values) * 1.15]
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=True,
        linecolor='black',
        linewidth=1,
        autorange=True # Use autorange and pre-reversed data
    ),
    margin=dict(l=150, r=40, t=30, b=80),
    showlegend=False,
    # Add source text as an annotation
    annotations=[
        dict(
            text=texts['source'],
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.12,
            xanchor='right',
            yanchor='top',
            font=dict(size=10, color='gray')
        )
    ]
)

# Update trace-specific text font properties
fig.update_traces(
    textfont=dict(
        family='Arial',
        size=12,
        color='black'
    )
)

# --- 5. Output the chart as a PNG image ---
output_image_path = json_file_path.with_suffix('.png')
fig.write_image(output_image_path, scale=2)

print(f"Chart successfully generated and saved to {output_image_path}")