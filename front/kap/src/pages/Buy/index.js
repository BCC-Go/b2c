
import { Link, Route, Router, Switch, useNavigate } from "react-router-dom";
import React, { useState, Component } from 'react';
import FootNav from '../../components/FootNav'
import { IoMdArrowBack } from "react-icons/io";
import "./buy.css";
import Box from "@mui/material/Box";
import InputLabel from "@mui/material/InputLabel";
import MenuItem from "@mui/material/MenuItem";
import FormControl from "@mui/material/FormControl";
import Select from "@mui/material/Select";
import { FaCreditCard } from "react-icons/fa";
import ModeEditIcon from '@mui/icons-material/ModeEdit';

function Buy() {


    const navigate = useNavigate();


    const [coupon, setCoupon] = React.useState("");
    const [addr, setAddr] = React.useState("");
    const [request, setRequest] = React.useState("");

    const handleChange = (event) => {
        setCoupon(event.target.value);
    };
    const handleChange1 = (event) => {
        setAddr(event.target.value);
    };
    const handleChange2 = (event) => {
        setRequest(event.target.value);
    };

    return (
        <div className="Main">

            <div className="Searchbox">
                <button style={{ backgroundColor: 'white', border: 'none' }} onClick={() => navigate(-1)}>
                    <IoMdArrowBack className="pic" size="15" />
                </button>
                <div className="Searchin">
                    주문·결제 하기
                    </div>
            </div>
            <div className="BuyBody">
                <div className="Top">
                    <div className="PurchaseInfo">
                        <div className="Title">
                            구매정보
                        </div>
                        <div className="PurchaseBox">
                            <div className="ProductPic">
                                사진.PNG
                            </div>
                            <div className="ProductInfo">
                                상품이름
                                <div>
                                    10,000원
                                </div>
                            </div>
                        </div>
                    </div>
                    <div className="Coupon">
                        <div className="Title">
                            적용쿠폰
                        </div>
                        <Box sx={{ maxWidth: "400px", height: "50px" }}>
                            <FormControl fullWidth>
                                <InputLabel id="demo-simple-select-label">쿠폰</InputLabel>
                                <Select
                                    labelId="demo-simple-select-label"
                                    id="demo-simple-select"
                                    value={coupon}
                                    label="쿠폰"
                                    onChange={handleChange}
                                >
                                    <MenuItem value={10}>적용가능한 쿠폰 없음</MenuItem>
                                    <MenuItem value={20}>쿠폰2</MenuItem>
                                    <MenuItem value={30}>쿠폰3</MenuItem>
                                </Select>
                            </FormControl>
                        </Box>
                    </div>
                </div>
                <div className="Middle">
                    <div className="Address">
                        <div className="Title">
                            배송지 선택
                        </div>
                        <Box sx={{ maxWidth: "400px", height: "50px" }}>
                            <FormControl fullWidth>
                                <InputLabel id="demo-simple-select-label">배송지</InputLabel>
                                <Select
                                    labelId="demo-simple-select-label"
                                    id="demo-simple-select"
                                    value={addr}
                                    label="쿠폰"
                                    onChange={handleChange1}
                                >
                                    <MenuItem value={10}>주소 없음</MenuItem>
                                    <MenuItem value={20}>경기도</MenuItem>
                                    <MenuItem value={30}>서울</MenuItem>
                                </Select>
                            </FormControl>
                        </Box>
                        <div className="Title">
                            배송시 요청사항
                        </div>
                        <Box sx={{ maxWidth: "400px", height: "50px" }}>
                            <FormControl fullWidth>
                                <InputLabel id="demo-simple-select-label">배송시 요청사항</InputLabel>
                                <Select
                                    labelId="demo-simple-select-label"
                                    id="demo-simple-select"
                                    value={request}
                                    label="쿠폰"
                                    onChange={handleChange2}
                                >
                                    <MenuItem value={10}>요청사항 없음</MenuItem>
                                    <MenuItem value={20}>문앞에 두고 가세요</MenuItem>
                                    <MenuItem value={30}>전화 NO</MenuItem>
                                </Select>
                            </FormControl>
                        </Box>
                    </div>
                    <div className="Card">
                        <div className="Title">
                            결제방법
                        </div>
                        <div className="Creditcard">
                            <FaCreditCard className="pic" size="37" />
                        VISA **** 0959
                        </div>
                        <button className="Edit" onClick={() => { }}>
                            <ModeEditIcon />
                        </button>
                    </div>
                </div>
            </div>
            <button className="FinalPurchase" type="button">10,000원 결제하기</button>

            <FootNav />

        </div >
    );

}


export default Buy;

