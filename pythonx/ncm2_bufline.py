# -*- coding: utf-8 -*-

import vim
from ncm2 import Ncm2Source, getLogger

logger = getLogger(__name__)


class Source(Ncm2Source):
    def on_complete(self, ctx):
        # how many lines up/down do we complete?
        # total, not each direction
        lines = 1000

        # current buffer for lookup
        bufnr = ctx["bufnr"]
        buf = vim.buffers[bufnr]

        # where are we, what's the current line look like.
        lnum = ctx["lnum"]
        ccol = ctx["ccol"]
        b = buf[lnum - 1]
        if ccol - 1 != len(b):  # we are not at the end of the current line
            return
        b = b.strip()

        matches = [] # output buffer

        beginl = max(lnum - 1 - int(lines // 2), 0)
        endl = lnum - 1 + int(lines // 2)
        stepl = 1000 # how many lines at once do we at most query?

        for lidx in range(beginl, endl, stepl):
            lines = buf[lidx : min(lidx + stepl, endl)]

            # convert 0 base to 1 base
            for i, line in enumerate(lines):
                if line.strip().startswith(b):
                    scan_lnum = lidx + i + 1
                    if scan_lnum != lnum:
                        item = self.match_formalize(ctx, line.strip())
                        matches.append(item)

        self.complete(ctx, ctx["startccol"], matches)


source = Source(vim)

on_complete = source.on_complete
