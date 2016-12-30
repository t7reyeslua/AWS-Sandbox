from pprint import pprint as pp
import image_processing as image_processing
import datetime
import os

# COLLECTIONS MANAGEMENT ==================================================================================
def create_collection(client, collection_id):
    print('%s.create_collection: %s' % (client.api_name, collection_id))
    response = client.api.create_collection(CollectionId=collection_id)
    pp(response)
    return response


def delete_collection(client, collection_id):
    print('%s.delete_collection: %s' % (client.api_name, collection_id))
    response = client.api.delete_collection(CollectionId=collection_id)
    pp(response)
    return response


def list_collections(client, max_results=100):
    print('%s.list_collections' % (client.api_name))
    collections = []
    response = client.api.list_collections(MaxResults=max_results)
    pp(response)
    collections.extend(response.get('CollectionIds', []))

    if response.get('NextToken', None) is not None:
        # Results are paginated
        more_results = True
        while more_results:
            next_token = response['NextToken']
            response = client.api.list_collections(MaxResults=max_results, NextToken=next_token)
            pp(response)
            collections.extend(response.get('CollectionIds', []))
            if response.get('NextToken', None) is None:
                more_results = False
    return collections


# FACES MANAGEMENT =======================================================================================
def index_faces(client, image_url, collection_id, external_image_id=None):
    print('%s.index_faces of image %s in collection: %s' % (client.api_name, image_url, collection_id))
    response = None
    with open(image_url, 'rb') as image:
        if external_image_id is None:
            response = client.api.index_faces(Image={'Bytes': image.read()}, CollectionId=collection_id)
        else:
            # Make sure the external image id has a fc_ prefix and has a unique suffix
            now_str = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d%H%M%S%f')
            external_image_id = external_image_id + '_' + now_str
            if 'fc_' not in external_image_id:
                external_image_id = 'fc_' + external_image_id
            response = client.api.index_faces(Image={'Bytes': image.read()}, CollectionId=collection_id,
                                              ExternalImageId=external_image_id)
        pp(response)
    return response

def index_faces_directory(client, directory, collection_id, external_image_id=None):
    '''
    Indexes all faces from all pictures found in the given directory.  As with the original index_faces
    it is recommended that each image only contains one single face so it can be easily identified later by
    using the external_image_id. If two persons appear on same picture, then both will be marked with same eid
    and will not be possible to distinguish between them. If no external_image_id is received, then the
    name of the directory will be used. Therefore, it is recommended to name the directory with the name of the
    person in the pictures to be indexed.

    '''
    print('%s.index_faces_directory of %s in collection: %s' % (client.api_name, directory, collection_id))
    responses = []
    directory = directory.rstrip('/') # Get rid of trailing slash if exists
    if external_image_id is None:
        external_image_id = directory.split('/')[-1]
    indexed_pictures_folder = directory + '/indexed/'
    for filename in os.listdir(directory):
        if not (filename.lower().endswith('.png') or filename.lower().endswith('.jpg')):
            continue # skip non-image files

        # Index face in this picture
        image_url = directory + filename
        response = index_faces(client, image_url, collection_id, external_image_id=external_image_id)
        responses.append(response)

        # Move picture to other folder to mark it as indexed
        os.makedirs(indexed_pictures_folder, exist_ok=True)
        os.rename(image_url, indexed_pictures_folder + filename)

    return responses

def delete_faces(client, face_ids, collection_id):
    print('%s.delete_faces %s in collection: %s' % (client.api_name, face_ids, collection_id))
    response = client.api.delete_faces(CollectionId=collection_id, FaceIds=face_ids)
    pp(response)
    return response

def delete_faces_by_external_image_id(client, external_image_id, collection_id):
    print('%s.delete_faces_by_external_image_id %s in collection: %s' % (client.api_name, external_image_id, collection_id))
    face_ids = []

    faces = list_faces(client, collection_id)
    for face in faces:
        if external_image_id in face.get('ExternalImageId', ''):
            face_ids.append(face.get('ImageId', ''))

    response = client.api.delete_faces(CollectionId=collection_id, FaceIds=face_ids)
    pp(response)
    return response

def list_faces(client, collection_id, max_results=100):
    print('%s.list_faces in collection: %s' % (client.api_name, collection_id))
    faces = []
    response = client.api.list_faces(CollectionId=collection_id, MaxResults=max_results)
    pp(response)
    faces.extend(response.get('Faces', []))

    if response.get('NextToken', None) is not None:
        # Results are paginated
        more_results = True
        while more_results:
            next_token = response['NextToken']
            response = client.api.list_faces(CollectionId=collection_id, MaxResults=max_results, NextToken=next_token)
            pp(response)
            faces.extend(response.get('Faces', []))
            if response.get('NextToken', None) is None:
                more_results = False
    return faces

# NON-STORAGE IMAGE OPERATIONS ===========================================================================
def detect_faces(client, image_url, attributes=None):
    print('%s.detect_faces of image: %s' % (client.api_name, image_url))
    response = None
    if attributes is None:
        attributes = ['ALL']
    with open(image_url, 'rb') as image:
        response = client.api.detect_faces(Image={'Bytes': image.read()}, Attributes=attributes)
        pp(response)
    return response


def detect_labels(client, image_url, min_confidence=50.0):
    print('%s.detect_labels of image: %s' % (client.api_name, image_url))
    response = None
    with open(image_url, 'rb') as image:
        response = client.api.detect_labels(Image={'Bytes': image.read()}, MinConfidence=min_confidence)
        pp(response)
    return response


def compare_faces(client, source_image_url, target_image_url, similarity_threshold=80.0):
    print('%s.compare_faces of source %s and target %s' % (client.api_name, source_image_url, target_image_url))
    response = None
    with open(source_image_url, 'rb') as source_image, open(target_image_url, 'rb') as target_image:
        response = client.api.compare_faces(SourceImage={'Bytes': source_image.read()},
                                            TargetImage={'Bytes': target_image.read()},
                                            SimilarityThreshold=similarity_threshold)
        pp(response)
    return response

# STORAGE IMAGE OPERATIONS ===============================================================================
def search_faces(client, face_id, collection_id, max_faces=10, face_match_threshold=80.0):
    print('%s.search_faces of face: %s' % (client.api_name, face_id))
    response = client.api.search_faces_by_image(
        FaceId=face_id,
        CollectionId=collection_id,
        MaxFaces=max_faces,
        FaceMatchThreshold=face_match_threshold)
    pp(response)
    return response

def search_faces_by_image(client, image_url, collection_id, max_faces=10, face_match_threshold=80.0):
    print('%s.search_faces_by_image of image: %s' % (client.api_name, image_url))
    response = None
    with open(image_url, 'rb') as image:
        response = client.api.search_faces_by_image(
            Image={'Bytes': image.read()},
            CollectionId=collection_id,
            MaxFaces=max_faces,
            FaceMatchThreshold=face_match_threshold)
        pp(response)
    return response

def search_all_faces_by_image(client, image_url, collection_id, max_faces=10, face_match_threshold=80.0):
    print('%s.search_all_faces_by_image of image: %s' % (client.api_name, image_url))
    response = None
    faces_recognized = []
    res = detect_faces(client, image_url)
    face_details = res.get('FaceDetails', [])
    face_image_urls = image_processing.create_face_crops(image_url, face_details)

    for i, face_image_url in enumerate(face_image_urls):
        res = search_faces_by_image(client, face_image_url, collection_id,
                                    face_match_threshold=face_match_threshold)
        res['FaceMatches'] = sorted(res['FaceMatches'], key=lambda k: k['Similarity'], reverse=True)
        face = res['FaceMatches'][:1]
        if len(face) > 0:
            face = face[0]
        else:
            face = {}
        face['ImageUrl'] = face_image_url
        face['FaceDetails'] = face_details[i]
        face['FaceDetails'].pop('Landmarks', None)
        faces_recognized.append(face)

    pp(faces_recognized)
    image_processing.delete_picture_files(face_image_urls)
    image_processing.show_face_names_on_image(image_url, face_details, faces_recognized)
    return response