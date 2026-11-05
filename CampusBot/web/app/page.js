export default function Home() {
  return (
    <>
      <nav className="nav">
        <span className="logo">🎓 École Schulz</span>
        <div className="links">
          <a href="#programmes">Programmes</a>
          <a href="#admissions">Admissions</a>
          <a href="#campus">Campus</a>
        </div>
      </nav>

      <header className="hero">
        <h1>Bienvenue à l'École Schulz</h1>
        <p>
          Une question sur les cours, les inscriptions ou la vie du campus ?
          CampusBot vous répond, en bas à droite de l'écran.
        </p>
      </header>

      <main className="cards">
        <article id="programmes">
          <h2>Programmes</h2>
          <p>Découvrez nos formations et leur organisation.</p>
        </article>
        <article id="admissions">
          <h2>Admissions</h2>
          <p>Conditions, calendrier et démarches d'inscription.</p>
        </article>
        <article id="campus">
          <h2>Vie du campus</h2>
          <p>Associations, événements et services aux étudiants.</p>
        </article>
      </main>

      <footer className="footer">© {new Date().getFullYear()} École Schulz</footer>
    </>
  );
}
