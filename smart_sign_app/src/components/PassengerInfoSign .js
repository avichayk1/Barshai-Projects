import React, { useState } from 'react';
import AccessTimeIcon from '@mui/icons-material/AccessTime';
import ArrowForwardIcon from '@mui/icons-material/ArrowForward';
import DirectionsBusIcon from '@mui/icons-material/DirectionsBus';

const PassengerInfoSign = () => {
  const [screenWidth, setScreenWidth] = useState(556); // mm
  const [screenHeight, setScreenHeight] = useState(206); // mm
  const [fontSize, setFontSize] = useState(25); // mm
  const [letterSpacing, setLetterSpacing] = useState(0.5); // mm
  const [fontThickness, setFontThickness] = useState("normal"); // normal, bold, or thin
  const [digitFontSize, setDigitFontSize] = useState(34); // mm
  const [lineSpacing, setLineSpacing] = useState(15); // mm for space between lines

  const [lines] = useState([
    { line: "42", destination: "לתחנה מרכזית", schedule: "11" },
    { line: "188", destination: "רררררררררררררר", schedule: "10,15" },
    { line: "95", destination: "בן גוריון", schedule: "1" },
    { line: "95", destination: "בן גוריון", schedule: "1" },
    // { line: "", destination: "רררררררררררררררררררררררררררררררררר", schedule: "" },
  ]);

  return (
    <div>
      {/* UI for adjusting the sizes with text inputs */}
      <div style={{ marginBottom: '20px' }}>
        <div>
          <label>Screen Width (mm): </label>
          <input
            type="text"
            value={screenWidth}
            onChange={(e) => setScreenWidth(Number(e.target.value))}
          />
          <span> mm</span>
        </div>
        <div>
          <label>Screen Height (mm): </label>
          <input
            type="text"
            value={screenHeight}
            onChange={(e) => setScreenHeight(Number(e.target.value))}
          />
          <span> mm</span>
        </div>
        <div>
          <label>Font Size (mm): </label>
          <input
            type="text"
            value={fontSize}
            onChange={(e) => setFontSize(Number(e.target.value))}
          />
          <span> mm</span>
        </div>
        <div>
          <label>Letter Spacing (mm): </label>
          <input
            type="text"
            value={letterSpacing}
            onChange={(e) => setLetterSpacing(Number(e.target.value))}
          />
          <span> mm</span>
        </div>
        <div>
          <label>Font Thickness: </label>
          <select
            value={fontThickness}
            onChange={(e) => setFontThickness(e.target.value)}
          >
            <option value="normal">Normal</option>
            <option value="bold">Bold</option>
            <option value="thin">Thin</option>
          </select>
        </div>
        <div>
          <label>Digit Font Size (mm): </label>
          <input
            type="text"
            value={digitFontSize}
            onChange={(e) => setDigitFontSize(Number(e.target.value))}
          />
          <span> mm</span>
        </div>
        <div>
          <label>Line Spacing (mm): </label>
          <input
            type="text"
            value={lineSpacing}
            onChange={(e) => setLineSpacing(Number(e.target.value))}
          />
          <span> mm</span>
        </div>
      </div>

      {/* Icons Container */}
      <div
        style={{
          width: `${screenWidth}mm`,
          backgroundColor: "#999",
          color: "#fff",
          display: "flex",
          justifyContent: "space-around",
          marginBottom: "1px",  // Space between the icons and the screen
        }}
      >
        <div style={{ textAlign: "center", fontWeight: "bold" }}>
          <AccessTimeIcon style={{ fontSize: '45mm' }} />
        </div>
        <div style={{ textAlign: "center", fontWeight: "bold" }}>
          <ArrowForwardIcon style={{ fontSize: '45mm' }} />
        </div>
        <div style={{ textAlign: "center", fontWeight: "bold" }}>
          <DirectionsBusIcon style={{ fontSize: '45mm' }} />
        </div>
      </div>

      {/* Screen Container */}
      <div
        style={{
          width: `${screenWidth}mm`,
          height: `${screenHeight}mm`,
          backgroundColor: "#fff",
          color: "#000",
          padding: "0px",
          fontFamily: "Arial, sans-serif",
          fontSize: `${fontSize}mm`,
        }}
      >
        {/* Content Rows using grid layout */}
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "auto auto auto", // Adjust columns based on content size
            gridRowGap: `${lineSpacing}mm`,  // Gap between rows
            gridColumnGap: "0mm",  // No gap between columns 
        }}
        >
          {/* Content for each row */}
          {lines.map((row, index) => (
            <React.Fragment key={index}>
              <div
                style={{
                  textAlign:"left",
                  overflow: "hidden",
                  whiteSpace: "nowrap",
                  fontFamily: 'Noto Sans', // Monospace font
                  fontSize: `${digitFontSize}mm`,
                  fontWeight: fontThickness,
                  margin: 0, // Remove any margin
                  padding: 0, // Remove any padding
                }}
              >
                {row.schedule} {/* Schedule comes first */}
              </div>
              <div
                style={{
                  overflow: "hidden",
                  whiteSpace: "nowrap",
                  fontFamily: 'Noto Sans', // Monospace font
                  fontSize: `${fontSize}mm`,
                  fontWeight: fontThickness,
                  margin: 0, // Remove any margin
                  padding: 0, // Remove any padding
                }}
              >
                {row.destination} {/* Destination is in the middle */}
              </div>
              <div
                style={{
                  textAlign:"right",
                  overflow: "hidden",
                  whiteSpace: "nowrap",
                  fontFamily: 'Noto Sans', // Monospace font
                  fontSize: `${digitFontSize}mm`,
                  fontWeight: fontThickness,
                  margin: 0, // Remove any margin
                  padding: 0, // Remove any padding
                }}
              >
                {row.line} {/* Line number comes last */}
              </div>
            </React.Fragment>
          ))}
        </div>
      </div>

      <style>
        {`
          @keyframes scrollText {
            0% { transform: translateX(100%); }
            100% { transform: translateX(-100%); }
          }
        `}
      </style>
    </div>
  );
};

export default PassengerInfoSign;
