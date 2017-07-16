# aksakalli.github.io

source for: [aksakalli.github.io](http://aksakalli.github.io/)

## Running locally

You need Ruby and gem before starting, then:

```bash
# install jekyll and bundler
gem install jekyll bundler

# install dependencies
bundle install

# run jekyll
jekyll serve
```

## Converting Notebooks

```bash
cd notebooks
jupyter nbconvert --config jekyll.py <notebook_name>.ipynb
```

## License

[Creative Commons - Attribution-NonCommercial-ShareAlike 3.0 Unported](http://creativecommons.org/licenses/by-nc-sa/3.0/).
