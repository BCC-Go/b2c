import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import { BrowserRouter } from "react-router-dom";
import { CookiesProvider } from 'react-cookie'
import { Provider } from 'react-redux';
import { createStore, combineReducers } from 'redux';

let 기본state = [{ id: 0, name: '멋진신발', quan: 2 }];

function reducer(state = 기본state, 액션) {
  if (액션.type === '수량증가') {

    let copy = [...state];
    copy[액션.데이터].quan++;
    return copy

  } else if (액션.type === '수량감소') {

    let copy = [...state];
    copy[액션.데이터].quan--;
    return copy

  } else {
    return state
  }

}


let alert초기값 = true;

function reducer2(state = alert초기값, 액션) {
  if (액션.type === 'alert닫기') {
    return false
  } else {
    return state
  }
}

let store = createStore(combineReducers({ reducer, reducer2 }))

ReactDOM.render(
  <React.StrictMode>
    <CookiesProvider>
      <BrowserRouter>
        <Provider store={store}>
          <App />
        </Provider>
      </BrowserRouter>
    </CookiesProvider>
  </React.StrictMode>,
  document.getElementById('root')
);

// // If you want to start measuring performance in your app, pass a function
// // to log results (for example: reportWebVitals(console.log))
// // or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
// reportWebVitals();
