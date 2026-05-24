import sys
import json
import pathlib
import plotly.graph_objects as go

# --- 1. Load Data ---
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])
output_filename_base = json_path.stem

# --- 2. Prepare Data for Plotting ---
categories = [d['category'] for d in chart_data]
values = [d['value'] for d in chart_data]
numerators = [d['annotation_top_numerator'] for d in chart_data]
denominators = [d['annotation_top_denominator'] for d in chart_data]

# --- 3. Create Figure ---
fig = go.Figure()

# --- 4. Add Bar Trace ---
fig.add_trace(go.Bar(
    x=list(range(len(categories))),
    y=values,
    marker_color=colors[0] if colors else '#000000',
    showlegend=False,
    width=0.7
))

# --- 5. Prepare Layout Elements (Annotations and Shapes) ---
annotations = []
shapes = []

# Top fraction annotations and lines
y_num_paper = 1.09
y_den_paper = 1.01
y_line_paper = 1.05
for i, cat in enumerate(categories):
    annotations.append(go.layout.Annotation(
        x=i, y=y_num_paper, text=numerators[i], xref='x', yref='paper',
        showarrow=False, font=dict(family="Arial", size=11, color='black'),
        align='center'
    ))
    annotations.append(go.layout.Annotation(
        x=i, y=y_den_paper, text=denominators[i], xref='x', yref='paper',
        showarrow=False, font=dict(family="Arial", size=11, color='black'),
        align='center'
    ))
    shapes.append(go.layout.Shape(
        type='line', x0=i - 0.25, y0=y_line_paper, x1=i + 0.25, y1=y_line_paper,
        xref='x', yref='paper', line=dict(color='black', width=1)
    ))

# Bottom year labels and lines
y_year_line_paper = -0.16
y_year_text_paper = -0.22
year_labels = texts.get('x_axis_years', [])
if len(year_labels) == 3:
    # 1999
    annotations.append(go.layout.Annotation(
        x=0, y=y_year_text_paper, text=year_labels[0], xref='x', yref='paper',
        showarrow=False, font=dict(family="Arial", size=12, color='black')
    ))
    shapes.append(go.layout.Shape(
        type='line', x0=-0.5, y0=y_year_line_paper, x1=0.5, y1=y_year_line_paper,
        xref='x', yref='paper', line=dict(color='black', width=1)
    ))
    # 2000
    annotations.append(go.layout.Annotation(
        x=6.5, y=y_year_text_paper, text=year_labels[1], xref='x', yref='paper',
        showarrow=False, font=dict(family="Arial", size=12, color='black')
    ))
    shapes.append(go.layout.Shape(
        type='line', x0=0.5, y0=y_year_line_paper, x1=12.5, y1=y_year_line_paper,
        xref='x', yref='paper', line=dict(color='black', width=1)
    ))
    # 2001
    annotations.append(go.layout.Annotation(
        x=17.5, y=y_year_text_paper, text=year_labels[2], xref='x', yref='paper',
        showarrow=False, font=dict(family="Arial", size=12, color='black')
    ))
    shapes.append(go.layout.Shape(
        type='line', x0=12.5, y0=y_year_line_paper, x1=22.5, y1=y_year_line_paper,
        xref='x', yref='paper', line=dict(color='black', width=1)
    ))

# Vertical separator lines for year groups
shapes.append(go.layout.Shape(
    type='line', x0=0.5, y0=-0.01, x1=0.5, y1=1,
    xref='x', yref='paper', line=dict(color='black', width=1)
))
shapes.append(go.layout.Shape(
    type='line', x0=12.5, y0=-0.01, x1=12.5, y1=1,
    xref='x', yref='paper', line=dict(color='black', width=1)
))

# --- 6. Update Layout and Axes ---
fig.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=14, color="black"),
    margin=dict(l=80, r=20, t=100, b=100),
    annotations=annotations,
    shapes=shapes
)

fig.update_xaxes(
    tickvals=list(range(len(categories))),
    ticktext=categories,
    showline=True,
    linewidth=1.5,
    linecolor='black',
    ticks='outside',
    tickfont=dict(size=12)
)

fig.update_yaxes(
    title_text=texts.get('y_axis_title'),
    title_font=dict(size=16),
    range=[0, 16],
    tickvals=[0, 2, 4, 6, 8, 10, 12, 14, 16],
    showline=True,
    linewidth=1.5,
    linecolor='black',
    ticks='outside',
    showgrid=False,
    zeroline=False
)

# --- 7. Output Image ---
output_path = f"{output_filename_base}.png"
fig.write_image(output_path, scale=2)
print(f"Chart saved to '{output_path}'")