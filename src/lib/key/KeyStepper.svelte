<script>
    export let features = [];
    export let selections = {}; // bind:selections
    
    
    function toggleMulti(key, id, checked) {
        const set = new Set(selections[key] || []);
        checked ? set.add(id) : set.delete(id);
        selections = { ...selections, [key]: Array.from(set) };
        dispatchChange();
    }
    
    
    function setOne(key, id) {
        selections = { ...selections, [key]: id };
        dispatchChange();
    }
    
    
    import { createEventDispatcher } from 'svelte';
    const dispatch = createEventDispatcher();
    function dispatchChange(){ dispatch('change', { selections }); }
</script>


<section class="ks">
    {#each features as f}
    <div class="card">
        <h3>{f.label}</h3>
        {#if f.type === 'one'}
        <div class="opts">
            {#each f.options as o}
            <label class="opt">
                <input type="radio" name={f.key} value={o.id}
                checked={selections[f.key] === o.id}
                on:change={() => setOne(f.key, o.id)} />
                <span>{o.label}</span>
            </label>
            {/each}
        </div>
        {:else if f.type === 'multi'}
        <div class="opts">
            {#each f.options as o}
            <label class="opt">
                <input type="checkbox" value={o.id}
                checked={(selections[f.key]||[]).includes(o.id)}
                on:change={(e) => toggleMulti(f.key, o.id, e.currentTarget.checked)} />
                <span>{o.label}</span>
            </label>
            {/each}
        </div>
        {/if}
    </div>
    {/each}
</section>


<style>
    .ks { display: grid; gap: 12px; }
    .card { border:1px solid var(--ri-border, rgba(0,0,0,.1)); border-radius:12px; padding:12px 14px; background:#fff; }
    .card h3 { margin:0 0 8px 0; font: 600 16px/1.3 Quicksand, system-ui, sans-serif; color: var(--ink,#111); }
    .opts { display:grid; gap:6px; }
    .opt { display:flex; align-items:center; gap:8px; }
</style>