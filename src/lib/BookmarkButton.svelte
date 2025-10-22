<script>
  import { Star } from 'lucide-svelte';
  
  export let rockId;
  export let isBookmarked = false;
  export let onToggle;
  export let size = 22;
  export let className = '';
</script>

<button 
  class="bookmark-btn {className} {isBookmarked ? 'bookmarked' : ''}"
  on:click={(e) => {
    e.stopPropagation(); // Prevent triggering card flip or other actions
    onToggle(rockId);
  }}
  aria-label={isBookmarked ? 'Remove from review' : 'Mark for review'}
  title={isBookmarked ? 'Remove from review' : 'Mark for review'}
>
  <Star size={size} fill={isBookmarked ? 'currentColor' : 'none'} />
</button>

<style>
  .bookmark-btn {
    background: none;
    border: none;
    cursor: pointer;
    color: #999;
    transition: all 0.2s ease;
    padding: 8px;
    border-radius: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.1));
  }
  
  .bookmark-btn:hover {
    color: #ffd700;
    background-color: rgba(0, 0, 0, 0.05);
    transform: scale(1.1);
  }
  
  .bookmark-btn.bookmarked {
    color: #ffd700;
  }
  
  .bookmark-btn:active {
    transform: scale(0.95);
  }
  
  .bookmark-btn:focus {
    outline: 2px solid #ffd700;
    outline-offset: 2px;
  }
</style>