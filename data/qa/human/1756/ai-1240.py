import sys
import json
import pathlib
import plotly.graph_objects as go

# 1. Argument Parsing and File Handling
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <path_to_json_file>", file=sys.stderr)
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}", file=sys.stderr)
    sys.exit(1)

output_path = json_path.with_suffix(".png")

# 2. Load JSON data
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except (json.JSONDecodeError, FileNotFoundError) as e:
    print(f"Error reading or parsing JSON file: {e}", file=sys.stderr)
    sys.exit(1)

# 3. Data Preparation
chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

categories = texts['categories']
series1 = chart_data[0]
series2 = chart_data[1]

# Negate values for the first series to create the diverging effect
series1_values_neg = [-v for v in series1['values']]

# 4. Create Figure
fig = go.Figure()

# 5. Add Traces
# Left side bars (Reliance on principles)
fig.add_trace(go.Bar(
    y=categories,
    x=series1_values_neg,
    orientation='h',
    name=series1['name'],
    marker=dict(color=colors[0], line=dict(width=0)),
    text=series1['values'],  # Display original positive values
    textposition='outside',
    textfont=dict(family="Arial", size=12, color='black'),
    hoverinfo='none'
))

# Right side bars (Ability to change)
fig.add_trace(go.Bar(
    y=categories,
    x=series2['values'],
    orientation='h',
    name=series2['name'],
    marker=dict(color=colors[1], line=dict(width=0)),
    text=series2['values'],
    textposition='outside',
    textfont=dict(family="Arial", size=12, color='black'),
    hoverinfo='none'
))

# 6. Update Layout
# Determine a dynamic axis range to prevent text clipping
max_val = max(max(series1['values']), max(series2['values']))
axis_range = max_val * 1.25

# Combine title and subtitle using HTML for styling
title_text = f"<b>{texts['title']}</b><br><span style='font-size:15px; color:#555555;'>{texts['subtitle']}</span>"

# Combine source and logo notes
source_text = f"{texts['source']}<br><b>{texts['logo']}</b>"

fig.update_layout(
    barmode='relative',
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    font=dict(family="Arial", size=12, color='black'),
    margin=dict(l=100, r=40, t=140, b=100),
    title=dict(
        text=title_text,
        y=0.98,
        x=0,
        xanchor='left',
        yanchor='top',
        font=dict(size=20, family="Arial")
    ),
    xaxis=dict(
        showticklabels=False,
        showgrid=False,
        zeroline=False,
        showline=False,
        range=[-axis_range, axis_range]
    ),
    yaxis=dict(
        showline=False,
        showgrid=False,
        ticks='',
        tickfont=dict(size=14),
        autorange='reversed'  # Ensure the first category appears at the top
    ),
    annotations=[
        # Left header
        dict(
            xref='x', yref='y',
            x=-sum(series1['values'])/len(series1['values']),
            y=categories[0],
            yshift=35,
            text=f"<b>{series1['name']}</b>",
            showarrow=False,
            font=dict(size=14)
        ),
        # Right header
        dict(
            xref='x', yref='y',
            x=sum(series2['values'])/len(series2['values']),
            y=categories[0],
            yshift=35,
            text=f"<b>{series2['name']}</b>",
            showarrow=False,
            font=dict(size=14)
        ),
        # Source/Logo text
        dict(
            xref='paper', yref='paper',
            x=0, y=0.01,
            xanchor='left', yanchor='top',
            text=source_text,
            showarrow=False,
            align='left',
            font=dict(size=11, color='#555555')
        )
    ]
)

# 7. Output Image
fig.write_image(output_path, scale=2)
print(f"Chart saved to {output_path}")