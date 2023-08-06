### TravisCI Build status:
![image](https://travis-ci.org/dunovank/jupyter-themes.svg?branch=develop)

### Interactive Binder Demo
[![Binder](http://mybinder.org/badge.svg)](http://mybinder.org:/repo/dunovank/jupyter-themes)

### Links
[jupyterthemes on PyPI](https://pypi.python.org/pypi/jupyterthemes/)

[jupyterthemes on GitHub](https://github.com/dunovank/jupyter-themes)

### Install with pip
```sh
pip install jupyterthemes
```

### Command Line Usage
```
usage: jt [-h] [-l] [-t THEME] [-f MONOFONT] [-fs MONOSIZE] [-nf NBFONT]
          [-nfs NBFONTSIZE] [-tf TCFONT] [-tfs TCFONTSIZE] [-m MARGINS]
          [-cursw CURSORWIDTH] [-cursc CURSORCOLOR] [-cellw CELLWIDTH]
          [-lineh LINEHEIGHT] [-alt] [-vim] [-T] [-N] [-r]
```


|        options        |   arg     |     default   |
|:----------------------|:---------:|:-------------:|
| Usage help            |  -h       |      --       |
| List Themes           |  -l       |      --       |
| Theme Name to Install |  -t       |      --       |
| Code Font             |  -f       |   droidmono   |
| Code Font-Size        |  -fs      |      11       |
| Notebook Font         |  -nf      |    exosans    |
| Notebook Font Size    |  -nfs     |      13       |
| Text/MD Cell Font     |  -tf      |   loraserif   |
| Text/MD Cell Fontsize |  -tfs     |      13       |
| Intro Page Margins    |  -m       |     auto      |
| Cell Width            |  -cellw   |      980      |
| Line Height           |  -lineh   |      170      |
| Cursor Width          |  -cursw   |       2       |
| Cursor Color          |  -cursc   |      --       |
| Alt Text/MD Layout    |  -alt     |      --       |
| Alt Prompt Layout     |  -altp    |      --       |
| Style Vim NBExt*      |  -vim     |      --       |
| Toolbar Visible       |  -T       |      --       |
| Name & Logo Visible   |  -N       |      --       |
| Restore Default       |  -r       |      --       |

\* Vim extension compatibility provided by [alextfkd](https://github.com/alextfkd)

### Examples
```sh
# list available themes
# oceans16 | grade3 | chesterish | onedork
jt -l

# select theme...
jt -t chesterish

# toggle toolbar ON and notebook name ON
jt -t grade3 -T -N

# set code font to 'Roboto Mono' 12pt
# (see monospace font table below)
jt -t oceans16 -f roboto -fs 12

# set code font to Fira Mono, 11.5pt
# 3digit font-size gets converted into float (115-->11.5)
jt -t grade3 -f fira -fs 115

# set text-cell/markdown and notebook fonts
# (see sans-serif & serif font tables below)
jt -t onedork -tf georgiaserif -nf droidsans

# adjust cell width, line-height of codecells
jt -t chesterish -cellw 900 -lineh 170

# fix the container-margins on the intro page (defaults to 'auto')
jt -t onedork -m 200

# adjust cursor width (in px) and make cursor red (r)
# options: b (blue), o (orange), r (red), p (purple), g (green)
jt -t grade3 -cursc r -cursw 5

# toggle toolbar ON and notebook name ON
jt -t grade3 -T -N

# choose alternate txt/markdown layout (-alt)
# and alternate cell prompt (narrow, no numbers)
jt -t grade3 -alt -altp

# restore default theme
jt -r
```



