import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Rompecabezas del Ártico", page_icon="🧩", layout="wide"
)

st.title("🧩 Rompecabezas Visual: Ártico")
st.write(
    "Selecciona la dificultad, arrastra las piezas al tablero y encájalas en"
    " su lugar."
)

# Selector de nivel
nivel = st.selectbox(
    "Selecciona la dificultad:", ["Fácil (3x2)", "Intermedio (4x3)", "Difícil (6x4)"]
)

filas, columnas = 3, 2
if "Intermedio" in nivel:
    filas, columnas = 4, 3
elif "Difícil" in nivel:
    filas, columnas = 6, 4

# Componente web dinámico integrado en Streamlit
puzzle_html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            background-color: #f4f6f8;
            margin: 0;
            padding: 10px;
        }}
        #game-container {{
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
            justify-content: center;
        }}
        #board, #pieces {{
            border: 2px dashed #ccc;
            border-radius: 8px;
            background: #fff;
            position: relative;
        }}
        #board {{
            border-style: solid;
            border-color: #3b82f6;
            background-size: cover;
        }}
        .tile {{
            box-sizing: border-box;
            border: 1px solid rgba(255,255,255,0.6);
            position: absolute;
            cursor: grab;
            user-select: none;
            touch-action: none;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            border-radius: 4px;
        }}
        .tile:active {{
            cursor: grabbing;
            z-index: 1000 !important;
        }}
        .drop-zone {{
            position: absolute;
            border: 1px dashed #cbd5e1;
            box-sizing: border-box;
        }}
        #win-message {{
            display: none;
            margin-top: 15px;
            padding: 10px 20px;
            background: #22c55e;
            color: white;
            font-weight: bold;
            border-radius: 5px;
            font-size: 18px;
        }}
    </style>
</head>
<body>

<div id="win-message">🎉 ¡Felicidades! Has completado el rompecabezas.</div>

<div id="game-container">
    <div>
        <h4 style="text-align:center; margin:5px;">Tablero</h4>
        <div id="board"></div>
    </div>
    <div>
        <h4 style="text-align:center; margin:5px;">Piezas</h4>
        <div id="pieces"></div>
    </div>
</div>

<script>
    const rows = {filas};
    const cols = {columnas};
    const imgUrl = "https://images.unsplash.com/photo-1517783999520-f068d7431a60?auto=format&fit=crop&w=600&q=80"; // Imagen de paisaje helado/ártico

    const board = document.getElementById('board');
    const piecesContainer = document.getElementById('pieces');
    const winMsg = document.getElementById('win-message');

    const width = 450;
    const height = 300;
    const tileW = width / cols;
    const tileH = height / rows;

    board.style.width = width + 'px';
    board.style.height = height + 'px';
    piecesContainer.style.width = (tileW + 20) + 'px';
    piecesContainer.style.height = height + 'px';

    let placedCount = 0;
    const totalTiles = rows * cols;

    // Crear zonas de destino
    for (let r = 0; r < rows; r++) {{
        for (let c = 0; c < cols; c++) {{
            const zone = document.createElement('div');
            zone.className = 'drop-zone';
            zone.style.width = tileW + 'px';
            zone.style.height = tileH + 'px';
            zone.style.left = (c * tileW) + 'px';
            zone.style.top = (r * tileH) + 'px';
            board.appendChild(zone);
        }}
    }}

    // Generar piezas desordenadas
    let indices = Array.from({{length: totalTiles}}, (_, i) => i);
    indices.sort(() => Math.random() - 0.5);

    indices.forEach((index) => {{
        const r = Math.floor(index / cols);
        const c = index % cols;

        const tile = document.createElement('div');
        tile.className = 'tile';
        tile.style.width = tileW + 'px';
        tile.style.height = tileH + 'px';
        tile.style.backgroundImage = `url('${{imgUrl}}')`;
        tile.style.backgroundSize = `${{width}}px ${{height}}px`;
        tile.style.backgroundPosition = `-${{c * tileW}}px -${{r * tileH}}px`;

        // Posición inicial en la lista de piezas
        const randomTop = Math.random() * (height - tileH);
        tile.style.left = '10px';
        tile.style.top = randomTop + 'px';

        tile.dataset.correctLeft = c * tileW;
        tile.dataset.correctTop = r * tileH;
        tile.dataset.locked = "false";

        makeDraggable(tile);
        piecesContainer.appendChild(tile);
    }});

    function makeDraggable(el) {{
        let isDragging = false;
        let startX, startY, initialLeft, initialTop;

        el.addEventListener('mousedown', startDrag);
        el.addEventListener('touchstart', startDrag, {{passive: false}});

        function startDrag(e) {{
            if (el.dataset.locked === "true") return;
            isDragging = true;

            // Mover al contenedor global para poder arrastrarlo sobre el tablero
            document.body.appendChild(el);

            const clientX = e.touches ? e.touches[0].clientX : e.clientX;
            const clientY = e.touches ? e.touches[0].clientY : e.clientY;

            startX = clientX;
            startY = clientY;

            const rect = el.getBoundingClientRect();
            initialLeft = rect.left;
            initialTop = rect.top;

            el.style.position = 'fixed';
            el.style.left = initialLeft + 'px';
            el.style.top = initialTop + 'px';
            el.style.zIndex = 1000;

            document.addEventListener('mousemove', moveDrag);
            document.addEventListener('touchmove', moveDrag, {{passive: false}});
            document.addEventListener('mouseup', endDrag);
            document.addEventListener('touchend', endDrag);
        }}

        function moveDrag(e) {{
            if (!isDragging) return;
            if (e.cancelable) e.preventDefault();

            const clientX = e.touches ? e.touches[0].clientX : e.clientX;
            const clientY = e.touches ? e.touches[0].clientY : e.clientY;

            const dx = clientX - startX;
            const dy = clientY - startY;

            el.style.left = (initialLeft + dx) + 'px';
            el.style.top = (initialTop + dy) + 'px';
        }}

        function endDrag() {{
            if (!isDragging) return;
            isDragging = false;

            document.removeEventListener('mousemove', moveDrag);
            document.removeEventListener('touchmove', moveDrag);

            const boardRect = board.getBoundingClientRect();
            const tileRect = el.getBoundingClientRect();

            const targetLeft = boardRect.left + parseFloat(el.dataset.correctLeft);
            const targetTop = boardRect.top + parseFloat(el.dataset.correctTop);

            // Umbral de ajuste (Snap)
            const tolerance = 40;
            if (Math.abs(tileRect.left - targetLeft) < tolerance && 
                Math.abs(tileRect.top - targetTop) < tolerance) {{

                // Encajar en la posición exacta
                el.style.position = 'absolute';
                el.style.left = el.dataset.correctLeft + 'px';
                el.style.top = el.dataset.correctTop + 'px';
                el.style.border = 'none';
                el.style.boxShadow = 'none';
                el.dataset.locked = "true";
                board.appendChild(el);

                placedCount++;
                if (placedCount === totalTiles) {{
                    winMsg.style.display = 'block';
                }}
            }} else {{
                // Regresar al panel lateral si no encaja
                piecesContainer.appendChild(el);
                el.style.position = 'absolute';
                el.style.left = '10px';
            }}
        }}
    }}
</script>
</body>
</html>
"""

components.html(puzzle_html, height=450)