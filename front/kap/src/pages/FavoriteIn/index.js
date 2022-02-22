
import { Link, Route, Router, Switch, useNavigate } from "react-router-dom";
import React, { useState, Component } from 'react';
import FootNav from '../../components/FootNav'
import ShoppingCartIcon from '@mui/icons-material/ShoppingCart';
import { IoMdArrowBack } from "react-icons/io";
import FavoriteBorderIcon from '@mui/icons-material/FavoriteBorder';
import "./favin.css";
import { FaStar } from "react-icons/fa";
import Productd from "../../components/ProductDetail/Productd";
import Review from "../../components/ProductDetail/Review";
import Ask from "../../components/ProductDetail/Ask";

function FavoriteIn() {
    const navigate = useNavigate();
    const [mode, Setmode] = useState(<Productd />);


    return (
        <div className="Main">

            <div className="Searchbox">
                <button style={{ backgroundColor: 'white', border: 'none' }} onClick={() => navigate(-1)}>
                    <IoMdArrowBack className="pic" size="15" />
                </button>
                <div className="Searchin">
                    쇼핑몰 이름
                    </div>
                <button style={{ backgroundColor: 'white', border: 'none' }} icon={<ShoppingCartIcon size="15" />} onClick={() => { }}>
                    <ShoppingCartIcon />
                </button>
            </div>

            <div className="Body">

                <div className="ContentBox">
                    <div className="ContentPic">
                        사진.PNG
                        </div>
                    <div className="ContentName1">
                        상품 이름
                            <button style={{ backgroundColor: 'white', border: 'none' }} icon={<FavoriteBorderIcon size="15" />} onClick={() => { }}>
                            <FavoriteBorderIcon />
                        </button>
                    </div>
                    <div className="Price1">
                        <div className="Discount">
                            50 %
                                <div className="DiscountPrice">
                                20,000원
                                </div>
                        </div>
                        <div className="FinalPrice1">
                            10,000 원
                            </div>
                    </div>
                    <div className="TwoButton">
                        <button className="Cartbutton" type="button">장바구니 담기</button>
                        <button className="Buybutton" type="button">바로구매</button>
                    </div>

                </div>
                <div className="ModButton">
                    <button type="button" onClick={() => Setmode(<Productd />)}>상품상세</button>
                    <button type="button" onClick={() => Setmode(<Review />)}>상품평</button>
                    <button style={{ borderRight: "none" }} type="button" onClick={() => Setmode(<Ask />)}>상품문의</button>
                </div>
                <div>
                    {mode}
                </div>
            </div>
            <div className="Bottom" style={{ backgroundColor: "white" }}>
                <button className="Review"><FaStar className="pic" size="13" /> 리뷰(899)</button>
                <div className="BottomPrice">
                    <div className="Discount">
                        50%
                        </div>
                    <div className="FinalPrice1">
                        10,000 원
                            </div>
                </div>
                <Link to="./Buy"> <button className="Buybutton22" type="button">구매</button></Link>
            </div>
            <FootNav />

        </div >
    );

}


export default FavoriteIn;

