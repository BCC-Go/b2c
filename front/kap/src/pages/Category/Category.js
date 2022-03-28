import React, { useState, useEffect } from "react";
import { Navigate, useNavigate } from "react-router-dom";
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import SettingsIcon from '@mui/icons-material/Settings';
import "./category.css";
import FootNav from '../../components/FootNav';
import axios from "axios";

axios.defaults.headers.common['Session'] = document.cookie;
function Category(props) {

    const [my, setmy] = useState([]);
    const [cat, setCat] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        axios
            .get(`http://3.38.153.192:5000/mypage`)
            .then((res) => {
                setmy(res.data)
                console.log(res.data)
            })
            .catch((err) => console.log(err));
        axios
            .get(`http://3.38.153.192:5000/category/large`)
            .then((res) => {
                setCat(res.data)
                console.log(res.data)
            })
            .catch((err) => console.log(err));
    }, []);
    return (
        <>
            <div className="iconid">
                <div style={{ display: 'flex' }}>
                    <AccountCircleIcon color="action" fontSize="large" />

                    <div className="username" style={{ fontWeight: 'bold', marginLeft: 20 }}>
                        {my.name} 님 {cat.name}
                        <div className="usergrade" style={{ fontWeight: 'lighter', fontSize: 14 }}>
                            {my.rank} 등급
                    </div>
                    </div>
                </div>
                <div className="settingbutton">
                    <button style={{ backgroundColor: 'transparent', border: 'none' }}>
                        <SettingsIcon fontSize="medium" />
                    </button>
                </div>
            </div>
            <div className="categorybundle">
                <div className="categorytitle">
                    카테고리
                </div>
                <div className="bundle">
                    {
                        cat.map(function (a, i) {
                            return (
                                <div className="bundleiconname" style={{ fontSize: 10, margin: 16 }} key={i} onClick={() => { navigate('/Category/mid/' + cat[i].id) }}>
                                    {cat[i].name}
                                    <div className="bundleicon">
                                        <img src={'https://b2c-imagebucket.s3.ap-northeast-2.amazonaws.com/category/' + (i + 1) + '.jpeg'} style={{ width: '60px', height: '60px', borderRadius: 10 }}></img>
                                    </div>
                                </div>
                            )
                        })
                    }
                </div>
            </div>
            <div className="categorytitle">
                Event!
            </div>
            <div className="eventbanner">
                배너
            </div>
            <div className="eventbanner">
                배너
            </div>
            <FootNav />
        </>
    );
}

export default Category