import React, { useState } from 'react';
import Box from '@mui/material/Box';
import CssBaseline from '@mui/material/CssBaseline';
import BottomNavigation from '@mui/material/BottomNavigation';
import BottomNavigationAction from '@mui/material/BottomNavigationAction';
import FavoriteIcon from '@mui/icons-material/Favorite';
import Paper from '@mui/material/Paper';
import HomeIcon from '@mui/icons-material/Home';
import SearchIcon from '@mui/icons-material/Search';
import TableRowsIcon from '@mui/icons-material/TableRows';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import { Link } from "react-router-dom";

function FootNav() {
    const [value, setValue] = useState(0);
    const ref = React.useRef(null);
    return (
        <div>
            <Box sx={{ pb: 7 }} ref={ref}>
                <CssBaseline />

                <Paper sx={{ position: 'fixed', bottom: 0, left: 0, right: 0 }} elevation={3}>
                    <BottomNavigation
                        showlabels='true'
                        max-width='480px'
                        width='100 %'
                        value={value}
                        onChange={(event, newValue) => {
                            setValue(newValue);
                        }}
                    >
                        <Link to="/category"><BottomNavigationAction width='20 %' icon={<TableRowsIcon />} /></Link>
                        <Link to="/Search"><BottomNavigationAction width='20 %' icon={<SearchIcon />} /></Link>
                        <Link to="/"><BottomNavigationAction width='20 %' icon={<HomeIcon />} /></Link>
                        <Link to="/Favorite"><BottomNavigationAction width='20 %' icon={<FavoriteIcon />} /></Link>
                        <Link to="/Login"><BottomNavigationAction width='20 %' icon={<AccountCircleIcon />} /></Link>
                    </BottomNavigation>
                </Paper>
            </Box>
        </div >
    );
}

export default FootNav;