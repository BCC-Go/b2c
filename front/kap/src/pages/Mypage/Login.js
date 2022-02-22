import React, { useState, useEffect } from "react";
import axios from "axios";
import { useCookies } from "react-cookie";
import { Link } from 'react-router-dom';
import { useNavigate } from "react-router-dom";

axios.defaults.withCredentials = true;
axios.defaults.headers.common['Session'] = document.cookie;

function Login() {
    const navigate = useNavigate();

    const [loginId, SetloginId] = useState("");
    const [password, Setpassword] = useState("");

    const idHandler = (e) => {
        e.preventDefault();
        SetloginId(e.target.value);
    };

    const passwordHandler = (e) => {
        e.preventDefault();
        Setpassword(e.target.value);
    };

    const [cookies, setCookie, removeCookie] = useCookies(['session_id']);
    const [rest, setRest] = useState([]);



    async function login() {
        await axios.post(`http://3.38.153.192:5000/login`, {
            'login_id': loginId,
            'password': password
        },
        ).then(async res => {
            if (res.data['session_id'] === 0) {
                console.log("실패")
                alert("로그인 실패")
            }
            else {
                setCookie('session_id', res.data['session_id'], { maxAge: 2000 })
                // API 요청하는 콜마다 헤더에 accessToken 담아 보내도록 설정
                axios.defaults.headers.common['Session'] = document.cookie;
                console.log('로그인 성공')
                navigate('/');
            }
        }
        )

    }

    // useEffect(() => {
    //     if (login) {
    //         navigate('/');
    //     }
    // });


    return (
        <>
            <div
                style={{
                    display: "flex",
                    flexDirection: "column",
                    justifyContent: "center",
                    alignItems: "center",
                    width: "100%",
                    height: "100vh",
                }}
            >


                <label>Id</label>
                <input type="text" value={loginId} onChange={idHandler}></input>
                <label>Password</label>
                <input type="password" value={password} onChange={passwordHandler}></input>

                <button onClick={login}>로그인</button>


            </div>
        </>
    );
}

export default Login;