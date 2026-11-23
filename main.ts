// Entry for make.fun's news-image-20261122 bounty: the day's world news
// of Sunday 22 November 2026 on one newspaper front page.
//
// entry.png beside this file is the finished image; this program only
// copies those exact bytes to /output/entry.png, because the judge reads
// the file as submitted and nothing else.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
copyFileSync(new URL('./entry.png', import.meta.url), join(outDir, 'entry.png'));
