// sketchfab-scrape.mjs
import fetch from "node-fetch";
import * as cheerio from "cheerio";

const UA = { "User-Agent": "Mozilla/5.0" };

function abs(base, href) {
  try { return new URL(href, base).toString(); } catch { return href || ""; }
}

function licenseNameFromCC(url = "") {
  const u = url.toLowerCase();
  if (u.includes("/publicdomain/zero/")) return "CC0 Public Domain";
  if (u.includes("/licenses/by-nc-sa/")) return "CC Attribution-NonCommercial-ShareAlike";
  if (u.includes("/licenses/by-nc-nd/")) return "CC Attribution-NonCommercial-NoDerivatives";
  if (u.includes("/licenses/by-nc/"))    return "CC Attribution-NonCommercial";
  if (u.includes("/licenses/by-sa/"))    return "CC Attribution-ShareAlike";
  if (u.includes("/licenses/by-nd/"))    return "CC Attribution-NoDerivatives";
  if (u.includes("/licenses/by/"))       return "CC Attribution";
  return "";
}

async function fetchText(url) {
  const res = await fetch(url, { headers: UA, timeout: 20000 });
  if (!res.ok) throw new Error(`HTTP ${res.status} for ${url}`);
  return res.text();
}

async function getOEmbed(modelUrl) {
  const o = new URL("https://sketchfab.com/oembed");
  o.searchParams.set("url", modelUrl);
  const res = await fetch(o, { headers: UA, timeout: 15000 });
  if (!res.ok) return null;
  return res.json();
}

export async function extract(url) {
  const link = url.split("?")[0];

  // 1) oEmbed for title/author (most robust across template tweaks)
  let title = "", author_name = "", author_url = "";
  try {
    const o = await getOEmbed(link);
    if (o) {
      title = (o.title || "").trim();
      author_name = (o.author_name || "").trim();
      author_url = (o.author_url || "").trim();
    }
  } catch { /* fall back to scrape */ }

  // 2) Scrape page for license (and fill any missing author bits)
  const html = await fetchText(link);
  const $ = cheerio.load(html);

  if (!title) {
    title = ($('meta[property="og:title"]').attr("content") || $("h1, h2").first().text() || "").trim();
  }

  // Author fallbacks (hardened): exclude non-profile hubs like /members, /community, /blog, etc.
  const BAD = /^(?:\/(?:members|community|blog|help|explore|buy|pricing|press|masters|education|museums|store)|https?:\/\/[^/]+\/(?:members|community))/i;

  if (!author_url || !author_name) {
    // Prefer the visible author block near the top (link next to avatar/name)
    const topAuthorLink =
      $('a[href]').filter((_, el) => {
        const href = ($(el).attr("href") || "").trim();
        const txt  = ($(el).text() || "").trim();
        if (!href || BAD.test(href)) return false;
        // profile pattern: /Handle or https://sketchfab.com/Handle (no extra path)
        const isProfile =
          /^\/[A-Za-z0-9_-]+\/?$/.test(href) ||
          /^https?:\/\/(www\.)?sketchfab\.com\/[A-Za-z0-9_-]+\/?$/.test(href);
        // avoid generic “Members”/“Community” text too
        const badTxt = /members|community/i.test(txt);
        return isProfile && !badTxt;
      }).first();

    if (topAuthorLink.length) {
      author_url ||= abs("https://sketchfab.com/", topAuthorLink.attr("href"));
      // Author text sometimes sits in a sibling span; try closest text node
      author_name ||= (topAuthorLink.text() || topAuthorLink.attr("title") || "").trim();
    }
  }

  // Bonus: JSON-LD (if present) to fill any remaining gaps
  if (!author_name || !author_url) {
    $('script[type="application/ld+json"]').each((_, el) => {
      try {
        const data = JSON.parse($(el).text() || "{}");
        const a = data?.author;
        if (a && typeof a === "object") {
          author_name ||= (a.name || "").trim();
          author_url  ||= (a.url || "").trim();
        }
      } catch {}
    });
  }

  // License (derive from CC URL)
  const license_url = $('a[href*="creativecommons.org"]').first().attr("href") || "";
  let license = licenseNameFromCC(license_url);

  return {
    model_3d: {
      link,
      title,
      author_name,
      author_url,
      license,
      license_url
    }
  };
}

// CLI
if (import.meta.url === `file://${process.argv[1]}`) {
  const urlArg = process.argv[2];
  if (!urlArg) {
    console.error("Usage: node sketchfab-scrape.mjs <model_url>");
    process.exit(1);
  }
  extract(urlArg)
    .then(obj => console.log(JSON.stringify(obj, null, 2)))
    .catch(err => { console.error(err); process.exit(2); });
}
