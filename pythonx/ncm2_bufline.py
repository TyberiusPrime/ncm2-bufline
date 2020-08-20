# -*- coding: utf-8 -*-

import vim
from ncm2 import Ncm2Source, getLogger
import re
from copy import deepcopy

logger = getLogger(__name__)


class Source(Ncm2Source):

    def on_complete(self, ctx):
        lines = 1000

        lnum = ctx['lnum']
        ccol = ctx['ccol']
        b = ctx['typed'].strip()

        bufnr = ctx['bufnr']
        buf = vim.buffers[bufnr]

        matches = []

        matcher = self.matcher_get(ctx)

        matches = []
        seen = {}

        beginl = max(lnum - 1 - int(lines / 2), 0)
        endl = lnum - 1 + int(lines / 2)
        stepl = 1000

        for lidx in range(beginl, endl, stepl):
            lines = buf[lidx: min(lidx + stepl, endl)]

            # convert 0 base to 1 base
            for i, line in enumerate(lines):
                if line.strip().startswith(b):
                    scan_lnum = lidx + i + 1
                    if scan_lnum != lnum:
                        item = self.match_formalize(ctx, line.strip())
                        matches.append(item)

        self.complete(ctx, ctx['startccol'], matches)


source = Source(vim)

on_complete = source.on_complete
