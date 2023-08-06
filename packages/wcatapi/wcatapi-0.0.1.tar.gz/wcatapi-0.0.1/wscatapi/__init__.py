import requests, io

class img:
    """
    img.download(filename: str, encoding: str): download img
    img.as_bytes(): get bytes from img
    img.as_file(): get file from img
    img.url: url to img
    """
    def __init__(self, url: str):
        """image

        Args:
            url (str): url to img
        """
        self.url = url
    
    def as_bytes(self):
        """get bytes from image

        Returns:
            bytes: bytes from image
        """
        return requests.get(self.url).content

    def as_file(self):
        """get file with image

        Returns:
            BytesIO: file with image
        """
        return io.BytesIO(self.as_bytes())

    def download(self, filename: str):
        """download file

        Args:
            filename (str): filename to save
        """
        with open(filename, "wb") as f:
            f.write(self.get_bytes())

def random_cat():
    """random cat

    Returns:
        img: class img
    """
    return img(requests.get("https://api.wispace.ru/cat/api").json()[0])

__all__ = ["img", "random_cat"]
