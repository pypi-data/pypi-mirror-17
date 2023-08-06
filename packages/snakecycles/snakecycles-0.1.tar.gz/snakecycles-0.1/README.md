SnakeCycles
===========

Parse snakefood's output to detect import cycles.

Usage:

    sfood | snakecycles
    
Of course, you can clean sfood's output with `grep -v`

    sfood | grep -v virtualenv | snakecycles
    
