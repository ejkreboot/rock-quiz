<script>
    import '../../lib/styles/geology.css';
    import { onMount } from 'svelte';
    import { Box as Cube } from 'lucide-svelte'; // 3D cube icon
    import rocksManifest from '$lib/rocks-manifest.json';
    import Modal from '$lib/Modal.svelte';
    import RockModel from '$lib/RockModel.svelte';
    import rock_defs from '$lib/rock_defs.json';

    let modalOpen = false;
    let modalComponent = null;
    let modalProps = {};
    let modalTitle = "";

    function open3DModal(rockName) {
        const def = rock_defs.find(r => r.name === rockName);
        if (def && def.model_3d) {
            modalComponent = RockModel;
            modalProps = { name: def.name, ...def.model_3d };
            modalTitle = `3D Model of ${def.name}`;
            modalOpen = true;
        }
    }

    onMount(() => {
        document.title = "Geology Field Guide - Minerals & Rocks Reference";
    });

    function getRockThumbnail(name) {
        // Normalize name for manifest lookup
        if (!rocksManifest[name]) return null;
        return rocksManifest[name][0];
    }
</script>

<div class="wrap">
    <header class="intro-section">
        <h1>🗿 Geology Field Guide</h1>
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
        </section>  
        
    
                    <details class="category-section">
                            <summary class="category-title">🧪 Minerals</summary>
                            <div class="specimens-grid">
            
            <div class="specimen-card">
                                                <h3 class="specimen-name">Augite <span class="specimen-type">(pyroxene)</span>{#if getRockThumbnail('Augite')}<img class="rock-thumb" src={getRockThumbnail('Augite')} alt="Augite thumbnail" loading="lazy" />{/if}
                                                    <button class="model-btn" on:click={() => open3DModal('Augite')} title="View 3D Model"><Cube size={18} /></button>
                                                </h3>
                <div class="specimen-description">Dark green to black; blocky, stubby crystals; 2 cleavages at ~90°.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Composition:</strong> Ca-Fe-Mg silicate</div>
                    <div class="detail-item"><strong>Formation:</strong> Crystallizes in mafic/intermediate igneous rocks</div>
                    <div class="detail-item"><strong>Occurs in:</strong> <em>Basalt</em>, <em>Gabbro</em>, <em>Andesite</em></div>
                </div>
            </div>
            
            <div class="specimen-card">
                                                <h3 class="specimen-name">Biotite <span class="specimen-type">(mica)</span>{#if getRockThumbnail('Biotite')}<img class="rock-thumb" src={getRockThumbnail('Biotite')} alt="Biotite thumbnail" loading="lazy" />{/if}
                                                    <button class="model-btn" on:click={() => open3DModal('Biotite')} title="View 3D Model"><Cube size={18} /></button>
                                                </h3>
                <div class="specimen-description">Black/brown; splits into flexible sheets; glassy luster.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Composition:</strong> K-Fe-Mg mica</div>
                    <div class="detail-item"><strong>Formation:</strong> Intermediate–felsic magmas or metamorphism</div>
                    <div class="detail-item"><strong>Occurs in:</strong> <em>Granite</em>, <em>Schist</em>, <em>Gneiss</em></div>
                </div>
            </div>
            
            <div class="specimen-card">
                                                <h3 class="specimen-name">Calcite{#if getRockThumbnail('Calcite')}<img class="rock-thumb" src={getRockThumbnail('Calcite')} alt="Calcite thumbnail" loading="lazy" />{/if}
                                                    <button class="model-btn" on:click={() => open3DModal('Calcite')} title="View 3D Model"><Cube size={18} /></button>
                                                </h3>
                <div class="specimen-description">White or colorless; reacts vigorously with acid; rhombohedral cleavage (3 not at 90°).</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Composition:</strong> CaCO₃</div>
                    <div class="detail-item"><strong>Formation:</strong> Precipitation or biological secretion in marine settings</div>
                    <div class="detail-item"><strong>Occurs in:</strong> <em>Limestone</em>, metamorphs to <em>Marble</em></div>
                </div>
            </div>
            
            <div class="specimen-card">
                                                <h3 class="specimen-name">Chalcopyrite{#if getRockThumbnail('Chalcopyrite')}<img class="rock-thumb" src={getRockThumbnail('Chalcopyrite')} alt="Chalcopyrite thumbnail" loading="lazy" />{/if}
                                                    <button class="model-btn" on:click={() => open3DModal('Chalcopyrite')} title="View 3D Model"><Cube size={18} /></button>
                                                </h3>
                <div class="specimen-description">Brass-yellow metallic; tarnishes iridescent purple; softer than pyrite.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Composition:</strong> CuFeS₂</div>
                    <div class="detail-item"><strong>Formation:</strong> Hydrothermal veins</div>
                    <div class="detail-item"><strong>Associated with:</strong> <em>Pyrite</em>, <em>Galena</em></div>
                </div>
            </div>
            
            <div class="specimen-card">
                                                <h3 class="specimen-name">Fluorite{#if getRockThumbnail('Fluorite')}<img class="rock-thumb" src={getRockThumbnail('Fluorite')} alt="Fluorite thumbnail" loading="lazy" />{/if}
                                                    <button class="model-btn" on:click={() => open3DModal('Fluorite')} title="View 3D Model"><Cube size={18} /></button>
                                                </h3>
                <div class="specimen-description">Purple, green, or clear; 4 perfect cleavages (octahedral); glassy.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Composition:</strong> CaF₂</div>
                    <div class="detail-item"><strong>Formation:</strong> Hydrothermal deposits or sedimentary veins</div>
                    <div class="detail-item"><strong>Associated with:</strong> <em>Galena</em>, <em>Calcite</em></div>
                </div>
            </div>
            
            <div class="specimen-card">
                                                <h3 class="specimen-name">Galena{#if getRockThumbnail('Galena')}<img class="rock-thumb" src={getRockThumbnail('Galena')} alt="Galena thumbnail" loading="lazy" />{/if}
                                                    <button class="model-btn" on:click={() => open3DModal('Galena')} title="View 3D Model"><Cube size={18} /></button>
                                                </h3>
                <div class="specimen-description">Metallic silver-gray; cubic cleavage (3 at 90°); very dense.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Composition:</strong> PbS</div>
                    <div class="detail-item"><strong>Formation:</strong> Hydrothermal veins in limestones</div>
                    <div class="detail-item"><strong>Note:</strong> Primary ore of lead</div>
                </div>
            </div>
            
            <div class="specimen-card">
                                                <h3 class="specimen-name">Garnet{#if getRockThumbnail('Garnet')}<img class="rock-thumb" src={getRockThumbnail('Garnet')} alt="Garnet thumbnail" loading="lazy" />{/if}
                                                    <button class="model-btn" on:click={() => open3DModal('Garnet')} title="View 3D Model"><Cube size={18} /></button>
                                                </h3>
                <div class="specimen-description">Commonly red/brown; glassy dodecahedral crystals; no cleavage.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Composition:</strong> Fe-Mg-Ca-Al silicate</div>
                    <div class="detail-item"><strong>Formation:</strong> Medium–high grade metamorphism</div>
                    <div class="detail-item"><strong>Occurs in:</strong> <em>Schist</em>, <em>Gneiss</em></div>
                </div>
            </div>
            
            <div class="specimen-card">
                                                <h3 class="specimen-name">Goethite{#if getRockThumbnail('Goethite')}<img class="rock-thumb" src={getRockThumbnail('Goethite')} alt="Goethite thumbnail" loading="lazy" />{/if}
                                                    <button class="model-btn" on:click={() => open3DModal('Goethite')} title="View 3D Model"><Cube size={18} /></button>
                                                </h3>
                <div class="specimen-description">Brown to black; earthy to submetallic; brownish streak.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Composition:</strong> FeO(OH)</div>
                    <div class="detail-item"><strong>Formation:</strong> Weathering product of Fe minerals</div>
                    <div class="detail-item"><strong>Occurs in:</strong> Soils, bog iron, oxidized <em>Hematite</em> zones</div>
                </div>
            </div>
            
            <div class="specimen-card">
                                                <h3 class="specimen-name">Graphite{#if getRockThumbnail('Graphite')}<img class="rock-thumb" src={getRockThumbnail('Graphite')} alt="Graphite thumbnail" loading="lazy" />{/if}
                                                    <button class="model-btn" on:click={() => open3DModal('Graphite')} title="View 3D Model"><Cube size={18} /></button>
                                                </h3>
                <div class="specimen-description">Silvery gray; greasy feel; very soft; marks paper.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Composition:</strong> Carbon</div>
                    <div class="detail-item"><strong>Formation:</strong> Metamorphism of organic matter</div>
                    <div class="detail-item"><strong>Occurs in:</strong> <em>Schist</em>, <em>Marble</em></div>
                </div>
            </div>
            
            <div class="specimen-card">
                                                <h3 class="specimen-name">Gypsum{#if getRockThumbnail('Gypsum')}<img class="rock-thumb" src={getRockThumbnail('Gypsum')} alt="Gypsum thumbnail" loading="lazy" />{/if}
                                                    <button class="model-btn" on:click={() => open3DModal('Gypsum')} title="View 3D Model"><Cube size={18} /></button>
                                                </h3>
                <div class="specimen-description">Colorless to white; very soft (scratched by fingernail); one perfect cleavage.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Composition:</strong> CaSO₄·2H₂O</div>
                    <div class="detail-item"><strong>Formation:</strong> Evaporite deposits</div>
                    <div class="detail-item"><strong>Occurs in:</strong> <em>Rock gypsum</em>, precursor to <em>Anhydrite</em></div>
                </div>
            </div>
            
            <div class="specimen-card">
                                                <h3 class="specimen-name">Halite{#if getRockThumbnail('Halite')}<img class="rock-thumb" src={getRockThumbnail('Halite')} alt="Halite thumbnail" loading="lazy" />{/if}
                                                    <button class="model-btn" on:click={() => open3DModal('Halite')} title="View 3D Model"><Cube size={18} /></button>
                                                </h3>
                <div class="specimen-description">Colorless; cubic cleavage; salty taste.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Composition:</strong> NaCl</div>
                    <div class="detail-item"><strong>Formation:</strong> Evaporite mineral in arid basins</div>
                    <div class="detail-item"><strong>Occurs in:</strong> <em>Rock salt</em></div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Hematite{#if getRockThumbnail('Hematite')}<img class="rock-thumb" src={getRockThumbnail('Hematite')} alt="Hematite thumbnail" loading="lazy" />{/if}
                    <button class="model-btn" on:click={() => open3DModal('Hematite')} title="View 3D Model"><Cube size={18} /></button>
                </h3>
                <div class="specimen-description">Metallic to earthy red/brown; reddish streak; heavy.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Composition:</strong> Fe₂O₃</div>
                    <div class="detail-item"><strong>Formation:</strong> Oxidation of iron minerals or chemical precipitation</div>
                    <div class="detail-item"><strong>Occurs in:</strong> Banded iron formations</div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Hornblende <span class="specimen-type">(amphibole)</span>{#if getRockThumbnail('Hornblende')}<img class="rock-thumb" src={getRockThumbnail('Hornblende')} alt="Hornblende thumbnail" loading="lazy" />{/if}
                    <button class="model-btn" on:click={() => open3DModal('Hornblende')} title="View 3D Model"><Cube size={18} /></button>
                </h3>
                <div class="specimen-description">Black; splintery habit; 2 cleavages at 60° and 120°.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Composition:</strong> Ca-Na-Mg-Fe amphibole</div>
                    <div class="detail-item"><strong>Formation:</strong> Intermediate–felsic magmas and metamorphism</div>
                    <div class="detail-item"><strong>Occurs in:</strong> <em>Andesite</em>, <em>Diorite</em>, <em>Amphibolite</em></div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Kaolinite{#if getRockThumbnail('Kaolinite')}<img class="rock-thumb" src={getRockThumbnail('Kaolinite')} alt="Kaolinite thumbnail" loading="lazy" />{/if}
                    <button class="model-btn" on:click={() => open3DModal('Kaolinite')} title="View 3D Model"><Cube size={18} /></button>
                </h3>
                <div class="specimen-description">White, dull, powdery; earthy odor when damp; very soft.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Composition:</strong> Al₂Si₂O₅(OH)₄</div>
                    <div class="detail-item"><strong>Formation:</strong> Weathering of feldspar in humid climates</div>
                    <div class="detail-item"><strong>Occurs in:</strong> <em>Shale</em>, clay deposits</div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Magnetite{#if getRockThumbnail('Magnetite')}<img class="rock-thumb" src={getRockThumbnail('Magnetite')} alt="Magnetite thumbnail" loading="lazy" />{/if}
                    <button class="model-btn" on:click={() => open3DModal('Magnetite')} title="View 3D Model"><Cube size={18} /></button>
                </h3>
                <div class="specimen-description">Black; magnetic; metallic to submetallic.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Composition:</strong> Fe₃O₄</div>
                    <div class="detail-item"><strong>Formation:</strong> Igneous and metamorphic origin</div>
                    <div class="detail-item"><strong>Occurs in:</strong> <em>Gabbro</em>, <em>Basalt</em>, <em>BIFs</em></div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Muscovite <span class="specimen-type">(mica)</span>{#if getRockThumbnail('Muscovite')}<img class="rock-thumb" src={getRockThumbnail('Muscovite')} alt="Muscovite thumbnail" loading="lazy" />{/if}
                    <button class="model-btn" on:click={() => open3DModal('Muscovite')} title="View 3D Model"><Cube size={18} /></button>
                </h3>
                <div class="specimen-description">Colorless to silvery; splits into elastic sheets.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Composition:</strong> K-Al silicate mica</div>
                    <div class="detail-item"><strong>Formation:</strong> Felsic igneous and metamorphic rocks</div>
                    <div class="detail-item"><strong>Occurs in:</strong> <em>Granite</em>, <em>Schist</em>, <em>Pegmatite</em></div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Olivine{#if getRockThumbnail('Olivine')}<img class="rock-thumb" src={getRockThumbnail('Olivine')} alt="Olivine thumbnail" loading="lazy" />{/if}
                    <button class="model-btn" on:click={() => open3DModal('Olivine')} title="View 3D Model"><Cube size={18} /></button>
                </h3>
                <div class="specimen-description">Olive-green; granular (sugary texture); no cleavage.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Composition:</strong> (Mg,Fe)₂SiO₄</div>
                    <div class="detail-item"><strong>Formation:</strong> Early crystallization from mafic magma</div>
                    <div class="detail-item"><strong>Occurs in:</strong> <em>Basalt</em>, <em>Peridotite</em>; alters to <em>Serpentine</em></div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Plagioclase feldspar{#if getRockThumbnail('Plagioclase Feldspar')}<img class="rock-thumb" src={getRockThumbnail('Plagioclase Feldspar')} alt="Plagioclase Feldspar thumbnail" loading="lazy" />{/if}
                    <button class="model-btn" on:click={() => open3DModal('Plagioclase Feldspar')} title="View 3D Model"><Cube size={18} /></button>
                </h3>
                <div class="specimen-description">White to gray; striations on cleavage faces; 2 cleavages ~90°.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Composition:</strong> Na-Ca feldspar series</div>
                    <div class="detail-item"><strong>Occurs in:</strong> Most igneous rocks (esp. <em>Basalt</em>, <em>Andesite</em>, <em>Gabbro</em>, <em>Diorite</em>)</div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Potassium feldspar{#if getRockThumbnail('Orthoclase Feldspar')}<img class="rock-thumb" src={getRockThumbnail('Orthoclase Feldspar')} alt="Orthoclase Feldspar thumbnail" loading="lazy" />{/if}
                    <button class="model-btn" on:click={() => open3DModal('Orthoclase Feldspar')} title="View 3D Model"><Cube size={18} /></button>
                </h3>
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
                <h3 class="specimen-name">Quartz{#if getRockThumbnail('Quartz')}<img class="rock-thumb" src={getRockThumbnail('Quartz')} alt="Quartz thumbnail" loading="lazy" />{/if}
                    <button class="model-btn" on:click={() => open3DModal('Quartz')} title="View 3D Model"><Cube size={18} /></button>
                </h3>
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
                <h3 class="specimen-name">Sulfur{#if getRockThumbnail('Sulfur')}<img class="rock-thumb" src={getRockThumbnail('Sulfur')} alt="Sulfur thumbnail" loading="lazy" />{/if}
                    <button class="model-btn" on:click={() => open3DModal('Sulfur')} title="View 3D Model"><Cube size={18} /></button>
                </h3>
                <div class="specimen-description">Bright yellow; smells when rubbed; soft.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Composition:</strong> Native element</div>
                    <div class="detail-item"><strong>Formation:</strong> Volcanic and evaporite settings</div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Talc{#if getRockThumbnail('Talc')}<img class="rock-thumb" src={getRockThumbnail('Talc')} alt="Talc thumbnail" loading="lazy" />{/if}
                    <button class="model-btn" on:click={() => open3DModal('Talc')} title="View 3D Model"><Cube size={18} /></button>
                </h3>
                <div class="specimen-description">White to green; pearly; very soft (soapy feel).</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Composition:</strong> Mg silicate</div>
                    <div class="detail-item"><strong>Formation:</strong> Hydrothermal alteration of mafic rocks</div>
                    <div class="detail-item"><strong>Occurs in:</strong> <em>Serpentinite</em>, <em>Soapstone</em></div>
                </div>
            </div>
        </div>
        </details>
    
    
                <details class="category-section">
                    <summary class="category-title">🌋 Igneous Rocks</summary>
                    <div class="specimens-grid">
            
            <div class="specimen-card">
                <h3 class="specimen-name">Andesite{#if getRockThumbnail('Andesite')}<img class="rock-thumb" src={getRockThumbnail('Andesite')} alt="Andesite thumbnail" loading="lazy" />{/if}
                    <button class="model-btn" on:click={() => open3DModal('Andesite')} title="View 3D Model"><Cube size={18} /></button>
                </h3>
                <div class="specimen-description">Gray; fine-grained; intermediate composition; often porphyritic.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Minerals:</strong> Plagioclase, amphibole, pyroxene</div>
                    <div class="detail-item"><strong>Environment:</strong> Volcanic arcs (subduction zones)</div>
                    <div class="detail-item"><strong>Intrusive equivalent:</strong> <em>Diorite</em></div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Basalt{#if getRockThumbnail('Basalt')}<img class="rock-thumb" src={getRockThumbnail('Basalt')} alt="Basalt thumbnail" loading="lazy" />{/if}
                    <button class="model-btn" on:click={() => open3DModal('Basalt')} title="View 3D Model"><Cube size={18} /></button>
                </h3>
                <div class="specimen-description">Black; fine-grained; mafic; sometimes vesicular.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Minerals:</strong> Pyroxene, Ca-plagioclase, olivine</div>
                    <div class="detail-item"><strong>Environment:</strong> Oceanic crust, lava flows</div>
                    <div class="detail-item"><strong>Intrusive equivalent:</strong> <em>Gabbro</em></div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Diorite{#if getRockThumbnail('Diorite')}<img class="rock-thumb" src={getRockThumbnail('Diorite')} alt="Diorite thumbnail" loading="lazy" />{/if}
                    <button class="model-btn" on:click={() => open3DModal('Diorite')} title="View 3D Model"><Cube size={18} /></button>
                </h3>
                <div class="specimen-description">"Salt and pepper" coarse-grained mix of white and black minerals.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Minerals:</strong> Plagioclase + hornblende</div>
                    <div class="detail-item"><strong>Intrusive equivalent of:</strong> <em>Andesite</em></div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Gabbro{#if getRockThumbnail('Gabbro')}<img class="rock-thumb" src={getRockThumbnail('Gabbro')} alt="Gabbro thumbnail" loading="lazy" />{/if}
                    <button class="model-btn" on:click={() => open3DModal('Gabbro')} title="View 3D Model"><Cube size={18} /></button>
                </h3>
                <div class="specimen-description">Coarse-grained dark rock; mostly pyroxene + plagioclase.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Intrusive equivalent of:</strong> <em>Basalt</em></div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Granite{#if getRockThumbnail('Granite')}<img class="rock-thumb" src={getRockThumbnail('Granite')} alt="Granite thumbnail" loading="lazy" />{/if}
                    <button class="model-btn" on:click={() => open3DModal('Granite')} title="View 3D Model"><Cube size={18} /></button>
                </h3>
                <div class="specimen-description">Coarse-grained; pink or gray; quartz + feldspar + mica.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Type:</strong> Felsic, continental crust</div>
                    <div class="detail-item"><strong>Extrusive equivalent:</strong> <em>Rhyolite</em></div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Obsidian{#if getRockThumbnail('Obsidian')}<img class="rock-thumb" src={getRockThumbnail('Obsidian')} alt="Obsidian thumbnail" loading="lazy" />{/if}
                    <button class="model-btn" on:click={() => open3DModal('Obsidian')} title="View 3D Model"><Cube size={18} /></button>
                </h3>
                <div class="specimen-description">Glassy black volcanic glass; conchoidal fracture; sharp edges.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Note:</strong> Same composition as rhyolite but cooled too fast for crystals</div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Peridotite{#if getRockThumbnail('Peridotite')}<img class="rock-thumb" src={getRockThumbnail('Peridotite')} alt="Peridotite thumbnail" loading="lazy" />{/if}
                    <button class="model-btn" on:click={() => open3DModal('Peridotite')} title="View 3D Model"><Cube size={18} /></button>
                </h3>
                <div class="specimen-description">Coarse-grained; greenish (olivine-rich); ultramafic.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Note:</strong> Mantle rock; parent to basaltic magma</div>
                    <div class="detail-item"><strong>Alters to:</strong> <em>Serpentinite</em></div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Pumice{#if getRockThumbnail('Pumice')}<img class="rock-thumb" src={getRockThumbnail('Pumice')} alt="Pumice thumbnail" loading="lazy" />{/if}
                    <button class="model-btn" on:click={() => open3DModal('Pumice')} title="View 3D Model"><Cube size={18} /></button>
                </h3>
                <div class="specimen-description">Light gray; frothy; very light and floats; felsic.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Note:</strong> Vesicular volcanic glass from explosive eruptions</div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Rhyolite{#if getRockThumbnail('Rhyolite')}<img class="rock-thumb" src={getRockThumbnail('Rhyolite')} alt="Rhyolite thumbnail" loading="lazy" />{/if}
                    <button class="model-btn" on:click={() => open3DModal('Rhyolite')} title="View 3D Model"><Cube size={18} /></button>
                </h3>
                <div class="specimen-description">Light-colored; fine-grained; felsic; often with quartz phenocrysts.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Extrusive equivalent of:</strong> <em>Granite</em></div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Scoria{#if getRockThumbnail('Scoria')}<img class="rock-thumb" src={getRockThumbnail('Scoria')} alt="Scoria thumbnail" loading="lazy" />{/if}
                    <button class="model-btn" on:click={() => open3DModal('Scoria')} title="View 3D Model"><Cube size={18} /></button>
                </h3>
                <div class="specimen-description">Dark red/black; vesicular; heavier than pumice; mafic.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Note:</strong> Basaltic lava with gas bubbles</div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Tuff{#if getRockThumbnail('Tuff')}<img class="rock-thumb" src={getRockThumbnail('Tuff')} alt="Tuff thumbnail" loading="lazy" />{/if}
                    <button class="model-btn" on:click={() => open3DModal('Tuff')} title="View 3D Model"><Cube size={18} /></button>
                </h3>
                <div class="specimen-description">Consolidated volcanic ash; fine-grained; can be welded or unwelded.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Formation:</strong> Explosive volcanic eruptions and ash falls</div>
                    <div class="detail-item"><strong>Texture:</strong> Pyroclastic (fragmental)</div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Volcanic breccia{#if getRockThumbnail('Volcanic Breccia')}<img class="rock-thumb" src={getRockThumbnail('Volcanic Breccia')} alt="Volcanic Breccia thumbnail" loading="lazy" />{/if}
                    <button class="model-btn" on:click={() => open3DModal('Volcanic Breccia')} title="View 3D Model"><Cube size={18} /></button>
                </h3>
                <div class="specimen-description">Angular volcanic fragments cemented together.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Formation:</strong> Explosive eruptions or volcanic landslides</div>
                </div>
            </div>
            
        </div>
        </details>
    
    
                <details class="category-section">
                    <summary class="category-title">🪨 Sedimentary Rocks</summary>
                    <div class="specimens-grid">
            <div class="specimen-card">
                <h3 class="specimen-name">Arkose sandstone{#if getRockThumbnail('Arkose')}<img class="rock-thumb" src={getRockThumbnail('Arkose')} alt="Arkose thumbnail" loading="lazy" />{/if}
                    <button class="model-btn" on:click={() => open3DModal('Arkose')} title="View 3D Model"><Cube size={18} /></button>
                </h3>
                <div class="specimen-description">Coarse-grained; pinkish; rich in feldspar.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Environment:</strong> Alluvial fans near granitic source</div>
                    <div class="detail-item"><strong>Matures into:</strong> <em>Quartz sandstone</em></div>
                </div>
            </div>
                        
            <div class="specimen-card">
                <h3 class="specimen-name">Chert{#if getRockThumbnail('Chert')}<img class="rock-thumb" src={getRockThumbnail('Chert')} alt="Chert thumbnail" loading="lazy" />{/if}
                    <button class="model-btn" on:click={() => open3DModal('Chert')} title="View 3D Model"><Cube size={18} /></button>
                </h3>
                <div class="specimen-description">Hard, dense; conchoidal fracture; dull to waxy luster.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Composition:</strong> Microcrystalline quartz</div>
                    <div class="detail-item"><strong>Environment:</strong> Deep marine; chemical or biogenic silica</div>
                    <div class="detail-item"><strong>Metamorphic equivalent:</strong> <em>Quartzite</em></div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Coal{#if getRockThumbnail('Coal')}<img class="rock-thumb" src={getRockThumbnail('Coal')} alt="Coal thumbnail" loading="lazy" />{/if}
                    <button class="model-btn" on:click={() => open3DModal('Coal')} title="View 3D Model"><Cube size={18} /></button>
                </h3>
                <div class="specimen-description">Black; lightweight; sooty streak; organic origin.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Formation:</strong> Compaction of plant material in swamps</div>
                    <div class="detail-item"><strong>Metamorphic equivalent:</strong> <em>Graphite</em></div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Conglomerate{#if getRockThumbnail('Conglomerate')}<img class="rock-thumb" src={getRockThumbnail('Conglomerate')} alt="Conglomerate thumbnail" loading="lazy" />{/if}
                    <button class="model-btn" on:click={() => open3DModal('Conglomerate')} title="View 3D Model"><Cube size={18} /></button>
                </h3>
                <div class="specimen-description">Rounded pebbles cemented together.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Environment:</strong> Rivers or beaches with strong currents</div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Dolostone{#if getRockThumbnail('Dolostone')}<img class="rock-thumb" src={getRockThumbnail('Dolostone')} alt="Dolostone thumbnail" loading="lazy" />{/if}
                    <button class="model-btn" on:click={() => open3DModal('Dolostone')} title="View 3D Model"><Cube size={18} /></button>
                </h3>
                <div class="specimen-description">Reacts weakly with acid when powdered; tan-gray color.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Composition:</strong> CaMg(CO₃)₂</div>
                    <div class="detail-item"><strong>Formation:</strong> Mg-rich fluids altering <em>Limestone</em></div>
                    <div class="detail-item"><strong>Metamorphic equivalent:</strong> <em>Dolomitic marble</em></div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Limestone{#if getRockThumbnail('Limestone')}<img class="rock-thumb" src={getRockThumbnail('Limestone')} alt="Limestone thumbnail" loading="lazy" />{/if}
                    <button class="model-btn" on:click={() => open3DModal('Limestone')} title="View 3D Model"><Cube size={18} /></button>
                </h3>
                <div class="specimen-description">Reacts with acid; usually gray to tan.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Composition:</strong> Calcite</div>
                    <div class="detail-item"><strong>Environment:</strong> Marine; biological or chemical origin</div>
                    <div class="detail-item"><strong>Metamorphic equivalent:</strong> <em>Marble</em></div>
                    <div class="detail-item"><strong>Subtypes:</strong> Chalk, Coquina, Fossiliferous, Micritic, Oolitic</div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Quartz sandstone{#if getRockThumbnail('Quartz sandstone')}<img class="rock-thumb" src={getRockThumbnail('Quartz sandstone')} alt="Quartz sandstone thumbnail" loading="lazy" />{/if}
                    <button class="model-btn" on:click={() => open3DModal('Quartz sandstone')} title="View 3D Model"><Cube size={18} /></button>
                </h3>
                <div class="specimen-description">Gritty; mostly quartz; often light-colored.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Environment:</strong> Beach or desert</div>
                    <div class="detail-item"><strong>Metamorphic equivalent:</strong> <em>Quartzite</em></div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Gypsum{#if getRockThumbnail('Gypsum')}<img class="rock-thumb" src={getRockThumbnail('Gypsum')} alt="Gypsum thumbnail" loading="lazy" />{/if}
                    <button class="model-btn" on:click={() => open3DModal('Rock gypsum')} title="View 3D Model"><Cube size={18} /></button>
                </h3>
                <div class="specimen-description">Soft; white/pink; scratched by fingernail.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Type:</strong> Evaporite deposit; CaSO₄·2H₂O</div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Rock salt{#if getRockThumbnail('Rock salt')}<img class="rock-thumb" src={getRockThumbnail('Rock salt')} alt="Rock salt thumbnail" loading="lazy" />{/if}
                    <button class="model-btn" on:click={() => open3DModal('Rock salt')} title="View 3D Model"><Cube size={18} /></button>
                </h3>
                <div class="specimen-description">Transparent cubic crystals; salty taste.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Type:</strong> Evaporite deposit; NaCl</div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Mudstone{#if getRockThumbnail('Mudstone')}<img class="rock-thumb" src={getRockThumbnail('Mudstone')} alt="Mudstone thumbnail" loading="lazy" />{/if}
                    <button class="model-btn" on:click={() => open3DModal('Mudstone')} title="View 3D Model"><Cube size={18} /></button>
                </h3>
                <div class="specimen-description">Fine-grained; non-fissile (doesn't split easily); blocky fracture.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Composition:</strong> Clay and silt</div>
                    <div class="detail-item"><strong>Environment:</strong> Quiet water environments</div>
                    <div class="detail-item"><strong>Related to:</strong> <em>Shale</em> (fissile) and <em>Siltstone</em> (coarser)</div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Sandstone{#if getRockThumbnail('Sandstone')}<img class="rock-thumb" src={getRockThumbnail('Sandstone')} alt="Sandstone thumbnail" loading="lazy" />{/if}
                    <button class="model-btn" on:click={() => open3DModal('Sandstone')} title="View 3D Model"><Cube size={18} /></button>
                </h3>
                <div class="specimen-description">Medium-grained; composed of sand-sized particles; often cross-bedded.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Environment:</strong> Desert, beach, or shallow marine</div>
                    <div class="detail-item"><strong>Metamorphic equivalent:</strong> <em>Quartzite</em></div>
                    <div class="detail-item"><strong>Subtypes:</strong> <em>Arkose</em>, <em>Quartz sandstone</em></div>
                </div>
            </div>

            <div class="specimen-card">
                <h3 class="specimen-name">Shale{#if getRockThumbnail('Shale')}<img class="rock-thumb" src={getRockThumbnail('Shale')} alt="Shale thumbnail" loading="lazy" />{/if}
                    <button class="model-btn" on:click={() => open3DModal('Shale')} title="View 3D Model"><Cube size={18} /></button>
                </h3>
                <div class="specimen-description">Fine-grained; splits into thin sheets; dull luster.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Composition:</strong> Clay minerals</div>
                    <div class="detail-item"><strong>Environment:</strong> Quiet water (lakes, deep marine)</div>
                    <div class="detail-item"><strong>Metamorphic sequence:</strong> <em>Slate → Phyllite → Schist → Gneiss</em></div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Siltstone{#if getRockThumbnail('Siltstone')}<img class="rock-thumb" src={getRockThumbnail('Siltstone')} alt="Siltstone thumbnail" loading="lazy" />{/if}
                    <button class="model-btn" on:click={() => open3DModal('Siltstone')} title="View 3D Model"><Cube size={18} /></button>
                </h3>
                <div class="specimen-description">Fine-grained; gritty feel when rubbed; intermediate between sandstone and shale.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Grain size:</strong> Silt (1/16 - 1/256 mm)</div>
                    <div class="detail-item"><strong>Environment:</strong> Quiet water with some current activity</div>
                    <div class="detail-item"><strong>Related to:</strong> <em>Mudstone</em> and <em>Shale</em></div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Travertine{#if getRockThumbnail('Travertine')}<img class="rock-thumb" src={getRockThumbnail('Travertine')} alt="Travertine thumbnail" loading="lazy" />{/if}
                    <button class="model-btn" on:click={() => open3DModal('Travertine')} title="View 3D Model"><Cube size={18} /></button>
                </h3>
                <div class="specimen-description">Porous limestone; often banded; forms around hot springs.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Formation:</strong> Precipitation from calcium-rich groundwater</div>
                    <div class="detail-item"><strong>Environment:</strong> Hot springs, caves, or streams</div>
                    <div class="detail-item"><strong>Related to:</strong> <em>Limestone</em></div>
                </div>
            </div>
        </div>
        </details>
    
    
                <details class="category-section">
                    <summary class="category-title">🔥 Metamorphic Rocks</summary>
                    <div class="specimens-grid">
            <div class="specimen-card">
                <h3 class="specimen-name">Amphibolite{#if getRockThumbnail('Amphibolite')}<img class="rock-thumb" src={getRockThumbnail('Amphibolite')} alt="Amphibolite thumbnail" loading="lazy" />{/if}
                    <button class="model-btn" on:click={() => open3DModal('Amphibolite')} title="View 3D Model"><Cube size={18} /></button>
                </h3>
                <div class="specimen-description">Dark, coarse-grained; amphibole-rich; may show weak foliation.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Parent:</strong> <em>Basalt</em> or <em>Gabbro</em></div>
                    <div class="detail-item"><strong>Grade:</strong> Medium–high</div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Gneiss{#if getRockThumbnail('Gneiss')}<img class="rock-thumb" src={getRockThumbnail('Gneiss')} alt="Gneiss thumbnail" loading="lazy" />{/if}
                    <button class="model-btn" on:click={() => open3DModal('Gneiss')} title="View 3D Model"><Cube size={18} /></button>
                </h3>
                <div class="specimen-description">Alternating light/dark bands; coarse foliation.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Parent:</strong> <em>Granite</em> or <em>Schist</em></div>
                    <div class="detail-item"><strong>Grade:</strong> High</div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Metaconglomerate{#if getRockThumbnail('Metaconglomerate')}<img class="rock-thumb" src={getRockThumbnail('Metaconglomerate')} alt="Metaconglomerate thumbnail" loading="lazy" />{/if}
                    <button class="model-btn" on:click={() => open3DModal('Metaconglomerate')} title="View 3D Model"><Cube size={18} /></button>
                </h3>
                <div class="specimen-description">Pebbles deformed or stretched within finer matrix.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Parent:</strong> <em>Conglomerate</em></div>
                    <div class="detail-item"><strong>Grade:</strong> Variable</div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Hornfels{#if getRockThumbnail('Hornfels')}<img class="rock-thumb" src={getRockThumbnail('Hornfels')} alt="Hornfels thumbnail" loading="lazy" />{/if}
                    <button class="model-btn" on:click={() => open3DModal('Hornfels')} title="View 3D Model"><Cube size={18} /></button>
                </h3>
                <div class="specimen-description">Fine-grained; hard; non-foliated; contact metamorphic rock.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Parent:</strong> Various rocks (shale, sandstone, etc.)</div>
                    <div class="detail-item"><strong>Formation:</strong> Contact metamorphism near igneous intrusions</div>
                    <div class="detail-item"><strong>Grade:</strong> Medium–high</div>
                </div>
            </div>

            <div class="specimen-card">
                <h3 class="specimen-name">Marble{#if getRockThumbnail('Marble')}<img class="rock-thumb" src={getRockThumbnail('Marble')} alt="Marble thumbnail" loading="lazy" />{/if}
                    <button class="model-btn" on:click={() => open3DModal('Marble')} title="View 3D Model"><Cube size={18} /></button>
                </h3>
                <div class="specimen-description">Crystalline; reacts with acid; sugary texture; usually white.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Parent:</strong> <em>Limestone</em> or <em>Dolostone</em></div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Phyllite{#if getRockThumbnail('Phyllite')}<img class="rock-thumb" src={getRockThumbnail('Phyllite')} alt="Phyllite thumbnail" loading="lazy" />{/if}
                    <button class="model-btn" on:click={() => open3DModal('Phyllite')} title="View 3D Model"><Cube size={18} /></button>
                </h3>
                <div class="specimen-description">Silky sheen; fine-grained; wavy foliation.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Parent:</strong> <em>Slate</em> (from shale)</div>
                    <div class="detail-item"><strong>Grade:</strong> Low–medium</div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Quartzite{#if getRockThumbnail('Quartzite')}<img class="rock-thumb" src={getRockThumbnail('Quartzite')} alt="Quartzite thumbnail" loading="lazy" />{/if}
                    <button class="model-btn" on:click={() => open3DModal('Quartzite')} title="View 3D Model"><Cube size={18} /></button>
                </h3>
                <div class="specimen-description">Hard; sugary texture; scratches glass; fused quartz grains.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Parent:</strong> <em>Quartz sandstone</em></div>
                    <div class="detail-item"><strong>Grade:</strong> Any</div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Schist{#if getRockThumbnail('Schist')}<img class="rock-thumb" src={getRockThumbnail('Schist')} alt="Schist thumbnail" loading="lazy" />{/if}
                    <button class="model-btn" on:click={() => open3DModal('Schist')} title="View 3D Model"><Cube size={18} /></button>
                </h3>
                <div class="specimen-description">Sparkly mica-rich foliation; medium to coarse-grained.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Parent:</strong> <em>Phyllite</em> or <em>Shale</em></div>
                    <div class="detail-item"><strong>Grade:</strong> Medium–high</div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Serpentinite{#if getRockThumbnail('Serpentinite')}<img class="rock-thumb" src={getRockThumbnail('Serpentinite')} alt="Serpentinite thumbnail" loading="lazy" />{/if}
                    <button class="model-btn" on:click={() => open3DModal('Serpentinite')} title="View 3D Model"><Cube size={18} /></button>
                </h3>
                <div class="specimen-description">Greenish, waxy luster; slick feel; derived from ultramafic rock.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Parent:</strong> <em>Peridotite</em> (hydrated olivine)</div>
                    <div class="detail-item"><strong>Grade:</strong> Low</div>
                </div>
            </div>
            
            <div class="specimen-card">
                <h3 class="specimen-name">Slate{#if getRockThumbnail('Slate')}<img class="rock-thumb" src={getRockThumbnail('Slate')} alt="Slate thumbnail" loading="lazy" />{/if}
                    <button class="model-btn" on:click={() => open3DModal('Slate')} title="View 3D Model"><Cube size={18} /></button>
                </h3>
                <div class="specimen-description">Dark gray; very fine-grained; splits into flat sheets with a "ping" sound.</div>
                <div class="specimen-details">
                    <div class="detail-item"><strong>Parent:</strong> <em>Shale</em></div>
                    <div class="detail-item"><strong>Grade:</strong> Low</div>
                </div>
            </div>
        </div>
        </details>
</div>

<Modal
    bind:open={modalOpen}
    component={modalComponent}
    props={modalProps}
    title={modalTitle}
/>

<style>
    .model-btn {
        appearance: none;
        border: 1px solid color-mix(in srgb, var(--accent) 45%, #ccc 55%);
        background: white;
        color: var(--ink);
        padding: .35rem .55rem;
        border-radius: 8px;
        font-weight: 600;
        cursor: pointer;
        transition: transform .04s ease, box-shadow .15s ease, border-color .15s ease, background .15s ease;
        margin-left: 0.5em;
        vertical-align: middle;
        display: inline-flex;
        align-items: center;
        gap: 0.25rem;
    }
    .model-btn:hover {
        border-color: var(--accent);
        background: color-mix(in srgb, var(--accent) 12%, white 88%);
        box-shadow: 0 6px 18px rgba(0,0,0,.08);
    }
    .model-btn:focus-visible {
        outline: none;
        box-shadow: 0 0 0 3px color-mix(in srgb, var(--accent) 40%, transparent);
    }
    .model-btn:active { 
        transform: translateY(1px); 
    }
    .rock-thumb {
        width: 38px;
        height: 38px;
        object-fit: cover;
        border-radius: 6px;
        margin-right: 0.5em;
        vertical-align: middle;
        box-shadow: 0 1px 4px rgba(0,0,0,0.10);
    }
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
    .specimen-name img.rock-thumb {
        margin-left: auto;
        margin-right: 0;
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
    
</style>

