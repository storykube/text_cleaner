# Storykube Text Cleaner
A really rough text cleaner with an ugly code. **But very useful**. 
We've taken the liberty here of following all the worst bad practices. Make good use of the micro ugly library.

## How to install.

First of all, **install the storykube sentence tokenizer**

```bash
pip3 install git+https://github.com/storykube/sentence-tokenizer.git
```

Then:
```bash
pip3 install git+https://github.com/storykube/text_cleaner.git
```

## Usage.
```python
#!/usr/bin/python3
from text_cleaner import Clean


r = Clean.that("ON YOUTUBE FRIDAY morning, several hundred viewers watched a live?animated video of a female Minecraft avatar with bare breasts opening a present full of the poop emoji. In the video’s thumbnail, two inflated breasts held up a poop Minecraft brick.")

print(r)
```