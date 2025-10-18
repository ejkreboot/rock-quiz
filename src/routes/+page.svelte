<script>
  import { onMount } from 'svelte';
  import Svelecte from 'svelecte';
  import {  Box as Cube } from 'lucide-svelte'; // 3D cube icon
  import Modal from '$lib/Modal.svelte';
  import RockInfo from '$lib/RockInfo.svelte';
  import RockModel from '$lib/RockModel.svelte';
  import rock_defs from '$lib/rock_defs.json';
  
  // Data state
  let manifest = {};
  let classes = [];
  let current = null;      // { url, label }
  let revealed = false;
  
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
    
    // NEW: load credits
    try {
      const c = await fetch("/rocks/credits.json");
      const items = await c.json();
      items.forEach(({ file, url }) => {
        creditsMap.set((file || "").replace(/^\/+/, ""), url);
      });
    } catch (e) {
      console.warn("credits.json not found or invalid:", e);
    }
    
    ready = true;
    buildPracticeDeck();
    nextImage();
  });
  
  function onSelectionChange() {
    // Force a new array reference so Svelte definitely reacts
    selectedList = [...(selectedList || [])];
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
  $: chosenLabels = (selectedList?.length ? selectedList : classes)
    .filter(lbl => (manifest[lbl]?.length ?? 0) > 0)
    .sort((a, b) => a.localeCompare(b));
  
  $: currentRockDef = rock_defs.find(r => r.name === current?.label);
  
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
    return `<div class="sv-inlined">
      ${opt.$selected ? svg_checked : svg_empty}
      <span>${opt.text}</span>
    </div>`;
    }
    
  </script>
  
  
  <div class="wrap">
    <header class="app-header">
      <h1>Rock ID Practice</h1>
      <a href="/overview" class="overview-link">📚 Field Guide</a>
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
        options={classes}        
        closeOnSelect={false} 
        bind:value={selectedList}
        renderer={svgRenderer} 
        collapseSelection="always" 
        clearable 
        keepSelectionInList={true} 
        onChange={onSelectionChange}  
        searchProps={{skipSort: true}}
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
  
  @media (max-width: 640px) {
    .filter-section {
      flex-direction: column;
      align-items: stretch;
    }
    
    .filter-select {
      min-width: auto;
    }
  }
</style>