Halt is Defeat
==============

Halt is Defeat is a "time-traveling" programming language, making use of
the features of the `Sphinx <https://github.com/benburrill/sphinx>`_
instruction set architecture.

By the end of the semester, I had only finished the typechecker and had
not started on the code generator.  This repo only has the work I did
during the semester.  Since then, I finished the code generator and
added new features.  For the current version (which also has better
documentation explaining what the heck this language even is and what I
mean by time-travel), see:
https://github.com/benburrill/halt_is_defeat.

:sup:`(I would've sent the code generator back in time, but I'm pretty
sure plagiarizing from your future-self would be a form of academic
dishonesty)`

Anyway, there are probably a few takeaways you can get from here, even
if you're making a less-weird language.

Parser:
    One thing that was perhaps a little over-engineered, but I think was
    pretty neat, was my use of coroutines to manage the parser context.
    You can see what it looks like in hidc/parser/grammar.py.

    Calling a ``Parser.routine``-decorated coroutine returns a reusable
    parsing "rule", which consumes tokens when awaited.  If the rule
    doesn't match (returns None), it is backtracked automatically, or
    if wrapped by ``expect()`` it will raise an error (with an
    auto-generated error message) in that case.
    
    The nice thing is you can parameterize the parser rules and pass them
    to other generic rules, or just plain coroutines like ``comma_list``
    and ``bin_op``, and it's all fairly simple to implement.  You don't
    really need coroutines for this sort of thing, but there's something
    to it I think.

Type-checker:
    For analyzing the control flow, I have a method for blocks which
    returns a flag enum of possible ways the block could "exit" (return,
    infinite loop, etc), see hidc/ast/blocks.py.
    
    In this version, ``LoopBlock.exit_modes`` was bugged (fixed in
    https://github.com/benburrill/halt_is_defeat), but I think the
    overall approach with the flag enums is pretty nice and flexible so
    long as you don't have particularly complicated control flow (like
    labeled blocks).
    
    There are some weird type coercion rules in this version, which I
    have since simplified somewhat.  I'd probably avoid/postpone doing
    implicit type-coercions if I was to do this project again, as it
    turned out to be more complicated than I expected and no matter what
    type-coercion rules I chose, I was always a bit dissatisfied with
    some aspect of it.

Code generator:
    The code generator
    (`hidc/codegen/generator.py <https://github.com/benburrill/halt_is_defeat/blob/main/hidc/codegen/generator.py>`_)
    is a bit of a mess, but one of the things I do like from it is the
    abstraction of the ``Bubble``\ s and ``Accessor``\ s which made
    managing the stack pretty easy and allowed for a few simple
    optimizations without much effort.
    
    The bigger takeaway though is probably in the calling conventions
    and in choosing language features that can be implemented without
    dynamic allocation (if you're targetting a low-level target without
    malloc/free).
    
    As long as you're not trying to create a real-world compiler, you
    have the freedom to choose whatever calling conventions and stack
    layout you want.
    For example, I don't use a *stack pointer* (pointing to the top of
    the call stack), I just use a *frame pointer* (pointing to the
    bottom of the function's call frame).  This might be a problem if
    there were hardware interrupts, but I don't care since that would be
    a form of real-time external input (which would require an actual
    time-machine to implement for the Sphinx architecture).  This
    somewhat simplifies the management of the stack, since I only ever
    need to update the frame pointer before and after function calls.
    
    I also don't have dynamic allocation, but I do allow variable-length
    stack-allocated arrays (similar to C's VLAs/alloca, but with array
    usage restrictions to make it safe).  Unlike C though, I can use the
    other end of the stack (where the heap would be) to put my VLAs,
    which simplifies the implementation.
