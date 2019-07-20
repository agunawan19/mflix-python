$path = ".\venv"

If (!(test-path $path)) {
    py -m venv $path
}

.\venv\Scripts\activate

pip install -r .\requirements.txt