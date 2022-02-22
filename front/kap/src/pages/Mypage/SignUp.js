import React, { useState, useEffect } from "react";
import axios from "axios";
import { useCookies } from "react-cookie";


function SignUp() {
    const [loginId, SetloginId] = useState("");
    const [password, Setpassword] = useState("");
    const [phone, Setphone] = useState("");
    const [sex, Setsex] = useState("");
    const [birth, Setbirth] = useState("");
    const [address, Setaddress] = useState("");
    const [name, Setname] = useState("");

    const nameHandler = (e) => {
        e.preventDefault();
        Setname(e.target.value);
    };
    const idHandler = (e) => {
        e.preventDefault();
        SetloginId(e.target.value);
    };

    const passwordHandler = (e) => {
        e.preventDefault();
        Setpassword(e.target.value);
    };

    const phoneHandler = (e) => {
        e.preventDefault();
        Setphone(e.target.value);
    };
    const sexHandler = (e) => {
        e.preventDefault();
        Setsex(e.target.value);
    };
    const birthHandler = (e) => {
        e.preventDefault();
        Setbirth(e.target.value);
    };
    const addressHandler = (e) => {
        e.preventDefault();
        Setaddress(e.target.value);
    };




    const [cookies, setCookie] = useCookies(['rememberText']);
    useEffect(() => {
        if (cookies.rememberText !== undefined) {

            SetloginId(cookies.rememberText);
            Setpassword(cookies.rememberText);
            Setphone(cookies.rememberText);
            Setsex(cookies.rememberText);
            Setbirth(cookies.rememberText);
            Setaddress(cookies.rememberText);
            Setname(cookies.rememberText);
            submitHandler(true);
        }
    }, []);

    function submitHandler() {

        setCookie('rememberText',
            loginId,
            password,
            phone,
            sex,
            birth,
            address,
            name, { path: `http://3.38.153.192:5000/regist` });


        axios
            .post(`http://3.38.153.192:5000/regist`, {

                'login_id': loginId,
                'password': password,
                'phone': phone,
                'sex': sex,
                'birth': birth,
                'address': address,
                'name': name
            })
            .then((res) => console.log(res));

    };

    return (
        <>
            <div
                style={{
                    display: "flex",
                    justifyContent: "center",
                    alignItems: "center",
                    width: "100%",
                    height: "100vh",
                }}
            >

                <label>Name</label>
                <input type="text" value={name} onChange={nameHandler}></input>
                <label>Id</label>
                <input type="text" value={loginId} onChange={idHandler}></input>
                <label>Password</label>
                <input type="password" value={password} onChange={passwordHandler}></input>
                <label>Id1</label>
                <input type="text" value={phone} onChange={phoneHandler}></input>
                <label>Id2</label>
                <input type="text" value={sex} onChange={sexHandler}></input>
                <label>Id3</label>
                <input type="text" value={birth} onChange={birthHandler}></input>
                <label>Id4</label>
                <input type="text" value={address} onChange={addressHandler}></input>

                <button onClick={(submitHandler)}>회원가입</button>

            </div>
        </>
    );
}

export default SignUp;