import React from 'react';
import { useNavigate } from 'react-router-dom';
import Button from '@mui/material/Button';
import Container from '@mui/material/Container';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Forms from './components/forms'; 
const Homep = () => {
  const navigate = useNavigate();

  return (
    <Container maxWidth="sm">
      <Box 
        display="flex" 
        flexDirection="column" 
        alignItems="center" 
        justifyContent="center" 
        minHeight="100vh"
        textAlign="center"
      >
        <Typography variant="h4" gutterBottom>
          Welcome to Our Application
        </Typography>
        <Button 
          variant="contained" 
          color="primary" 
          style={{ marginBottom: '10px' }}
          onClick={() => navigate("/electricalSign")}
        >
          Electrical Sign
        </Button>
        <Button 
          variant="contained" 
          color="primary" 
          style={{ marginBottom: '10px' }}
          onClick={() => navigate("/TestSize")}
        >
          Size Test
        </Button>
        <Button 
          variant="contained" 
          color="secondary"
          style={{ marginBottom: '10px' }}

          onClick={() => navigate("/characterCalculator")}
        >
          Character Calculator
        </Button>
        <Button 
          variant="contained" 
          color="secondary"
          style={{ marginBottom: '10px' }}
          onClick={() => navigate("/Forms")}
        >
          מערכת טפסים
        </Button>
      </Box>
      
    </Container>
  );
};

export default Homep;
