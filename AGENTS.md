# LounasMCP Agent Instructions

This document is written for AI Agents (like Claude, Cursor, Antigravity, or other LLMs) that are consuming the `LounasMCP` server.

## Server Metadata
- **Name**: `LounasMCP`
- **Domain**: Scraping and retrieving lunch menus for a configured location in Finland.
- **Configuration**: The target website is configurable via the `LOUNAS_SOURCE_URL` environment variable. Agents should read the returned addresses to confirm the current active city/location.

## Cache Strategy
- The server uses a daily file-based cache (`.lounas_cache.json`). The responses are resolved locally in `<5ms` once cached for that calendar day, avoiding redundant scraping network overhead.

## Exposed Tools

### `get_sello_lunch_menus`

#### Description
Retrieves today's lunch menus for all restaurants located in and around the configured location.

#### Parameters
*None* (Retrieves today's menus for the active location by default).

#### Expected Return Format
The tool returns a formatted Markdown string. Example structure:

```markdown
### La Torrefazione Sello
(Hours: 10:30-14, Distance: 60m, Address: Leppävaarankatu 3, 02600 Espoo)
- **Chorizopasta** [14,00e]
  *Description: Chorizoa, mausteista tomaattikastiketta, parmesaania ja basilikaa*
- **Porkkanarisotto ja briejuustoa** [14,90e]
  *Description: Porkkanapyreetä, briejuustoa, rucolaa ja pistaasia*

### Food & Co Quartetto Plus
(Hours: 10:45-13:15, Distance: 630m, Address: Linnoitustie 9-11 E, 02600 Espoo)
- **Katso päivän lounaslista ravintolan sivuilta!**
  *Link: https://www.compass-group.fi/ravintolat-ja-ruokalistat/foodco/kaupungit/espoo/quartetto-plus/*
```

## Parsing Guidelines
1. **Distance Filters**: You can sort restaurants based on the `Distance` field (e.g., `60m`, `860m`, `1.2km`).
2. **Lunch Hours**: Check the `Hours` metadata to verify if the restaurant is currently serving lunch or closed.
3. **Missing Menus**: If a menu says "Katso päivän lounaslista...", it means the menu is hosted externally. Provide the customer with the link retrieved from the `Link:` field.
4. **Diets & Allergens**: Common Finnish abbreviations like `L` (Lactose-free / Laktoositon), `G` (Gluten-free / Gluteeniton), `M` (Milk-free / Maidoton), or `Veg` (Vegan) are often embedded in the dish descriptions. Interpret these to answer allergy questions.
