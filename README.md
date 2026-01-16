# Batch Photo to PDF

[![Built with Python](https://img.shields.io/badge/built%20with-Python-blue.svg)](https://www.python.org/)

A Python command-line utility for batch converting images from a specified directory into a single, cohesive PDF document, ordered chronologically.

This tool is especially useful for compiling screenshots of a presentation, lecture notes, or daily work logs into a single, easy-to-read file.

## Key Features

* **Batch Processing**: Converts all supported image files (`.jpg`, `.png`, etc.) in a directory.
* **Chronological Sorting**: Automatically sorts images by their file modification date (oldest first) before adding them to the PDF.
* **Orientation Control**: Set the output PDF to Portrait (`P`) or Landscape (`L`).
* **Date Filtering**: An optional flag (`--today-only`) to process only images from the current date in a directory.
* **Smart Cropping**: An optional flag (`--smart-crop`) to automatically detect and crop the main presentation slide from screenshots (e.g., Zoom, Meet), removing toolbars and participant videos.

---

## Setup and Installation

### 1. Clone the Repository

```bash
git clone https://github.com/mauri101-Ar/batch-photo-to-pdf.git
cd batch-photo-to-pdf
```

### 2. Create a Virtual Environment (Recommended)

#### For Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

#### For Windows

```bash
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install Dependencies

This project requires several Python libraries. You can install them all using the provided *requirements.txt* file.

```bash
pip install -r requirements.txt
```

## Usage

The script is run from the command line, providing a directory path, an orientation, and optional flags.  

```bash
python image_compiler.py [DIRECTORY_PATH] [ORIENTATION] [OPTIONS]
```

### Arguments

DIRECTORY_PATH: (Required) The path to the folder containing your images.  
ORIENTATION: (Required) The page orientation: **P** for Portrait or **L** for Landscape.  

### Options

**--today-only**: *(Optional)* If set, only processes images modified on the current date.  
**--smart-crop**: *(Optional)* If set, attempts to detect and crop the main presentation area, removing window borders or toolbars.  
**-h**, **--help**: Show the help message and exit.  

## Examples

### 1. Basic Conversion (Portrait)

Convert all images in the "my-notes" folder into a portrait-mode PDF.

```bash
python image_compiler.py /path/to/my-notes P
```

### 2. Landscape Mode

Convert all images in the "slides" folder into a landscape-mode PDF.

```bash
python image_compiler.py /path/to/slides L
```

### 3. Filter for Today's Images

Convert only the images from today in the "daily-work" folder.

```bash
python image_compiler.py /path/to/daily-work P --today-only
```

### 4. Smart Cropping for Screenshots

Convert all screenshots, attempting to crop out the Meet/Zoom toolbars. This is best used with landscape mode.

```bash
python image_compiler.py /path/to/screenshots L --smart-crop
```

### 5. Combined: Today's Screenshots, Cropped

Combine flags to create a PDF of only today's screenshots, with smart cropping applied.

```bash
python image_compiler.py /path/to/screenshots P --today-only --smart-crop
```

## Output File Location & Naming

The generated PDF will be saved in a new folder named **`PDF`** created inside your **current working directory** (i.e., the directory you are in when you run the `python` command).

If the `PDF` folder does not exist, the script will create it automatically.

The file name itself is automatically generated based on the input directory and options:

* **Standard (no flags):**
  * `PDF/[directory_name]_compiled.pdf`
  * *Example: `PDF/my-notes_compiled.pdf`*

* **With `--today-only` flag:**
  * `PDF/[directory_name]_today_[YYYYMMDD].pdf`
  * *Example: `PDF/my-notes_today_20251117.pdf`*

At the end of the script, the full absolute path to the generated file is printed to the console.

## Next steps (improvement options)

If you're interested in adding a feature, fixing a bug, or improving the documentation, your contributions are welcome.  
Check out the [CONTRIBUTE.md](CONTRIBUTE.md) file to learn how.  

Here are some of the features we'd love to see implemented in the future. If any of these interest you, feel free to open an issue or start working on a pull request.

* **Custom Output Path and Name**: This feature would give users full control over where the PDF is saved and what it's named. This would involve adding two optional arguments, --output-dir and --output-name, to override the default behavior of saving to the PDF/ folder.
* **Support for Different Page Sizes**: This would allow formats other than A4 by adding a --page-size argument that accepts standard strings like Letter, Legal, A3, etc.
* **Implement "Crop Profiles"** *(--crop-profile)*: This feature would replace the current --smart-crop flag with a more powerful argument that accepts specific profiles (e.g., zoom, meet, teams). This will allow for much more reliable cropping based on the screenshot source.
* **Grid Mode**: The goal is to allow users to place multiple images on a single PDF page. This could be implemented by adding an argument like --grid-size 2x2 (for 4 images) or --grid-size 1x2 (for 2 images, side-by-side). This feature will require new logic to calculate the (x, y, w, h) coordinates for each image within the page margins.
* **Package for PyPI**: To make the tool easier to install and run from anywhere, this would involve adding a pyproject.toml (or setup.py) file. This would allow users to pip install the project and run it as a simple command (e.g., batchpdf /path/fotos P) instead of python image_compiler.py.

## License

This project is licensed under the MIT License.
