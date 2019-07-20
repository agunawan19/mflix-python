$path = ".\venv"
$file = ".\requirements.txt"

If (!(test-path $path)) {
    py -m venv $path
}

.\venv\Scripts\activate

pip install -r $file