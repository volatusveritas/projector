if exists("b:current_syntax")
    finish
endif


syntax case match


syntax keyword projType abacus rational scroll lever chest chain backpack

syntax match projNumber /\<\d*\.\?\d*\>/
syntax match projComment /--.*$/


highlight link projType    Type
highlight link projNumber  Number
highlight link projComment Comment
