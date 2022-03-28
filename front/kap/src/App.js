import './App.css';
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Mainpage from './pages/Mainpage';
import New from './pages/New';
import Best from './pages/Best';
import Favorite from './pages/Favorite';
import FavoriteIn from './pages/FavoriteIn';
import Buy from './pages/Buy';
import SignUp from './pages/Mypage/SignUp';
import Login from './pages/Mypage/Login';
import Category from './pages/Category/Category';
import Category2 from './pages/Category/Category2';
import Category3 from './pages/Category/Category3';
import Detail from './pages/Category/Detail';
import Mypage2 from './pages/Mypage/Mypage2';
import Cart from './pages/Cart/Cart';
import Search from './pages/Search/Search';
import Coupon from './pages/Coupon/Coupon';

function App() {

  return (
    <div className="App">

      <Routes>
        <Route path="/" element={<Mainpage />}></Route>
        <Route path="/New" element={<New />}></Route>
        <Route path="/Best" element={<Best />}></Route>
        <Route path="/Favorite" element={<Favorite />}></Route>
        <Route path="/Favorite/FavoriteIn" element={<FavoriteIn />}></Route>
        <Route path="/Favorite/FavoriteIn/Buy" element={<Buy />}></Route>
        <Route path="/SignUp" element={<SignUp />}></Route>
        <Route path="/Login" element={<Login />}></Route>
        <Route path="/Mypage2/Login" element={<Login />}></Route>
        <Route path="/Mypage2/Coupon" element={<Coupon />}></Route>
        <Route path="/Category" element={<Category />}></Route>
        <Route path="/Category/mid/:id" element={<Category2 />}></Route>
        <Route path="/Category/mid/small/:id" element={<Category3 />}></Route>
        <Route path="/Category/mid/small/detail/:id" element={<Detail />}></Route>
        <Route path="/Mypage2" element={<Mypage2 />}></Route>
        <Route path="/Cart" element={<Cart />}></Route>
        <Route path="/Search" element={<Search />}></Route>
      </Routes>

    </div>
  );
}

export default App;
