import React, { useState, useEffect } from "react";
import { createRoutesFromChildren, Link, useNavigate } from "react-router-dom";
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import SettingsIcon from '@mui/icons-material/Settings';
import "./category.css";
import FootNav from '../../components/FootNav';
import food from "../../public/imgs/food.jpg"
import cloth from "../../public/imgs/cloth.jpg"
import household from "../../public/imgs/household.jpg"
import electronic from "../../public/imgs/electronic.jpg"
import axios from "axios";


function Category() {

    const [my, setmy] = useState([]);


    useEffect(() => {
        axios
            .get(`http://3.38.153.192:5000/mypage`)
            .then((res) => {
                setmy(res.data)
            })
            .catch((err) => console.log(err));
    }, []);

    return (
        <>
            <div className="iconid">
                <div style={{ display: 'flex' }}>
                    <AccountCircleIcon color="action" fontSize="large" />

                    <div className="username" style={{ fontWeight: 'bold', marginLeft: 20 }}>
                        {my.name} 님
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

                    <div className="bundleiconname" style={{ fontSize: 10, margin: 16 }}>
                        의류
                            <Link to='./Cloth'>
                            <div className="bundleicon">
                                <img src={cloth} style={{ width: '60px', height: '60px', borderRadius: 10 }} />
                            </div>
                        </Link>
                    </div>

                    <div className="bundleiconname" style={{ fontSize: 10, margin: 17 }}>
                        가전
                        <div className="bundleicon">
                            <img src={electronic} style={{ width: '60px', height: '60px', borderRadius: 10 }} />
                        </div>
                    </div>
                    <div className="bundleiconname" style={{ fontSize: 10, margin: 17 }}>
                        생활용품
                        <div className="bundleicon">
                            <img src={household} style={{ width: '60px', height: '60px', borderRadius: 10 }} />
                        </div>
                    </div>
                    <div className="bundleiconname" style={{ fontSize: 10, margin: 17 }}>
                        식품
                        <div className="bundleicon">
                            <img src={food} style={{ width: '60px', height: '60px', borderRadius: 10 }} />
                        </div>
                    </div>
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