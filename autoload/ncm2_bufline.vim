if get(s:, 'loaded', 0)
    finish
endif
let s:loaded = 1

let g:ncm2_bufline#proc = yarp#py3({
    \ 'module': 'ncm2_bufline',
    \ 'on_load': { -> ncm2#set_ready(g:ncm2_bufline#source)}
    \ })

let g:ncm2_bufline#source = extend(get(g:, 'ncm2_bufline#source', {}), {
            \ 'name': 'bufline',
            \ 'ready': 0,
            \ 'priority': 5,
            \ 'mark': 'l',
            \ 'on_complete': 'ncm2_bufline#on_complete',
            \ 'on_warmup': 'ncm2_bufline#on_warmup',
            \ }, 'keep')

func! ncm2_bufline#init()
    call ncm2#register_source(g:ncm2_bufline#source)
endfunc

func! ncm2_bufline#on_warmup(ctx)
    call g:ncm2_bufline#proc.jobstart()
endfunc

func! ncm2_bufline#on_complete(ctx)
    call g:ncm2_bufline#proc.try_notify('on_complete', a:ctx)
endfunc

