<script>
    import { createEventDispatcher } from 'svelte';
    import { ChevronLeft, ChevronRight } from 'lucide-svelte';
    
    export let name;
    export let images = [];
    
    const dispatch = createEventDispatcher();
    let currentIndex = 0;
    
    function nextImage() {
        currentIndex = (currentIndex + 1) % images.length;
    }
    
    function prevImage() {
        currentIndex = (currentIndex - 1 + images.length) % images.length;
    }
    
    function goToImage(index) {
        currentIndex = index;
    }
    
    function handleKeydown(event) {
        if (event.key === 'ArrowLeft') {
            prevImage();
        } else if (event.key === 'ArrowRight') {
            nextImage();
        } else if (event.key === 'Escape') {
            dispatch('close');
        }
    }
</script>

<svelte:window on:keydown={handleKeydown} />

<div class="carousel-container">
    {#if images.length > 0}
        <div class="carousel-main">
            <button class="nav-btn prev" on:click={prevImage} disabled={images.length <= 1} title="Previous image">
                <ChevronLeft size={32} />
            </button>
            
            <div class="image-container">
                <img 
                    src={images[currentIndex]} 
                    alt="{name} specimen {currentIndex + 1}" 
                    class="main-image"
                />
                <div class="image-counter">
                    {currentIndex + 1} of {images.length}
                </div>
            </div>
            
            <button class="nav-btn next" on:click={nextImage} disabled={images.length <= 1} title="Next image">
                <ChevronRight size={32} />
            </button>
        </div>
        
        {#if images.length > 1}
            <div class="thumbnail-strip">
                {#each images as image, index}
                    <button 
                        class="thumbnail {index === currentIndex ? 'active' : ''}"
                        on:click={() => goToImage(index)}
                        title="View specimen {index + 1}"
                    >
                        <img src={image} alt="{name} specimen {index + 1}" />
                    </button>
                {/each}
            </div>
        {/if}
    {:else}
        <div class="no-images">
            <p>No specimen images available for {name}</p>
        </div>
    {/if}
</div>

<style>
    .carousel-container {
        display: flex;
        flex-direction: column;
        height: 100%;
        background: white;
    }
    
    .carousel-main {
        display: flex;
        align-items: center;
        background: #f8f9fa;
        flex: 1;
        min-height: 550px;
    }
    
    .nav-btn {
        background: rgba(255, 255, 255, 0.9);
        border: none;
        cursor: pointer;
        padding: 1rem;
        margin: 0 1rem;
        border-radius: 50%;
        transition: all 0.2s;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    .nav-btn:hover:not(:disabled) {
        background: white;
        transform: scale(1.05);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    
    .nav-btn:disabled {
        opacity: 0.3;
        cursor: not-allowed;
    }
    
    .image-container {
        flex: 1;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        position: relative;
        padding: 2rem;
    }
    
    .main-image {
        max-width: 100%;
        max-height: 500px;
        object-fit: contain;
        border-radius: 8px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
        background: white;
    }
    
    .image-counter {
        position: absolute;
        bottom: 1rem;
        right: 1rem;
        background: rgba(0, 0, 0, 0.7);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 500;
    }
    
    .thumbnail-strip {
        display: flex;
        gap: 0.5rem;
        padding: 1rem 1.5rem;
        background: white;
        border-top: 1px solid #e9ecef;
        overflow-x: auto;
        scrollbar-width: thin;
    }
    
    .thumbnail {
        flex-shrink: 0;
        width: 80px;
        height: 60px;
        border: 2px solid transparent;
        border-radius: 6px;
        overflow: hidden;
        cursor: pointer;
        transition: all 0.2s;
        background: none;
        padding: 0;
    }
    
    .thumbnail:hover {
        border-color: #8B5A2B;
        transform: scale(1.05);
    }
    
    .thumbnail.active {
        border-color: #8B5A2B;
        box-shadow: 0 0 0 2px rgba(139, 90, 43, 0.2);
    }
    
    .thumbnail img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    
    .no-images {
        padding: 3rem;
        text-align: center;
        color: #6c757d;
    }
    
    .no-images p {
        font-size: 1.1rem;
        margin: 0;
    }
</style>