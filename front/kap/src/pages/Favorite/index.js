
import { Link, useNavigate } from "react-router-dom";
import React, { useState, useEffect } from 'react';
import FootNav from '../../components/FootNav'
import ShoppingCartIcon from '@mui/icons-material/ShoppingCart';
import { IoMdArrowBack } from "react-icons/io";
import ShoppingCartCheckoutOutlinedIcon from '@mui/icons-material/ShoppingCartCheckoutOutlined';
import axios from 'axios'
import LikeButton from '../../components/Button/LikeButton';
import "./fav.css";


function Favorite(props) {

    const navigate = useNavigate();


    const [like, setLike] = useState(false)

    useEffect(async () => {
        const fetchData = async () => {
            const res = await axios.get(`http://3.38.153.192:5000/like`, {
                'product_id': 3
            },
            )
            if (res.data.type === 'liked') setLike(true)
        }
        fetchData()
    }, []);
    const toggleLike = async (e) => {
        const res = await axios.post(`http://3.38.153.192:5000/like`, {
            'product_id': 3
        },
        )
        setLike(!like)
    }



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
                <div className="Body22">

                    <div className="ContentBox1">
                        <Link to="./FavoriteIn" style={{ textDecoration: "none", color: 'black' }}>
                            <div className="ContentPic1">
                                사진.PNG
                        </div>
                            <div className="CompanyName">
                                브랜드 이름
                            </div>

                            <div className="ContentName">
                                상품 이름
                            </div>
                        </Link>
                        <div className="likecart">
                            <div className="Much">
                                10,000 원
                        </div>
                            <div className="both">
                                <LikeButton />
                                <button className="click" type="button"><ShoppingCartCheckoutOutlinedIcon sx={{ fontSize: 20 }} /></button>
                            </div>
                        </div>
                    </div>


                </div>
            </div>
            <FootNav />

        </div >
    );

}

export default Favorite;

