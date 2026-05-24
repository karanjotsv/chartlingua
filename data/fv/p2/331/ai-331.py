import sys
import json
import pathlib
import plotly.graph_objects as go

# --- 1. Load Data ---
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# --- 2. Prepare Chart Data and Styles ---
data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']
fonts = chart_data['fonts']
table_data = chart_data['table_data']

labels = [d['label'] for d in data]
values = [d['value'] for d in data]

# Determine text position and size based on slice value
text_positions = ['inside' if v > 5 else 'outside' for v in values]
text_font_sizes = [fonts['pie_label_inside_size'] if pos == 'inside' else fonts['pie_label_outside_size'] for pos in text_positions]

# --- 3. Create Pie Chart ---
fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    hole=0,
    marker_colors=colors['pie_slices'],
    pull=[0.02] * len(values),
    texttemplate="%{value}%<br>%{label}",
    textposition=text_positions,
    textfont=dict(
        family=fonts['family'],
        size=text_font_sizes,
        color=colors['pie_label_text']
    ),
    hoverinfo='label+percent',
    sort=False,
    direction='clockwise',
    rotation=100
))

# --- 4. Create Title ---
title_text = (
    f"<span style='font-weight:bold; color:{colors['title_highlight']};'>{texts['title_part1']}</span>"
    f"<span style='color:{colors['title_main']};'> {texts['title_part2']}</span>"
)

# --- 5. Add Table using Annotations and Shapes ---
annotations = []
shapes = []

# Table position and dimensions
table_x_start = 0.8
table_x_end = 1.0
table_y_start = 0.65
row_height = 0.05
col_width_cat = 0.15

# Table Title
annotations.append(dict(
    xref="paper", yref="paper",
    x=table_x_start, y=table_y_start + 0.05,
    xanchor='left', yanchor='bottom',
    text=f"<b>{texts['table_title']}</b>",
    font=dict(family=fonts['family'], size=fonts['table_title_size'], color=colors['table_title']),
    showarrow=False
))
# Table Subtitle
annotations.append(dict(
    xref="paper", yref="paper",
    x=table_x_end, y=table_y_start + 0.05,
    xanchor='right', yanchor='bottom',
    text=f"<b>{texts['table_subtitle']}</b>",
    font=dict(family=fonts['family'], size=fonts['table_subtitle_size'], color=colors['table_title']),
    showarrow=False
))

# Table Lines
shapes.append(dict(type='line', xref='paper', yref='paper', x0=table_x_start, y0=table_y_start + 0.04, x1=table_x_end, y1=table_y_start + 0.04, line=dict(color=colors['table_lines'], width=2)))
shapes.append(dict(type='line', xref='paper', yref='paper', x0=table_x_start, y0=table_y_start + 0.03, x1=table_x_end, y1=table_y_start + 0.03, line=dict(color=colors['table_lines'], width=1)))

# Table Rows
current_y = table_y_start
for item in table_data:
    # Category
    annotations.append(dict(
        xref='paper', yref='paper',
        x=table_x_start, y=current_y,
        xanchor='left', yanchor='middle',
        text=item['category'],
        font=dict(family=fonts['family'], size=fonts['table_text_size'], color=colors['table_text']),
        showarrow=False
    ))
    # Value
    annotations.append(dict(
        xref='paper', yref='paper',
        x=table_x_end, y=current_y,
        xanchor='right', yanchor='middle',
        text=item['value'],
        font=dict(family=fonts['family'], size=fonts['table_text_size'], color=colors['table_text']),
        showarrow=False
    ))
    current_y -= row_height

# --- 6. Configure Layout ---
fig.update_layout(
    title_text=title_text,
    title_x=0,
    title_y=0.98,
    title_font=dict(
        family=fonts['family'],
        size=fonts['title_size']
    ),
    showlegend=False,
    paper_bgcolor='white',
    plot_bgcolor='white',
    width=800,
    height=600,
    margin=dict(t=80, b=40, l=40, r=40),
    annotations=annotations,
    shapes=shapes
)

# --- 7. Save Image ---
filename_base = json_path.stem
output_filename = f"{filename_base}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")