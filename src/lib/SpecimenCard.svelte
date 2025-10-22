<script>
    import { Box as Cube } from 'lucide-svelte';
    import { createEventDispatcher } from 'svelte';
    import BookmarkButton from './BookmarkButton.svelte';
    import { bookmarks } from './stores/bookmarks.js';
    
    export let specimen;
    export let thumbnail = null;
    export let hasImages = false;
    
    const dispatch = createEventDispatcher();
    
    function open3DModal() {
        dispatch('open3d', { name: specimen.name });
    }
    
    function openImageCarousel() {
        dispatch('opencarousel', { name: specimen.name });
    }
</script>

<div class="specimen-card">
    <div class="card-header">
        <BookmarkButton 
            rockId={specimen.name}
            isBookmarked={bookmarks.isBookmarked(specimen.name, $bookmarks)}
            onToggle={bookmarks.toggle}
            className="specimen-bookmark"
        />
    </div>
    
    <h3 class="specimen-name">
        <div class="name-content">
            {specimen.name}
            {#if specimen.specimen_type}
                <span class="specimen-type">({specimen.specimen_type})</span>
            {/if}
        </div>
        
        <div class="action-buttons">
            {#if thumbnail}
                <button 
                    class="thumbnail-btn" 
                    on:click={openImageCarousel} 
                    title="View all {specimen.name} specimens"
                    disabled={!hasImages}
                >
                    <img 
                        class="rock-thumb" 
                        src={thumbnail} 
                        alt="{specimen.name} thumbnail" 
                        loading="lazy" 
                    />
                </button>
            {/if}
            
            <button 
                class="model-btn" 
                on:click={open3DModal} 
                title="View 3D Model"
            >
                <Cube size={16} />
            </button>
        </div>
    </h3>
    
    <div class="specimen-description">
        {specimen.description}
    </div>
    
    <div class="specimen-details">
        {#each specimen.details as detail}
            <div class="detail-item">
                <strong>{detail.label}:</strong> 
                <span>{detail.value}</span>
            </div>
        {/each}
    </div>
</div>

<style>
    .specimen-card {
        border: 1px solid #ddd;
        border-radius: 12px;
        padding: 1.5rem;
        background: white;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        position: relative;
    }
    
    .card-header {
        position: absolute;
        top: 12px;
        right: 12px;
        z-index: 10;
    }
    
    :global(.specimen-bookmark) {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(4px);
        border-radius: 6px;
        padding: 4px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    :global(.specimen-bookmark:hover) {
        background: rgba(255, 255, 255, 0.95);
    }
    
    .specimen-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
    }
    
    .specimen-name {
        font-size: 1.3rem;
        margin: 0 40px 1rem 0;
        color: #2c3e50;
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .name-content {
        display: flex;
        align-items: center;
        flex-wrap: wrap;
        gap: 0.5rem;
    }
    
    .action-buttons {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        flex-shrink: 0;
    }
    
    .specimen-type {
        font-size: 0.9rem;
        color: #7f8c8d;
        font-weight: normal;
    }
    
    .thumbnail-btn {
        background: none;
        border: none;
        cursor: pointer;
        padding: 0;
        border-radius: 6px;
        overflow: hidden;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        height: 32px;
        width: 42px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .thumbnail-btn:not(:disabled):hover {
        transform: scale(1.05);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    
    .thumbnail-btn:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }
    
    .rock-thumb {
        width: 100%;
        height: 100%;
        object-fit: cover;
        border-radius: 6px;
        display: block;
    }
    
    .model-btn {
        appearance: none;
        border: 1px solid color-mix(in srgb, var(--accent) 45%, #ccc 55%);
        background: white;
        color: var(--ink);
        padding: 8px;
        border-radius: 6px;
        font-weight: 600;
        cursor: pointer;
        transition: transform 0.04s ease, box-shadow 0.15s ease, border-color 0.15s ease, background 0.15s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        height: 32px;
        width: 32px;
    }
    
    .model-btn:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        border-color: var(--accent);
        background: #f8f9fa;
    }
    
    .specimen-description {
        font-size: 1rem;
        line-height: 1.5;
        color: #34495e;
        margin-bottom: 1rem;
        font-style: italic;
    }
    
    .specimen-details {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }
    
    .detail-item {
        font-size: 0.9rem;
        line-height: 1.4;
        color: #555;
    }
    
    .detail-item strong {
        color: #2c3e50;
        margin-right: 0.5rem;
    }
    
    .detail-item span {
        font-style: italic;
    }
</style>