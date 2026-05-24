import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# --- 1. Load Data from JSON ---
if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <path_to_json>")
    sys.exit(1)

json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# --- 2. Extract data and settings from JSON ---
data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

main_chart_data = data['main_chart']
inset_chart_data = data['inset_chart']

# --- 3. Create Figure ---
fig = go.Figure()

# --- 4. Add Main Chart Trace ---
fig.add_trace(go.Bar(
    y=main_chart_data['categories'],
    x=main_chart_data['values'],
    orientation='h',
    marker=dict(color=colors['bars']),
    text=[f"{v}%" for v in main_chart_data['values']],
    textposition='inside',
    insidetextanchor='middle',
    textfont=dict(color=colors['text_light'], family="Arial", weight='bold'),
    hoverinfo='none',
    xaxis='x1',
    yaxis='y1'
))

# --- 5. Add Inset Chart Trace ---
fig.add_trace(go.Bar(
    y=inset_chart_data['categories'],
    x=inset_chart_data['values'],
    orientation='h',
    marker=dict(color=colors['bars']),
    text=[f"{v}%" for v in inset_chart_data['values']],
    textposition='outside',
    textfont=dict(color=colors['text_dark'], family="Arial"),
    hoverinfo='none',
    xaxis='x2',
    yaxis='y2'
))

# --- 6. Configure Layout ---
fig.update_layout(
    # Titles and Font
    title=dict(
        text=f"<b>{texts['title']}</b>",
        font=dict(family="Arial", size=16),
        x=0.05,
        xanchor='left'
    ),
    font=dict(family="Arial", size=11),
    showlegend=False,
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    margin=dict(l=250, r=40, t=80, b=80),

    # Main Axes (x1, y1)
    xaxis=dict(
        domain=[0.0, 0.45],
        showticklabels=False,
        showgrid=True,
        gridcolor=colors['grid'],
        zeroline=False,
        range=[0, max(main_chart_data['values']) * 1.15]
    ),
    yaxis=dict(
        domain=[0.0, 1.0],
        autorange="reversed",
        showgrid=False,
        zeroline=False,
        showline=False,
        ticks='',
        tickfont=dict(size=10)
    ),

    # Inset Axes (x2, y2)
    xaxis2=dict(
        domain=[0.62, 0.98],
        showticklabels=False,
        showgrid=False,
        zeroline=False,
        range=[0, max(inset_chart_data['values']) * 1.25]
    ),
    yaxis2=dict(
        domain=[0.25, 0.73],
        autorange="reversed",
        showgrid=False,
        showticklabels=False, # Labels are added as annotations
        ticks=''
    ),

    # Shapes for inset box and connector lines
    shapes=[
        # Inset background box
        go.layout.Shape(
            type="rect", xref="paper", yref="paper",
            x0=0.58, y0=0.22, x1=1.0, y1=0.76,
            line=dict(color=colors['lines'], width=1),
            fillcolor=colors['background'],
            layer="below"
        ),
        # Top connector line
        go.layout.Shape(
            type="line", xref="paper", yref="paper",
            x0=0.24, y0=0.56, x1=0.58, y1=0.76,
            line=dict(color=colors['lines'], width=1)
        ),
        # Bottom connector line
        go.layout.Shape(
            type="line", xref="paper", yref="paper",
            x0=0.24, y0=0.5, x1=0.58, y1=0.22,
            line=dict(color=colors['lines'], width=1)
        )
    ]
)

# --- 7. Add Annotations for Labels and Text ---
annotations = [
    # Subtitle
    go.layout.Annotation(
        text=texts['subtitle'],
        xref="paper", yref="paper",
        x=0.5, y=1.01,
        showarrow=False,
        xanchor='center',
        font=dict(size=12, color=colors['lines'])
    ),
    # Inset title
    go.layout.Annotation(
        text=texts['inset_title'],
        xref="paper", yref="paper",
        x=0.6, y=0.74,
        align='left',
        showarrow=False,
        xanchor='left', yanchor='bottom',
        font=dict(size=12)
    ),
    # Footer Left
    go.layout.Annotation(
        text=texts['footer_left'],
        xref="paper", yref="paper",
        x=0, y=-0.08,
        showarrow=False,
        xanchor='left',
        font=dict(size=10, color=colors['lines'])
    ),
    # Source (Footer Right)
    go.layout.Annotation(
        text=texts['source'],
        xref="paper", yref="paper",
        x=1, y=-0.08,
        showarrow=False,
        xanchor='right',
        font=dict(size=10, color=colors['lines'])
    )
]

# Add annotations for inset chart y-axis labels (for right alignment)
for category in inset_chart_data['categories']:
    annotations.append(go.layout.Annotation(
        text=category,
        x=0,
        y=category,
        xref='x2 domain',
        yref='y2',
        showarrow=False,
        xanchor='right',
        ax=-10,  # pixels to shift left from x position
        align='right',
        font=dict(size=10)
    ))
fig.update_layout(annotations=annotations)


# --- 8. Output Image ---
output_filename = json_path.stem + ".png"
fig.write_image(output_filename, scale=2)
print(f"Chart saved as {output_filename}")