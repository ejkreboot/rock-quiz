<script>
    import { page } from '$app/stores';
    import { Mountain, Brain, BookOpen } from 'lucide-svelte';
    
    $: currentPath = $page.url.pathname;
</script>

<nav class="site-nav">
    <div class="nav-container">
        <a href="/" class="nav-brand">
            🗿 School Of Rocks (and Minerals)
        </a>
        
        <div class="nav-links">
            <a 
                href="/" 
                class="nav-link {currentPath === '/' ? 'active' : ''}"
                title="Home"
            >
                <Mountain size={18} />
                <span>Home</span>
            </a>
            
            <a 
                href="/quiz" 
                class="nav-link {currentPath === '/quiz' ? 'active' : ''}"
                title="Rock Identification Quiz"
            >
                <Brain size={18} />
                <span>Quiz</span>
            </a>
            
            <a 
                href="/overview" 
                class="nav-link {currentPath === '/overview' ? 'active' : ''}"
                title="Field Guide Reference"
            >
                <BookOpen size={18} />
                <span>Field Guide</span>
            </a>
        </div>
    </div>
</nav>

<style>
    .site-nav {
        background: linear-gradient(135deg, #f5f1eb 0%, #e8ddd4 100%);
        border-bottom: 1px solid #d4c4b0;
        position: sticky;
        top: 0;
        z-index: 100;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    .nav-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 2rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        height: 60px;
    }
    
    .nav-brand {
        font-size: 1.5rem;
        font-weight: 700;
        color: #5d4e37;
        text-decoration: none;
        transition: color 0.2s ease;
    }
    
    .nav-brand:hover {
        color: #8B5A2B;
    }
    
    .nav-links {
        display: flex;
        gap: 1rem;
    }
    
    .nav-link {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        color: #5d4e37;
        text-decoration: none;
        border-radius: 8px;
        transition: all 0.2s ease;
        font-weight: 500;
    }
    
    .nav-link:hover {
        background: rgba(93, 78, 55, 0.1);
        color: #8B5A2B;
    }
    
    .nav-link.active {
        background: rgba(93, 78, 55, 0.15);
        color: #8B5A2B;
        font-weight: 600;
    }
    
    .nav-link span {
        font-size: 0.9rem;
    }
    
    @media (max-width: 768px) {
        .nav-container {
            padding: 0 1rem;
        }
        
        .nav-brand {
            font-size: 1.3rem;
        }
        
        .nav-link span {
            display: none;
        }
        
        .nav-links {
            gap: 0.5rem;
        }
        
        .nav-link {
            padding: 0.5rem;
        }
    }
</style>