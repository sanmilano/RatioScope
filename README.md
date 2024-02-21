# **RatioScope**
Introducing a user-friendly image dataset optimization app that effortlessly allows you to calculate the aspect ratios of your dataset for easy sorting, resizing, and cropping for training with bucket resolutions. The application provides pre-configured SDXL common resolutions and popular aspect ratios for swift adjustments, while also offering the flexibility to set up custom resolutions. Original images remain in their original folder, with the app creating a new folder containing copies in .png format for organized dataset management. Designed for efficient batch processing, this lightweight tool simplifies the optimization process, ensuring a seamless experience.

## **Automatic Installation for Windows:**

**Step 1:** Clone this repository or download all the files into a folder.

**Step 2:** Run `install.bat` - This will create a virtual environment and download all necessary files without affecting other Python installations on your system.

**Step 3:** Use `run.bat` to start the application.

## **Manual Installation:**

**Step 1:** Clone this repository or download all the files into a folder.

**Step 2:** Open cmd and type:
```bash
python -m venv venv
call venv\Scripts\activate
pip install pillow gradio
```

**Step 3:** Once everything is downloaded and installed, open cmd again and type:
```bash
call venv\Scripts\activate
python app.py
```

## **Automatic Installation for Linux / MacOS:**

**Step 1:** Clone this repository or download all the files into a folder.

**Step 2:** Run `install.sh` - This will create a virtual environment and download all necessary files without affecting other Python installations on your system.

**Step 3:** Use `run.sh` to start the application.

If you have any suggestions or features you would like to see added to this app, please don't hesitate to contact me!
