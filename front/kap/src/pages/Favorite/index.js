
import { Link, useNavigate } from "react-router-dom";
import React, { useState, useEffect } from 'react';
import FootNav from '../../components/FootNav'
import ShoppingCartIcon from '@mui/icons-material/ShoppingCart';
import { IoMdArrowBack } from "react-icons/io";
import ShoppingCartCheckoutOutlinedIcon from '@mui/icons-material/ShoppingCartCheckoutOutlined';
import axios from 'axios';
// import LikeButton from '../../components/Button/LikeButton';
// import style from '../../styles/fav.css';
import "../Favorite/fav.css";
import { connect } from 'react-redux';
import { HeartOutlined, HeartFilled } from '@ant-design/icons';
axios.defaults.headers.common['Session'] = document.cookie;
function Favorite() {

    const navigate = useNavigate();
    const [mid, setmid] = useState([]);

    useEffect(() => {
        axios
            .get(`http://3.38.153.192:5000/like/0`)
            .then((res) => {
                setmid(res.data)
                console.log(res.data)
            })
            .catch((err) => console.log(err));
    }, []);


    return (
        <>
            <div className="Main">
                <div className="Searchbox">
                    <button style={{ backgroundColor: 'white', border: 'none', marginRight: '15px' }} onClick={() => navigate(-1)}>
                        <IoMdArrowBack className="pic" size="18" />
                    </button>
                    <div className="Searchin" style={{ fontWeight: "bold", display: "flex", justifyContent: "center", fontSize: "20px" }}>
                        좋아요한 상품
                    </div>
                    <button style={{ backgroundColor: 'white', border: 'none' }} icon={<ShoppingCartIcon size="15" />} onClick={() => { }}>
                        <ShoppingCartIcon />
                    </button>
                </div>
                <div className="category3body" style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'center' }}>
                    {
                        mid.map(function (a, i) {
                            return <Memory mid={mid[i]} key={i} />
                        })
                    }
                </div>
            </div >
            <FootNav />
        </>
    );

}

function Memory(props) {


    const navigate = useNavigate();
    const [mid, setmid] = useState([]);
    const [like, setLike] = useState(false);
    const pid = props.mid.product_id;

    useEffect(() => {
        axios
            .get(`http://3.38.153.192:5000/like/0`)
            .then((res) => {
                setmid(res.data)
                console.log(res.data)
            })
    }, []);
    const toggleLike = async (e) => {
        setLike(false);
        const res = await axios
            .post(`http://3.38.153.192:5000/like/0`, {
                'pid': props.mid.product_id,
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
            <div className="ContentBox1" >
                <div className="ContentPic1" onClick={() => { navigate('/Category/mid/small/detail/' + props.mid.id) }}>
                    사진.PNG
                                        </div>
                <div className="CompanyName" style={{ marginLeft: '5px' }}>
                    {props.mid.brand}
                </div>

                <div className="ContentName" style={{ marginLeft: '5px' }}>
                    {props.mid.name}
                </div>

                <div className="likecart">
                    <div className="PriceAll12" style={{ display: 'flex', flexDirection: 'column', fontSize: '10px', marginLeft: '3px' }}>
                        {
                            props.mid.rate ? (
                                <div>
                                    <div className="Discount12">
                                        <div className="Rate12">
                                            {props.mid.rate}
                                        </div>
                                        <div className="DiscountPricel">
                                            {props.mid.price} 원
                                                                </div>
                                    </div>
                                    <div className="Much">
                                        {props.mid.amount} 원
                                                            </div>
                                </div>
                            ) : (
                                <div className="Much">
                                    {props.mid.price} 원
                                </div>
                            )
                        }

                        <div className="both">
                            {
                                like == false && props.mid.like == 1 ? (<HeartFilled style={{ color: 'red', fontSize: '20px', marginTop: '5px' }} onClick={toggleDelete} />)
                                    :
                                    (<HeartOutlined style={{ fontSize: '20px', marginTop: '5px' }} onClick={toggleLike} />)

                            }

                            <button className="click" type="button" onClick={() => {
                                // props.dispatch({ type: '항목추가', 데이터: { id: mid.id, name: mid.name, quan: 1 } });
                                // // navigate('./')
                            }}>
                                <ShoppingCartCheckoutOutlinedIcon sx={{ fontSize: 20 }} />
                            </button>
                        </div>
                    </div>
                </div >
            </div >
        </>
    );

}

export default Favorite


