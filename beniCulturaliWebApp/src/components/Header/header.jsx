import "./header.css";
import Logo from "../../assets/logo";
import HeroSection from "../Text/HeroSection";

function Header() {
    return (
        <>
            <div className="header-container">
                <header className="top-header">
                    <Logo testoLogo="Magic" logo="./assets/imgHomepage/CENACOLO.ico" />

                    <nav className="top-nav">
                        <ul>
                            <li><a href="#home" aria-label="Home">Home</a></li>
                            <li><a href="#about" aria-label="About">About</a></li>
                            <li><a href="contact" aria-label="Contact">Contact</a></li>
                        </ul>
                    </nav>

                </header>
                
            </div>
        </>
    )
}

export default Header;