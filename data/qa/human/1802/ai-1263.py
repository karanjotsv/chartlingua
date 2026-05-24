import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

# Extract data from JSON
data_series = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

# Data is ordered top-to-bottom in JSON. Reverse for Plotly's bottom-to-top rendering.
data_series.reverse()
colors.reverse()

categories = [item['category'] for item in data_series]
values = [item['value'] for item in data_series]

# Create figure
fig = go.Figure()

# Add bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors),
    text=values,
    textposition='outside',
    texttemplate='%{text}',
    cliponaxis=False  # Prevents text labels from being clipped
))

# Update layout
title_text = f"<b>{texts['title']}</b><br>{texts['subtitle']}"
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.02,
        y=0.95,
        xanchor='left',
        yanchor='top',
        font=dict(size=20)
    ),
    xaxis=dict(
        visible=False,
        range=[0, max(values) * 1.15]  # Add padding for text labels
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=False,
        autorange="reversed" # An alternative to reversing data, but reversing data is often more explicit
    ),
    font=dict(
        family="Arial",
        size=14,
        color="black"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=170, r=40, t=140, b=160),
    showlegend=False
)
# Reverse y-axis to match the original image order (top-to-bottom)
fig.update_yaxes(autorange="reversed")

# Add source text as an annotation
fig.add_annotation(
    text=texts['source'],
    align='left',
    showarrow=False,
    xref='paper',
    yref='paper',
    x=0,
    y=-0.18,
    xanchor='left',
    yanchor='top'
)

# Add line separator above the footer
fig.add_shape(
    type="line",
    xref="paper",
    yref="paper",
    x0=0,
    y0=-0.26,
    x1=1,
    y1=-0.26,
    line=dict(
        color="grey",
        width=1,
    )
)

# Add footer text as an annotation
fig.add_annotation(
    text=f"<b>{texts['footer']}</b>",
    align='left',
    showarrow=False,
    xref='paper',
    yref='paper',
    x=0,
    y=-0.28,
    xanchor='left',
    yanchor='top'
)


# Output the image
base_filename = json_file_path.rsplit('.', 1)[0]
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")