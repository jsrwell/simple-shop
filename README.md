# Simple Shop Manager

## Description

This project is a simple shop management system built using Python and Tkinter. It allows users to manage inventory, add, delete, and view products, and filter products by date range.

## Installation Instructions

### Clone the repository

```bash
git clone https://github.com/yourusername/yourproject.git
```

### Navigate to the project directory

```bash
cd yourproject
```

### Create and activate a virtual environment

```bash
python -m venv venv
```

For Windows:
```bash
.\venv\Scripts\activate
```

For Unix/Linux:
```bash
source venv/bin/activate
```

### Install the required dependencies

```bash
pip install -r requirements.txt
```

## Usage Instructions

### Run the application

```bash
pyinstaller --onefile --noconsole --icon=images/tkinter.png --add-data "images;images" --add-data "inventory.db;." --add-data ".venv\Lib\site-packages\babel;babel" --paths=.venv\Scripts app.py
```

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add new feature'`)
5. Push to the branch (`git push origin feature`)
6. Create a new Pull Request

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Credits

- **Author:** [Wellington Ramos (jsrwell)](https://github.com/jsrwell)
- **Email:** wellingtonjsramos@hotmail.com
