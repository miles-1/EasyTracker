import json

def getAnnotations(file_name,name="",iden=-1):
    f = open(file_name,"r")
    dataStr = f.read()
    f.close()
    data = json.loads(dataStr)
    url = ""
    if name == "" and iden == -1:
        return None
    elif name is not "":
        for image in data["images"]:
            if image["file_name"] == name.split("/")[-1]:
                iden = image["id"]
                break
    elif iden is not -1:
        for image in data["images"]:
            if image["id"] == iden:
                name = image["file_name"]
                url = image["coco_url"]
                break
    
    categories = {}
    for cat in data["categories"]:
        categories[cat["id"]] = cat["name"]

    annotations = {}
    for ann in data["annotations"]:
        if ann["image_id"] == iden and ann["iscrowd"] == 0:
            if categories[ann["category_id"]] not in annotations:
                annotations[categories[ann["category_id"]]] = ann["segmentation"]
            else:
                annotations[categories[ann["category_id"]]] += ann["segmentation"]

    return (annotations,url,name)
    

def getCatsandMaxIDs(file_name):
    f = open(file_name,"r")
    dataStr = f.read()
    f.close()
    data = json.loads(dataStr)
    categories = {}

    for cat in data["categories"]:
        categories[cat["name"]] = cat["id"]

    maxPhotoID = 0
    for image in data["images"]:
        maxPhotoID = max(maxPhotoID,image["id"])
    
    maxAnnID = 0
    for ann in data["annotations"]:
        maxAnnID = max(maxAnnID,ann["id"])

    return (categories,maxPhotoID,maxAnnID)


def getIDs(file_name):
    f = open(file_name,"r")
    dataStr = f.read()
    f.close()
    data = json.loads(dataStr)
    ident_list = []
    for image in data["images"]:
        ident_list += [str(image["id"])]
    
    return ident_list


def setImage(file_name, segs, category_id, ann_id, width=0, height=0, picture_name="", url="", max_id=0, date=""):
    f = open(file_name,"r")  # open for reading and writing
    dataStr = f.read()
    f.close()
    data = json.loads(dataStr)
    present = False
    iden = 0

    for image in data["images"]:
        if image["file_name"] == picture_name or image["coco_url"] == url or image["flickr_url"] == url:
            iden = image["id"]
            present = True
            break

    if not present:
        iden = max_id + 1
        data["images"] += [{"license": 0,
                            "file_name": picture_name,
                            "coco_url": url,
                            "height": height,
                            "width": width,
                            "date_captured": date,
                            "flickr_url": url,
                            "id": iden
            }] 
        
    area = 0.0
    for seg in segs:
        area += polygonArea(seg)

    data["annotations"] += [{"segmentation":segs,
                             "area": area,
                             "iscrowd": 0,
                             "image_id": iden,
                             "bbox": getBBox(segs),
                             "category_id": category_id,
                             "id": ann_id}]
    
    dataStr = json.dumps(data)
    f = open(file_name,"w")
    f.write(dataStr)
    f.close()
    return present


############## Supplemental ##############




def polygonArea(xy):
    area = 0.0
    n = len(xy)//2
    X = [xy[2*i] for i in range(n)]
    Y = [xy[2*i + 1] for i in range(n)]
    # Calculate value with shoelace formula 
    j = n - 1
    for i in range(0,n): 
        area += (X[j] + X[i]) * (Y[j] - Y[i]) 
        j = i
    return abs(area / 2.0)


def getBBox(segs):
    n = len(segs[0])//2
    X = [segs[0][2*i] for i in range(n)]
    Y = [segs[0][2*i + 1] for i in range(n)]
    maxX = max(X)
    minX = min(X)
    maxY = max(Y)
    minY = min(Y)
    if len(segs) > 1:
        for seg in segs[1:]:
            n = len(seg)//2
            X = [seg[2*i] for i in range(n)]
            Y = [seg[2*i + 1] for i in range(n)]

            t_maxX = max(X)
            t_minX = min(X)
            t_maxY = max(Y)
            t_minY = min(Y)

            maxX = max(maxX, t_maxX)
            minX = min(minX, t_minX)
            maxY = max(maxY, t_maxY)
            minY = min(minY, t_minY)
    return [minX, minY, maxX-minX, maxY-minY]    
