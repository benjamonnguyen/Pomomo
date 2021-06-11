# Purpose
This directory contains JavaScript and CSS for SquareSpace code injection into the head element of Pomomo web pages.

# Prerequisites
0. Install [npm](https://blog.npmjs.org/post/85484771375/how-to-install-npm.html)
1. Install `uglify-js` to minify JavaScript.
```shell
$ npm install -g uglify-js
```
2. Install `uglify-css` to minify CSS.
```shell
$ npm install -g uglify-css
```

# Usage
1. From the Pomomo root directory, execute the following:
```shell
$ sh website/squarespace/code-injection/bin/build.sh
```
2. Copy the contents of `Pomomo/website/squarespace/code-injection/bundle/bundle.html`.
3. Paste into SquareSpace's code injection Header field (in advanced settings).
4. Verify that the changes work.
5. Delete the directory `Pomomo/website/squarespace/bundle/` when everything looks good.
