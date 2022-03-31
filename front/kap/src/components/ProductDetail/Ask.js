import React, { useState, useEffect } from "react";
import { Navigate, useNavigate } from "react-router-dom";
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import SettingsIcon from '@mui/icons-material/Settings';
import FootNav from '../../components/FootNav';
import axios from "axios";

axios.defaults.headers.common['Session'] = document.cookie;
function Ask(props) {

    const [mid, setmid] = useState([]);
    const [mid2, setmid2] = useState([]);
    const [title, setTitle] = useState([]);
    const [content, setContent] = useState([]);
    const [hashtag, setHashtag] = useState([]);
    var pid = window.location.href;
    pid = pid.substring(48, pid.length);

    useEffect(() => {
        axios
            .get(`http://3.38.153.192:5000/product/question/${pid}`)
            .then((res) => {
                setmid2(res.data)
                console.log(res.data)
            })
            .catch((err) => console.log(err));

        axios
            .get(`http://3.38.153.192:5000/detail/${pid}`, {
                'pid': mid.id,
            })
            .then((res) => {
                setmid(res.data)
                console.log(res.data)
            })
            .catch((err) => console.log(err));
    }, []);

    function Handler() {
        axios
            .post(`http://3.38.153.192:5000/product/question/regist`, {
                'product_id': mid.id,
                'title': title,
                'content': content,
                'hashtag': hashtag,
            })
            .then((res) => {
                console.log(res)
            })
            .catch((err) => console.log(err));

    };
    return (
        <>
            <div>

                <div>
                    {
                        mid2.question_title ? (
                            <div>
                                {mid2.question_title}

                            </div>
                        ) : (
                            <div>
                                문의없음
                            </div>
                        )
                    }

                </div>

            </div>
            <div >
                제목
                <input value={title} onChange={(e) => setTitle(e.target.value)}></input>
            </div>
            <div >
                문의내용
                <input value={content} onChange={(e) => setContent(e.target.value)}></input>
            </div>
            <div >
                해쉬태그입력
                <input value={hashtag} onChange={(e) => setHashtag(e.target.value)}></input>
            </div>
            <div>

            </div>
            <button type='button' onClick={Handler}>입력</button>
        </>
    );
}

export default Ask