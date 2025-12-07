# webapp.py
import subprocess
import tempfile
from pathlib import Path

from flask import Flask, render_template_string, request, send_file, redirect, url_for

from pdf_to_text import extract_text

app = Flask(__name__)

TEMPLATE = """
<!doctype html>
<title>DAR List Parser</title>
<h1>DAR List Parser</h1>
<p>Upload a PDF or text file, or paste text below. Choose a parser and output format.</p>

<form method="post" enctype="multipart/form-data">
  <fieldset>
    <legend>Input</legend>
    <p>
      <label>PDF or TXT file:
        <input type="file" name="file">
      </label>
    </p>
    <p>
      <label>PDF pages (e.g. 36-43, optional):
        <input type="text" name="pages">
      </label>
    </p>
    <p>OR paste text:</p>
    <p>
      <textarea name="pasted" rows="10" cols="80"></textarea>
    </p>
  </fieldset>

  <fieldset>
    <legend>Options</legend>
    <p>
      <label><input type="radio" name="parser" value="original" checked> General parser</label>
      <label><input type="radio" name="parser" value="virginia"> Virginia parser</label>
    </p>
    <p>
      <label><input type="radio" name="format" value="psv" checked> Pipe-delimited (.csv with |)</label>
      <label><input type="radio" name="format" value="csv"> Comma-delimited (.csv)</label>
    </p>
  </fieldset>

  <p><button type="submit">Process</button></p>
</form>

{% if error %}
  <p style="color:red;">{{ error }}</p>
{% endif %}
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template_string(TEMPLATE)

    # Handle POST
    parser_choice = request.form.get("parser", "original")
    fmt = request.form.get("format", "psv")
    pages = request.form.get("pages", "").strip()
    pasted = request.form.get("pasted", "").strip()
    upload = request.files.get("file")

    if not upload and not pasted:
        return render_template_string(TEMPLATE, error="Please upload a file or paste text.")

    # create temp working dir
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)

        # Step 1: get plain text
        if upload:
            # Determine if PDF or text by extension
            filename = upload.filename or "input"
            suffix = Path(filename).suffix.lower()
            file_path = tmpdir_path / filename
            upload.save(file_path)

            if suffix == ".pdf":
                text = extract_text(file_path, pages=pages or None)
            else:
                text = file_path.read_text(encoding="utf-8", errors="ignore")
        else:
            text = pasted

        # Write text to temp file for the existing parser CLI
        input_txt = tmpdir_path / "input.txt"
        input_txt.write_text(text, encoding="utf-8")

        # Prepare output dir
        out_dir = tmpdir_path / "out"
        out_dir.mkdir(exist_ok=True)

        # Step 2: call the appropriate parser script
        if parser_choice == "virginia":
            cmd = ["python", "virginia_parser.py", str(input_txt), str(out_dir)]
            # virginia parser uses --psv to choose pipe
            if fmt == "psv":
                cmd.append("--psv")
        else:
            # original parser: --csv or --psv is mutually exclusive
            cmd = ["python", "original_parser.py", str(input_txt), str(out_dir)]
            if fmt == "psv":
                cmd.append("--psv")
            else:
                cmd.append("--csv")

        try:
            subprocess.check_call(cmd)
        except subprocess.CalledProcessError as e:
            return render_template_string(TEMPLATE, error=f"Parser failed: {e}")

        # Step 3: find the output file (same stem as input: input.csv)
        out_files = list(out_dir.glob("*.csv"))
        if not out_files:
            return render_template_string(TEMPLATE, error="No output file produced by parser.")

        output_file = out_files[0]

        # Send file to user
        return send_file(
            output_file,
            as_attachment=True,
            download_name="parsed_output.csv",
            mimetype="text/csv",
        )


if __name__ == "__main__":
    # For local testing (not in Docker)
    app.run(host="0.0.0.0", port=5000, debug=True)
