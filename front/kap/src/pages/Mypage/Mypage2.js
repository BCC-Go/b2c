import React, { useState, useEffect } from "react";
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import SettingsIcon from '@mui/icons-material/Settings';
import NotificationsIcon from '@mui/icons-material/Notifications';
import MessageOutlinedIcon from '@mui/icons-material/MessageOutlined';
import ConfirmationNumberOutlinedIcon from '@mui/icons-material/ConfirmationNumberOutlined';
import SavingsOutlinedIcon from '@mui/icons-material/SavingsOutlined';
import "./mypage2.css";
import FootNav from '../../components/FootNav';
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { Link } from "react-router-dom";

axios.defaults.headers.common['Session'] = document.cookie;

function Mypage2() {

    const navigate = useNavigate();

    const [my, setmy] = useState([]);

    async function logout() {
        await axios.post(`http://3.38.153.192:5000/logout`, {
            // 'login_id': loginId,
            // 'password': password
        },
        ).then(async res => {
            //     // API 요청하는 콜마다 헤더에 accessToken 담아 보내도록 설정
            console.log('로그아웃 성공')
            navigate('./login')
        }
        )
    }

    useEffect(() => {
        axios
            .get(`http://3.38.153.192:5000/mypage`)
            .then((res) => {
                setmy(res.data)
            })
            .catch((err) => console.log(err));
    }, []);

    return (
        <div className="mypagecontain" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <div className="iconid">
                <div style={{ display: 'flex' }}>
                    <AccountCircleIcon color="action" fontSize="large" />
                    <div className="username" style={{ fontWeight: 'bold', margin: 10 }}>
                        {my.name} 님
                    </div>
                </div>
                <div className="settingbutton">
                    <button style={{ backgroundColor: 'transparent', border: 'none' }}>
                        <NotificationsIcon color="action" fontSize="medium" />
                    </button>
                    <button style={{ backgroundColor: 'transparent', border: 'none' }}>
                        <SettingsIcon color="action" fontSize="medium" />
                    </button>
                </div>
            </div>
            <div className="myuserbox">
                <div className="rank">
                    {my.rank}
                </div>
                <button type="button"
                    style={{ color: 'gray', backgroundColor: 'transparent', border: 'none' }}>
                    혜택보기
                </button>

            </div>
            <div style={{ display: 'flex', width: '70%', justifyContent: 'space-between', marginTop: '10px' }}>
                <button className="mesbutton">
                    <MessageOutlinedIcon fontSize="medium" />
                    <div style={{ display: 'flex' }}>
                        리뷰&nbsp;
                    </div>
                </button>
                <button className="mesbutton">
                    <Link to='./Coupon'>
                        <ConfirmationNumberOutlinedIcon fontSize="medium" />
                    </Link>
                    <div style={{ display: 'flex' }}>
                        COUPON&nbsp; <div style={{ color: 'red' }}> {my.coupon_num}</div>
                    </div>
                </button>
                <button className="mesbutton">
                    <SavingsOutlinedIcon fontSize="medium" />
                    <div style={{ display: 'flex' }}>
                        POINT&nbsp; <div style={{ color: 'red' }}> {my.point}</div>
                    </div>
                </button>
            </div>
            <div className="orderarrive">
                <div className="ordertitle">
                    주문/배송조회
                </div>
                <div className="orderstatus">
                    <div className="ordernumber">
                        0
                        <div className="ordertext">
                            입금/결제
                        </div>
                    </div>
                    <div className="ordernumber">
                        0
                        <div className="ordertext">
                            배송중
                        </div>
                    </div>
                    <div className="ordernumber">
                        0
                        <div className="ordertext">
                            배송완료
                        </div>
                    </div>
                    <div className="ordernumber">
                        12
                        <div className="ordertext">
                            구매확정
                        </div>
                    </div>
                </div>
            </div>
            <div className="mypagebanner">
                배너
            </div>
            <div className="shopping">
                쇼핑
                <button className="shopbttn" type="button">구매내역</button>
                <button className="shopbttn" type="button">찜목록</button>
                <button className="shopbttn" type="button">EVENT</button>
            </div>
            <div className="shopping2">
                고객센터
                <button className="shopbttn" type="button">공지사항</button>
                <button className="shopbttn" type="button">Q & A</button>
                <button className="shopbttn" type="button">고객센터</button>
                <button className="shopbttn" type="button" onClick={logout}>로그아웃</button>
            </div>
            <FootNav />
        </div>
    );
}
export default Mypage2