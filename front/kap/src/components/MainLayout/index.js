
import { Link } from "react-router-dom";
import React from 'react';
import FootNav from '../../components/FootNav'
import Nav from '../../components/Nav'
import ShoppingCartIcon from '@mui/icons-material/ShoppingCart';
import Slider from "react-slick";


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
            overflow: "hidden"
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

function MainLayout() {



    return (
        <>
            <div className="App">
                로고
         <input></input><button>검색</button>
                <Link to="/Cart"><button type="button" style={{ backgroundColor: 'white', border: 'none' }}><ShoppingCartIcon /></button></Link>

            </div>
            <Nav />
            <div className="banner">
                <SimpleSlider />
            </div>

            <div>
                오늘의 상품 추천!
      </div>
            <FootNav />

        </>
    );
}

export default MainLayout;
