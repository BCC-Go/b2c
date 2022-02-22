import './home.css';
import { Link } from 'react-router-dom';
import axios from 'axios'
import React, { useState, useEffect } from 'react';
import { useCookies } from 'react-cookie';

axios.defaults.withCredentials = true;
axios.defaults.headers.common['Session'] = document.cookie;

// api.add_resource(Mypage, '/mypage')
// api.add_resource(CouponList, '/coupon')


const Project = () => {
    const [cookies, setCookie, removeCookie] = useCookies(['session_id']);
    const [rest, setRest] = useState([]);

    async function login() {
        await axios.post(`http://3.38.153.192:5000/login`, {
            'login_id': 'idhh',
            'password': 'pas'
        },
        ).then(async res => {
            setCookie('session_id', res.data['session_id'], { maxAge: 2000 })
            // API 요청하는 콜마다 헤더에 accessToken 담아 보내도록 설정
            axios.defaults.headers.common['Session'] = document.cookie;
            // axios.get('/main/recommand')
            // .then(res => {
            //   console.log(res);	
            // })
        }
        )
    }



    return (
        <div>


            <button onClick={login}>session 받기</button>
            <Link to='/test2' style={{ textDecoration: 'none' }}>
                <button >이미지 페이지 이동</button>
            </Link>
            <div>{document.cookie}</div>

        </div>
    );
}

export default Project;