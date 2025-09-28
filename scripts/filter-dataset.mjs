import { promises as fs } from "fs";
import path from "path";

const SRC = new URL("../static/rocks", import.meta.url).pathname;   // your dataset root
const DEST = new URL("../static/filtered", import.meta.url).pathname;

// ✅ Allowed folder names (from our curated rock + mineral lists)
const ALLOWED = new Set([
  // Igneous
  "peridotite", "basalt", "gabbro", "andesite", "diorite", "rhyolite", "granite", "tuff",
  // Sedimentary
  "mudstone", "shale", "siltstone", "sandstone", "conglomerate",
  "rock_salt", "rock_gypsum", "travertine", "limestone", "chert", "coal",
  // Metamorphic
  "slate", "phyllite", "schist", "gneiss", "hornfels", "quartzite", "marble", "migmatite",
  // Minerals
  "quartz", "plagioclase_feldspar", "potassium_feldspar", "muscovite_mica",
  "biotite_mica", "olivine", "pyroxene", "amphibole",
  "calcite", "gypsum", "halite", "hematite", "magnetite",
  "garnet", "kyanite", "staurolite", "corundum"
]);

async function copyDir(src, dest) {
  await fs.mkdir(dest, { recursive: true });
  const entries = await fs.readdir(src, { withFileTypes: true });
  for (const entry of entries) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);
    if (entry.isDirectory()) {
      await copyDir(srcPath, destPath);
    } else if (entry.isFile()) {
      await fs.copyFile(srcPath, destPath);
    }
  }
}

async function main() {
  await fs.mkdir(DEST, { recursive: true });
  const items = await fs.readdir(SRC, { withFileTypes: true });

  for (const item of items) {
    if (!item.isDirectory()) continue;
    const folder = item.name;

    // normalize folder names to match ALLOWED
    const norm = folder.toLowerCase().replace(/\s+/g, "_");
    if (ALLOWED.has(norm)) {
      console.log(`✅ Copying ${folder}`);
      await copyDir(path.join(SRC, folder), path.join(DEST, folder));
    } else {
      console.log(`❌ Skipping ${folder}`);
    }
  }

  console.log("Done filtering dataset.");
}

main().catch((err) => {
  console.error("Error:", err);
  process.exit(1);
});
