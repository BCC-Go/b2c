import React, { useState, useEffect } from "react";
import { Navigate, useNavigate } from "react-router-dom";
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import SettingsIcon from '@mui/icons-material/Settings';
import FootNav from '../../components/FootNav';
import axios from "axios";

axios.defaults.headers.common['Session'] = document.cookie;
function Ask() {

    const [mid, setmid] = useState([]);
    var pid = window.location.href;
    pid = pid.substring(48, pid.length);

    useEffect(() => {
        axios
            .get(`http://3.38.153.192:5000/detail/${pid}`, {
                'pid': mid.id,
            })
            .then((res) => {
                setmid(res.data)
                console.log(res.data)
            })

    }, [pid]);
    return (

        <div >
            {mid.summary}
        </div>

    );
}

export default Ask