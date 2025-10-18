<script>
    import '../../lib/styles/geology.css';
    import { onMount } from 'svelte';
    
    onMount(() => {
        (function () {
            const familiesEl = document?.getElementById('rid-families');
            const examplesEl = document?.getElementById('rid-examples');
            const clearBtn   = document?.getElementById('rid-clear');
            const checks     = [...document?.querySelectorAll('#rock-id [data-trait]')];
            
            // ★ NEW: gallery nodes + manifest store
            const galleryEl      = document?.getElementById('rid-gallery');
            const galleryHintEl  = document?.getElementById('rid-gallery-hint');
            let ROCKS_MANIFEST   = {};   // { "Andesite": ["/rocks/Andesite/..", ...], ... }
            
            // Quick normalizer so “Volcanic breccia” → “Volcanic Breccia”
            const norm = (s='') => s
            .toString()
            .trim()
            .replace(/\s+/g, ' ')
            .toLowerCase()
            .replace(/\b\w/g, c => c.toUpperCase());
            
            // Load manifest once (served from /static as /rocks-manifest.json)
            fetch('/rocks-manifest.json')
            .then(r => r.json())
            .then(json => { ROCKS_MANIFEST = json || {}; })
            .catch(() => { ROCKS_MANIFEST = {}; });
            
            const rules = [
            { when:['glassy','vesicular'], fam:['Igneous (extrusive)'], ex:['Pumice (light)','Scoria (dark)'] },
            { when:['glassy'], fam:['Igneous (extrusive glass)'], ex:['Obsidian'] },
            { when:['vesicular'], fam:['Igneous (extrusive)'], ex:['Scoria','Vesicular Basalt','Pumice'] },
            { when:['coarse_crystals'], fam:['Igneous (intrusive)'], ex:['Granite','Diorite','Gabbro','Peridotite'] },
            { when:['fine_crystals'], fam:['Igneous (extrusive)'], ex:['Basalt','Andesite','Rhyolite'] },
            { when:['angular_clasts'], fam:['Pyroclastic / Clastic'], ex:['Volcanic Breccia','Sedimentary Breccia'] },
            { when:['rounded_clasts'], fam:['Clastic sedimentary'], ex:['Conglomerate'] },
            { when:['bedding'], fam:['Clastic/Chemical sedimentary'], ex:['Sandstone','Shale','Limestone','Dolostone'] },
            { when:['acid_strong'], fam:['Carbonate sedimentary/metamorphic'], ex:['Limestone','Chalk','Coquina','Fossiliferous limestone','Travertine','Marble (also reacts)'] },
            { when:['acid_weak'], fam:['Carbonate (dolomite-rich)'], ex:['Dolostone','Dolomitic marble'] },
            { when:['salty'], fam:['Evaporite sedimentary'], ex:['Rock Salt (Halite)'] },
            { when:['very_soft'], fam:['Evaporite / Soft minerals'], ex:['Rock Gypsum (Mohs 2)'] },
            { when:['magnetic'], fam:['Fe-rich / Mafic'], ex:['Magnetite (mineral)','Basalt (weak)'] },
            { when:['foliated_shiny'], fam:['Metamorphic (medium–high grade)'], ex:['Schist'] },
            { when:['foliated_dull'], fam:['Metamorphic (low grade)'], ex:['Slate','Phyllite'] },
            { when:['banded_gneiss'], fam:['Metamorphic (high grade)'], ex:['Gneiss','Migmatite'] },
            { when:['sugary_quartz','scratches_glass'], fam:['Metamorphic (quartz-rich)'], ex:['Quartzite'] },
            { when:['sugary_calcite','acid_strong'], fam:['Metamorphic (carbonate)'], ex:['Marble'] },
            { when:['fossils'], fam:['Biochemical sedimentary'], ex:['Fossiliferous limestone','Coquina','Chalk','Shale with fossils'] }
            ];
            
            function renderMap(map, container, chip=false){
                container.innerHTML='';
                [...map.entries()].sort((a,b)=>b[1]-a[1]).forEach(([txt])=>{
                    if(chip){
                        const span=document.createElement('span');
                        span.className='chip';
                        span.textContent=txt;
                        container.appendChild(span);
                    } else {
                        const li=document.createElement('li');
                        li.textContent=txt;
                        li.dataset.example = txt;            // ★ make clickable for gallery
                        container.appendChild(li);
                    }
                });
            }
            
            // ★ NEW: render gallery for a list of rock names (strings)
            function renderGallery(names=[]){
                if(!galleryEl) return;
                galleryEl.innerHTML = '';
                const wanted = [];
                
                // Take up to first 3 names with images
                names.forEach(n=>{
                    const key = norm(n).replace(/\s+\(.*?\)$/, ''); // strip brackets like "(light)"
                    const altKeys = [key, key.replace('Rock ', ''), key.replace('Volcanic ', '')];
                    let imgs = null;
                    for(const k of altKeys){
                        if(ROCKS_MANIFEST[k]) { imgs = ROCKS_MANIFEST[k]; break; }
                    }
                    if(imgs && imgs.length) {
                        wanted.push({ name: key, imgs: imgs.slice(0, 6) }); // cap per rock
                    }
                });
                
                if(!wanted.length){
                    galleryEl.innerHTML = '<div class="gallery-empty hint">No images found for the current suggestions.</div>';
                    return;
                }
                
                wanted.forEach(({name, imgs})=>{
                    // section title card
                    const h = document.createElement('h4');
                    h.className = 'gallery-subtitle';
                    h.textContent = name;
                    galleryEl.appendChild(h);
                    
                    const row = document.createElement('div');
                    row.className = 'thumb-row';
                    imgs.forEach(src=>{
                        const a   = document.createElement('a');
                        a.href    = src;
                        a.target  = '_blank';
                        a.rel     = 'noopener noreferrer';
                        
                        const fig = document.createElement('figure');
                        fig.className = 'thumb';
                        const img = document.createElement('img');
                        img.loading = 'lazy';
                        img.decoding = 'async';
                        img.alt = name;
                        img.src = src;
                        
                        fig.appendChild(img);
                        a.appendChild(fig);
                        row.appendChild(a);
                    });
                    galleryEl.appendChild(row);
                });
            }
            
            function evaluate(){
                const active = new Set(checks.filter(c=>c.checked).map(c=>c.dataset.trait));
                const fam = new Map(), ex = new Map();
                rules.forEach(r=>{
                    if(r.when.every(t=>active.has(t))){
                        (r.fam||[]).forEach(f=>fam.set(f,(fam.get(f)||0)+1));
                        (r.ex||[]).forEach(e=>ex.set(e,(ex.get(e)||0)+1));
                    }
                });
                if(!fam.size && !ex.size){
                    familiesEl.innerHTML = '<span class="chip">Start with texture → fabric → tests</span>';
                    examplesEl.innerHTML = '<li>Try toggling <em>coarse crystals</em> or <em>bedding</em> or <em>acid fizz</em>.</li>';
                    renderGallery([]); // ★ clear
                    return;
                }
                renderMap(fam, familiesEl, true);
                examplesEl.innerHTML='';
                const sorted = [...ex.entries()].sort((a,b)=>b[1]-a[1]).map(([t])=>t);
                sorted.slice(0,10).forEach((t)=>{
                    const li=document.createElement('li'); li.textContent=t; li.dataset.example=t; examplesEl.appendChild(li);
                });
                // ★ refresh gallery with top 3 example buckets
                renderGallery(sorted.slice(0,3));
            }
            
            // interactions
            clearBtn?.addEventListener('click', ()=>{ checks.forEach(c=>c.checked=false); evaluate(); });
            checks.forEach(c=>c.addEventListener('change', evaluate));
            
            // ★ clicking an example focuses the gallery on that rock
            examplesEl?.addEventListener('click', (e)=>{
                const li = e.target.closest('li[data-example]');
                if(!li) return;
                renderGallery([li.dataset.example]);
                galleryHintEl && (galleryHintEl.textContent = `Showing images for “${li.dataset.example}”.`);
            });
            
            evaluate();
        })();
    });
</script>

<div class="wrap">
    <header class="intro-section">
        <h1>🗿 Geology Field Guide</h1>
        <p class="intro-text">
            Comprehensive reference for minerals, igneous, sedimentary, and metamorphic rocks. See below for 
            classification methods and an interactive rock ID helper. Below that is a full catalog of rock 
            types and their characteristics.
        </p>
    </header>
    
    <!-- ========== Rock ID Helper (styled for your theme) ========== -->
    <section id="rock-id" class="wrap rid">
        <header class="rid-hero">
            <h1>🧭 How to Identify a Rock</h1>
            <p class="hint">A quick, systematic approach + an interactive trait picker to narrow possibilities.</p>
        </header>
        
        <!-- Method -->
        <div class="rid-accordion">
            <details open>
                <summary>1) Texture first: crystalline vs. clastic vs. glassy</summary>
                <ul>
                    <li><b>Crystalline</b> (interlocking crystals) → igneous or metamorphic.</li>
                    <li><b>Clastic</b> (individual grains/clasts) → sedimentary.</li>
                    <li><b>Glassy/frothy</b> → volcanic glass (obsidian, pumice, scoria).</li>
                </ul>
            </details>
            <details>
                <summary>2) Structures & fabric</summary>
                <ul>
                    <li><b>Vesicles</b> → pumice/scoria/vesicular basalt.</li>
                    <li><b>Bedding</b> & cross-beds → sandstone/shale/limestone.</li>
                    <li><b>Foliation</b> → slate → phyllite → schist → gneiss (increasing grade).</li>
                    <li><b>Banded light/dark</b> → gneiss; <b>angular fragments</b> → breccia.</li>
                </ul>
            </details>
            <details>
                <summary>3) Simple field tests</summary>
                <ul>
                    <li><b>Dilute HCl</b> fizz → limestone/calcite; weak/slow (powder) → dolostone.</li>
                    <li><b>Hardness</b>: fingernail ≈2 (gypsum); glass ≈5.5–6.</li>
                    <li><b>Streak</b>: red = hematite; sulfur odor on scratch = sphalerite.</li>
                    <li><b>Taste</b>: salty = halite / rock salt (only if safe).</li>
                </ul>
            </details>
            <details>
                <summary>4) Mineral clues</summary>
                <ul>
                    <li>Quartz + K-feldspar + mica (coarse) → granite; fine equivalent → rhyolite.</li>
                    <li>Plagioclase + hornblende/pyroxene (coarse) → diorite/gabbro.</li>
                    <li>Olivine-rich → peridotite; alters to serpentinite.</li>
                </ul>
            </details>
            <details>
                <summary>5) Context</summary>
                <ul>
                    <li>Near volcanoes → <i>igneous</i>. Shallow seas → <i>carbonates</i>.</li>
                    <li>Contact aureole → hornfels; regional belts → foliated metamorphics.</li>
                </ul>
            </details>
        </div>
        
        <!-- Trait Picker -->
        <section class="rid-tool">
            <h2>🔎 Trait Picker</h2>
            <p class="hint">Toggle traits you observe. Suggestions update instantly.</p>
            
            <div class="rid-grid">
                <fieldset>
                    <legend>Texture & Fabric</legend>
                    <label><input type="checkbox" data-trait="glassy"> Glassy</label>
                    <label><input type="checkbox" data-trait="vesicular"> Vesicular (bubbly)</label>
                    <label><input type="checkbox" data-trait="coarse_crystals"> Coarse crystals</label>
                    <label><input type="checkbox" data-trait="fine_crystals"> Fine crystals</label>
                    <label><input type="checkbox" data-trait="angular_clasts"> Angular clasts</label>
                    <label><input type="checkbox" data-trait="rounded_clasts"> Rounded clasts</label>
                    <label><input type="checkbox" data-trait="bedding"> Bedding / layers</label>
                    <label><input type="checkbox" data-trait="foliated_shiny"> Foliated (shiny micas)</label>
                    <label><input type="checkbox" data-trait="foliated_dull"> Foliated (dull/slaty)</label>
                    <label><input type="checkbox" data-trait="banded_gneiss"> Banded light/dark</label>
                </fieldset>
                
                <fieldset>
                    <legend>Simple Tests</legend>
                    <label><input type="checkbox" data-trait="acid_strong"> Fizzes strongly with acid</label>
                    <label><input type="checkbox" data-trait="acid_weak"> Weak/slow acid reaction (powder)</label>
                    <label><input type="checkbox" data-trait="salty"> Salty taste</label>
                    <label><input type="checkbox" data-trait="very_soft"> Very soft (fingernail scratches)</label>
                    <label><input type="checkbox" data-trait="magnetic"> Magnetic</label>
                    <label><input type="checkbox" data-trait="scratches_glass"> Scratches glass easily</label>
                </fieldset>
                
                <fieldset>
                    <legend>Other Clues</legend>
                    <label><input type="checkbox" data-trait="fossils"> Fossils present</label>
                    <label><input type="checkbox" data-trait="sugary_calcite"> Sugary calcite texture</label>
                    <label><input type="checkbox" data-trait="sugary_quartz"> Sugary quartz texture</label>
                </fieldset>
            </div>
            
            <div class="rid-actions">
                <button type="button" class="btn" id="rid-clear">Reset</button>
            </div>
            
            <div class="rid-output">
                <h3>Likely Families</h3>
                <div id="rid-families" class="chips"></div>
                <h3>Examples to Compare</h3>
                <ul id="rid-examples" class="examples"></ul>
                <p class="hint">Combine traits: <em>vesicular + dark</em> → Scoria; <em>glassy + vesicular</em> → Pumice.</p>
            </div>
            <div class="rid-gallery">
                <h3>Image Gallery</h3>
                <div id="rid-gallery" class="gallery-grid" aria-live="polite"></div>
                <p class="hint" id="rid-gallery-hint">
                    Click an example above to focus the gallery, or toggle traits to refresh suggestions.
                </p>
            </div>
        </section>
    </section>
    
    
    <!-- ========== /Rock ID Helper ========== -->
    
    <section class="category-section">
        <h2 class="category-title">🧪 Minerals</h2>
        <div class="specimens-grid">
            
            <div class="specimen-card">
                <h3 class="specimen-name">Augite <span class="specimen-type">(pyroxene)</span></h3>
                <div class="specimen-description">Dark green to black; blocky, stubby crystals; 2 cleavages at ~90°.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Composition:</strong> Ca-Fe-Mg silicate</div>
                    <div class="detail-item"><strong>Formation:</strong> Crystallizes in mafic/intermediate igneous rocks</div>
                    <div class="detail-item"><strong>Occurs in:</strong> <em>Basalt</em>, <em>Gabbro</em>, <em>Andesite</em></div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Biotite <span class="specimen-type">(mica)</span></h3>
                <div class="specimen-description">Black/brown; splits into flexible sheets; glassy luster.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Composition:</strong> K-Fe-Mg mica</div>
                    <div class="detail-item"><strong>Formation:</strong> Intermediate–felsic magmas or metamorphism</div>
                    <div class="detail-item"><strong>Occurs in:</strong> <em>Granite</em>, <em>Schist</em>, <em>Gneiss</em></div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Calcite</h3>
                <div class="specimen-description">White or colorless; reacts vigorously with acid; rhombohedral cleavage (3 not at 90°).</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Composition:</strong> CaCO₃</div>
                    <div class="detail-item"><strong>Formation:</strong> Precipitation or biological secretion in marine settings</div>
                    <div class="detail-item"><strong>Occurs in:</strong> <em>Limestone</em>, metamorphs to <em>Marble</em></div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Chalcopyrite</h3>
                <div class="specimen-description">Brass-yellow metallic; tarnishes iridescent purple; softer than pyrite.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Composition:</strong> CuFeS₂</div>
                    <div class="detail-item"><strong>Formation:</strong> Hydrothermal veins</div>
                    <div class="detail-item"><strong>Associated with:</strong> <em>Pyrite</em>, <em>Galena</em></div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Fluorite</h3>
                <div class="specimen-description">Purple, green, or clear; 4 perfect cleavages (octahedral); glassy.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Composition:</strong> CaF₂</div>
                    <div class="detail-item"><strong>Formation:</strong> Hydrothermal deposits or sedimentary veins</div>
                    <div class="detail-item"><strong>Associated with:</strong> <em>Galena</em>, <em>Calcite</em></div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Galena</h3>
                <div class="specimen-description">Metallic silver-gray; cubic cleavage (3 at 90°); very dense.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Composition:</strong> PbS</div>
                    <div class="detail-item"><strong>Formation:</strong> Hydrothermal veins in limestones</div>
                    <div class="detail-item"><strong>Note:</strong> Primary ore of lead</div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Garnet</h3>
                <div class="specimen-description">Commonly red/brown; glassy dodecahedral crystals; no cleavage.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Composition:</strong> Fe-Mg-Ca-Al silicate</div>
                    <div class="detail-item"><strong>Formation:</strong> Medium–high grade metamorphism</div>
                    <div class="detail-item"><strong>Occurs in:</strong> <em>Schist</em>, <em>Gneiss</em></div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Goethite</h3>
                <div class="specimen-description">Brown to black; earthy to submetallic; brownish streak.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Composition:</strong> FeO(OH)</div>
                    <div class="detail-item"><strong>Formation:</strong> Weathering product of Fe minerals</div>
                    <div class="detail-item"><strong>Occurs in:</strong> Soils, bog iron, oxidized <em>Hematite</em> zones</div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Graphite</h3>
                <div class="specimen-description">Silvery gray; greasy feel; very soft; marks paper.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Composition:</strong> Carbon</div>
                    <div class="detail-item"><strong>Formation:</strong> Metamorphism of organic matter</div>
                    <div class="detail-item"><strong>Occurs in:</strong> <em>Schist</em>, <em>Marble</em></div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Gypsum</h3>
                <div class="specimen-description">Colorless to white; very soft (scratched by fingernail); one perfect cleavage.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Composition:</strong> CaSO₄·2H₂O</div>
                    <div class="detail-item"><strong>Formation:</strong> Evaporite deposits</div>
                    <div class="detail-item"><strong>Occurs in:</strong> <em>Rock gypsum</em>, precursor to <em>Anhydrite</em></div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Halite</h3>
                <div class="specimen-description">Colorless; cubic cleavage; salty taste.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Composition:</strong> NaCl</div>
                    <div class="detail-item"><strong>Formation:</strong> Evaporite mineral in arid basins</div>
                    <div class="detail-item"><strong>Occurs in:</strong> <em>Rock salt</em></div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Hematite</h3>
                <div class="specimen-description">Metallic to earthy red/brown; reddish streak; heavy.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Composition:</strong> Fe₂O₃</div>
                    <div class="detail-item"><strong>Formation:</strong> Oxidation of iron minerals or chemical precipitation</div>
                    <div class="detail-item"><strong>Occurs in:</strong> Banded iron formations</div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Hornblende <span class="specimen-type">(amphibole)</span></h3>
                <div class="specimen-description">Black; splintery habit; 2 cleavages at 60° and 120°.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Composition:</strong> Ca-Na-Mg-Fe amphibole</div>
                    <div class="detail-item"><strong>Formation:</strong> Intermediate–felsic magmas and metamorphism</div>
                    <div class="detail-item"><strong>Occurs in:</strong> <em>Andesite</em>, <em>Diorite</em>, <em>Amphibolite</em></div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Kaolinite</h3>
                <div class="specimen-description">White, dull, powdery; earthy odor when damp; very soft.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Composition:</strong> Al₂Si₂O₅(OH)₄</div>
                    <div class="detail-item"><strong>Formation:</strong> Weathering of feldspar in humid climates</div>
                    <div class="detail-item"><strong>Occurs in:</strong> <em>Shale</em>, clay deposits</div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Magnetite</h3>
                <div class="specimen-description">Black; magnetic; metallic to submetallic.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Composition:</strong> Fe₃O₄</div>
                    <div class="detail-item"><strong>Formation:</strong> Igneous and metamorphic origin</div>
                    <div class="detail-item"><strong>Occurs in:</strong> <em>Gabbro</em>, <em>Basalt</em>, <em>BIFs</em></div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Muscovite <span class="specimen-type">(mica)</span></h3>
                <div class="specimen-description">Colorless to silvery; splits into elastic sheets.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Composition:</strong> K-Al silicate mica</div>
                    <div class="detail-item"><strong>Formation:</strong> Felsic igneous and metamorphic rocks</div>
                    <div class="detail-item"><strong>Occurs in:</strong> <em>Granite</em>, <em>Schist</em>, <em>Pegmatite</em></div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Olivine</h3>
                <div class="specimen-description">Olive-green; granular (sugary texture); no cleavage.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Composition:</strong> (Mg,Fe)₂SiO₄</div>
                    <div class="detail-item"><strong>Formation:</strong> Early crystallization from mafic magma</div>
                    <div class="detail-item"><strong>Occurs in:</strong> <em>Basalt</em>, <em>Peridotite</em>; alters to <em>Serpentine</em></div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Plagioclase feldspar</h3>
                <div class="specimen-description">White to gray; striations on cleavage faces; 2 cleavages ~90°.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Composition:</strong> Na-Ca feldspar series</div>
                    <div class="detail-item"><strong>Occurs in:</strong> Most igneous rocks (esp. <em>Basalt</em>, <em>Andesite</em>, <em>Gabbro</em>, <em>Diorite</em>)</div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Potassium feldspar</h3>
                <div class="specimen-description">Pink to white; often with exsolution lamellae; 2 cleavages ~90°.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Composition:</strong> K-Al-Si feldspar</div>
                    <div class="detail-item"><strong>Occurs in:</strong> <em>Granite</em>, <em>Rhyolite</em></div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Pyrite</h3>
                <div class="specimen-description">Brassy yellow metallic; cubic crystals; greenish-black streak.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Composition:</strong> FeS₂</div>
                    <div class="detail-item"><strong>Formation:</strong> Hydrothermal and sedimentary</div>
                    <div class="detail-item"><strong>Alters to:</strong> <em>Goethite</em>, <em>Hematite</em></div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Quartz</h3>
                <div class="specimen-description">Colorless to many colors; glassy; conchoidal fracture; no cleavage.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Composition:</strong> SiO₂</div>
                    <div class="detail-item"><strong>Note:</strong> Very stable</div>
                    <div class="detail-item"><strong>Occurs in:</strong> <em>Granite</em>, <em>Sandstone</em>, <em>Quartzite</em></div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Sphalerite</h3>
                <div class="specimen-description">Brown to black; resinous luster; sulfur odor when scratched; yellow streak.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Composition:</strong> ZnS</div>
                    <div class="detail-item"><strong>Formation:</strong> Hydrothermal veins</div>
                    <div class="detail-item"><strong>Note:</strong> Main ore of zinc</div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Sulfur</h3>
                <div class="specimen-description">Bright yellow; smells when rubbed; soft.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Composition:</strong> Native element</div>
                    <div class="detail-item"><strong>Formation:</strong> Volcanic and evaporite settings</div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Talc</h3>
                <div class="specimen-description">White to green; pearly; very soft (soapy feel).</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Composition:</strong> Mg silicate</div>
                    <div class="detail-item"><strong>Formation:</strong> Hydrothermal alteration of mafic rocks</div>
                    <div class="detail-item"><strong>Occurs in:</strong> <em>Serpentinite</em>, <em>Soapstone</em></div>
                </div>
            </div>
        </div>
    </section>
    
    <section class="category-section">
        <h2 class="category-title">🌋 Igneous Rocks</h2>
        <div class="specimens-grid">
            
            <div class="specimen-card">
                <h3 class="specimen-name">Andesite</h3>
                <div class="specimen-description">Gray; fine-grained; intermediate composition; often porphyritic.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Minerals:</strong> Plagioclase, amphibole, pyroxene</div>
                    <div class="detail-item"><strong>Environment:</strong> Volcanic arcs (subduction zones)</div>
                    <div class="detail-item"><strong>Intrusive equivalent:</strong> <em>Diorite</em></div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Basalt</h3>
                <div class="specimen-description">Black; fine-grained; mafic; sometimes vesicular.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Minerals:</strong> Pyroxene, Ca-plagioclase, olivine</div>
                    <div class="detail-item"><strong>Environment:</strong> Oceanic crust, lava flows</div>
                    <div class="detail-item"><strong>Intrusive equivalent:</strong> <em>Gabbro</em></div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Diorite</h3>
                <div class="specimen-description">"Salt and pepper" coarse-grained mix of white and black minerals.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Minerals:</strong> Plagioclase + hornblende</div>
                    <div class="detail-item"><strong>Intrusive equivalent of:</strong> <em>Andesite</em></div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Gabbro</h3>
                <div class="specimen-description">Coarse-grained dark rock; mostly pyroxene + plagioclase.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Intrusive equivalent of:</strong> <em>Basalt</em></div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Granite</h3>
                <div class="specimen-description">Coarse-grained; pink or gray; quartz + feldspar + mica.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Type:</strong> Felsic, continental crust</div>
                    <div class="detail-item"><strong>Extrusive equivalent:</strong> <em>Rhyolite</em></div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Obsidian</h3>
                <div class="specimen-description">Glassy black volcanic glass; conchoidal fracture; sharp edges.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Note:</strong> Same composition as rhyolite but cooled too fast for crystals</div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Peridotite</h3>
                <div class="specimen-description">Coarse-grained; greenish (olivine-rich); ultramafic.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Note:</strong> Mantle rock; parent to basaltic magma</div>
                    <div class="detail-item"><strong>Alters to:</strong> <em>Serpentinite</em></div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Pumice</h3>
                <div class="specimen-description">Light gray; frothy; very light and floats; felsic.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Note:</strong> Vesicular volcanic glass from explosive eruptions</div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Rhyolite</h3>
                <div class="specimen-description">Light-colored; fine-grained; felsic; often with quartz phenocrysts.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Extrusive equivalent of:</strong> <em>Granite</em></div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Scoria</h3>
                <div class="specimen-description">Dark red/black; vesicular; heavier than pumice; mafic.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Note:</strong> Basaltic lava with gas bubbles</div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Volcanic breccia</h3>
                <div class="specimen-description">Angular volcanic fragments cemented together.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Formation:</strong> Explosive eruptions or volcanic landslides</div>
                </div>
            </div>
            
        </div>
    </section>
    
    <section class="category-section">
        <h2 class="category-title">🪨 Sedimentary Rocks</h2>
        <div class="specimens-grid">
            <div class="specimen-card">
                <h3 class="specimen-name">Arkose sandstone</h3>
                <div class="specimen-description">Coarse-grained; pinkish; rich in feldspar.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Environment:</strong> Alluvial fans near granitic source</div>
                    <div class="detail-item"><strong>Matures into:</strong> <em>Quartz sandstone</em></div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Breccia</h3>
                <div class="specimen-description">Angular rock fragments in a finer matrix.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Formation:</strong> Near source areas (faults, talus slopes)</div>
                    <div class="detail-item"><strong>Related to:</strong> <em>Conglomerate</em> (rounded clasts)</div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Chert</h3>
                <div class="specimen-description">Hard, dense; conchoidal fracture; dull to waxy luster.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Composition:</strong> Microcrystalline quartz</div>
                    <div class="detail-item"><strong>Environment:</strong> Deep marine; chemical or biogenic silica</div>
                    <div class="detail-item"><strong>Metamorphic equivalent:</strong> <em>Quartzite</em></div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Coal</h3>
                <div class="specimen-description">Black; lightweight; sooty streak; organic origin.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Formation:</strong> Compaction of plant material in swamps</div>
                    <div class="detail-item"><strong>Metamorphic equivalent:</strong> <em>Graphite</em></div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Conglomerate</h3>
                <div class="specimen-description">Rounded pebbles cemented together.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Environment:</strong> Rivers or beaches with strong currents</div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Dolostone</h3>
                <div class="specimen-description">Reacts weakly with acid when powdered; tan-gray color.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Composition:</strong> CaMg(CO₃)₂</div>
                    <div class="detail-item"><strong>Formation:</strong> Mg-rich fluids altering <em>Limestone</em></div>
                    <div class="detail-item"><strong>Metamorphic equivalent:</strong> <em>Dolomitic marble</em></div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Limestone</h3>
                <div class="specimen-description">Reacts with acid; usually gray to tan.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Composition:</strong> Calcite</div>
                    <div class="detail-item"><strong>Environment:</strong> Marine; biological or chemical origin</div>
                    <div class="detail-item"><strong>Metamorphic equivalent:</strong> <em>Marble</em></div>
                    <div class="detail-item"><strong>Subtypes:</strong> Chalk, Coquina, Fossiliferous, Micritic, Oolitic</div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Quartz sandstone</h3>
                <div class="specimen-description">Gritty; mostly quartz; often light-colored.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Environment:</strong> Beach or desert</div>
                    <div class="detail-item"><strong>Metamorphic equivalent:</strong> <em>Quartzite</em></div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Rock gypsum</h3>
                <div class="specimen-description">Soft; white/pink; scratched by fingernail.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Type:</strong> Evaporite deposit; CaSO₄·2H₂O</div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Rock salt</h3>
                <div class="specimen-description">Transparent cubic crystals; salty taste.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Type:</strong> Evaporite deposit; NaCl</div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Shale</h3>
                <div class="specimen-description">Fine-grained; splits into thin sheets; dull luster.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Composition:</strong> Clay minerals</div>
                    <div class="detail-item"><strong>Environment:</strong> Quiet water (lakes, deep marine)</div>
                    <div class="detail-item"><strong>Metamorphic sequence:</strong> <em>Slate → Phyllite → Schist → Gneiss</em></div>
                </div>
            </div>
        </div>
    </section>
    
    <section class="category-section">
        <h2 class="category-title">🔥 Metamorphic Rocks</h2>
        <div class="specimens-grid">
            <div class="specimen-card">
                <h3 class="specimen-name">Amphibolite</h3>
                <div class="specimen-description">Dark, coarse-grained; amphibole-rich; may show weak foliation.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Parent:</strong> <em>Basalt</em> or <em>Gabbro</em></div>
                    <div class="detail-item"><strong>Grade:</strong> Medium–high</div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Gneiss</h3>
                <div class="specimen-description">Alternating light/dark bands; coarse foliation.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Parent:</strong> <em>Granite</em> or <em>Schist</em></div>
                    <div class="detail-item"><strong>Grade:</strong> High</div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Metaconglomerate</h3>
                <div class="specimen-description">Pebbles deformed or stretched within finer matrix.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Parent:</strong> <em>Conglomerate</em></div>
                    <div class="detail-item"><strong>Grade:</strong> Variable</div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Marble</h3>
                <div class="specimen-description">Crystalline; reacts with acid; sugary texture; usually white.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Parent:</strong> <em>Limestone</em> or <em>Dolostone</em></div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Phyllite</h3>
                <div class="specimen-description">Silky sheen; fine-grained; wavy foliation.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Parent:</strong> <em>Slate</em> (from shale)</div>
                    <div class="detail-item"><strong>Grade:</strong> Low–medium</div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Quartzite</h3>
                <div class="specimen-description">Hard; sugary texture; scratches glass; fused quartz grains.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Parent:</strong> <em>Quartz sandstone</em></div>
                    <div class="detail-item"><strong>Grade:</strong> Any</div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Schist</h3>
                <div class="specimen-description">Sparkly mica-rich foliation; medium to coarse-grained.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Parent:</strong> <em>Phyllite</em> or <em>Shale</em></div>
                    <div class="detail-item"><strong>Grade:</strong> Medium–high</div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Serpentinite</h3>
                <div class="specimen-description">Greenish, waxy luster; slick feel; derived from ultramafic rock.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Parent:</strong> <em>Peridotite</em> (hydrated olivine)</div>
                    <div class="detail-item"><strong>Grade:</strong> Low</div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Slate</h3>
                <div class="specimen-description">Dark gray; very fine-grained; splits into flat sheets with a "ping" sound.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Parent:</strong> <em>Shale</em></div>
                    <div class="detail-item"><strong>Grade:</strong> Low</div>
                </div>
            </div>
        </div>
    </section>
</div>

<style>
    /* Custom styles for the overview page using geology.css variables */
    .intro-section {
        text-align: center;
        margin-bottom: 3rem;
        padding: 2rem 1rem;
        background: linear-gradient(135deg, var(--card-bg), var(--bg));
        border-radius: var(--radius);
        box-shadow: var(--shadow);
    }
    
    li {
        padding: 5px; 
    }
    
    label {
        padding-left: 2em;
        text-indent: -1.5em;
    }
    .intro-text {
        font-size: 1.1rem;
        color: var(--muted);
        line-height: 1.6;
        max-width: 600px;
        margin: 0 auto;
    }
    
    .category-section {
        margin-bottom: 3rem;
    }
    
    .category-title {
        font-family: 'Rubik Distressed', system-ui, sans-serif;
        font-size: clamp(1.5rem, 2vw + 1rem, 2rem);
        color: var(--title);
        margin-bottom: 1.5rem;
        text-shadow: 0 1px 0 rgba(0,0,0,0.03);
        border-bottom: 2px solid var(--accent);
        padding-bottom: 0.5rem;
    }
    
    .specimens-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
        gap: 1.5rem;
        margin-bottom: 2rem;
    }
    
    .specimen-card {
        background: var(--card-bg);
        border-radius: var(--radius);
        padding: 1.5rem;
        box-shadow: var(--shadow);
        border: 1px solid rgba(0,0,0,0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .specimen-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 32px rgba(0,0,0,0.15);
    }
    
    .specimen-name {
        font-size: 1.2rem;
        font-weight: 700;
        color: var(--title);
        margin: 0 0 0.75rem 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        flex-wrap: wrap;
    }
    
    .specimen-type {
        font-size: 0.9rem;
        color: var(--accent);
        font-weight: 500;
        font-style: italic;
    }
    
    .specimen-description {
        color: var(--ink);
        font-weight: 500;
        margin-bottom: 1rem;
        line-height: 1.5;
    }
    
    .specimen-details {
        display: flex;
        flex-direction: column;
        gap: 0.4rem;
    }
    
    .detail-item {
        font-size: 0.95rem;
        line-height: 1.4;
        color: var(--muted);
    }
    
    .detail-item strong {
        color: var(--accent);
        font-weight: 600;
    }
    
    .detail-item em {
        color: var(--title);
        font-weight: 500;
        font-style: normal;
    }
    
    /* ---- Mini gallery (matches your theme) ---- */
    :global(.rid-gallery) { margin-top: 1rem; }
    :global(.rid-gallery h3) { margin: .25rem 0 .4rem; color: var(--title); }
    :global(.gallery-subtitle) {
        margin: .6rem 0 .2rem;
        color: var(--accent);
        font-weight: 800;
        letter-spacing: .2px;
    }
    :global(.gallery-grid) { display: grid; gap: .6rem; }
    :global(.thumb-row) { display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: .6rem; }
    :global(.thumb) {
        background: var(--card-bg);
        border: 1px solid rgba(0,0,0,.06);
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 2px 10px rgba(0,0,0,.05);
        aspect-ratio: 4 / 3;
        display: grid;
        place-items: center;
    }
    :global(.thumb img) {
        width: 100%; height: 100%;
        object-fit: cover;
        transform: translateZ(0);
        transition: transform .18s ease;
        display: block;
    }
    :global(.thumb:hover img) { transform: scale(1.04); }
    :global(.gallery-empty) { padding: .6rem .2rem; }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .specimens-grid {
            grid-template-columns: 1fr;
            gap: 1rem;
        }
        
        .specimen-card {
            padding: 1.25rem;
        }
        
        .intro-section {
            margin-bottom: 2rem;
            padding: 1.5rem 1rem;
        }
    }
    
    @media (max-width: 480px) {
        .specimen-name {
            font-size: 1.1rem;
        }
        
        .specimen-description {
            font-size: 0.95rem;
        }
        
        .detail-item {
            font-size: 0.9rem;
        }
    }
    /* ---- rock-id component: uses your variables/fonts ---- */
    .rid-hero{
        background: var(--card-bg);
        border: 1px solid rgba(0,0,0,.06);
        border-radius: var(--radius);
        box-shadow: var(--shadow);
        padding: 1rem 1.2rem;
    }
    .rid-hero h1{ margin:0 0 .25rem 0; }
    .rid-accordion details{
        background: #fff;
        border: 1px solid rgba(0,0,0,.08);
        border-radius: var(--radius);
        padding: .7rem .9rem;
        margin: .6rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,.04);
    }
    .rid-accordion summary{
        cursor:pointer;
        font-weight: 700;
        color: var(--ink);
    }
    .rid-accordion ul{ margin:.5rem 0 .2rem 1.1rem }
    
    .rid-tool{
        margin-top: 1rem;
        background: #fff;
        border: 1px solid rgba(0,0,0,.08);
        border-radius: var(--radius);
        padding: 1rem;
        box-shadow: var(--shadow);
    }
    .rid-tool h2{
        font-family: 'Quicksand', system-ui, sans-serif;
        margin: .25rem 0 .2rem;
        color: var(--title);
    }
    .rid-grid{
        display:grid;
        gap:.8rem;
        grid-template-columns: repeat(auto-fit, minmax(230px,1fr));
    }
    fieldset{
        border: 1px solid rgba(0,0,0,.08);
        border-radius: 12px;
        padding: .6rem .8rem;
        background: var(--card-bg);
    }
    legend{ color: var(--muted); padding: 0 .4rem; }
    label{ display:block; margin:.25rem 0; color: var(--ink); }
    .rid-actions{ margin:.6rem 0; }
    .chips{ display:flex; gap:.5rem; flex-wrap:wrap; }
    .chip{
        background: var(--card-bg);
        border: 1px solid rgba(0,0,0,.08);
        border-radius: 999px;
        padding: .22rem .6rem;
        font-weight: 700;
        color: var(--accent);
    }
    .examples{ margin:.4rem 0 0 1rem; }
</style>

