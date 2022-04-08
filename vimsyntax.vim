if exists("b:current_syntax")
    finish
endif


syntax case match


syntax keyword projBool on off
syntax keyword projKeyword of as to
syntax keyword projType abacus rational scroll lever chest chain dictionary

syntax match projComment /--.*$/
syntax match projIdentifier /[a-zA-Z_][a-zA-Z0-9_]*/
syntax match projNumber /\<\d*\.\?\d*\>/

syntax region projString start=/"/ skip=/\\"/ end=/"/


highlight link projBool       Boolean
highlight link projComment    Comment
highlight link projIdentifier Identifier
highlight link projKeyword    Keyword
highlight link projNumber     Number
highlight link projString     String
highlight link projType       Type
