import React, { useState, useEffect } from "react";
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import SettingsIcon from '@mui/icons-material/Settings';
import NotificationsIcon from '@mui/icons-material/Notifications';
import MessageOutlinedIcon from '@mui/icons-material/MessageOutlined';
import ConfirmationNumberOutlinedIcon from '@mui/icons-material/ConfirmationNumberOutlined';
import SavingsOutlinedIcon from '@mui/icons-material/SavingsOutlined';
import FootNav from '../../components/FootNav';
import { useNavigate } from "react-router-dom";
import axios from "axios";

axios.defaults.headers.common['Session'] = document.cookie;


function Cloth() {

    const [cloth, setcloth] = useState([]);

    useEffect(() => {
        axios
            .get(`http://3.38.153.192:5000/category/large`)
            .then((res) => {
                console.log(res)
            })
            .catch((err) => console.log(err));
    }, []);

    useEffect(() => {
        axios
            .get(`http://3.38.153.192:5000/category/item/`)
            .then((res) => {
                setcloth(res.data)
            })
            .catch((err) => console.log(err));
    }, []);
    return (
        <>
            <div>
                의류
        </div>
            <div>
                {cloth[0]}
            </div>
        </>
    );
}

export default Cloth;