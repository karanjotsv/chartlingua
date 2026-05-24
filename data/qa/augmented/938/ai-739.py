import sys
import json
import plotly.graph_objects as go

def create_chart(json_filepath):
    """
    Generates a chart from a JSON data file and saves it as a PNG image.
    """
    try:
        with open(json_filepath, 'r', encoding='utf-8') as f:
            chart_info = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at '{json_filepath}'")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from the file '{json_filepath}'")
        sys.exit(1)

    chart_data = chart_info.get('chart_data', [])
    texts = chart_info.get('texts', {})
    colors = chart_info.get('colors', [])

    if not chart_data:
        print("Error: 'chart_data' is missing or empty in the JSON file.")
        sys.exit(1)

    # Extract data for plotting, no reversal needed due to autorange='reversed'
    y_categories = [d['category'] for d in chart_data]
    x_values = [d['value'] for d in chart_data]

    # Create the figure
    fig = go.Figure()

    # Add the bar trace
    fig.add_trace(go.Bar(
        y=y_categories,
        x=x_values,
        orientation='h',
        marker=dict(color=colors[0] if colors else '#2772c3'),
        text=x_values,
        textposition='outside',
        textfont=dict(family="Arial", size=12, color='black'),
        cliponaxis=False,
        hoverinfo='none'
    ))

    # Update layout
    annotations = []
    if texts.get('source_text'):
        annotations.append(
            dict(
                xref='paper', yref='paper',
                x=1.0, y=-0.12,
                xanchor='right', yanchor='top',
                text=texts['source_text'],
                showarrow=False,
                font=dict(family="Arial", size=12, color='#666666')
            )
        )

    fig.update_layout(
        font=dict(family="Arial", size=12, color='black'),
        plot_bgcolor='white',
        showlegend=False,
        xaxis=dict(
            title=texts.get('x_axis_title', ''),
            showgrid=True,
            gridcolor='#e0e0e0',
            griddash='dot',
            zeroline=False,
            range=[0, 950]  # Set range to provide space for text labels
        ),
        yaxis=dict(
            title=texts.get('y_axis_title', ''),
            autorange='reversed',  # This ensures the first item in the data is at the top
            showgrid=False,
            zeroline=False
        ),
        margin=dict(l=120, r=60, t=40, b=80),
        annotations=annotations
    )

    # Determine output filename and save the image
    base_filename = json_filepath.rsplit('.', 1)[0]
    output_filename = f"{base_filename}.png"
    
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_json_file>")
        sys.exit(1)
    
    json_path = sys.argv[1]
    create_chart(json_path)