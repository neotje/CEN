#pragma once

#define TERN(O,A,B)         _TERN(_ENA_1(O),B,A)    // OPTION converted to '0' or '1'
#define TERN0(O,A)          _TERN(_ENA_1(O),0,A)    // OPTION converted to A or '0'
#define TERN1(O,A)          _TERN(_ENA_1(O),1,A)    // OPTION converted to A or '1'
#define TERN_(O,A)          _TERN(_ENA_1(O),,A)     // OPTION converted to A or '<nul>'
#define _TERN(E,V...)       __TERN(_CAT(T_,E),V)    // Prepend 'T_' to get 'T_0' or 'T_1'
#define __TERN(T,V...)      ___TERN(_CAT(_NO,T),V)  // Prepend '_NO' to get '_NOT_0' or '_NOT_1'
#define ___TERN(P,V...)     THIRD(P,V)              // If first argument has a comma, A. Else B.

//
// Primitives supporting precompiler REPEAT
//
#define FIRST(a,...)     a
#define SECOND(a,b,...)  b
#define THIRD(a,b,c,...) c

//
// scodes
//

#define CODE(n, f) case n: f(); break;