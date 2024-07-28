from flask import Flask, request, send_file, render_template # For API
import fitz  # For PDF Manipulation

app = Flask(__name__) # Create a Flask app
app.config["DEBUG"] = True # Enable debug mode

'''
This route is used to render the HTML form for uploading the PDF file
and specifying the stamp parameters.
'''
@app.route('/')
def index():
    return render_template('stamp_pdf.html')

'''
This route is used to stamp the PDF file with the specified parameters.
It returns the stamped PDF file to the user for download.
'''
@app.route('/stamp_pdf', methods=['POST'])
def stamp_pdf():
    pdf_file = request.files['pdf']
    if not pdf_file:
        return "No file uploaded", 400

    try:
        file_path = save_uploaded_file(pdf_file)
        doc = fitz.open(file_path)

        pages = request.form.get('pages', '0')
        page_numbers = parse_page_numbers(pages, doc)

        size = request.form.get('size', None)
        w, h = parse_size(size)

        color = request.form.get('color', 'Black')

        stamp_elements = request.form.get('stamp_elements', 'h1,h2,h3')
        h1 = request.form.get('h1', '')
        h2 = request.form.get('h2', '')
        h3 = request.form.get('h3', '')

        elements = {'h1': h1, 'h2': h2, 'h3': h3}
        stamp_content = prepare_stamp_content(elements, stamp_elements)
        if not stamp_content.strip():
            return "No text content provided", 400

        link = request.form.get('link', None)

        rotation = int(request.form.get('rotation', '0'))
        frame = request.form.get('frame', 'False').lower() == 'true'

        for page_num in page_numbers:
            page = doc.load_page(page_num)
            rect = find_empty_space_in_top_30_percent(page, w, h)
            if not rect:
                return "No empty space found in the top 30% of the document", 400
            insert_stamp(page, rect, stamp_content, color, rotation, frame)

        output_path = 'stamped.pdf'
        doc.save(output_path)
        doc.close()

        return send_file(output_path, as_attachment=True, download_name='stamped.pdf')
    except Exception as e:
        return str(e), 500

'''
This function uploads the selected PDF file to the current directory.
'''
def save_uploaded_file(pdf_file):
    file_path = "uploaded.pdf"
    pdf_file.save(file_path)
    return file_path

'''
This function parses the page numbers from the form.
Its default value is '-1' which selects every page.
Otherwise, it selects the specified page numbers.
'''
def parse_page_numbers(pages, doc):
    if pages == '-1':
        return list(range(len(doc)))
    else:
        return [int(p.strip()) for p in pages.split(',') if p.strip().isdigit()]

'''
This function parses the size parameter from the form.
Its default value is '80,80' which sets the width and height of the stamp to 80 points.
'''
def parse_size(size):
    if size and ',' in size:
        try:
            w, h = map(float, size.split(','))
            return w, h
        except ValueError:
            raise ValueError("Invalid size parameter")
    else:
        return 80, 80  # Default width and height

'''
This function prepares the stamp content by order of the elements.
The elements and their order are provided in the form input.
'''
def prepare_stamp_content(elements, stamp_elements):
    stamp_content = ''
    for elem in stamp_elements.split(','):
        if elem in elements and elements[elem]:
            stamp_content += elements[elem] + '\n'
    return stamp_content

'''
This function finds an empty space in the top 30% of the page by
iterating over the page in steps of 5 points.
It takes the page object, width, and height of the stamp as input.
'''
def find_empty_space_in_top_30_percent(page, w, h):
    top_30_percent_height = page.rect.height * 0.3
    step = 5  # Move 5 points each time when searching for empty space
    for y in range(0, int(top_30_percent_height), step):
        for x in range(0, int(page.rect.width), step):
            rect = fitz.Rect(x, y, x + w, y + h)
            if is_empty_space(page, rect):
                return rect
    return None

'''
This function checks if the given rectangle is an empty space
by looking for a text box on the page.
'''
def is_empty_space(page, rect):
    text = page.get_textbox(rect)
    return text.strip() == ''

'''
This function inserts the stamp content into the given rectangle.
It also draws a frame around the stamp if the frame parameter is True.
'''
def insert_stamp(page, rect, stamp_content, color, rotation, frame):
    page.insert_textbox(rect, stamp_content.strip(), fontsize=12, color=fitz.utils.getColor(color), rotate=rotation)
    if frame:
        page.draw_rect(rect, color=fitz.utils.getColor(color), width=1)

if __name__ == "__main__": # Run the Flask app
    app.run(debug=True)
