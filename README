# PDF Stamper App

## Files
- `app.py`: The main Python file containing the Flask application and PDF manipulation logic.
- `stamp_pdf.html`: The HTML template for the web form where users can upload a PDF and specify stamping parameters.

## Instalization
- pip install Flask PyMuPDF

## Run Code
- flask run

## Routes
- `/`
    - Method: GET
    - Description: Renders the HTML form for uploading the PDF file and specifying the stamp parameters.
- `/stamp_pdf`
    - Method: POST
    - Description: Processes the uploaded PDF file and stamps it with the specified parameters. Returns the stamped PDF file for download.

## Form Parameters
- `pdf`: The PDF file to be stamped (required).
- `pages`: Pages to stamp (comma-separated, -1 for all pages).
- `size`: Stamp size in the format width,height (default is 80,80).
- `color`: Color of the stamp (default is Black).
- `h1`, `h2`, `h3`: Text content for the stamp.
- `stamp_elements`: Order of elements to be included in the stamp (default is h1,h2,h3).
- `link`: Link associated with the stamp (optional).
- `rotation`: Rotation angle of the stamp in degrees (default is 0).
- `frame`: Draw a frame around the stamp (checkbox, optional).

## Functions
- `save_uploaded_file(pdf_file)`: Uploads the selected PDF file to the current directory.
- `parse_page_numbers(pages, doc)`: Parses the page numbers from the form input. Selects all pages if the input is -1.
- `parse_size(size)`: Parses the size parameter from the form input. Default is 80,80.
- `prepare_stamp_content(elements, stamp_elements)`: Prepares the stamp content by the order of the elements provided in the form input.
- `find_empty_space_in_top_30_percent(page, w, h)`: Finds an empty space in the top 30% of the page for the stamp.
- `is_empty_space(page, rect)`: Checks if the given rectangle is an empty space on the page.
- `insert_stamp(page, rect, stamp_content, color, rotation, frame)`: Inserts the stamp content into the specified rectangle. Draws a frame around the stamp if specified.

## Error Handling
The application provides error messages for common issues, such as no file uploaded, invalid size parameter, and no empty space found for the stamp.

