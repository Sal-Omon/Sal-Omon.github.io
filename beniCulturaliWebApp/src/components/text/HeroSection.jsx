export default function HeroSection({ titolo, sottotitolo, sfondo }) {
    return <div className="hero-section">
        <img className="sfondo" src={sfondo} alt="sfondo" />
        <div className="hero-content">
            <h1>{titolo}</h1>
            <h2>{sottotitolo}</h2>
        </div>
    </div>

}