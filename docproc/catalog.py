import os, hashlib, mimetypes, re
import os.path


def create_sha(f):
    """Create SHA1 hash of file.

    Inputs:
        f: filepath
    Outputs:
        h: SHA1 hash of file
    """
    BLOCKSIZE = 65536
    sha = hashlib.sha1()

    # Open the file and read into hash object
    with open(f, 'rb') as f:
        buf = f.read(BLOCKSIZE)
        while len(buf) > 0:
            sha.update(buf)
            buf = f.read(BLOCKSIZE)
    h = sha.hexdigest()
    return h


def get_file_name(f):
    """Get file name from file path.

    Inputs:
        f: file path
    Outputs:
        n: file name
    """
    n = f.rsplit('/',1)[-1]
    return n


def get_file_type(f):
    """Extract filetype.

    Use mimetype to extract the file type.
    Inputs:
        f: file path
    Outputs:
        t: tuple of the 2 part mimetype
    """
    try:
        mimetype = mimetypes.guess_type(f)[0]
        t = mimetype.split('/')
    except:
        t = ('nk', 'nk')
        print(f)
    return t


def create_file_metadata(f):
    """Extract file metadata.

    Create dictionary of file metadata.
    Inputs:
        f: filepath
    Outputs:
        m: dictionary of file metadata
    """
    m = dict()
    m['file_path'] = f
    m['filesize'] = os.path.getsize(f)
    #mimetype = magic.from_file(f, mime=True)
    m['fileext'] = os.path.splitext(f)[1].upper()
    m['filetype'] = get_file_type(f)
    m['filename'] = get_file_name(f)
    return m


def check_empty_file(f):
    """RULE 1: empty / black file.

    Check whether file is empty.
    Inputs:
        f: filename
    Outputs:
        boolen for check pass/fail
    """
    if os.path.getsize(f) == 0:
        return True
    else:
        return False


def check_temporary_file(f):
    """RULE 2: temporary / cache file.

    Filename begins with double underscore
    and file size is between 4096 or 4135 bytes(CHECK THE DISTRIBUTION OF FILE SIZE
    ACROSS ALL FILES BEGINNING WITH A DOUBLE UNDERSCORE).
    Inputs:
        f: filename
    Outputs:
        boolen for check pass/fail
    """
    filesize = os.path.getsize(f)
    filename = get_file_name(f)

    if filename[:2] == '__' and (filesize == 4096 or filesize == 4135):
        return True
    else:
        return False


def check_generic_footer(f):
    """RULE 3:  generic footer message.

    (eg. LEGAL DISCLAIMER/Please consider the environment when
    printing/For low cost fares, etc.
    Inputs:
        f: filename
    Outputs:
        boolen for check pass/fail
    """
    filesize = os.path.getsize(f)
    filename = get_file_name(f)

    if filename[:3] =='ATT' and filesize < 10000:
        return True
    else:
        return False


def check_file_access_doc(f):
    """RULE 4: file access doc.

    Inputs:
        f: filename
    Outputs:
        boolen for check pass/fail
    """
    rule4_regex = r"^MIME Type:\tDirectory"
    filetype = get_file_type(f)

    if ('text' in filetype[0] and os.path.getsize(f)<40000000):
        sample = open(f, 'r', encoding='utf-8', errors='ignore').read()
        matches=re.findall(rule4_regex,str(sample), re.MULTILINE)
        if matches:
            return True
        else:
            return False

