import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import About from "./components/About";
import Play from "./components/Play";
import NavigationBar from "./components/NavigationBar";
import "./App.css";

function App() {
  return (
    <div className="App">
      <Router>
        <NavigationBar />
        <Routes>
          <Route path="/about" element={<About />} />
          <Route path="/play" element={<Play />} />
          <Route
            path="/"
            element={
              <>
                <h1 style={{ fontSize: '50px', padding: '260px' }}>Welcome to JUVE</h1>
                <Link to="/play">
                  <button style={{ }}>Try a Demo</button>
                </Link>
              </>
            }
          />
        </Routes>
      </Router>
    </div>
  );
}

export default App;

//<div style={{ display: 'flex', flexDirection: 'column', padding: '16px', margin: '1px', alignItems: 'flex-start'}}>
//      <h2 style={{ fontSize: '24px' }}>Welcome to</h2>
//      <h1 style={{ fontSize: '36px', fontWeight: 'bold' }}>JUVE</h1>
//    </div>


//  const [apples, setApples] = useState([]);
//
//  const appleImages = [
//    "https://www.collinsdictionary.com/images/thumb/apple_158989157_250.jpg?version=5.0.17",
//  ];
//
//  const minTimeBetweenApples = 1000; // Minimum time between apple creations (in milliseconds)
//
//  useEffect(() => {
//    const createApple = () => {
//      const currentTime = Date.now();
//
//      if (currentTime - lastAppleCreationTime >= minTimeBetweenApples) {
//        lastAppleCreationTime = currentTime;
//
//        const apple = (
//          <div
//            key={currentTime}
//            className="apple"
//            onMouseOver={() => handleAppleHover(currentTime)}
//          >
//            <img
//              src={appleImages[Math.floor(Math.random() * appleImages.length)]}
//              alt="Apple"
//            />
//          </div>
//        );
//
//        setApples((prevApples) => [...prevApples, apple]);
//      }
//    };
//
//    const handleAppleHover = (time) => {
//      setApples((prevApples) => prevApples.filter((apple) => apple.key !== time));
//    };
//
//    let lastAppleCreationTime = 0;
//    const appleCreationInterval = setInterval(createApple, 1000);
//
//    return () => clearInterval(appleCreationInterval);
//  }, []);
