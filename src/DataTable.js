// DataTable.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Link,
  Button,
} from '@mui/material';

const DataTable = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    // Replace 'your-api-endpoint' with the actual API endpoint you want to fetch data from.
    axios.get('http://192.168.1.187:5008/containers')
      .then((response) => {
        setData(response.data);
      })
      .catch((error) => {
        console.error('Error fetching data:', error);
      });
  }, []);

  const handleButtonClick = async (containerName, host) => {
    try {
      // Send a POST request to 'http://192.168.1.187:5008/containers' and append 'containerName' as a parameter
      const response = await axios.post(`http://192.168.1.187:5008/containers/${containerName}`, {
        action: "start",
        host: host,
      });
      console.log('POST request successful:', response.data);
    } catch (error) {
      console.error('Error sending POST request:', error);
    }
  };

  return (
    <TableContainer component={Paper}>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Container Name</TableCell>
            <TableCell>State</TableCell>
            <TableCell>URL</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {data.map((item, index) => (
            <TableRow key={index}>
              <TableCell>{item.ContainerName}</TableCell>
              <TableCell>
                <Button
                  variant="contained"
                  color="primary"
                  onClick={() => handleButtonClick(item.ContainerName, item.Host)}
                >
                  {item.State}
                </Button>
              </TableCell>
              <TableCell>
                <Link href={item.URL} target="_blank" rel="noopener noreferrer">
                  {item.URL}
                </Link>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default DataTable;
