import json
import time

class Img_Tag ():
    def load_tags(self):
        print("load tags")
        with open('data_tags.json', 'r', encoding='utf-8') as f:
            self.data_tag = json.load(f)
        print("load tags success!")
        return self.data_tag

    def write_tags(self):
        print("write tags")
        with open('data_tags.json', 'w', encoding='utf-8') as f:
            json.dump(self.data_tag, f, indent=4)
        print("write tags success!")

    def tags_to_id(self, tags):
        ids = []
        for tag in tags:
            if not self.exist_tag(tag):
                ids.append(self.create_tag(tag)['tag_id'])
            else:
                ids.append(self.find_by_name(tag)['tag_id'])
        return ids

    def exist_tag(self, tag):
        if any(t['tag_name'] == tag for t in self.data_tag):
            return True
        else:
            return False

    def create_tag(self, tag):
        new_tag = {}
        new_tag['tag_id'] = len(self.data_tag)
        new_tag['tag_name'] = tag
        new_tag['create_time'] = time_now()
        self.data_tag.append(new_tag)
        print("== new tag name: \"" + new_tag['tag_name'] + "\", tag ID: " + str(new_tag['tag_id']))
        print("== create time: " + str(new_tag['create_time']) + "\n")
        return new_tag

    def find_by_name(self, tag):
        return [t for t in self.data_tag if t['tag_name'] == tag][0]

def time_now():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

if __name__ == '__main__':
    img_tag = Img_Tag()
    img_tag.load_tags()
    print(img_tag.tags_to_id(["banana", "apple"]))
    print(img_tag.tags_to_id(["apple", "pie", "banana"]))
    print(img_tag.tags_to_id(["pie", "banana", "apple"]))
    img_tag.write_tags()