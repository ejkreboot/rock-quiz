import { writable } from 'svelte/store';
import { browser } from '$app/environment';

// Create a writable store for bookmarked rocks
function createBookmarkStore() {
  // Initialize with empty set, will be loaded from localStorage in browser
  const { subscribe, set, update } = writable(new Set());

  return {
    subscribe,
    
    // Load bookmarks from localStorage
    load: () => {
      if (browser) {
        try {
          const saved = localStorage.getItem('bookmarkedRocks');
          if (saved) {
            const bookmarkArray = JSON.parse(saved);
            set(new Set(bookmarkArray));
          }
        } catch (e) {
          console.warn('Failed to load bookmarks from localStorage:', e);
        }
      }
    },
    
    // Save bookmarks to localStorage
    save: (bookmarks) => {
      if (browser) {
        try {
          localStorage.setItem('bookmarkedRocks', JSON.stringify([...bookmarks]));
        } catch (e) {
          console.warn('Failed to save bookmarks to localStorage:', e);
        }
      }
    },
    
    // Toggle bookmark for a rock
    toggle: (rockId) => {
      update(bookmarks => {
        const newBookmarks = new Set(bookmarks);
        if (newBookmarks.has(rockId)) {
          newBookmarks.delete(rockId);
        } else {
          newBookmarks.add(rockId);
        }
        
        // Save to localStorage
        if (browser) {
          try {
            localStorage.setItem('bookmarkedRocks', JSON.stringify([...newBookmarks]));
          } catch (e) {
            console.warn('Failed to save bookmarks to localStorage:', e);
          }
        }
        
        return newBookmarks;
      });
    },
    
    // Check if a rock is bookmarked
    isBookmarked: (rockId, bookmarks) => {
      return bookmarks.has(rockId);
    },
    
    // Get count of bookmarked rocks
    getCount: (bookmarks) => {
      return bookmarks.size;
    },
    
    // Clear all bookmarks
    clear: () => {
      set(new Set());
      if (browser) {
        try {
          localStorage.removeItem('bookmarkedRocks');
        } catch (e) {
          console.warn('Failed to clear bookmarks from localStorage:', e);
        }
      }
    }
  };
}

export const bookmarks = createBookmarkStore();