# ascii-maker

Yet another (slow) image to ascii art converter.

```

       ywwww|  |wwww,
       $NNNN|  $NNNN|
       $NNNN|  $NNNN|
          NN|  $NN
    )gg   NN|  $NN  )ggc
    ]NN   NN|  $NN  ]NNL
    ]NN   NN|  $NN  ]NNL
    ]NNNN|        NNNNNL
    ``````        `````

```

# Inspiration

We made this thing because most ascii art tools are really mediocre: they focus too much on larger output texts, as opposed to small ones. That makes it so that you can't really use them for small logos in the terminal and things like that.
Also, some ascii tools only care about the darkness and brightness, and not so much about the shape, whereas this tool also consider the shape of the characters in relationship to the original shape.

The downside is that this tool can be a bit slower, taking around 10 seconds (depending on cpu) to render a 60 cells square image.

# How to use

First, clone the repo and install the required dependencies using pip:

```
pip install pillow termcolor
```

Now, run the tool like this:

```
python main.py [image path]
```

You can increase or decrease the size in cells by doing:

```
python main.py --width=[cells] [image path]
```

By default, dark pixels in the image will turn into text, and white pixels will turn into empty space. If you want it to do the opposite thing, you can do:

```
python main.py --invert [image path]
```

You can also combine options like this:

```
python main.py --invert --width=30 cool_logo.png
```

# Demo
For a demo, refer to the (reddit post)[https://www.reddit.com/r/unixporn/comments/fbvk98/oc_create_ascii_art_from_images/].
