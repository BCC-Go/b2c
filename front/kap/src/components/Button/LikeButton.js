// import React, { useState, useEffect } from 'react';
// import { HeartOutlined, HeartFilled } from '@ant-design/icons';
// import axios from 'axios';

// axios.defaults.headers.common['Session'] = document.cookie;
// function LikeButton(props) {
//     const [like, setLike] = useState([]);
//     const [all, setAll] = useState([]);
//     var cid = window.location.href;
//     cid = cid.substring(41, cid.length);
//     const pid = all.product_id;

//     useEffect(() => {
//         axios
//             .get(`http://3.38.153.192:5000/category/item/${cid}`)
//             .then((res) => {
//                 setAll(res.data)
//                 console.log(res.data)
//             })
//     }, [cid]);



//     const toggleLike = async (e) => {
//         const res = await axios
//             .post(`http://3.38.153.192:5000/like/0`, {
//                 "pid": all.product_id,
//             })
//             .then((res) => {
//                 setLike(1)
//                 console.log(res.data)
//             })
//     };
//     const toggleDelete = async (e) => {
//         const res = await axios
//             .delete(`http://3.38.153.192:5000/like/${pid}`)
//             .then((res) => {
//                 setLike(0)
//                 console.log(like)
//             })
//     };

//     return (
//         <div>
//             {
//                 all.like == 1 ? (<HeartFilled style={{ color: 'red', fontSize: '20px', marginTop: '5px' }} onClick={toggleDelete} />) :
//                     (<HeartOutlined style={{ fontSize: '20px', marginTop: '5px' }} onClick={toggleLike} />)

//             }
//         </div>
//     );
//     // if (all.like == 1) {
//     //     return <HeartFilled style={{ color: 'red', fontSize: '20px', marginTop: '5px' }} onClick={toggleDelete} />
//     // }
//     // else {
//     //     return <HeartOutlined style={{ fontSize: '20px', marginTop: '5px' }} onClick={toggleLike} />
//     // }



// }

// export default LikeButton;