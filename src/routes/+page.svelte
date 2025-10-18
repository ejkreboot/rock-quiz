<script>
  import { Mountain, BookOpen, Brain } from 'lucide-svelte';
</script>

<svelte:head>
  <title>Rock & Mineral ID - Learn Geology</title>
  <meta name="description" content="Master rock and mineral identification with interactive tools" />
</svelte:head>

<main class="container">
  <!-- Hero Section -->
  <section class="hero">
    <div class="hero-icon">
      <Mountain size={56} />
    </div>
    <h1>Rock & Mineral ID</h1>
    <p class="tagline">Master geology through interactive learning</p>
  </section>

  <!-- Navigation Cards -->
  <section class="nav-section">
    <a href="/quiz" class="nav-card quiz">
      <Brain size={32} />
      <h2>Practice Quiz</h2>
      <p>Test your identification skills</p>
      <span class="arrow">→</span>
    </a>

    <a href="/overview" class="nav-card guide">
      <BookOpen size={32} />
      <h2>Field Guide</h2>
      <p>Browse rocks & minerals</p>
      <span class="arrow">→</span>
    </a>
  </section>

  <!-- Features -->
  <section class="features">
    <div class="feature">
      <span class="emoji">🔬</span>
      <span>200+ Specimens</span>
    </div>
    <div class="feature">
      <span class="emoji">🧊</span>
      <span>3D Models</span>
    </div>
    <div class="feature">
      <span class="emoji">📚</span>
      <span>Detailed Info</span>
    </div>
  </section>

  <!-- Footer -->
  <footer>
    <p>Perfect for geology students and enthusiasts</p>
  </footer>
</main>

<style>
  :global(body) {
    margin: 0;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background: linear-gradient(135deg, #fefcfb 0%, #f7f3f0 100%);
    min-height: 100vh;
  }

  .container {
    max-width: 800px;
    margin: 0 auto;
    padding: 2rem;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    text-align: center;
  }

  /* Hero */
  .hero {
    color: var(--text);
    margin-bottom: 3rem;
  }

  .hero-icon {
    margin-bottom: 1rem;
    opacity: 0.7;
    color: var(--accent);
  }

  .hero h1 {
    font-size: 3rem;
    font-weight: 800;
    margin: 0 0 0.5rem 0;
    color: var(--title);
  }

  .tagline {
    font-size: 1.2rem;
    margin: 0;
    opacity: 0.8;
    font-weight: 300;
    color: var(--text-muted);
  }

  /* Navigation Cards */
  .nav-section {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1.5rem;
    margin-bottom: 3rem;
  }

  .nav-card {
    background: white;
    padding: 2rem;
    border-radius: 16px;
    text-decoration: none;
    color: inherit;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
  }

  .nav-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 48px rgba(0, 0, 0, 0.15);
  }

  .nav-card.quiz {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
  }

  .nav-card.guide {
    background: linear-gradient(135deg, #f093fb, #f5576c);
    color: white;
  }

  .nav-card h2 {
    font-size: 1.5rem;
    margin: 1rem 0 0.5rem 0;
    font-weight: 600;
  }

  .nav-card p {
    margin: 0 0 1rem 0;
    opacity: 0.9;
  }

  .arrow {
    position: absolute;
    bottom: 1rem;
    right: 1.5rem;
    font-size: 1.2rem;
    font-weight: bold;
    transition: transform 0.3s ease;
  }

  .nav-card:hover .arrow {
    transform: translateX(4px);
  }

  /* Features */
  .features {
    display: flex;
    justify-content: center;
    gap: 2rem;
    margin-bottom: 3rem;
    flex-wrap: wrap;
  }

  .feature {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: var(--text);
    background: rgba(255, 255, 255, 0.8);
    padding: 0.75rem 1.25rem;
    border-radius: 50px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    border: 1px solid rgba(0, 0, 0, 0.05);
    font-weight: 500;
  }

  .emoji {
    font-size: 1.2rem;
  }

  /* Footer */
  footer {
    color: var(--text-muted);
    opacity: 0.8;
    margin-top: auto;
  }

  footer p {
    margin: 0;
    font-size: 0.9rem;
  }

  /* Mobile Responsive */
  @media (max-width: 768px) {
    .container {
      padding: 1.5rem;
    }

    .hero h1 {
      font-size: 2.5rem;
    }

    .tagline {
      font-size: 1.1rem;
    }

    .nav-section {
      grid-template-columns: 1fr;
      gap: 1rem;
    }

    .nav-card {
      padding: 1.5rem;
    }

    .features {
      gap: 1rem;
    }

    .feature {
      padding: 0.5rem 1rem;
      font-size: 0.9rem;
    }
  }

  @media (max-width: 480px) {
    .hero h1 {
      font-size: 2rem;
    }
  }
</style>
