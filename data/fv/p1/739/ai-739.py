import sys
import json
import plotly.graph_objects as go

def main():
    """
    Generates a chart from a JSON data file provided as a command-line argument.
    """
    if len(sys.argv) != 2:
        print("Usage: python generate_chart.py <json_file_path>")
        sys.exit(1)

    json_path = sys.argv[1]

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at '{json_path}'")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{json_path}'")
        sys.exit(1)

    chart_data = config.get('chart_data', [])
    texts = config.get('texts', {})
    colors = config.get('colors', {})

    categories = [item['category'] for item in chart_data]
    values = [item['value'] for item in chart_data]
    # Format text labels to use a comma for the decimal separator, as in the original image.
    text_labels = [str(v).replace('.', ',') for v in values]

    fig = go.Figure()

    # Add the main line trace
    fig.add_trace(go.Scatter(
        x=categories,
        y=values,
        mode='lines+markers+text',
        line=dict(color=colors.get('main_series', '#5F6B7A')),
        marker=dict(color=colors.get('main_series', '#5F6B7A'), size=6),
        text=text_labels,
        textposition='top center',
        textfont=dict(
            family="Arial",
            size=12,
            color=colors.get('text', '#000000')
        ),
        hoverinfo='none'
    ))

    # Combine title and subtitle using HTML for styling
    title_text = f"<b>{texts.get('title', '')}</b><br>{texts.get('subtitle', '')}"

    fig.update_layout(
        title=dict(
            text=title_text,
            y=0.95,
            x=0.5,
            xanchor='center',
            yanchor='top',
            font=dict(
                family="Arial",
                size=18,
                color=colors.get('text', '#000000')
            )
        ),
        xaxis=dict(
            title_text=texts.get('x_axis_title'),
            tickvals=categories,
            showline=True,
            linewidth=1,
            linecolor='black',
            showgrid=False,
            zeroline=False
        ),
        yaxis=dict(
            visible=False  # The Y-axis is not visible in the original chart
        ),
        plot_bgcolor=colors.get('plot_bg', '#E9E9E9'),
        paper_bgcolor=colors.get('paper_bg', '#FFFFFF'),
        font=dict(
            family="Arial",
            size=12,
            color=colors.get('text', '#000000')
        ),
        showlegend=False,
        margin=dict(t=100, b=80, l=40, r=40),
        annotations=[
            dict(
                text=texts.get('source', ''),
                showarrow=False,
                xref="paper",
                yref="paper",
                x=0.95,
                y=-0.2,
                xanchor='right',
                yanchor='bottom',
                font=dict(
                    family="Arial",
                    size=10
                )
            )
        ]
    )

    # Derive output filename from the input JSON path
    base_name = json_path.rsplit('.', 1)[0]
    output_filename = f"{base_name}.png"

    # Save the figure as a high-resolution PNG image
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == "__main__":
    # Wrap in a main function for clarity, even though not strictly required
    # by the prompt, it is good practice.
    main()