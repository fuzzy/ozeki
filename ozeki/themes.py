from itertools import cycle

from textual.theme import Theme

THEMES = cycle(
    [
        {
            "name": "light",
            "theme": Theme(
                name="kakejiku-light",
                primary="#1a1a1a",  # Sumi black (main text)
                secondary="#8b0000",  # Vermilion ink (accents, stamps)
                accent="#c19a6b",  # Muted gold (highlight or focal elements)
                foreground="#1a1a1a",  # Deep ink tone
                background="#f8f4e3",  # Washi paper base
                success="#6b8e23",  # Olive green (natural, understated)
                warning="#b5651d",  # Earthy orange (subtle contrast)
                error="#990000",  # Dark red (without overwhelming)
                surface="#ede6d0",  # Scroll body (slightly off-washi)
                panel="#dcd2b2",  # Borders or side panels (gold-tan trim)
                dark=False,
                variables={
                    "block-cursor-text-style": "none",
                    "footer-key-foreground": "#8b0000",  # Red accent
                    "input-selection-background": "#c19a6b 35%",
                    "highlight-foreground": "#c19a6b",
                    "highlight-background": "#f0e8cc",
                },
            ),
        },
        {
            "name": "dark",
            "theme": Theme(
                name="kakejiku-dark",
                primary="#e0c07d",  # Gold script ink (primary accent)
                secondary="#a93f2e",  # Deep vermilion (seals, alerts)
                accent="#82664a",  # Aged bronze (secondary highlight)
                foreground="#e8e6dc",  # Pale ink on dark scroll
                background="#1a1a1a",  # Lacquer-black base
                success="#6f9f6a",  # Subtle green (nature balance)
                warning="#d19a66",  # Burnt orange
                error="#a93434",  # Dried crimson ink
                surface="#2a2a2a",  # Scroll body
                panel="#33302a",  # Faintly warm dark background
                dark=True,
                variables={
                    "block-cursor-text-style": "bold",
                    "footer-key-foreground": "#e0c07d",
                    "input-selection-background": "#a93f2e 30%",
                    "highlight-foreground": "#e0c07d",
                    "highlight-background": "#2f2c26",
                },
            ),
        },
        {
            "name": "sakura-new",
            "theme": Theme(
                name="sakura",
                primary="#3a1c2b",  # Darker plum (near-black for max contrast)
                secondary="#d44d7a",  # Vibrant sakura pink (better pop)
                accent="#c97b95",  # Muted but clearer pink
                foreground="#3a1c2b",  # Matches primary (critical for text)
                background="#fff4f9",  # Kept pale for softness
                success="#5a8a4e",  # Deeper green (leaves)
                warning="#d67c45",  # Brighter peach (sunset)
                error="#b53d3d",  # Stronger red (wilted bloom)
                surface="#f8e8ee",  # Unchanged
                panel="#e8d5df",  # Unchanged
                dark=False,
                variables={
                    "block-cursor-text-style": "none",
                    "footer-key-foreground": "#d44d7a",  # Now more vibrant
                    "input-selection-background": "#c97b95 50%",  # Higher opacity
                    "highlight-foreground": "#3a1c2b",  # Dark plum
                    "highlight-background": "#f0d6e3",  # Unchanged
                },
            ),
        },
        {
            "name": "oni",
            "theme": Theme(
                name="oni",
                primary="#e8f3f8",  # Pale ice/ghostly light (text)
                secondary="#2e8b57",  # Oni green (accent)
                accent="#4169e1",  # Royal blue (oni costume highlights)
                foreground="#e8f3f8",  # Bright text for contrast
                background="#0f1a1f",  # Dark navy (night sky)
                success="#48d597",  # Vibrant jade (success)
                warning="#ff9e3b",  # Fiery orange (warning)
                error="#e63b3b",  # Blood red (error)
                surface="#1a2a33",  # Deeper navy (surface)
                panel="#223b4d",  # Metallic blue (panels)
                dark=True,  # Dark theme base
                variables={
                    "block-cursor-text-style": "bold",  # Stands out
                    "footer-key-foreground": "#48d597",  # Jade green
                    "input-selection-background": "#4169e1 40%",  # Blue highlight
                    "highlight-foreground": "#0f1a1f",  # Dark bg for contrast
                    "highlight-background": "#2e8b57",  # Oni green
                },
            ),
        },
    ]
)
