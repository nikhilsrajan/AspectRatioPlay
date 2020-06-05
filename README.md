# AspectRatioPlay
Playing with the vertices to see how the triangle's aspect ratio changes.

# What is this?

<img src="img/aspect-ratio.png"
     alt="aspect-ratio pygame window"
     width = "500"
     style="display: block; margin: auto;" />

```
    Commands:
    ---------
      <TAB> : change vertex
        <W> : move vertex up
        <S> : move vertex down
        <A> : move vertex left
        <D> : move vertex right
        <Q> : rotate triangle counter-clockwise
        <E> : rotate triangle clockwise
    <SPACE> : stop movement
        <H> : display commands
```

I wanted something which could show me what triangles of different aspect ratio looks like. <br>
This code helps me play around with the vertices of a triangle and prints out the aspect ratio in the terminal.


# How to run
I have used pipenv to manage dependencies so make sure to install that.

```
$ pip install pipenv
```

Once you have `pipenv`...

```
$ pipenv shell
$ pipenv update
```

Finally,

```
$ python AspectRatio.py
```

To exit from `pipenv` shell simply enter...

```
$ exit
```