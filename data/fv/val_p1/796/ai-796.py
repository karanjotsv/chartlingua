import sys
import json
from pathlib import Path
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def main():
    """
    Main function to generate the chart from a JSON file.
    """
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <path_to_json_file>")
        sys.exit(1)

    json_path = Path(sys.argv[1])
    if not json_path.is_file():
        print(f"Error: JSON file not found at '{json_path}'")
        sys.exit(1)

    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data_full = json.load(f)

    chart_data = chart_data_full['chart_data']
    chart_texts = chart_data_full['texts']
    colors = chart_data_full['colors']

    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.15)

    # Add traces to subplots
    for i, data_series in enumerate(chart_data):
        fig.add_trace(
            go.Scatter(
                x=data_series['x_values'],
                y=data_series['y_values'],
                name=data_series['name'],
                mode='lines',
                line=dict(color=colors[i], width=2)
            ),
            row=i + 1,
            col=1
        )

    # Update layout and styling
    fig.update_layout(
        font_family="Arial",
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.25,
            xanchor="left",
            x=0
        ),
        margin=dict(l=60, r=40, t=100, b=100),
        height=600
    )
    
    # Add subplot titles using annotations for precise placement
    fig.add_annotation(
        text=f"<b>{chart_texts['title_top']}</b>",
        xref="paper", yref="paper",
        x=0.5, y=1.0,
        showarrow=False,
        font=dict(size=14, family="Arial"),
        xanchor='center',
        yanchor='bottom'
    )
    fig.add_annotation(
        text=f"<b>{chart_texts['title_bottom']}</b>",
        xref="paper", yref="paper",
        x=0.5, y=0.4,
        showarrow=False,
        font=dict(size=14, family="Arial"),
        xanchor='center',
        yanchor='bottom'
    )

    # Update Y-axes
    fig.update_yaxes(
        range=chart_data[0]['y_axis_range'],
        gridcolor='#EAEAF2',
        zeroline=False,
        row=1, col=1
    )
    fig.update_yaxes(
        range=chart_data[1]['y_axis_range'],
        gridcolor='#EAEAF2',
        zeroline=False,
        row=2, col=1
    )

    # Update X-axes
    fig.update_xaxes(
        gridcolor='#EAEAF2',
        zeroline=False,
        tickvals=['06:00', '08:00', '10:00', '12:00', '14:00'],
        showticklabels=True,
        row=2, col=1
    )
    
    # Hide the x-axis line on the top plot but keep the grid
    fig.update_xaxes(showline=False, row=1, col=1)
    
    # Show axis lines
    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
    
    # Output the image
    output_filename = json_path.stem + ".png"
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved as {output_filename}")

if __name__ == "__main__":
    # The prompt asks for a script, not a function, but wrapping in main() is good practice
    # for clarity and to prevent global variable scope issues.
    # The execution starts here when run as a script.
    main()