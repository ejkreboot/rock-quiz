<script>
    import { onMount } from 'svelte';
    import { bookmarks } from '$lib/stores/bookmarks.js';
    import rockMetadata from '$lib/rock_metadata.json';
    import rocksManifest from '$lib/rocks-manifest.json';
    import Modal from '$lib/Modal.svelte';
    import RockModel from '$lib/RockModel.svelte';
    import ImageCarousel from '$lib/ImageCarousel.svelte';
    import SpecimenCard from '$lib/SpecimenCard.svelte';
    import Navigation from '$lib/Navigation.svelte';
    import { Star, Trash2 } from 'lucide-svelte';
    
    let modalOpen = false;
    let modalComponent = null;
    let modalProps = {};
    let modalTitle = "";
    
    // Convert object-based metadata to array format for compatibility
    const specimens = Object.values(rockMetadata);
    
    // Reactive bookmarked specimens
    $: bookmarkedSpecimens = specimens.filter(specimen => 
        bookmarks.isBookmarked(specimen.name, $bookmarks)
    );
    
    // Group bookmarked specimens by category
    $: groupedBookmarkedSpecimens = bookmarkedSpecimens.reduce((groups, specimen) => {
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
    
    function clearAllBookmarks() {
        if (confirm('Are you sure you want to clear all bookmarks? This cannot be undone.')) {
            bookmarks.clear();
        }
    }
    
    onMount(() => {
        document.title = "Review Bookmarked Rocks - Geology Study Guide";
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
    <header class="review-header">
        <div class="header-content">
            <h1>
                <Star size={32} fill="#ffd700" color="#ffd700" />
                Review Collection
            </h1>
            <p class="subtitle">
                {#if $bookmarks.size === 0}
                    You haven't bookmarked any rocks yet. Visit the quiz or field guide to start bookmarking!
                {:else if $bookmarks.size === 1}
                    You have 1 rock bookmarked for review.
                {:else}
                    You have {$bookmarks.size} rocks bookmarked for review.
                {/if}
            </p>
        </div>
        
        {#if $bookmarks.size > 0}
            <button class="clear-btn" on:click={clearAllBookmarks}>
                <Trash2 size={16} />
                Clear All
            </button>
        {/if}
    </header>
    
    {#if $bookmarks.size === 0}
        <div class="empty-state">
            <div class="empty-icon">
                <Star size={64} color="#ccc" />
            </div>
            <h2>No bookmarked rocks yet</h2>
            <p>Start bookmarking rocks you want to review by clicking the star icon on flashcards or in the field guide.</p>
            <div class="empty-actions">
                <a href="/quiz" class="action-btn primary">Start Quiz</a>
                <a href="/overview" class="action-btn">Browse Field Guide</a>
            </div>
        </div>
    {:else}
        <section class="specimens-section">
            {#each categoryOrder as category}
                {#if groupedBookmarkedSpecimens[category]}
                    <details class="category-section" open>
                        <summary class="category-title">
                            {getCategoryIcon(category)} {category}
                            <span class="category-count">({groupedBookmarkedSpecimens[category].length})</span>
                        </summary>
                        <div class="specimens-grid">
                            {#each groupedBookmarkedSpecimens[category] as specimen}
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
    {/if}
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
    
    .review-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 3rem;
        padding: 2rem;
        background: linear-gradient(135deg, #fff8e1 0%, #f4f1eb 100%);
        border-radius: 16px;
        border: 2px solid #ffd700;
        gap: 2rem;
    }
    
    .header-content h1 {
        font-size: 2.5rem;
        margin: 0 0 0.5rem 0;
        color: #5d4e37;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .subtitle {
        font-size: 1.1rem;
        color: #666;
        margin: 0;
        line-height: 1.5;
    }
    
    .clear-btn {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.75rem 1rem;
        background: #dc3545;
        color: white;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        font-weight: 600;
        transition: all 0.2s ease;
        white-space: nowrap;
    }
    
    .clear-btn:hover {
        background: #c82333;
        transform: translateY(-1px);
    }
    
    .empty-state {
        text-align: center;
        padding: 4rem 2rem;
        color: #666;
    }
    
    .empty-icon {
        margin-bottom: 1.5rem;
        opacity: 0.5;
    }
    
    .empty-state h2 {
        font-size: 1.5rem;
        margin-bottom: 1rem;
        color: #5d4e37;
    }
    
    .empty-state p {
        font-size: 1.1rem;
        margin-bottom: 2rem;
        max-width: 500px;
        margin-left: auto;
        margin-right: auto;
        line-height: 1.6;
    }
    
    .empty-actions {
        display: flex;
        gap: 1rem;
        justify-content: center;
        flex-wrap: wrap;
    }
    
    .action-btn {
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        text-decoration: none;
        font-weight: 600;
        transition: all 0.2s ease;
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .action-btn.primary {
        background: linear-gradient(135deg, #8B5A2B 0%, #A0522D 40%, #CD853F 100%);
        color: white;
    }
    
    .action-btn:not(.primary) {
        background: white;
        color: #5d4e37;
        border: 2px solid #5d4e37;
    }
    
    .action-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    
    .specimens-section {
        margin-top: 2rem;
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
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .category-title:hover {
        background: linear-gradient(135deg, #e9ecef 0%, #dee2e6 100%);
    }
    
    .category-count {
        font-size: 1rem;
        color: #666;
        font-weight: 500;
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
        
        .review-header {
            flex-direction: column;
            align-items: stretch;
            gap: 1rem;
        }
        
        .header-content h1 {
            font-size: 2rem;
        }
        
        .clear-btn {
            align-self: flex-end;
        }
        
        .specimens-grid {
            grid-template-columns: 1fr;
            padding: 1rem;
        }
        
        .empty-actions {
            flex-direction: column;
            align-items: center;
        }
        
        .action-btn {
            width: 200px;
            justify-content: center;
        }
    }
</style>