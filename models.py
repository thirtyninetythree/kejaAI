
class HouseDetailObject:
    def __init__(self, images:list[str], link: str, description: str, title: str):
        self.images = images
        self.link = link
        self.description = description
        self.title = title
    
    def to_dict(self):
        return {
            "images": self.images,
            "link": self.link,
            "description": self.description,
            "title": self.title
        }


    