import logo from './logo.svg';
import './App.css';
import cat from "./cat standing.png"

function App() {
  return (
    <div className="App">
      <div class = "container">
        <h1>About Me</h1>
        <p>
            Hello everyone, 
            My name is Diego Ozuna, I am a senior here at CSUSB and will graduate in December 2024.
            I am majoring in Computer Science with a minor in Mathematics. Since transfering, I have been on the Dean's
            List. I want to work closely with Machine Learning and AI which is why I am interested mostly in the field of Data Science.
        </p>
        <p>
            My hobbies are film photography and video games. I like to play first-person shooters, MOBAs,
            and some survival games. My interest in photography comes from a class I took in highschool.
        </p>
        <p>
            If you have questions about stuff in Comp Sci or Math I will try to help, as helping others also helps me. :)
        </p>

        <div class="highlightGIT">
            <a href="https://github.com/DiegoOzuna/Platform-Computing">My GITHUB Page</a>
        </div>

        <div>
            <p>Here is a list of my classes below...</p>
            <ol class = "listClass">
                <li>CSE 4310 : Algorithm Analysis</li>
                <li>CSE 4500 : Platforming Computing</li>
                <li>CSE 5000 : Formal Languages and Automata</li>
                <li>CSE 5120 : Intro Artificial Intelligence</li>
                <li>CSE 5250 : Parallel Algorithms</li>
                <li>CSE 5953 : Independent Study</li>
            </ol>
            <p>Two of my classes are online, the others are in person Monday and Wednesday.
            </p>
        </div>
        <img src={cat} alt="cat" class="center"/>


    </div>
    </div>
  );
}

export default App;
