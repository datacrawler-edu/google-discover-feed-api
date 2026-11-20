// Start one capped run, then read its persisted report and Dataset.
import { readFile } from "node:fs/promises";
import { setTimeout as delay } from "node:timers/promises";

const input = JSON.parse(await readFile(new URL("../../data/sample-input.json", import.meta.url), "utf8"));
const token = process.env.APIFY_API_TOKEN;
if (!token) throw new Error("Set APIFY_API_TOKEN before calling Apify.");
const base = "https://api.apify.com/v2/";
const actor = "datascraperes~google-discover-scraper";

async function call(path, body) {
    const response = await fetch(base + path, {
        method: body === undefined ? "GET" : "POST",
        redirect: "error",
        signal: AbortSignal.timeout(25000),
        headers: { Authorization: "Bearer " + token, "Content-Type": "application/json" },
        body: body === undefined ? undefined : JSON.stringify(body),
    });
    if (!response.ok) throw new Error("Apify returned HTTP " + response.status);
    return response.json();
}

let id;
try {
    ({ data: { id } } = await call("actors/" + actor + "/runs?timeout=120&maxTotalChargeUsd=0.01", input));
    if (!id) throw new Error("Missing run ID");
} catch (error) {
    throw new Error("Start was not confirmed. Check Apify Console before resubmitting.", { cause: error });
}
const terminal = new Set(["SUCCEEDED", "FAILED", "ABORTED", "TIMED-OUT"]);
const deadline = performance.now() + 180000;
let run;
do {
    run = (await call("actor-runs/" + encodeURIComponent(id) + "?waitForFinish=10")).data;
    if (terminal.has(run.status)) break;
    if (performance.now() >= deadline) throw new Error("Continue checking run " + id);
    await delay(1000);
} while (true);
const store = encodeURIComponent(run.defaultKeyValueStoreId);
const dataset = encodeURIComponent(run.defaultDatasetId);
const report = await call("key-value-stores/" + store + "/records/SUMMARY");
if (!Number.isInteger(report.articlesDelivered)) throw new Error("Unverified count for run " + id);
const cards = [];
for (let offset = 0; offset <= report.articlesDelivered; offset += 100) {
    const page = await call("datasets/" + dataset + "/items?limit=100&clean=false&offset=" + offset);
    cards.push(...page);
    if (page.length < 100) break;
}
if (cards.length !== report.articlesDelivered || new Set(cards.map(row => row.url)).size !== cards.length) {
    throw new Error("Dataset and SUMMARY disagree for run " + id);
}
console.log(JSON.stringify({runId: id, platformStatus: run.status, report, cards}, null, 2));
