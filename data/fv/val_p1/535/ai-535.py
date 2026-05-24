import sys
import json
import plotly.graph_objects as go

def main():
    """
    Generates a chart from a JSON data file provided as a command-line argument.
    """
    if len(sys.argv) != 2:
        print("Usage: python generate_chart.py <path_to_json_file>")
        sys.exit(1)

    json_path = sys.argv[1]

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except FileNotFoundError:
        print(f"Error: The file '{json_path}' was not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: The file '{json_path}' is not a valid JSON file.")
        sys.exit(1)

    chart_data = config.get('chart_data', [])
    texts = config.get('texts', {})
    colors = config.get('colors', {})

    fig = go.Figure()

    # Add traces from chart_data
    for i, series in enumerate(chart_data):
        trace_color = colors.get('series_colors', [])[i % len(colors.get('series_colors', ['#000']))]
        # Format text labels to use a comma as the decimal separator, like the original
        text_labels = [str(y).replace('.', ',') for y in series.get('y', [])]

        fig.add_trace(go.Scatter(
            x=series.get('x'),
            y=series.get('y'),
            mode='lines+markers+text',
            name=series.get('name', ''),
            line=dict(color=trace_color, width=2),
            marker=dict(color=trace_color, size=6),
            text=text_labels,
            textposition='top center',
            textfont=dict(
                family="Arial",
                size=14,
                color=colors.get('text_color', '#000000')
            ),
            hoverinfo='none'
        ))

    # Combine title and subtitle using HTML
    title_text = f"<b>{texts.get('title', '')}</b><br><span style='font-size: 16px;'>{texts.get('subtitle', '')}</span>"

    # Update layout
    fig.update_layout(
        title=dict(
            text=title_text,
            y=0.95,
            x=0.5,
            xanchor='center',
            yanchor='top'
        ),
        xaxis=dict(
            title_text=texts.get('x_axis_title'),
            showline=False,
            showgrid=False,
            zeroline=False,
            tickfont=dict(family="Arial", size=14, color=colors.get('text_color'))
        ),
        yaxis=dict(
            title_text=texts.get('y_axis_title'),
            visible=False, # Hide y-axis line, ticks, and labels as in the original
            range=[0, max(chart_data[0]['y']) * 1.2] # Ensure space for top text label
        ),
        plot_bgcolor=colors.get('plot_bg_color', '#FFFFFF'),
        paper_bgcolor=colors.get('paper_bg_color', '#FFFFFF'),
        font=dict(
            family="Arial",
            size=12,
            color=colors.get('text_color', '#000000')
        ),
        showlegend=False,
        margin=dict(l=40, r=40, t=100, b=80),
        annotations=[
            dict(
                text=texts.get('source', ''),
                showarrow=False,
                xref="paper",
                yref="paper",
                x=1.0,
                y=-0.2, # Position below the x-axis
                xanchor='right',
                yanchor='top',
                font=dict(family="Arial", size=12, color=colors.get('text_color'))
            )
        ]
    )
    
    # Determine output filename from JSON path
    if '.' in json_path:
        base_name = json_path.rsplit('.', 1)[0]
    else:
        base_name = json_path
    output_filename = f"{base_name}.png"
    
    # Save the figure as a PNG image
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == '__main__':
    main()