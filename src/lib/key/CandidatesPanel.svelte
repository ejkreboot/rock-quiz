<script>



$: raw = names.map(n => ({ name:n, score: scoreRock(n) }));
$: max = Math.max(0, ...raw.map(r=>r.score));
$: ranked = raw
.map(r => ({ ...r, pct: max>0 ? Math.round((r.score/max)*100) : 0 }))
.sort((a,b)=> b.pct - a.pct)
.slice(0, 8);


function practiceURL(){
    const top = ranked.filter(r=>r.pct>0).slice(0,4).map(r=>r.name).join(',');
    return top ? `/?types=${encodeURIComponent(top)}` : '/';
}
</script>


<section class="cp">
    <h3>Likely matches</h3>
    {#if max === 0}
    <p class="muted">Start choosing features to see candidates.</p>
    {:else}
    <ul class="list">
        {#each ranked as r}
        <li>
            <div class="row">
                <div class="name">{r.name}</div>
                <div class="pct">{r.pct}%</div>
            </div>
            <div class="bar"><span style={`width:${r.pct}%`}></span></div>
        </li>
        {/each}
    </ul>
    <a class="btn" href={practiceURL()}>Practice these</a>
    {/if}
</section>


<style>
    .cp { border:1px solid var(--ri-border, rgba(0,0,0,.1)); border-radius:12px; padding:12px 14px; background:#fff; }
    .cp h3 { margin:0 0 8px 0; font: 700 16px/1.3 Quicksand, system-ui, sans-serif; }
    .muted { color:#6b7280; margin:6px 0 0 0; }
    .list { list-style:none; margin:8px 0 12px; padding:0; display:grid; gap:10px; }
    .row { display:flex; align-items:center; gap:8px; }
    .row .name { font-weight:600; }
    .row .pct { margin-left:auto; color:#6b7280; font-size:0.9rem; }
    .bar { height:8px; background:#edf2f7; border-radius:999px; overflow:hidden; }
    .bar span { display:block; height:100%; background: linear-gradient(90deg, #85b7b6, #0ea5e9); }
    .btn { display:inline-block; margin-top:8px; padding:8px 12px; border-radius:10px; border:1px solid rgba(0,0,0,.1); text-decoration:none; color:inherit; background:#f6f7f9; }
</style>