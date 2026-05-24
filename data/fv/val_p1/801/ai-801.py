import sys
import json
import plotly.graph_objects as go

def main():
    # Check if a file path is provided
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_json_file>")
        sys.exit(1)

    json_path = sys.argv[1]

    # Read and parse the JSON file
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            chart_config = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at {json_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {json_path}")
        sys.exit(1)

    # Extract data from the JSON structure
    chart_data = chart_config.get('chart_data', [])
    texts = chart_config.get('texts', {})
    colors = chart_config.get('colors', [])

    # Prepare data for plotting in the correct visual order (top to bottom)
    # Plotly's y-axis for horizontal bars is categorical and plots from bottom up, so we reverse the data lists.
    categories = [d['category'] for d in chart_data]
    values = [d['value'] for d in chart_data]
    label_colors = [d['label_color'] for d in chart_data]

    # Create HTML-styled tick labels for colored text
    # The list is reversed to match the reversed data order for plotting
    y_tick_labels = [f'<span style="color: {c};">{l}</span>' for c, l in zip(label_colors, categories)][::-1]

    fig = go.Figure()

    # Add the horizontal bar trace
    fig.add_trace(go.Bar(
        x=values[::-1],
        y=categories[::-1],
        orientation='h',
        marker_color=colors[0] if colors else '#4e8ac9',
        text=[f'{v:,}' for v in values[::-1]],
        textposition='outside',
        textfont=dict(
            family="Arial",
            color=label_colors[::-1]
        ),
        cliponaxis=False # Prevent text from being clipped
    ))

    # Combine title and subtitle
    title_text = f"<b>{texts.get('title', '')}</b><br>{texts.get('subtitle', '')}"

    # Update layout
    fig.update_layout(
        title=dict(
            text=title_text,
            x=0.5,
            y=0.95,
            font=dict(family="Arial", size=18)
        ),
        xaxis=dict(
            title=texts.get('x_axis_title', 'Views'),
            showgrid=True,
            gridcolor='lightgrey',
            tickvals=[0, 500000, 1000000, 1500000, 2000000, 2500000, 3000000],
            ticktext=['0', '500 k', '1 M', '1.5 M', '2 M', '2.5 M', '3 M'],
            range=[0, max(values) * 1.18] # Add padding for outside text labels
        ),
        yaxis=dict(
            showticklabels=True,
            tickmode='array',
            tickvals=categories[::-1],
            ticktext=y_tick_labels,
            automargin=True
        ),
        font=dict(family="Arial", size=12),
        plot_bgcolor='#f0f0f0',
        paper_bgcolor='white',
        showlegend=False,
        margin=dict(l=10, r=60, t=100, b=50) # Use automargin on yaxis, but set others
    )

    # Determine output filename from input JSON path
    base_name = json_path.split('/')[-1].split('\\')[-1].rsplit('.', 1)[0]
    output_filename = f"{base_name}.png"
    
    # Write the image file
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == '__main__':
    main()