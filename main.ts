import { copyFile, mkdir } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outputDir = process.env.MAKEFUN_OUTPUT_DIR;

if (!outputDir) throw new Error("MAKEFUN_OUTPUT_DIR is required");
await mkdir(outputDir, { recursive: true });
await copyFile(resolve(here, "entry.png"), resolve(outputDir, "entry.png"));
