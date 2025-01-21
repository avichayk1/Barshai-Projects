import React from 'react';
import { useNavigate } from 'react-router-dom';
import Button from '@mui/material/Button';
import Container from '@mui/material/Container';
import Box from '@mui/material/Box';
import { Link } from '@mui/material';
import Typography from '@mui/material/Typography';
const CastomerTrip = () => {
  const navigate = useNavigate();

  return (
    <Container maxWidth="sm">
        <Typography variant="h4" gutterBottom>
          Welcome to Our Application
        </Typography>
      <Box 
        display="flex" 
        flexDirection="row"
        alignItems="center" 
        justifyContent="center" 
        minHeight="100vh"
        textAlign="center"
      >

        <Box 
        display="flex" 
        flexDirection="column" 
        marginTop="20%"
        marginRight="20%"

        minHeight="100vh"
        textAlign="center"
        >
        <Typography variant="h5" gutterBottom>
          טפסי שלטים
        </Typography>
        <Link 
          variant="contained" 
          color="primary" 
          style={{ marginBottom: '10px' }}
          to="https://forms.office.com/r/w74VJz3wq8" target="_blank" rel="noopener noreferrer"         >
          שלט מתחלף 
       </Link>
        <Link 
          variant="contained" 
          color="secondary"
          style={{ marginBottom: '10px' }}
          to="https://forms.office.com/r/7P0dJXqQrr" target="_blank" rel="noopener noreferrer"         >
          שלט משולב         
        </Link>
        <Link 
          variant="contained" 
          color="secondary"
          style={{ marginBottom: '10px' }}
          to="https://forms.office.com/r/zJwMbjbZQ3" target="_blank" rel="noopener noreferrer"         >
          שלט טלוויזיוני - רציף
        </Link>
        <Link 
          variant="contained" 
          color="secondary"
          style={{ marginBottom: '10px' }}
          to="https://forms.office.com/r/NZF9YA4UZU" target="_blank" rel="noopener noreferrer"         >
            שלט טלוויזיוני - לוז מרכזי 
        </Link>
        <Link 
          variant="contained" 
          color="secondary"
          style={{ marginBottom: '10px' }}
          to="https://forms.office.com/r/KENUbisqms" target="_blank" rel="noopener noreferrer"         >
          שלט 505 
        </Link>
        <Link 
          variant="contained" 
          color="secondary"
          style={{ marginBottom: '10px' }}
          to="https://forms.office.com/r/JwHjJTM44h" target="_blank" rel="noopener noreferrer"         >
          שלט סטאטי
        </Link>
        </Box>
        <Box 
          display="flex" 
          flexDirection="column" 
          marginTop="20%"
          marginLeft="20%"
          minHeight="100vh"
        >
           <Typography variant="h5" gutterBottom>
           טפסי תחנות ונסיעות
          </Typography>
        </Box>

      </Box>
      
    </Container>
  );
};

export default CastomerTrip;
