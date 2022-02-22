
import { Link, Route, Router, Switch } from "react-router-dom";
import React, { useState, Component } from 'react';
import FootNav from '../../components/FootNav'
import Nav from '../../components/Nav';
import ShoppingCartIcon from '@mui/icons-material/ShoppingCart';
import Slider from "react-slick";
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';
import SearchIcon from '@mui/icons-material/Search';

class SimpleSlider extends React.Component {
    render() {
        const settings = {
            className: "center",
            centerMode: true,
            infinite: true,
            slidesToShow: 1,
            autoplay: true,
            speed: 1000,
            autoplaySpeed: 4000,
            overflow: "hidden",
        };
        return (
            <div className="container" style={{ width: "100 vw" }}>
                <Slider {...settings}>
                    <div>
                        <img src="https://placehold.jp/3d4070/ffffff/300x150.png?text=1" />
                    </div>
                    <div>
                        <img src="https://placehold.jp/3d4070/ffffff/300x150.png?text=2" />
                    </div>
                    <div>
                        <img src="https://placehold.jp/3d4070/ffffff/300x150.png?text=3" />
                    </div>
                    <div>
                        <img src="https://placehold.jp/3d4070/ffffff/300x150.png?text=4" />
                    </div>
                    <div>
                        <img src="https://placehold.jp/3d4070/ffffff/300x150.png?text=5" />
                    </div>
                </Slider>
            </div>
        );
    }
}


class MultipleItems extends Component {
    render() {

        const settings = {
            // dots: true,
            // infinite: true,
            // centerMode: true,

            dots: false,
            infinite: false,
            slidesToShow: 4,
            speed: 500,


        };
        return (
            <div style={{
                Width: "100vw",
                height: "100px",
                justifyContent: "center",
                alignItems: "center",
                paddingTop: "10px",
                paddingLeft: "23px",
                arrows: "true"
            }
            }>
                {/* <h2> Multiple items </h2> */}
                < Slider {...settings}>
                    <div >
                        <img src="imgs/seed.png" height="65px" width="65px" />
                    </div>
                    <div>
                        <img src="imgs/seed.png" height="65px" width="65px" />
                    </div>
                    <div>
                        <img src="imgs/seed.png" height="65px" width="65px" />
                    </div>
                    <div>
                        <img src="imgs/seed.png" height="65px" width="65px" />
                    </div>
                    <div>
                        <img src="imgs/seed.png" height="65px" width="65px" />
                    </div>
                    <div>
                        <img src="imgs/seed.png" height="65px" width="65px" />
                    </div>
                    <div>
                        <img src="imgs/seed.png" height="65px" width="65px" />
                    </div>
                    <div>
                        <img src="imgs/seed.png" height="65px" width="65px" />
                    </div>
                </Slider >
            </div >
        );
    }
}

function Mainpage() {



    return (
        <div className="Mainp">
            <div className="App">
                로고
         <input placeholder='상품을 검색하세요'></input>
                <button style={{ backgroundColor: 'transparent' }}><SearchIcon fontSize="10" /></button>

                <Link to='./Cart'><button style={{ backgroundColor: 'white', border: 'none', marginTop: 10 }}><ShoppingCartIcon color="action" /></button></Link>
            </div>
            <Nav />
            <div className="banner">
                <SimpleSlider />
            </div>

            <div style={{ backgroundColor: "orange" }}>
                오늘의 추천 상품!
        <MultipleItems />
            </div>
            <div style={{ backgroundColor: "green" }}>
                XXX님과 비슷한 취향의 상품
        <MultipleItems />
            </div>
            <FootNav />

        </div >
    );
}

export default Mainpage;

