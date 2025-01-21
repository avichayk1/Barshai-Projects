import React from 'react';
import { useNavigate } from 'react-router-dom';
import Button from '@mui/material/Button';
import Container from '@mui/material/Container';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import { Link } from 'react-router-dom';
import { yellow } from '@mui/material/colors';
const FieldCheck = () => {
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
          Welcome to fieldCheck
        </Typography>
        <Link 
          variant="contained" 
          color="primary" 
          style={{ marginBottom: '10px', backgroundColor: '#1a237e'}}
          to="https://forms.office.com/r/d7r4est5Bw" target="_blank" rel="noopener noreferrer"         >
          בקרת שטח לפני הצבה
        </Link>
        <Link 
          variant="contained" 
          color="secondary"
          style={{ marginBottom: '10px' }}

          onClick={() => navigate("/characterCalculator")}
        >
          בקרת שטח לאחר הצבה
        </Link>
      </Box>
      
    </Container>
  );
};

export default FieldCheck;
