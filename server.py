import argparse
from mcp.server.fastmcp import FastMCP
from scraper import fetch_sello_lunch_menus

# Initialize FastMCP server
mcp = FastMCP("LounasMCP")

@mcp.tool()
def get_sello_lunch_menus() -> str:
    """
    Retrieve today's lunch menus for all restaurants in and around Kauppakeskus Sello, Espoo.
    
    Returns:
        A list of restaurants, their lunch hours, distance from Sello, address, and the daily menu items
        as a formatted string.
    """
    try:
        data = fetch_sello_lunch_menus()
        if not data:
            return "No lunch menus found for Sello today."
        
        # Format the output for easy reading by the LLM
        output = []
        for r in data:
            output.append(f"### {r['restaurant']}")
            meta = []
            if r['lunch_hours']:
                meta.append(f"Hours: {r['lunch_hours']}")
            if r['distance']:
                meta.append(f"Distance: {r['distance']}")
            if r['address']:
                meta.append(f"Address: {r['address']}")
            
            if meta:
                output.append(f"({', '.join(meta)})")
            
            for item in r['menu']:
                price_str = f" [{item['price']}]" if item.get('price') else ""
                dish_line = f"- **{item['name']}**{price_str}"
                output.append(dish_line)
                if item.get('info'):
                    output.append(f"  *Description: {item['info']}*")
                if item.get('link'):
                    output.append(f"  *Link: {item['link']}*")
            output.append("") # empty line between restaurants
            
        return "\n".join(output)
    except Exception as e:
        return f"Error fetching lunch menus: {str(e)}"

def main():
    parser = argparse.ArgumentParser(description="LounasMCP server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse"],
        default="stdio",
        help="Transport protocol (stdio or sse)"
    )
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host to bind for SSE transport"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to bind for SSE transport"
    )
    args = parser.parse_args()

    if args.transport == "sse":
        print(f"Starting LounasMCP SSE server on {args.host}:{args.port}")
        mcp.settings.host = args.host
        mcp.settings.port = args.port
        mcp.run(transport="sse")
    else:
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
