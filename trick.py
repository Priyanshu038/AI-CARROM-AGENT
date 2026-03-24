
CX, CY = 230, 230 

TRICKS = [
    {
        "id": "break", 
        "name": "Center Break", 
        "icon": "💥", 
        "diff": 4,
        "tag": "Scatter the opening cluster",
        "desc": "The opening power shot. Strike dead center with maximum force to scatter all pieces across the board.",
        "tips": [
            "Striker must be centered at the baseline",
            "Use absolute maximum force",
            "Aim straight at center of the formation"
        ],
        "pieces": [
            {"t": "rd", "x": CX, "y": CY},
            {"t": "wh", "x": CX + 28, "y": CY},
            {"t": "bk", "x": CX - 28, "y": CY},
            {"t": "wh", "x": CX, "y": CY + 28},
            {"t": "bk", "x": CX, "y": CY - 28}
        ],
        "shot": {"sx": CX, "ang": 270, "force": 1.0},
        "steps": [
            {"t": 200, "msg": "Striker positioned at center baseline — full force!"},
            {"t": 2200, "msg": "Power break! Pieces scatter in all directions"},
            {"t": 5000, "msg": "Goal: pocket your color pieces in the chaos"}
        ]
    },
    {
        "id": "direct", 
        "name": "Direct Pocket", 
        "icon": "🎯", 
        "diff": 1,
        "tag": "The foundation of carrom",
        "desc": "Align striker, piece, and pocket in a perfect straight line. The simplest and most reliable shot in carrom.",
        "tips": [
            "Visualize the straight line through all three points",
            "Medium force — don't over-power",
            "Your eyes should line up along the aim line"
        ],
        "pieces": [{"t": "bk", "x": 393, "y": 158}],
        "shot": {"sx": 160, "ang": 309, "force": 0.68},
        "steps": [
            {"t": 200, "msg": "See the ghost line — striker, piece & pocket are ALIGNED"},
            {"t": 2000, "msg": "Striker travels straight, hits piece dead center"},
            {"t": 4000, "msg": "Piece continues on the same line into the pocket!"}
        ]
    },
    {
        "id": "cut", 
        "name": "Cut Shot", 
        "icon": "✂️", 
        "diff": 2,
        "tag": "Deflect pieces sideways",
        "desc": "Hit the piece off-center (at the edge) — it deflects to the side based on contact geometry.",
        "tips": [
            "Aim at the EDGE of the piece, not the center",
            "Deflection angle equals the approach angle offset",
            "Use less force for more control of deflection"
        ],
        "pieces": [{"t": "wh", "x": 340, "y": 195}],
        "shot": {"sx": 270, "ang": 280, "force": 0.62},
        "steps": [
            {"t": 200, "msg": "Aim OFFSET from piece center — this is the cut"},
            {"t": 2200, "msg": "Striker clips the left edge of the piece"},
            {"t": 3500, "msg": "Piece deflects RIGHT — use this to reach hidden pockets!"}
        ]
    },
    {
        "id": "bank", 
        "name": "Bank Shot", 
        "icon": "🏦", 
        "diff": 3,
        "tag": "Bounce off the side wall",
        "desc": "Aim the striker at the side wall instead of the piece. It bounces and reaches a piece that would otherwise be blocked.",
        "tips": [
            "Angle of incidence = angle of reflection",
            "Calculate the bounce point on the wall first",
            "The piece appears unreachable — but the wall is your ally"
        ],
        "pieces": [{"t": "bk", "x": 148, "y": 240}],
        "shot": {"sx": CX, "ang": 326, "force": 0.70},
        "steps": [
            {"t": 200, "msg": "Piece is on the LEFT — aim at the RIGHT WALL"},
            {"t": 1800, "msg": "Striker bounces off the right wall at equal angle"},
            {"t": 4000, "msg": "Striker comes back left and strikes the piece!"}
        ]
    },
    {
        "id": "double", 
        "name": "Double Shot", 
        "icon": "🎱", 
        "diff": 2,
        "tag": "Chain two pieces at once",
        "desc": "Align two pieces on the same line as the pocket. Hit the first — it transfers momentum to the second, both can pocket.",
        "tips": [
            "All three points (piece1, piece2, pocket) must align",
            "First piece stops, second carries the momentum",
            "Works best when pieces are 1-2 piece-widths apart"
        ],
        "pieces": [{"t": "bk", "x": 361, "y": 248}, {"t": "bk", "x": 412, "y": 178}],
        "shot": {"sx": 240, "ang": 307, "force": 0.72},
        "steps": [
            {"t": 200, "msg": "Two pieces aligned with the pocket — DOUBLE opportunity!"},
            {"t": 2200, "msg": "Hit first piece — momentum transfers like billiards"},
            {"t": 4500, "msg": "Second piece gets the push and heads for the pocket!"}
        ]
    },
    {
        "id": "queen", 
        "name": "Queen Cover", 
        "icon": "♛", 
        "diff": 3,
        "tag": "Pocket the queen & cover",
        "desc": "Pocket the queen, then cover it with your own piece in the very next shot.",
        "tips": [
            "You MUST cover the queen in the very next shot",
            "Set up a cover piece behind the queen first",
            "Choose a pocket where you can easily follow with your piece"
        ],
        "pieces": [{"t": "rd", "x": CX, "y": 210}, {"t": "wh", "x": CX, "y": 258}],
        "shot": {"sx": CX, "ang": 270, "force": 0.52},
        "steps": [
            {"t": 200, "msg": "Queen ahead, your white piece right behind — perfect setup"},
            {"t": 2000, "msg": "Queen pockets first..."},
            {"t": 4000, "msg": "White follows to COVER! You keep the queen bonus ♛"}
        ]
    },
    {
        "id": "alley", 
        "name": "Alley Shot", 
        "icon": "🏹", 
        "diff": 4,
        "tag": "Thread the needle",
        "desc": "Thread the striker through a narrow gap between two blocking pieces to hit a target piece behind them.",
        "tips": [
            "Gap must be at least striker-width + small margin",
            "Extremely precise angle required — practice first",
            "Lower force gives more time to correct trajectory"
        ],
        "pieces": [{"t": "bk", "x": 237, "y": 212}, {"t": "bk", "x": 303, "y": 212}, {"t": "wh", "x": CX, "y": 158}],
        "shot": {"sx": CX, "ang": 270, "force": 0.52},
        "steps": [
            {"t": 200, "msg": "Two black pieces form a GATE — white target behind"},
            {"t": 2200, "msg": "Thread the striker exactly through the gap..."},
            {"t": 3500, "msg": "Striker passes through and strikes the white piece!"}
        ]
    },
    {
        "id": "ricochet", 
        "name": "Ricochet", 
        "icon": "⚡", 
        "diff": 4,
        "tag": "Piece bounces into pocket",
        "desc": "Hit a piece so it bounces off the wall and ricochets back into a pocket.",
        "tips": [
            "The piece must hit the wall at the right angle",
            "Calculate: piece-to-wall angle must equal wall-to-pocket angle",
            "Use medium force — too hard and it overshoots"
        ],
        "pieces": [{"t": "wh", "x": 180, "y": 180}],
        "shot": {"sx": 310, "ang": 287, "force": 0.65},
        "steps": [
            {"t": 200, "msg": "Aim to hit piece toward the LEFT wall"},
            {"t": 2200, "msg": "Piece bounces off the wall at equal angle"},
            {"t": 4000, "msg": "Ricochet! Piece redirects into a different pocket!"}
        ]
    }
]
