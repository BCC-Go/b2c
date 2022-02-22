import React from "react";
import ReactDOM from "react-dom";
import Slider from "react-slick";

import "../node_modules/slick-carousel/slick/slick.css";
import "../node_modules/slick-carousel/slick/slick-theme.css";
import "./styles.css";

class SimpleSlider extends React.Component {
    render() {
        const settings = {
            className: "center",
            centerMode: true,
            infinite: true,
            centerPadding: "20px",
            slidesToShow: 1,
            speed: 500
        };
        return (
            <div className="container">
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
