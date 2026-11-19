// news-image-20261118 entry (Node 22, standard library only): the image is
// the entry.png beside this file, drawn for this bounty with the
// render_frontpage.py script in this repository (PIL, no network, no
// randomness — re-running the script writes the same bytes), and the program
// copies it to /output/entry.png. The gate takes a whole PNG or JPEG of at
// most 1 MiB and 1024 by 1024 pixels, and the judge sees exactly the bytes
// copied.
//
// The image: a 1024x1024 PNG of 151,409 bytes (under the 1 MiB gate limit),
// drawn from the verified news of Wednesday 18 November 2026 — Iran's
// strikes on U.S. bases in Kuwait and Bahrain, the Xi–Putin meeting in
// Shenzhen, Peltola's Alaska win, Voyager 1's one light-day, and the Congo
// Ebola outbreak — by render_frontpage.py in this repository.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, statSync } from 'node:fs';
import { dirname, join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
const dest = join(outDir, 'entry.png');
copyFileSync(new URL('./entry.png', import.meta.url), dest);
// The gate reads exactly the bytes copied: confirm the copy landed whole.
const srcSize = statSync(new URL('./entry.png', import.meta.url)).size;
const dstSize = statSync(dest).size;
if (srcSize !== dstSize) throw new Error(`entry.png copy incomplete: ${dstSize} of ${srcSize} bytes`);
