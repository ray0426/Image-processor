import json
import time

class Img_Tag ():
    ''' load tags from data_tags.json file to self.data_tag '''
    ''' the file should exist before calling this function '''
    def load_tags(self):
        print("load tags")
        with open('data_tags.json', 'r', encoding='utf-8') as f:
            self.data_tag = json.load(f)
        print("load tags success!")
        return self.data_tag

    ''' write tags data from self.data_tag to data_tags.json file '''
    def write_tags(self):
        print("write tags")
        with open('data_tags.json', 'w', encoding='utf-8') as f:
            json.dump(self.data_tag, f, indent=4)
        print("write tags success!")

    ''' input a list of tag name (each is a string), and return a list of correspond tag id '''
    ''' if tag not exist, it will create it and save to self.data_tag by create_tag() '''
    def tags_to_id(self, tags):
        ids = []
        for tag in tags:
            if not self.exist_tag(tag):
                ids.append(self.create_tag(tag)['tag_id'])
            else:
                ids.append(self.find_by_name(tag)['tag_id'])
        return ids

    ''' judge is the tag exist in self.data_tag '''
    def exist_tag(self, tag):
        if any(t['tag_name'] == tag for t in self.data_tag):
            return True
        else:
            return False

    ''' create new tag and add to self.data_tag '''
    def create_tag(self, tag):
        new_tag = {}
        new_tag['tag_id'] = len(self.data_tag)
        new_tag['tag_name'] = tag
        new_tag['create_time'] = time_now()
        self.data_tag.append(new_tag)
        print("== new tag name: \"" + new_tag['tag_name'] + "\", tag ID: " + str(new_tag['tag_id']))
        print("== create time: " + str(new_tag['create_time']) + "\n")
        return new_tag

    ''' find tag in self.data_tag by name '''
    def find_by_name(self, tag_name):
        return [t for t in self.data_tag if t['tag_name'] == tag_name][0]

    ''' find tag in self.data_tag by id '''
    def find_by_id(self, tag_id):
        return [t for t in self.data_tag if t['tag_id'] == tag_id][0]

''' return the time with format '''
def time_now():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

if __name__ == '__main__':
    img_tag = Img_Tag()
    img_tag.load_tags()
    print(img_tag.tags_to_id(["banana", "apple"]))
    print(img_tag.tags_to_id(["apple", "pie", "banana"]))
    print(img_tag.tags_to_id(["pie", "banana", "apple"]))
    print(img_tag.tags_to_id(["peach", "orange", "mango", "melon", "tomato"]))
    img_tag.write_tags()