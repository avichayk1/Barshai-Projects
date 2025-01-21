import React, { useState} from 'react';
import './characterCalculator.css';
import { useNavigate } from 'react-router-dom';
import Button from '@mui/material/Button';
import Container from '@mui/material/Container';
import Box from '@mui/material/Box';
import Link from '@mui/material';
import Typography from '@mui/material/Typography';
import { TextField } from '@mui/material';
import { red } from '@mui/material/colors';
const Forms = () => {
    const navigate =useNavigate()
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
              Welcome to Barshai Forms
            </Typography>
            <Button 
              variant="contained" 
              color="primary" 
              style={{ marginBottom: '10px' }}
              onClick={() => navigate("/fieldCheck")}
            >
              בקרות שטח
            </Button>
            <Button 
              variant="contained" 
              color="secondary"
              style={{ marginBottom: '10px' }}
    
              onClick={() => navigate("/castomerTrip")}
            >
              מסע לקוח
            </Button>
            
          </Box>
          
        </Container>
      );
    

  };


export default Forms;
