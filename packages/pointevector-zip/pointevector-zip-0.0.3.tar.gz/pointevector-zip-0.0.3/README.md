# Overview
Process a ZIP file in a single-pass stream without loading the whole archive into memory.

# Usage
```
import pointevector.zip

parser = pointevector.zip.StreamParser()
for chunk in chunks():
    for header, file_data in parser.feed(chunk):
        pass # Do something with the file
    
    # (Optional) Stop when no more files are in the archive
    if parser.end_of_files:
        break
```
