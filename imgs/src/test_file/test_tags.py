
tag_exist = ['apple', 'banana', 'orange']

def tags_to_id(tags):
    ids = []
    for tag in tags:
        if new_tag(tag):
            ids.append(create_tag(tag))
        else:
            ids.append(find_by_name(tag))
    return ids

def new_tag(tag):
    if tag in tag_exist:
        return False
    else:
        return True

def create_tag(tag):
    tag_exist.append(tag)
    return len(tag_exist) - 1

def find_by_name(tag):
    return tag_exist.index(tag)

if __name__ == '__main__':
    print(tags_to_id(['banana', 'orange', 'peach']))
    print(tag_exist)