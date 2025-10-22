<script>
    import '../../lib/styles/geology.css';
    import { onMount } from 'svelte';
    import rocksManifest from '$lib/rocks-manifest.json';
    import rockMetadata from '$lib/rock_metadata.json';
    import Modal from '$lib/Modal.svelte';
    import RockModel from '$lib/RockModel.svelte';
    import ImageCarousel from '$lib/ImageCarousel.svelte';
    import SpecimenCard from '$lib/SpecimenCard.svelte';
    import Navigation from '$lib/Navigation.svelte';
    import { bookmarks } from '$lib/stores/bookmarks.js';

    let modalOpen = false;
    let modalComponent = null;
    let modalProps = {};
    let modalTitle = "";
    
    // Convert object-based metadata to array format for compatibility
    const specimens = Object.values(rockMetadata);

    // Group specimens by category
    const groupedSpecimens = specimens.reduce((groups, specimen) => {
        const category = specimen.category;
        if (!groups[category]) {
            groups[category] = [];
        }
        groups[category].push(specimen);
        return groups;
    }, {});

    function open3DModal(event) {
        const rockName = event.detail.name;
        const rockData = rockMetadata[rockName];
        if (rockData && rockData.model_3d) {
            modalComponent = RockModel;
            modalProps = { name: rockData.name, ...rockData.model_3d };
            modalTitle = `3D Model of ${rockData.name}`;
            modalOpen = true;
        }
    }

    function openImageCarousel(event) {
        const rockName = event.detail.name;
        const images = getRockImages(rockName);
        if (images && images.length > 0) {
            modalComponent = ImageCarousel;
            modalProps = { name: rockName, images: images };
            modalTitle = `${rockName} Specimens`;
            modalOpen = true;
        }
    }

    function getRockThumbnail(name) {
        if (!rocksManifest[name]) return null;
        return rocksManifest[name][0];
    }

    function getRockImages(name) {
        return rocksManifest[name] || [];
    }

    function hasImages(name) {
        return rocksManifest[name] && rocksManifest[name].length > 0;
    }

    onMount(() => {
        document.title = "Geology Field Guide - Minerals & Rocks Reference";
        // Load bookmarks
        bookmarks.load();
    });

    // Category order for display
    const categoryOrder = [
        'Minerals',
        'Igneous Rocks', 
        'Sedimentary Rocks',
        'Metamorphic Rocks'
    ];

    function getCategoryIcon(category) {
        switch (category) {
            case 'Minerals': return '🧪';
            case 'Igneous Rocks': return '🌋';
            case 'Sedimentary Rocks': return '🏔️';
            case 'Metamorphic Rocks': return '⚡';
            default: return '🪨';
        }
    }
</script>

<Navigation />

<div class="wrap">
    <header class="intro-section">
        <h1>🗿 <span class="gradient-text">Geology Field Guide</span></h1>
        <p class="intro-text">
            Comprehensive reference for minerals, igneous, sedimentary, and metamorphic rocks. See below for 
            classification methods. Below that is a full catalog of rock 
            types and their characteristics.
        </p>
    </header>
    
    <!-- ========== Rock ID Helper (styled for your theme) ========== -->
    <section id="rock-id" class="wrap rid">
        <header class="rid-hero">
            <h1>🧭 How to Identify a Rock</h1>
            <p class="hint">A quick, systematic approach + an interactive trait picker to narrow possibilities.</p>
        </header>

        <div class="rid-steps">
            <div class="rid-step">
                <h3>1. Check the Texture</h3>
                <p><strong>Glassy:</strong> Obsidian, volcanic glass<br>
                <strong>Very fine (aphanitic):</strong> Basalt, Rhyolite, Chert<br>
                <strong>Coarse (phaneritic):</strong> Granite, Gabbro<br>
                <strong>Vesicular (holes):</strong> Pumice, Scoria<br>
                <strong>Layered/Banded:</strong> Gneiss, Shale</p>
            </div>
            
            <div class="rid-step">
                <h3>2. Test Hardness</h3>
                <p><strong>Fingernail (2.5):</strong> Talc, Gypsum<br>
                <strong>Copper penny (3.5):</strong> Calcite, some micas<br>
                <strong>Steel knife (5.5):</strong> Most feldspars<br>
                <strong>Glass (5.5-6):</strong> Quartz scratches glass<br>
                <strong>Steel file (6.5):</strong> Garnet, some quartz</p>
            </div>
            
            <div class="rid-step">
                <h3>3. Observe Color & Luster</h3>
                <p><strong>Metallic:</strong> Galena, Magnetite, Hematite<br>
                <strong>Vitreous (glassy):</strong> Quartz, Feldspar<br>
                <strong>Pearly:</strong> Muscovite mica<br>
                <strong>Earthy/Dull:</strong> Kaolinite, some Hematite</p>
            </div>
            
            <div class="rid-step">
                <h3>4. Check Special Properties</h3>
                <p><strong>Magnetic:</strong> Magnetite<br>
                <strong>Reacts with acid:</strong> Calcite, Limestone<br>
                <strong>Flexible sheets:</strong> Mica<br>
                <strong>Salty taste:</strong> Halite<br>
                <strong>Conchoidal fracture:</strong> Quartz, Obsidian</p>
            </div>
        </div>
    </section>

    <!-- ========== Specimens organized by category ========== -->
    <section class="specimens-section">
        <h2>Specimen Collection</h2>
        <p class="section-description">Click on specimen photos to view all available images, or use the 3D button to view interactive models.</p>
        
        {#each categoryOrder as category}
            {#if groupedSpecimens[category]}
                <details class="category-section" open>
                    <summary class="category-title">
                        {getCategoryIcon(category)} {category}
                    </summary>
                    <div class="specimens-grid">
                        {#each groupedSpecimens[category] as specimen}
                            <SpecimenCard 
                                {specimen}
                                thumbnail={getRockThumbnail(specimen.name)}
                                hasImages={hasImages(specimen.name)}
                                on:open3d={open3DModal}
                                on:opencarousel={openImageCarousel}
                            />
                        {/each}
                    </div>
                </details>
            {/if}
        {/each}
    </section>
</div>

<Modal
    bind:open={modalOpen}
    component={modalComponent}
    props={modalProps}
    title={modalTitle}
    on:close={() => modalOpen = false}
/>

<style>
    .wrap {
        max-width: 1200px;
        margin: 0 auto;
        padding: 2rem;
    }

    .intro-section {
        text-align: center;
        margin-bottom: 3rem;
        padding: 2rem;
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 16px;
    }

    .intro-section h1 {
        font-size: 3rem;
        margin-bottom: 1rem;
        color: #2c3e50;
    }

    .gradient-text {
        background: linear-gradient(135deg, #556B2F 0%, #6B8E23 40%, #8FBC8F 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .intro-text {
        font-size: 1.2rem;
        color: #555;
        max-width: 600px;
        margin: 0 auto;
        line-height: 1.6;
    }

    /* Rock ID Helper Styles */
    .rid {
        margin: 3rem 0;
        padding: 2rem;
        background: linear-gradient(135deg, #f5f1eb 0%, #e8ddd4 100%);
        border-radius: 16px;
        color: #5d4e37;
    }

    .rid-hero {
        text-align: center;
        margin-bottom: 2rem;
    }

    .rid-hero h1 {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        color: #5d4e37;
    }

    .hint {
        font-size: 1.1rem;
        opacity: 0.8;
        color: #5d4e37;
    }

    .rid-steps {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
        gap: 2rem;
        margin-top: 2rem;
    }

    .rid-step {
        background: rgba(93, 78, 55, 0.08);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid rgba(93, 78, 55, 0.15);
    }

    .rid-step h3 {
        font-size: 1.3rem;
        margin-bottom: 1rem;
        color: #5d4e37;
    }

    .rid-step p {
        line-height: 1.6;
        font-size: 0.95rem;
    }

    /* Specimens Section */
    .specimens-section {
        margin-top: 3rem;
    }

    .specimens-section h2 {
        font-size: 2.5rem;
        text-align: center;
        margin-bottom: 1rem;
        color: #2c3e50;
    }

    .section-description {
        text-align: center;
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 2rem;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }

    .category-section {
        margin-bottom: 3rem;
        border: 1px solid #e9ecef;
        border-radius: 12px;
        overflow: hidden;
        background: white;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }

    .category-title {
        font-size: 1.5rem;
        font-weight: 700;
        padding: 1.5rem 2rem;
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        cursor: pointer;
        transition: background-color 0.2s ease;
        color: #2c3e50;
        border-bottom: 1px solid #dee2e6;
    }

    .category-title:hover {
        background: linear-gradient(135deg, #e9ecef 0%, #dee2e6 100%);
    }

    .specimens-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(500px, 1fr));
        gap: 1.5rem;
        padding: 2rem;
    }

    @media (max-width: 768px) {
        .wrap {
            padding: 1rem;
        }
        
        .intro-section h1 {
            font-size: 2rem;
        }
        
        .rid-steps {
            grid-template-columns: 1fr;
        }
        
        .specimens-grid {
            grid-template-columns: 1fr;
            padding: 1rem;
        }
    }
</style>