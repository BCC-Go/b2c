
import { Link, useNavigate } from "react-router-dom";
import React, { useState, useEffect } from 'react';
import FootNav from '../../components/FootNav'
import ShoppingCartIcon from '@mui/icons-material/ShoppingCart';
import { IoMdArrowBack } from "react-icons/io";
import ShoppingCartCheckoutOutlinedIcon from '@mui/icons-material/ShoppingCartCheckoutOutlined';
import axios from 'axios'
import LikeButton from '../../components/Button/LikeButton';
import "../Favorite/fav.css";
import { cardClasses } from "@mui/material";

axios.defaults.headers.common['Session'] = document.cookie;
function Category2() {

    var cid = window.location.href;
    cid = cid.substring(35, cid.length);

    const navigate = useNavigate();
    const [cat, setCat] = useState([]);
    const [like, setLike] = useState(false);

    useEffect(() => {
        axios
            .get(`http://3.38.153.192:5000/category/mid/${cid}`)
            .then((res) => {
                setCat(res.data)
                console.log(res.data)
            })
    }, [cid]);

    return (
        <div className="Main">
            <div className="Searchbox">
                <button style={{ backgroundColor: 'white', border: 'none', marginRight: '15px' }} onClick={() => navigate(-1)}>
                    <IoMdArrowBack className="pic" size="18" />
                </button>
                <div className="Searchin" style={{ fontWeight: "bold", display: "flex", justifyContent: "center", fontSize: "20px" }}>
                    카테고리
                </div>
                <button style={{ backgroundColor: 'white', border: 'none' }} icon={<ShoppingCartIcon size="15" />} onClick={() => { }}>
                    <ShoppingCartIcon />
                </button>
            </div>

            <div className="Body">
                {
                    cat.map(function (a, i) {

                        return (
                            <div className="midpro" onClick={() => { navigate('/Category/mid/small/' + cat[i].id) }}>
                                <div className="midpic">
                                    사진
                                </div>
                                <div className="midname">
                                    {cat[i].name}
                                </div>
                            </div>
                        )
                    })
                }
            </div>
            <FootNav />

        </div >
    );

}

export default Category2;

