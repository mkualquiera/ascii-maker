# ascii-maker

Image to ascii art converter.

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

# How to use

Clone the repo and run:

```
./build release
```

Now, run the tool like this:

```
./bin/asciimaker
```

All options (run ``./bin/asciimaker --help``) are:

```
  -b, --background           Also change background of the text
  -c, --color                Use colors
  -d, --defaults             Treat black and white as the default background
                             and foreground colors
  -g, --grasycale            Use grayscale
  -i, --input=FILE           Input image FILE
  -o, --output[=FILE]        Output to FILE instead of standard output
  -w, --width=WIDTH          Change the width in characters of the final image
  -?, --help                 Give this help list
      --usage                Give a short usage message
  -V, --version              Print program version
```