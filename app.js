// app.js — UI wiring. Engine lives in goblins.js, taste in pools.js.

"use strict";

const batchEl = document.getElementById("batch");
const keepersEl = document.getElementById("keepers");
const batchLabelEl = document.getElementById("batch-label");

const BATCH_SIZE = 10;
let batchNum = 0;

function reroll() {
  batchNum += 1;
  // retuned every roll so fresh keeps take effect immediately
  const pools = tunedPools(POOLS);
  const batch = generateBatch(BATCH_SIZE, pools, allKeepers());
  batchLabelEl.textContent = `batch ${batchNum}`;
  batchEl.replaceChildren(...batch.map((name) => {
    const li = document.createElement("li");
    const btn = document.createElement("button");
    btn.className = "goblin";
    btn.textContent = name;
    btn.title = "keep";
    btn.addEventListener("click", () => {
      if (keepName(name)) {
        btn.classList.add("kept");
        btn.disabled = true;
        renderKeepers();
      }
    });
    li.appendChild(btn);
    return li;
  }));
}

function renderKeepers() {
  const local = new Set(loadLocalKeepers().map((k) => k.toLowerCase()));
  keepersEl.replaceChildren(...allKeepers().map((name) => {
    const li = document.createElement("li");
    li.textContent = name;
    if (local.has(name.toLowerCase())) {
      li.className = "yours";
      const x = document.createElement("button");
      x.className = "drop";
      x.textContent = "×";
      x.title = "un-keep";
      x.addEventListener("click", () => {
        dropName(name);
        renderKeepers();
      });
      li.appendChild(x);
    }
    return li;
  }));
}

document.getElementById("reroll").addEventListener("click", reroll);

document.getElementById("copy").addEventListener("click", async (e) => {
  await navigator.clipboard.writeText(allKeepers().join("\n"));
  e.target.textContent = "Copied!";
  setTimeout(() => { e.target.textContent = "Copy list"; }, 1200);
});

renderKeepers();
reroll();
