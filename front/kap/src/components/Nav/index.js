import * as React from 'react';
import Box from '@mui/material/Box';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import { Link } from "react-router-dom";

function Nav() {

    const [value, setValue] = React.useState(0);

    const handleChange = (event, newValue) => {
        setValue(newValue);
    };


    return (
        <div className="navigation">
            <Box sx={{ width: '100%', bgcolor: 'background.paper' }}>
                <Tabs min-width='80px' value={value} onChange={handleChange} centered>
                    <Tab label="Home" width='25vw' />
                    <Link to="/New" style={{ textDecoration: 'none', color: 'black' }}><Tab label="New" width='25vw' /></Link>
                    <Link to="/Best" style={{ textDecoration: 'none', color: 'black' }}><Tab label="Best" width='25vw' /></Link>
                    <Link to="/Mypage2"><Tab label="Event" width='25vw' /></Link>
                </Tabs>
            </Box>
        </div>
    );
}

export default Nav;