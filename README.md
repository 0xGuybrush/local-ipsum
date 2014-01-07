#Local Ipsum

A Python web-based app that will strip the text content from a HTML page & replace with *lorem ipsum* text in a given language. Will also increase text length by ~30% (as a crude mesaure of translated languages often increasing in volume).

Developed just for fun, has reasonable success though struggles with some JavaScript injected content.

##Potential uses

Allows designers, developers and testers a quick way to view potential impact of localisation being retro-fitted onto a page, especially into non-Latin scripts. For example, it could be used to highlight:

+ Text currently served as images
+ Right-to-left impact
+ Overflow caused by longer text content
+ Text being injected via JavaScript
+ Font-size/colour contrast issues for different scripts


##Getting started

Once downloaded, simply run:

`python local-ipsum.py`

The application will run on port **8080**. Then visit in the browser:

`http://localhost:8080/ru/example.com`

##Currently supported languages

- Arabic (ar)
- Czech (cs)
- Norwegian (da)
- Greek (el)
- Hindi, (hi)
- Hebrew (iw)
- Japanese (ja)
- Korean (ko)
- Russian (ru)
- Chinese (zh)
