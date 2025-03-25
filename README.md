# arc: Send encrypted emails that your kids can read in the future.

* Create email addresses for your kids when they're born.
* Send them encrypted emails so that they're timestampped and you can talk about whatever is top of mind.
* Keep the decryption key, and (TODO) set some schedule by which you'll share the decryption keys with them.

## How it works:

```sh
arc send --recipient daughter@example.com letter.md
```

## Send to multiple recipients

```sh
arc send --recipient daughter1@example.com --recipient daughter2@example.com letter.md
```

## With subject

arc send --recipient daughter@example.com --subject "Happy Birthday" letter.md

```sh
arc send --recipient daughter@example.com --subject "Happy Birthday" letter.md
```

## With a folder

arc will automatically make a tar archive for you.

```sh
arc send --recipient daughter@example.com --subject "Happy Birthday" folder/
```

## Using uv

```sh
uv run python -m arc.cli --child1 send /Users/omar/Desktop/test-message.md
```

## Dedication

To my daughters:

An Arc can mean many things. In this case, an arc is meant as a continuation. We overlap now but who knows how many moments we will have together?

Even though I might seem absent-minded sometimes, deeply focused on some problem, in my office, typing away, please know that I think about you two all the time and you never leave my mind.
