import React, { useState} from 'react';
import './characterCalculator.css';
import { useNavigate } from 'react-router-dom';
import Button from '@mui/material/Button';
import Container from '@mui/material/Container';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import { TextField } from '@mui/material';
import { red } from '@mui/material/colors';
const CharacterCalculator = () => {
  const [characterHeight, setCharacterHeight] = useState('');
  const [digitHeight, setDigitHeight] = useState('');
  const [characterWidth, setCharacterWidth] = useState('');
  const [digitWidth, setDigitWidth] = useState('');
  const [characterWidthForSmallLeter, setCharacterWidthForSmallLeter] = useState('');
  const [spaceBetweenLines, setSpaceBetweenLines] = useState(0);
  const [characterThickness, setCharacterThickness] = useState('');
  const [digitThickness, setdigitThickness] = useState('');
  const [screenHeight, setScreenHeight] = useState('');
  const [screenWidth, setScreenWidth] = useState('');

//   const minScreenHeight=34*

  const handleCharacterChange = (event) => {
    setCharacterHeight(event.target.value);
    setCharacterWidth(event.target.value*0.6);
    setCharacterWidthForSmallLeter(event.target.value*0.2);
    setCharacterThickness(event.target.value*0.2);
    // let characterWidtht=characterWidth*24
    setScreenWidth((event.target.value*0.6*24+3*23))
  };
  const handleDigitChange = (event) => {
    setDigitHeight(event.target.value);
    setDigitWidth(event.target.value*0.6);
    // setCharacterWidthForSmallLeter(event.target.value*0.2);
    setdigitThickness(event.target.value*0.2);
    setSpaceBetweenLines(event.target.value*0.6);
    let newSpaceBetweenLines=event.target.value*0.6
    setScreenHeight(event.target.value*4+newSpaceBetweenLines*3)
  };
  return (
  <Container maxWidth="sm"style={{ backgroundColor: '#1a237e  ', color:'#ffeb3b'}} className="customContainer">
    <Box 
        display="flex" 
        flexDirection="column" 
        alignItems="center" 
        justifyContent="center" 
        minHeight="100vh"
        textAlign="center"
    >
        <Typography variant="h4" gutterBottom >
        Welcome To Character Calculator
        </Typography>
        <TextField
          label="character height"
          variant="outlined"
          value={characterHeight}
          onChange={handleCharacterChange}
          style={{ marginBottom: '10px' }}

          inputProps={{
            style: { marginBottom: '10px', color: '#ffeb3b',borderColor: '#ffeb3b' }
          }} 
          InputLabelProps={{
            style: { color: '#ffeb3b' }
          }}
        />
        <TextField
          label="digit height"
          variant="outlined"
          value={digitHeight}
          onChange={handleDigitChange}
          style={{ marginBottom: '10px' }}
          inputProps={{
            style: { marginBottom: '10px', color: '#ffeb3b' }
          }} 
          InputLabelProps={{
            style: { color: '#ffeb3b' }
          }}
        />
         <TextField
          label="character width"
          variant="outlined"
          value={characterWidth}
          style={{ marginBottom: '10px' }}
          inputProps={{
            style: { marginBottom: '10px', color: '#ffeb3b' }
          }} 
          InputLabelProps={{
            style: { color: '#ffeb3b' }
          }}
        />
          <TextField
          label="digit width"
          variant="outlined"
          value={  digitWidth}
          style={{ marginBottom: '10px' }}
          inputProps={{
            style: { marginBottom: '10px', color: '#ffeb3b' }
          }} 
          InputLabelProps={{
            style: { color: '#ffeb3b' }
          }}
        />
         <TextField
          label="Character width for small leter"
          variant="outlined"
          value={characterWidthForSmallLeter}
          style={{ marginBottom: '10px' }}
          inputProps={{
            style: { marginBottom: '10px', color: '#ffeb3b' }
          }} 
          InputLabelProps={{
            style: { color: '#ffeb3b' }
          }}
        />
         <TextField
          label="Character thickness"
          variant="outlined"
          value={characterThickness}
          style={{ marginBottom: '10px' }}
          inputProps={{
            style: { marginBottom: '10px', color: '#ffeb3b' }
          }} 
          InputLabelProps={{
            style: { color: '#ffeb3b' }
          }}
        />
           <TextField
          label="digit thickness"
          variant="outlined"
          value={digitThickness}
          style={{ marginBottom: '10px' }}
          inputProps={{
            style: { marginBottom: '10px', color: '#ffeb3b' }
          }} 
          InputLabelProps={{
            style: { color: '#ffeb3b' }
          }}
        />
        <TextField
          label="spaces between lines"
          variant="outlined"
          value={spaceBetweenLines}
          style={{ marginBottom: '10px' }}
          inputProps={{
            style: { marginBottom: '10px', color: '#ffeb3b' }
          }} 
          InputLabelProps={{
            style: { color: '#ffeb3b' }
          }}
        />
          <TextField
            label="screen height"
            variant="outlined"
            value={screenHeight}
            style={{ marginBottom: '10px' }}
            inputProps={{
              style: { marginBottom: '10px', color: '#ffeb3b' }
            }}  
            InputLabelProps={{
              style: { color: '#ffeb3b' }
            }}  
          />
          <TextField
            label="screen width"
            variant="outlined"
            value={screenWidth}
            style={{ marginBottom: '10px' }}
            inputProps={{
              style: { marginBottom: '10px', color: '#ffeb3b' }
            }}  
            InputLabelProps={{
              style: { color: '#ffeb3b' }
            }}  
          />
    </Box>
</Container>)
};

export default CharacterCalculator;
