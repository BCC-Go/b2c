import React, { useState, useEffect } from "react";
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import SettingsIcon from '@mui/icons-material/Settings';
import NotificationsIcon from '@mui/icons-material/Notifications';
import MessageOutlinedIcon from '@mui/icons-material/MessageOutlined';
import ConfirmationNumberOutlinedIcon from '@mui/icons-material/ConfirmationNumberOutlined';
import SavingsOutlinedIcon from '@mui/icons-material/SavingsOutlined';
import FootNav from '../../components/FootNav';
import { useNavigate } from "react-router-dom";
import axios from "axios";

function Coupon() {

    const [coup, setcoup] = useState([]);

    useEffect(() => {
        axios
            .get(`http://3.38.153.192:5000/coupon`)
            .then((res) => {
                setcoup(res.data)

            })
            .catch((err) => console.log(err));
    }, []);

    return (
        <>
            <button type="button">닫기</button>
            <div>
                보유 쿠폰 목록
            </div>
            <div>
                {
                    coup.length === 0 ? (
                        <div>
                            등록된 질문이 없습니다.
                        </div>
                    ) : (
                        coup.map((res, i) => {
                            <div>
                                {res.name}
                            </div>
                        })
                    )
                }
            </div>

        </>
    );
}

export default Coupon;

// {
//     coup.length === 0 ? (
//         <div>
//             등록된 질문이 없습니다.
//         </div>
//     ) : (
//     coup.map((res, index) => {
//         <div className={style.normallistall}>
//             <div className={style.normallist}>
//                 <div className={style.normalisttitle}>{res}</div>
//             </div>
//         </div>;
//     })
// )
// }