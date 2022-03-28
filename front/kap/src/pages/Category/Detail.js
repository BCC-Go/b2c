
import { useNavigate } from "react-router-dom";
import React, { useState, useEffect } from 'react';
import FootNav from '../../components/FootNav'
import ShoppingCartIcon from '@mui/icons-material/ShoppingCart';
import { IoMdArrowBack } from "react-icons/io";
import FavoriteBorderIcon from '@mui/icons-material/FavoriteBorder';
import "../Favorite/fav.css";
import { FaStar } from "react-icons/fa";
import axios from 'axios';
import { HeartOutlined, HeartFilled } from '@ant-design/icons';
import { Nav } from 'react-bootstrap';
import Productd from "../../components/ProductDetail/Productd";
import Review from "../../components/ProductDetail/Review";
import Ask from "../../components/ProductDetail/Ask";

function Detail() {

    const navigate = useNavigate();
    const [mid, setmid] = useState([]);
    const [mode, setMode] = useState(<Productd />);
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
        <div className="Main">

            <div className="Searchbox">
                <button style={{ backgroundColor: 'white', border: 'none', marginRight: '15px' }} onClick={() => navigate(-1)}>
                    <IoMdArrowBack className="pic" size="18" />
                </button>
                <div className="Searchin" style={{ fontWeight: "bold", display: "flex", justifyContent: "center", fontSize: "20px" }}>
                    {mid.brand}
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
                        {mid.name}
                        <div>
                            <Heart />
                        </div>
                    </div>
                    <div className="Price1">
                        {
                            mid.rate ? (
                                <>
                                    <div className="Discount">
                                        {mid.rate} %
                                <div className="DiscountPrice">
                                            {mid.price}원
                                </div>
                                    </div>
                                    <div className="FinalPrice1">
                                        {mid.amount} 원
                            </div>
                                </>
                            ) : (
                                <>
                                    <div className="FinalPrice1">
                                        {mid.price} 원
                            </div>
                                </>
                            )
                        }

                    </div>
                    <div className="TwoButton">
                        <button className="Cartbutton" type="button">장바구니 담기</button>
                        <button className="Buybutton" type="button">바로구매</button>
                    </div>

                </div>

                <Nav justify variant="tabs" defaultActiveKey="link-0" style={{ maxWidth: '480px', width: '100vw' }}>
                    <Nav.Item >
                        <Nav.Link eventKey="link-0" onClick={() => setMode(<Productd />)}>상품상세</Nav.Link>
                    </Nav.Item>
                    <Nav.Item>
                        <Nav.Link eventKey="link-1" onClick={() => setMode(<Review />)}>상품평</Nav.Link>
                    </Nav.Item>
                    <Nav.Item>
                        <Nav.Link eventKey="link-2" onClick={() => setMode(<Ask />)}>상품문의</Nav.Link>
                    </Nav.Item>
                </Nav>
                <div>
                    {mode}
                </div>
                <div>

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
                <button className="Buybutton22" type="button">구매</button>
            </div>
            <FootNav />

        </div >
    );

}

function Heart(props) {
    var pid = window.location.href;
    pid = pid.substring(48, pid.length);
    const [mid, setmid] = useState([]);
    const [like, setLike] = useState(false);
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


    const toggleLike = async (e) => {
        setLike(false);
        const res = await axios
            .post(`http://3.38.153.192:5000/like/0`, {
                'pid': mid.id,
            })
            .then((res) => {

                console.log(res.data)
            })
            .catch((err) => console.log(err));
    };

    const toggleDelete = async (e) => {
        setLike(true);
        await axios

            .delete(`http://3.38.153.192:5000/like/${pid}`)
            .then((res) => {
                console.log(res.data)
            })
            .catch((err) => console.log(err));
    };

    return (
        <>
            <div>
                {
                    like == false && mid.like == 1 ? (<HeartFilled style={{ color: 'red', fontSize: '20px', marginTop: '5px' }} onClick={toggleDelete} />)
                        :
                        (<HeartOutlined style={{ fontSize: '20px', marginTop: '5px' }} onClick={toggleLike} />)

                }
            </div>
        </>
    );
}

export default Detail;

