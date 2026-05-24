import sys
import json
import os
import plotly.graph_objects as go

def main():
    if len(sys.argv) != 2:
        print(f"Usage: python {os.path.basename(__file__)} <path_to_json_file>")
        sys.exit(1)

    json_path = sys.argv[1]
    if not os.path.exists(json_path):
        print(f"Error: File not found at {json_path}")
        sys.exit(1)

    base_name = os.path.splitext(os.path.basename(json_path))[0]
    output_filename = f"{base_name}.png"

    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)

    data = chart_info['chart_data']
    texts = chart_info['texts']
    colors = chart_info['colors']
    
    x_values = [d['x'] for d in data]
    y_values = [d['y'] for d in data]
    bar_colors = [colors['category_colors'][d['category']] for d in data]

    fig = go.Figure()

    # Main bar chart trace
    fig.add_trace(go.Bar(
        x=x_values,
        y=y_values,
        marker_color=bar_colors,
        marker_line_color=colors['bar_outline'],
        marker_line_width=1,
        showlegend=False
    ))
    
    # Scatter trace for solid white circles on 'Strong La Niña' bars
    solid_circle_x = [d['x'] for d in data if d['category'] == 'Strong La Niña']
    solid_circle_y = [d['y'] for d in data if d['category'] == 'Strong La Niña']
    fig.add_trace(go.Scatter(
        x=solid_circle_x,
        y=solid_circle_y,
        mode='markers',
        marker=dict(symbol='circle', color='white', size=6, line=dict(color='white', width=1)),
        showlegend=False
    ))

    # Scatter trace for hollow circles on other bars
    hollow_categories = ['Neutral', 'Weak La Niña', 'Moderate La Niña']
    hollow_circle_x = [d['x'] for d in data if d['category'] in hollow_categories]
    hollow_circle_y = [d['y'] for d in data if d['category'] in hollow_categories]
    fig.add_trace(go.Scatter(
        x=hollow_circle_x,
        y=hollow_circle_y,
        mode='markers',
        marker=dict(symbol='circle', color='white', size=6, line=dict(color=colors['bar_outline'], width=1)),
        showlegend=False
    ))
    
    # --- Custom Legend ---
    legend_shapes = []
    legend_annotations = []

    legend_swatch_colors = [
        colors['category_colors']['Very Strong El Niño'],
        colors['category_colors']['Strong El Niño'],
        colors['category_colors']['Moderate El Niño'],
        colors['category_colors']['Weak El Niño'],
        colors['category_colors']['Neutral'],
        colors['category_colors']['Weak La Niña'],
        colors['category_colors']['Moderate La Niña'],
        colors['category_colors']['Strong La Niña'],
    ]
    
    leg_x0, leg_y1 = 0.05, 0.92
    leg_w, leg_h = 0.04, 0.03
    
    for i, color in enumerate(legend_swatch_colors):
        y0 = leg_y1 - (i + 1) * leg_h
        y1 = leg_y1 - i * leg_h
        legend_shapes.append(
            dict(type="rect", xref="paper", yref="paper", x0=leg_x0, y0=y0, x1=leg_x0 + leg_w, y1=y1,
                 fillcolor=color, line=dict(color=colors['bar_outline'], width=1))
        )

    # Add circles to legend swatches
    circle_indices = [4, 5, 6, 7] # Neutral, Weak La Niña, Mod La Niña, Strong La Niña
    for i in circle_indices:
        y_center = leg_y1 - i * leg_h - leg_h / 2
        x_center = leg_x0 + leg_w / 2
        is_strong_la_nina = (i == 7)
        legend_shapes.append(
            dict(type="circle", xref="paper", yref="paper", x0=x_center-0.007, y0=y_center-0.012, x1=x_center+0.007, y1=y_center+0.012,
                 fillcolor='white', line=dict(color=colors['bar_outline'] if not is_strong_la_nina else 'white', width=1))
        )

    # Add legend text annotations
    leg_text_x = leg_x0 + leg_w + 0.02
    legend_annotations.extend([
        dict(xref="paper", yref="paper", x=leg_text_x, y=leg_y1 - 0.5 * leg_h,
             text=f"<span style='font-size: 20px;'>▲</span> {texts['legend_labels']['el_nino']}",
             align="left", showarrow=False, font=dict(family="Arial", size=16, color=colors['text_color'])),
        dict(xref="paper", yref="paper", x=leg_text_x, y=leg_y1 - 4.5 * leg_h,
             text=f"<span style='font-size: 20px;'>►</span> {texts['legend_labels']['neutral']}",
             align="left", showarrow=False, font=dict(family="Arial", size=16, color=colors['text_color'])),
        dict(xref="paper", yref="paper", x=leg_text_x, y=leg_y1 - 7.5 * leg_h,
             text=f"<span style='font-size: 20px;'>▼</span> {texts['legend_labels']['la_nina']}",
             align="left", showarrow=False, font=dict(family="Arial", size=16, color=colors['text_color']))
    ])

    # Add source annotation
    legend_annotations.append(
        dict(xref="paper", yref="paper", x=0.5, y=-0.15,
             text=texts['source'], showarrow=False,
             font=dict(family="Arial", size=10, color=colors['text_color']))
    )

    fig.update_layout(
        title=dict(
            text=f"<b>{texts['title']}</b>",
            y=0.97, x=0.05, xanchor='left', yanchor='top',
            font=dict(family="Arial", size=28, color=colors['text_color'])
        ),
        xaxis=dict(
            tickvals=[1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020],
            tickfont=dict(family="Arial", size=18, color=colors['text_color']),
            showgrid=False,
            zeroline=True,
            zerolinecolor=colors['text_color'],
            zerolinewidth=1
        ),
        yaxis=dict(
            range=[-0.45, 1.1],
            tickvals=[0, 0.25, 0.50, 0.75, 1.0],
            ticktext=['0 °C', '0.25', '0.50', '0.75', '1 °C'],
            tickfont=dict(family="Arial", size=18, color=colors['text_color']),
            gridcolor=colors['grid_lines'],
            zeroline=True,
            zerolinecolor=colors['text_color'],
            zerolinewidth=2
        ),
        plot_bgcolor=colors['plot_background'],
        paper_bgcolor=colors['plot_background'],
        showlegend=False,
        margin=dict(l=80, r=40, t=100, b=100),
        shapes=legend_shapes,
        annotations=legend_annotations,
        bargap=0.2
    )

    fig.write_image(output_filename, scale=2, width=1000, height=700)
    print(f"Chart saved to {output_filename}")

if __name__ == "__main__":
    main()