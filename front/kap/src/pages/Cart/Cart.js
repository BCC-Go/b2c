import React from 'react';
import './cart.css';
import FootNav from '../../components/FootNav'
import { Table } from 'react-bootstrap';
import { connect } from 'react-redux';


function Cart(props) {
    return (
        <>
            <div>
                장바구니
        </div>
            <div>
                <Table responsive className="carttable">
                    <tr>
                        <th>#</th>
                        <th>상품명</th>
                        <th>수량</th>
                        <th>변경</th>
                    </tr>
                    {props.state.map((a, i) => {
                        return (
                            <tr key={i}>
                                <td>{a.id}</td>
                                <td>{a.name}</td>
                                <td>{a.quan}</td>
                                <td><button onClick={() => { props.dispatch({ type: '수량증가', 데이터: a.id }) }}> + </button>
                                    <button onClick={() => { props.dispatch({ type: '수량감소', 데이터: a.id }) }}> - </button> </td>
                            </tr>
                        )
                    })}
                </Table>
                {props.alert열렸니 === true
                    ? (<div className="my-alert2">
                        <p>지금 구매하시면 20% 할인</p>
                        <button onClick={() => { props.dispatch({ type: 'alert닫기' }) }}>닫기</button>
                    </div>)
                    : null
                }
            </div>
            <FootNav />
        </>
    );
}

function state를props화(state) {
    console.log(state);
    return {
        state: state.reducer,
        alert열렸니: state.reducer2 //리듀서2에 있는거 가져오는법
    }
}
export default connect(state를props화)(Cart);