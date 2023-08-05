htmloverpdf
===========

A wrapper for http://weasyprint.org/ which allows compositing with existing PDF files.

API: `render(html)` Input is a HTML string and output is the PDF bytes.

For weasyprint this needs `cairo` and `cairocffi` etc., this adds `poppler` for reading PDFs. These are best installed via your package manager:

::

    apt install python3-gi-cairo gir1.2-poppler-0.18 python3-cairocffi python3-lxml gir1.2-pango-1.0

It parses the HTML looking for <img> tags with src urls ending ".pdf". Each one begins a new page and copies all source pages overlaying the weasyprint output.
The magic value "blank.pdf" outputs sections HTML without overlaying.

::

    python -m htmloverpdf < test.html > test.pdf
