import sys
import json
import plotly.graph_objects as go
import os

def main():
    """
    Main function to generate a chart from a JSON file.
    """
    if len(sys.argv) != 2:
        print(f"Usage: python {os.path.basename(sys.argv[0])} <json_file_path>")
        sys.exit(1)

    json_file_path = sys.argv[1]
    
    # Derive output filename from the input JSON filename
    base_name = os.path.splitext(os.path.basename(json_file_path))[0]
    output_image_path = f"{base_name}.png"

    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at '{json_file_path}'")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{json_file_path}'")
        sys.exit(1)

    chart_data = config['chart_data']
    texts = config['texts']
    colors = config['colors']

    # Prepare data for plotting
    categories = [item['category'] for item in chart_data]
    values = [item['value'] for item in chart_data]

    # Create the figure
    fig = go.Figure()

    # Add the horizontal bar trace
    fig.add_trace(go.Bar(
        y=categories,
        x=values,
        orientation='h',
        marker=dict(color=colors[0]),
        text=values,
        textposition='outside',
        texttemplate='<b>%{text}</b>',
        hoverinfo='none',
        cliponaxis=False
    ))

    # Update trace text font properties
    fig.update_traces(
        textfont=dict(
            family="Arial",
            size=18,
            color=colors[0]
        )
    )

    # Configure layout
    title_text = f"<b>{texts['title']}</b>" if texts.get('title') else None

    fig.update_layout(
        title=dict(
            text=title_text,
            font=dict(size=28, family="Arial", color='black'),
            x=0.05,
            y=0.92,
            xanchor='left',
            yanchor='top'
        ),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            showticklabels=False,
            fixedrange=True,
            range=[0, max(values) * 1.15]
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            showticklabels=True,
            tickfont=dict(size=20, family="Arial", color='black'),
            fixedrange=True
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=350, r=40, t=150, b=50),
        showlegend=False,
        font=dict(family="Arial")
    )

    # Save the figure to a PNG file
    fig.write_image(output_image_path, scale=2)
    print(f"Chart saved to {output_image_path}")

if __name__ == '__main__':
    main()