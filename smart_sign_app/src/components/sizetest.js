import React, { useState} from 'react';
import Container from '@mui/material/Container';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import { TextField } from '@mui/material';
import { red } from '@mui/material/colors';
const TestSize = () => {
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
        <p  style={ { fontFamily:'',
            fontSize:'70.86pt'}
           }
        >
            hey there
        </p>
     
    </Box>
</Container>)
};

export default TestSize;
