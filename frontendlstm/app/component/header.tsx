import './header.css';

export default function Header() {
  return (
    <header className="site-header">
      <a className="brand" href="/" aria-label="NextWord AI home">
        <span className="brand-mark">N<span>+</span></span>
        <span className="brand-text">nextword<span className="brand-light">.ai</span></span>
      </a>
      <div className="header-caption"><span className="header-dot" /> WORD PREDICTION STUDIO</div>
      <a className="header-link" href="https://github.com/amandx36/N3xtWord-LstmAi" target="_blank" rel="noreferrer">
        GitHub <span aria-hidden="true"></span>
      </a>
    </header>
  );
}
