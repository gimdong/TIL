import json

wavedrom_data = {
    "signal": [
        {"name": "clk", "wave": "p.....|..."},
        {"name": "CMD", "wave": "x.34x|=.x", "data": ["CMD(00)", "ADDR", "DATA", "CMD(FF)"]},
        {"name": "WE#", "wave": "01.0.|.1."},
        {"name": "RE#", "wave": "0...|.10"},
        {"name": "DQ[7:0]", "wave": "x3.x|=x.", "data": ["0x00", "0xFF", "Z"]}
    ]
}

html_template = f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>WaveDrom Timing Diagram</title>
  <script src="https://wavedrom.com/wavedrom.min.js"></script>
  <script src="https://wavedrom.com/skins/default.js"></script>
</head>
<body>
  <h2>Timing Diagram Example</h2>
  <script type="WaveDrom">
{json.dumps(wavedrom_data, indent=2)}
  </script>
  <script>
    WaveDrom.ProcessAll();
  </script>
</body>
</html>
"""

with open("wavedrom_diagram.html", "w") as f:
    f.write(html_template)

print("✅ wavedrom_diagram.html 파일이 생성되었습니다. 브라우저에서 열어보세요!")