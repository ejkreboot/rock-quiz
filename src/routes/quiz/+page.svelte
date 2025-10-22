<script>
  import { onMount } from 'svelte';
  import Svelecte from 'svelecte';
  import {  Box as Cube } from 'lucide-svelte'; // 3D cube icon
  import Modal from '$lib/Modal.svelte';
  import RockInfo from '$lib/RockInfo.svelte';
  import RockModel from '$lib/RockModel.svelte';
  import Navigation from '$lib/Navigation.svelte';
  import BookmarkButton from '$lib/BookmarkButton.svelte';
  import { bookmarks } from '$lib/stores/bookmarks.js';
  import rockMetadata from '$lib/rock_metadata.json';
  
  // Data state
  let manifest = {};
  let classes = [];
  let current = null;      // { url, label }
  let revealed = false;
  let chosenLabels = [];
  
  // Deck management
  let deck = [];           // fixed practice set = up to 5 per class
  let drawPile = [];       // shuffled copy we draw from (no repeats)
  let selectedList = [];   // Svelecte's current selection (array)
  
  // UI state
  let ready = false;       // flips true after manifest loads
  let modalOpen = false;
  let modalComponent = null;
  let modalProps = {};
  let modalTitle ="";
  
  // Credits data
  let creditURL = null;    // source link for current image
  let creditHost = null;   // pretty host text (e.g., geologysuperstore.com)
  let creditsMap = new Map();
  
  const PER_CLASS = 5;
  const ROCKS_PREFIX = "/rocks/";
  
  onMount(async () => {
    const res = await fetch("/rocks-manifest.json");
    manifest = await res.json();
    classes = Object.keys(manifest).sort((a, b) => a.localeCompare(b));
    
    try {
      const c = await fetch("/rocks/credits.json");
      const items = await c.json();
      items.forEach(({ file, url }) => {
        creditsMap.set((file || "").replace(/^\/+/, ""), url);
      });
    } catch (e) {
      console.warn("credits.json not found or invalid:", e);
    }
    
    // Load bookmarks
    bookmarks.load();
    
    ready = true;
    buildPracticeDeck();
    nextImage();
  });
  
  function onSelectionChange() {
    // Filter out any category markers that might have been selected
    const originalLength = selectedList ? selectedList.length : 0;
    selectedList = (selectedList || []).filter(item => {
      const itemStr = item ? item.toString() : '';
      return itemStr && 
             !itemStr.startsWith('__CATEGORY_') && 
             !itemStr.includes('__CATEGORY_') &&
             itemStr !== 'undefined' &&
             itemStr.trim().length > 0;
    });
    
    // Debug log if categories were filtered out
    if (originalLength !== selectedList.length) {
      console.log('Filtered out invalid selections');
    }
    
    // Force a new array reference so Svelte definitely reacts
    selectedList = [...selectedList];
    rebuildFromSelection();
  }
  
  
  function sampleUpTo(arr, n) {
    // partial Fisher–Yates: sample n without replacement
    const a = arr.slice();
    const k = Math.min(n, a.length);
    for (let i = 0; i < k; i++) {
      const j = i + Math.floor(Math.random() * (a.length - i));
      [a[i], a[j]] = [a[j], a[i]];
    }
    return a.slice(0, k);
  }
  
  function shuffleInPlace(a) {
    for (let i = a.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
  }
  
  function getRockCategory(rockName) {
    const rockData = rockMetadata[rockName];
    if (rockData) {
      if (rockData.rock_type === 'igneous') return 'Igneous Rocks';
      if (rockData.rock_type === 'sedimentary') return 'Sedimentary Rocks';
      if (rockData.rock_type === 'metamorphic') return 'Metamorphic Rocks';
    }
    return 'Minerals';
  }

  function organizeClassesByCategory() {
    const categories = {
      'Minerals': [],
      'Igneous Rocks': [],
      'Sedimentary Rocks': [],
      'Metamorphic Rocks': []
    };
    
    // Organize rocks by category
    classes.forEach(rockName => {
      const category = getRockCategory(rockName);
      categories[category].push(rockName);
    });
    
    // Build flat array with category markers
    const organizedOptions = [];
    Object.entries(categories).forEach(([category, rocks]) => {
      if (rocks.length > 0) {
        // Add category divider
        organizedOptions.push(`__CATEGORY_${category}__`);
        // Add sorted rocks in this category
        rocks.sort((a, b) => a.localeCompare(b)).forEach(rock => {
          organizedOptions.push(rock);
        });
      }
    });
    
    return organizedOptions;
  }

  function buildPracticeDeck(labels = classes) {
    const tmp = [];
    for (const label of labels.sort((a,b)=>a.localeCompare(b))) {
      const imgs = manifest[label] ?? [];
      const picks = sampleUpTo(imgs, PER_CLASS);
      for (const url of picks) tmp.push({ url, label });
    }
    deck = tmp;
    drawPile = shuffleInPlace(deck.slice());
  }
  
  // Computed properties
  $: {
    // Filter selectedList to remove category markers
    const filteredSelected = (selectedList || [])
      .filter(lbl => {
        const lblStr = lbl ? lbl.toString() : '';
        return lblStr && 
               !lblStr.startsWith('__CATEGORY_') && 
               !lblStr.includes('__CATEGORY_') &&
               lblStr !== 'undefined' &&
               lblStr.trim().length > 0 &&
               (manifest[lbl]?.length ?? 0) > 0;
      });
    
    // If we have valid selections after filtering, use them; otherwise use all classes
    chosenLabels = (filteredSelected.length > 0 ? filteredSelected : classes)
      .filter(lbl => (manifest[lbl]?.length ?? 0) > 0)
      .sort((a, b) => a.localeCompare(b));
  }
  
  $: currentRockDef = rockMetadata[current?.label];
  
  $: organizedOptions = ready ? organizeClassesByCategory() : [];
  
  function reshuffleDeck() {
    if (!ready) return;
    buildPracticeDeck(chosenLabels);
    current = null;
    revealed = false;
    nextImage();
  }
  
  // Alias for consistency
  const rebuildFromSelection = reshuffleDeck;
  
  function nextImage() {
    if (!drawPile.length) {
      drawPile = shuffleInPlace(deck.slice());
    }
    const card = drawPile.pop();
    if (!card) return;
    current = card;
    revealed = false;
    
    // NEW: look up credit for this image
    const key = keyFromImageURL(current.url);
    const url = creditsMap.get(key) || null;
    creditURL = url;
    creditHost = url ? new URL(url).hostname.replace(/^www\./, "") : null;
  }
  
  function reveal() {
    revealed = true;
  }
  

  
  // normalize "/rocks/Andesite/Andesite_001.png?x=y" -> "Andesite/Andesite_001.png"
  function keyFromImageURL(u) {
    const clean = (u || "").split("?")[0].split("#")[0];
    const idx = clean.lastIndexOf(ROCKS_PREFIX);
    const tail = idx !== -1 ? clean.slice(idx + ROCKS_PREFIX.length) : clean.replace(/^\//, "");
    return tail;
  }
  
  
  function openInfo() {
    if (!currentRockDef) return;
    modalComponent = RockInfo;
    modalProps = { info: currentRockDef };
    modalTitle = "Rock type details";
    modalOpen = true;
  }
  
  function openModel() {
    if (!currentRockDef?.model_3d) return;
    console.log("Opening model for", currentRockDef.name);
    modalComponent = RockModel;
    modalTitle = `3D Model of ${currentRockDef.name}`;
    modalProps = { name: currentRockDef.name, ...currentRockDef.model_3d };
    modalOpen = true;
  }
  
  // 18×18, rounded box. Strokes use currentColor so you can style via CSS.
  const svg_empty = `
  <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18"
      viewBox="0 0 18 18" aria-hidden="true" focusable="false">
    <rect x="2.25" y="2.25" width="13.5" height="13.5" rx="2.5" ry="2.5"
          fill="none" stroke="currentColor" stroke-width="1.5"/>
  </svg>`;
  
  const svg_checked = `
  <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18"
      viewBox="0 0 18 18" aria-hidden="true" focusable="false">
    <rect x="2.25" y="2.25" width="13.5" height="13.5" rx="2.5" ry="2.5"
          fill="none" stroke="currentColor" stroke-width="1.5"/>
    <path d="M5.2 9.4l2.3 2.3L12.8 6.6"
          fill="none" stroke="currentColor" stroke-width="2"
          stroke-linecap="round" stroke-linejoin="round"/>
  </svg>`;
  
  function svgRenderer(opt, _isSelected, _input) {
    // Check if this is a category divider
    if (opt.text && opt.text.startsWith('__CATEGORY_')) {
      const categoryName = opt.text.replace('__CATEGORY_', '').replace('__', '');
      return `<div class="sv-category-divider" onclick="return false;" onmousedown="return false;">
        <span>${categoryName}</span>
      </div>`;
    }
    
    return `<div class="sv-inlined">
      ${opt.$selected ? svg_checked : svg_empty}
      <span>${opt.text}</span>
    </div>`;
    }
    
  </script>

<Navigation />
  
  <div class="wrap">
    <header class="app-header">
      <h1>Rock ID Practice</h1>
    </header>
    <div class="toolbar">
      <button class="btn" on:click={nextImage}>Next Image</button>
      {#if !revealed}
        <span class="hint">(Click Image For Answer)</span>
      {:else}
        <div class="answer">{current?.label}</div>
        <button
          class="btn"
          on:click={openModel}
          disabled={currentRockDef?.model_3d?.link==""}
          aria-label="View 3D model"
        >
          <Cube size={18} />
        </button>
      <button class="btn" on:click={openInfo}>Info</button>
    {/if}
<!--    <button class="btn right" on:click={reshuffleDeck}>Shuffle Deck</button>-->
  </div>
  
  {#if current}
    <button
      class="card"
      on:click={reveal}
      aria-label="Show the rock type for this image"
      title="Click to reveal"
    >
      <div class="card-header">
        <BookmarkButton 
          rockId={current.label}
          isBookmarked={bookmarks.isBookmarked(current.label, $bookmarks)}
          onToggle={bookmarks.toggle}
          className="card-bookmark"
        />
      </div>
      <div class="rock-frame">
        <img src={current.url} alt="Rock sample" loading="eager" />
      </div>
    </button>
  {/if}
  
    <div class="credit">
      Image may be subject to copyright. Source:
      {#if creditURL}
         <a href={creditURL} target="_blank" rel="noopener noreferrer">{creditHost}</a>
      {:else}
        Unknown.
      {/if}
    </div>
  
  <div class="filter-section">
    <span class="filter-label">Filter rocks:</span>
    <div class="filter-select">
      <Svelecte
        multiple 
        options={organizedOptions}        
        closeOnSelect={false} 
        bind:value={selectedList}
        renderer={svgRenderer} 
        collapseSelection="always" 
        clearable 
        keepSelectionInList={true} 
        onChange={onSelectionChange}  
        searchProps={{skipSort: true}}
        disabledField="__CATEGORY_"
        disableHighlight={(opt) => opt && opt.toString().startsWith('__CATEGORY_')}
      />
    </div>
  </div>

</div>

<!-- Modal -->

<Modal
  bind:open={modalOpen}
  component={modalComponent}
  props={modalProps}
  title={modalTitle}
>
  <div slot="footer" class="">
    <button class="btn" on:click={() => (modalOpen = false)}>
      Close
    </button>
  </div>
</Modal>

<style>
  .app-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
    flex-wrap: wrap;
    gap: 1rem;
  }
  
  .app-header h1 {
    margin: 0;
  }
  
  .overview-link {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 0.75rem;
    background: linear-gradient(135deg, var(--accent), color-mix(in srgb, var(--accent) 80%, white 20%));
    color: white;
    text-decoration: none;
    border-radius: 8px;
    font-weight: 600;
    font-size: 0.9rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
  }
  
  .overview-link:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    text-decoration: none;
  }
  
  .overview-link:active {
    transform: translateY(0);
  }

  .filter-section {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-top: 1rem;
    flex-wrap: wrap;
  }
  
  .filter-label {
    font-weight: 500;
  }
  
  .filter-select {
    min-width: 300px;
    max-width: 100%;
    flex: 1;
  }

  button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    color: gray;
  }
  
  .card-header {
    position: absolute;
    top: 8px;
    right: 8px;
    z-index: 10;
  }
  
  :global(.card-bookmark) {
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(4px);
    border-radius: 6px;
    padding: 6px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  }
  
  :global(.card-bookmark:hover) {
    background: rgba(255, 255, 255, 0.95);
  }
  
  @media (max-width: 640px) {
    .filter-section {
      flex-direction: column;
      align-items: stretch;
    }
    
    .filter-select {
      min-width: auto;
    }
  }

  /* Category divider styling for Svelecte */
  :global(.sv-category-divider) {
    background-color: #f1f3f5 !important;
    font-weight: 600 !important;
    font-size: 0.8rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
    color: #495057 !important;
    padding: 10px 16px 8px 16px !important;
    border-bottom: 1px solid #dee2e6 !important;
    cursor: default !important;
    user-select: none;
    margin: 0 !important;
    width: 100% !important;
  }

  /* Make sure parent item is styled properly for category dividers */
  :global(.svelecte .sv-dropdown .sv-item:has(.sv-category-divider)) {
    background-color: #f1f3f5 !important;
    padding: 0 !important;
    pointer-events: none !important;
    border-radius: 0 !important;
    cursor: default !important;
  }

  :global(.svelecte .sv-dropdown .sv-item:has(.sv-category-divider):hover) {
    background-color: #f1f3f5 !important;
  }

  /* Disable hover and selection for disabled items (categories) */
  :global(.svelecte .sv-dropdown .sv-item[aria-disabled="true"]) {
    pointer-events: none !important;
    background-color: #f1f3f5 !important;
    cursor: default !important;
  }

  :global(.svelecte .sv-dropdown .sv-item[aria-disabled="true"]:hover) {
    background-color: #f1f3f5 !important;
  }

  /* Additional targeting for category items */
  :global(.svelecte .sv-dropdown .sv-item[data-value*="__CATEGORY_"]) {
    pointer-events: none !important;
    background-color: #f1f3f5 !important;
    cursor: default !important;
  }

  :global(.svelecte .sv-dropdown .sv-item[data-value*="__CATEGORY_"]:hover) {
    background-color: #f1f3f5 !important;
  }
</style>