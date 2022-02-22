
import { Link, Route, Router, Switch, useNavigate } from "react-router-dom";
import React, { useState, Component } from 'react';
import FootNav from '../../components/FootNav'
import ShoppingCartIcon from '@mui/icons-material/ShoppingCart';
import { IoMdArrowBack } from "react-icons/io";
import "./index.css";


function Best() {

    const navigate = useNavigate();

    return (
        <div className="Main">

            <div className="Searchbox">
                <button style={{ backgroundColor: 'white', border: 'none' }} onClick={() => navigate(-1)}>
                    <IoMdArrowBack className="pic" size="15" />
                </button>
                <div className="Searchin">
                    즐겨찾기
                    </div>
                <button style={{ backgroundColor: 'white', border: 'none' }} icon={<ShoppingCartIcon size="15" />} onClick={() => { }}>
                    <ShoppingCartIcon />
                </button>
            </div>

            <div className="Body">
                <div className="Count">
                    즐겨찾기한 상품 <div className="CountNumber">17</div>
                </div>
                <div className="Body2">
                    <div className="ContentBox">
                        <div className="ContentPic">
                            사진.PNG
                        </div>
                        <div className="CompanyName">
                            브랜드 이름
                            </div>
                        <div className="ContentName">
                            상품 이름
                            </div>
                        <div className="Price">
                            10,000 원
                        </div>
                    </div>
                    <div className="ContentBox">
                        <div className="ContentPic">
                            사진.PNG
                        </div>
                        <div className="CompanyName">
                            브랜드 이름
                            </div>
                        <div className="ContentName">
                            상품 이름
                            </div>
                        <div className="Price">
                            10,000 원
                        </div>
                    </div>

                </div>
            </div>
            <FootNav />

        </div >
    );

}

export default Best;

