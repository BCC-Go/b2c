
import { Link, useNavigate } from "react-router-dom";
import React, { useState, useEffect, Component } from 'react';
import FootNav from '../../components/FootNav'
import ShoppingCartIcon from '@mui/icons-material/ShoppingCart';
import { IoMdArrowBack } from "react-icons/io";
import ShoppingCartCheckoutOutlinedIcon from '@mui/icons-material/ShoppingCartCheckoutOutlined';
import axios from 'axios'
import LikeButton from '../../components/Button/LikeButton';
import { useTheme } from '@mui/material/styles';
import MobileStepper from '@mui/material/MobileStepper';
import Button from '@mui/material/Button';
import KeyboardArrowLeft from '@mui/icons-material/KeyboardArrowLeft';
import KeyboardArrowRight from '@mui/icons-material/KeyboardArrowRight';
import Slider from "react-slick";

function Search(props) {

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


    const theme = useTheme();
    const [activeStep, setActiveStep] = React.useState(0);

    const handleNext = () => {
        setActiveStep((prevActiveStep) => prevActiveStep + 1);
    };

    const handleBack = () => {
        setActiveStep((prevActiveStep) => prevActiveStep - 1);
    };

    const settings = {
        dots: true,
        infinite: true,
        speed: 500,
        slidesToShow: 1,
        slidesToScroll: 1
    };

    return (
        <div className="Main">

            <div className="Searchbox">
                <button style={{ backgroundColor: 'white', border: 'none' }} onClick={() => navigate(-1)}>
                    <IoMdArrowBack className="pic" size="15" />
                </button>
                <div className="Searchin">
                    검색
                </div>
            </div>
            <div>
                <input></input><button>검색</button>
            </div>
            <MobileStepper
                variant="dots"
                steps={3}
                position="static"
                activeStep={activeStep}
                sx={{ maxWidth: 400, flexGrow: 1 }}
                nextButton={
                    <Button size="small" onClick={handleNext} disabled={activeStep === 2}>

                        {theme.direction === 'rtl' ? (
                            <KeyboardArrowLeft />
                        ) : (
                            <KeyboardArrowRight />
                        )}
                    </Button>
                }
                backButton={
                    <Button size="small" onClick={handleBack} disabled={activeStep === 0}>
                        {theme.direction === 'rtl' ? (
                            <KeyboardArrowRight />
                        ) : (
                            <KeyboardArrowLeft />
                        )}

                    </Button>
                }
            />

            <div>
                <h2> Single Item</h2>
                <Slider {...settings}>
                    <div>
                        <h3>1</h3>
                    </div>
                    <div>
                        <h3>2</h3>
                    </div>
                    <div>
                        <h3>3</h3>
                    </div>
                    <div>
                        <h3>4</h3>
                    </div>
                    <div>
                        <h3>5</h3>
                    </div>
                </Slider>
            </div>

            <FootNav />

        </div >
    );

}

export default Search;

