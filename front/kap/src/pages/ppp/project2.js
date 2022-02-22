import './home.css';
import { Link } from 'react-router-dom';
import axios from 'axios'
import React, { useState, useEffect } from 'react';

axios.defaults.headers.common['Session'] = document.cookie;

const Project2 = () => {
    const [rest, setRest] = useState([]);
    async function test() {
        await axios.get(`http://3.38.153.192:5000/main/recommand`, {},
            // ).then(async res => console.log(res)
        ).then(async res => setRest(res))
        // )
    }

    // accessToken을 localStorage, cookie 등에 저장하지 않는다!

    async function mypage() {
        await axios.get(`http://3.38.153.192:5000/mypage`, {},
        ).then(async res => console.log(res)
        )

    }

    async function coupon() {
        await axios.get(`http://3.38.153.192:5000/coupon`, {},
        ).then(async res => console.log(res)
        )
    }

    async function like_add() {
        await axios.post(`http://3.38.153.192:5000/like`, {
            'product_id': 3
        },
        ).then(async res => console.log(res)
        )
    }

    async function like_delete() {
        await axios.delete(`http://3.38.153.192:5000/like/3`, {},
        ).then(async res => console.log(res)
        )
    }


    return (
        <div>
            <form action='http://3.38.153.192:5000/imgup' method='POST' encType='multipart/form-data'>
                <input type='file' name='file'></input>
                <input type='submit'></input>
            </form>


            <br />
            <button onClick={mypage}>mypage</button>
            <button onClick={coupon}>couponList</button>
            <div>
                <button onClick={like_add}>3번 상품 좋아요</button>
                <button onClick={like_delete}>3번 상품 좋아요 취소</button>
            </div>
        </div>

    );
}

export default Project2;

// test code user recommand product
{/* <div>
    <button onClick={test}>te</button>
    <button value={rest.data? rest.data[0].id:null}>zzz</button>
    <div>{rest.data? rest.data[0].name : null}</div>
    <div>{rest.data? rest.data[0].price : null}</div>
    
    <div>{rest.data? rest.data[1].name : null}</div>
    <div>{rest.data? rest.data[1].price : null}</div>
    
    <div>{rest.data? rest.data[2].name : null}</div>
    <div>{rest.data? rest.data[2].price : null}</div>
    
    <div>{rest.data? rest.data[3].name : null}</div>
    <div>{rest.data? rest.data[3].price : null}</div>
</div> */}